import fitz  # PyMuPDF for PDF reading
from PIL import Image
import pytesseract
import requests

# -------------------------
# PDF TOOL
# -------------------------
def load_pdf_tool(path: str) -> str:
    """Extract text from a PDF file."""
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"


# -------------------------
# IMAGE TOOL
# -------------------------
def load_image_tool(path: str) -> str:
    """Extract text from an image using OCR."""
    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"Error reading image: {e}"


# -------------------------
# SEARCH TOOL
# -------------------------
def search_tool(query: str) -> str:
    """Very simple web search using DuckDuckGo."""
    try:
        url = f"https://duckduckgo.com/?q={query}&ia=web"
        return f"Search results page: {url}"
    except Exception as e:
        return f"Error performing search: {e}"