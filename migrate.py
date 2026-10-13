import sqlite3
import shutil
from pathlib import Path

from app.database import Base, engine
from app.models.user import User
from app.models.events import Event
from app.models.booking import Booking
from app.models.tickets import Ticket
from app.models.payment import Payment
from app.models.coupon import Coupon
from app.models.notification import Notification


# Resolve the SQLite database path from the configured engine.
database_path = Path(engine.url.database)

# Create a backup before changing the existing database.
backup_path = database_path.with_name(database_path.stem + "Backup" + database_path.suffix)

if database_path.exists():
     if not backup_path.exists():
        shutil.copy2(database_path, backup_path)
        print(f"Database backup created: {backup_path}")
     else:
        print(f"Existing backup preserved: {backup_path}")
else:
    raise FileNotFoundError(f"Database not found: {database_path}")

# Create missing tables, including the coupons table.
Base.metadata.create_all(bind=engine)

# Add missing columns to the existing bookings table.
with sqlite3.connect(database_path) as connection:
    existing_columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(booking)").fetchall()}

    required_columns = {"coupon_id": "INTEGER REFERENCES coupons(id)",
        "discount_amount": "FLOAT NOT NULL DEFAULT 0.0",
        "final_amount": "FLOAT",}

    for column_name, column_definition in required_columns.items():
        if column_name not in existing_columns:
            connection.execute(f"ALTER TABLE booking ADD COLUMN "
                f"{column_name} {column_definition}")
            print(f"Added column: {column_name}")
        else:
            print(f"Column already exists: {column_name}")

    connection.commit()

# Migrate the existing notifications table.
with sqlite3.connect(database_path) as connection:
    columns = {row[1]
        for row in connection.execute("PRAGMA table_info(notifications)").fetchall()}

    # Migrate only if the old "type" column exists.
    if "type" in columns and "notification_type" not in columns:
            connection.execute("DROP TABLE IF EXISTS notifications_new")
            connection.execute("""CREATE TABLE notifications_new (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                event_id INTEGER REFERENCES events(id),
                title VARCHAR(150) NOT NULL,
                message VARCHAR(500) NOT NULL,
                notification_type VARCHAR(7) NOT NULL DEFAULT 'SYSTEM',
                is_read BOOLEAN NOT NULL DEFAULT 0,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)""")

        
            old_columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(notifications)"
            ).fetchall()
        }

            event_id_expression = (
            "event_id" if "event_id" in old_columns else "NULL"
        )
    
            connection.execute(f"""
            INSERT INTO notifications_new (
                id, user_id, event_id, title, message,
                notification_type, is_read, created_at
            )
            SELECT
                id,
                user_id,
                {event_id_expression},
                title,
                message,
                CASE UPPER(type)
                    WHEN 'BOOKING' THEN 'BOOKING'
                    WHEN 'PAYMENT' THEN 'PAYMENT'
                    WHEN 'SYSTEM' THEN 'SYSTEM'
                    ELSE 'EVENT'
                END,
                is_read,
                COALESCE(created_at, CURRENT_TIMESTAMP)
            FROM notifications
        """)

            connection.execute("DROP TABLE notifications")
            connection.execute("ALTER TABLE notifications_new RENAME TO notifications")

            connection.execute("""CREATE INDEX IF NOT EXISTS ix_notifications_id ON notifications(id)""")

            connection.execute("""CREATE INDEX IF NOT EXISTS ix_notifications_user_id ON notifications(user_id)""")

            print("Notifications table migrated successfully.")
    else:
        print("Notifications table already uses the updated schema.")

    connection.commit()

print("database migration completed.")