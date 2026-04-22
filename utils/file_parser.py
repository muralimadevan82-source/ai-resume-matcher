import io
import PyPDF2
import docx


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes."""
    text_parts = []
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    except Exception as e:
        return f"[PDF parse error: {e}]"
    return "\n".join(text_parts).strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX bytes."""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs).strip()
    except Exception as e:
        return f"[DOCX parse error: {e}]"


def parse_uploaded_file(uploaded_file) -> str:
    """Auto-detect file type and extract text."""
    name = uploaded_file.name.lower()
    raw = uploaded_file.read()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(raw)
    elif name.endswith(".docx"):
        return extract_text_from_docx(raw)
    else:
        try:
            return raw.decode("utf-8").strip()
        except Exception:
            return raw.decode("latin-1", errors="ignore").strip()
