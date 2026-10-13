import qrcode
import os

def generate_qr_code(ticket_code: str):
    
    folder = "static/qr"
    os.makedirs(folder, exist_ok=True)
    file_path = f"{folder}/{ticket_code}.png"
    qr = qrcode.make(ticket_code)
    qr.save(file_path)
    return file_path