import os
from src.encryption import encrypt_doc
from config import DATA_DIR, ENCRYPTED_DATA_DIR, DOC_FILE


def setup():
    """Run initial setup"""
    print("🚀 Family RAG Setup")
    
    # Stwórz foldery jeśli nie istnieją
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ENCRYPTED_DATA_DIR, exist_ok=True)
    
    # Sprawdź czy encrypted folder jest pusty
    encrypted_files = os.listdir(ENCRYPTED_DATA_DIR)
    
    if not encrypted_files:
        # Folder encrypted jest pusty - sprawdź czy dokument istnieje
        if not os.path.exists(DOC_FILE):
            print(f"❌ Place your family_lineage.docx in {DATA_DIR}/")
            print(f"   Current path: {os.path.abspath(DOC_FILE)}")
            return
        
        # Szyfruj dokument
        print("🔐 Encrypting document...")
        encrypt_doc()
        print("✓ Document encrypted successfully!")
    else:
        # Folder encrypted ma zawartość - pomij szyfrowanie
        print("✓ Encrypted folder already contains data, skipping encryption")
    
    print("✓ Setup complete!")
    print("\nNext: Run 'streamlit run ui/app.py'")


if __name__ == "__main__":
    setup()