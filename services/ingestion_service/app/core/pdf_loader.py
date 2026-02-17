import fitz  # PyMuPDF
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def extract_text_from_pdf(path: str) -> List[Dict]:
    """
    Extracts text from a PDF file page-by-page.

    Args:
        path (str): Path to the PDF file.

    Returns:
        List[Dict]: A list of dictionaries containing:
            - page (int): Page number
            - text (str): Extracted text
            - char_count (int): Number of characters in the page
    """

    pages = []

    # with fitz.open(path) as doc -> Automatically closes file
    # Prevents memory leaks
    # Prevents Windows file lock issues
    try:
        with fitz.open(path) as doc:
            logger.info(f"Opened PDF: {path}")
            
            for page_num, page in enumerate(doc):
                text = page.get_text("text").strip()  #.strip()->Extra whitespace, Blank page artifacts

                # Skip empty pages
                #Prevents:Garbage chunks, Useless embeddings,Vector DB pollution
                if not text:
                    logger.warning(f"Skipping empty page {page_num + 1}")
                    continue

                pages.append({
                    "page": page_num + 1,
                    "text": text,
                    "char_count": len(text)
                })

        logger.info(f"Successfully extracted {len(pages)} pages from {path}")
        return pages

    except Exception as e:
        logger.error(f"Error processing PDF {path}: {str(e)}")
        raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")



def extract_text_from_pdf_basic(path: str):
    doc = fitz.open(path) #Loads the PDF into memory.Creates a document object
    pages = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        pages.append({
            "page": page_num + 1,
            "text": text
        })

