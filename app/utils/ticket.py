import uuid

def generate_ticket_code():
    return "TKT-" + uuid.uuid4().hex[:8].upper()