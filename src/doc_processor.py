from docx import Document
from src.encryption import get_decrypted_doc_path, cleanup_temp_doc
from config import CHUNK_SIZE, CHUNK_OVERLAP
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_doc():
    """Extract text from encrypted DOC file"""
    temp_path = get_decrypted_doc_path()
    
    try:
        text = ""
        doc = Document(temp_path)
        
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                text += para.text + "\n"
        
        print(f"✓ Extracted {len(text)} characters from DOC")
        return text
    finally:
        cleanup_temp_doc(temp_path)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
    """Split text into chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)
    print(f"✓ Created {len(chunks)} chunks")
    return chunks