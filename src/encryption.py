import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY, ENCRYPTED_DOC_FILE, DOC_FILE, ENCRYPTED_DATA_DIR

def encrypt_doc():
    """Encrypt DOC file and save to encrypted_data/"""
    if not os.path.exists(ENCRYPTED_DATA_DIR):
        os.makedirs(ENCRYPTED_DATA_DIR)
    
    if not os.path.exists(DOC_FILE):
        print(f"❌ DOC file not found: {DOC_FILE}")
        return
    
    try:
        cipher = Fernet(ENCRYPTION_KEY.encode())
        
        with open(DOC_FILE, "rb") as f:
            doc_data = f.read()
        
        encrypted_data = cipher.encrypt(doc_data)
        
        with open(ENCRYPTED_DOC_FILE, "wb") as f:
            f.write(encrypted_data)
        
        print(f"✓ DOC encrypted and saved to {ENCRYPTED_DOC_FILE}")
    except Exception as e:
        print(f"❌ Encryption error: {e}")

def decrypt_doc():
    """Decrypt DOC and return bytes"""
    if not os.path.exists(ENCRYPTED_DOC_FILE):
        print(f"❌ Encrypted file not found: {ENCRYPTED_DOC_FILE}")
        raise FileNotFoundError(f"Encrypted file not found: {ENCRYPTED_DOC_FILE}")
    
    try:
        cipher = Fernet(ENCRYPTION_KEY.encode())
        
        with open(ENCRYPTED_DOC_FILE, "rb") as f:
            encrypted_data = f.read()
        
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data
    except Exception as e:
        print(f"❌ Decryption error: {e}")
        raise

def get_decrypted_doc_path(temp_path: str = "./temp_Rodzina_Karasi.docx"):
    """Decrypt DOC to temp file and return path"""
    try:
        decrypted_data = decrypt_doc()
        
        with open(temp_path, "wb") as f:
            f.write(decrypted_data)
        
        print(f"✓ Decrypted to {temp_path}")
        return temp_path
    except Exception as e:
        print(f"❌ Failed to create temp file: {e}")
        raise

def cleanup_temp_doc(temp_path: str = "./temp_Rodzina_Karasi.docx"):
    """Delete temporary decrypted DOC"""
    if os.path.exists(temp_path):
        os.remove(temp_path)
        print(f"✓ Cleaned up {temp_path}")
