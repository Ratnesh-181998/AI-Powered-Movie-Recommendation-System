import pdfplumber
import sys

def read_pdf(pdf_path):
    """Extract text from a PDF file"""
    print(f"\n{'='*80}")
    print(f"Reading: {pdf_path}")
    print(f"{'='*80}\n")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Total pages: {len(pdf.pages)}\n")
            
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"\n--- Page {page_num} ---\n")
                text = page.extract_text()
                if text:
                    print(text)
                else:
                    print("[No text content on this page]")
                print("\n" + "-"*80)
                
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Read both PDFs
    pdf1 = "Zee- MOVIE RECOMMENDER SYSTEM.pdf"
    pdf2 = "zee-movie-recommender-system.pdf"
    
    print("\n" + "="*80)
    print("PDF READER - Reading both PDFs one by one")
    print("="*80)
    
    # Read first PDF
    print("\n\n### FIRST PDF ###")
    read_pdf(pdf1)
    
    print("\n\n" + "="*80)
    print("="*80)
    
    # Read second PDF
    print("\n\n### SECOND PDF ###")
    read_pdf(pdf2)
    
    print("\n\nFinished reading both PDFs!")
