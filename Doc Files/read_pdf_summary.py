import pdfplumber
import os

def analyze_pdf(pdf_path):
    """Analyze and extract information from a PDF"""
    filename = os.path.basename(pdf_path)
    print(f"\n{'='*100}")
    print(f"PDF FILE: {filename}")
    print(f"{'='*100}\n")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
            print(f"📄 Total Pages: {num_pages}")
            print(f"📦 File Size: {os.path.getsize(pdf_path) / 1024:.2f} KB\n")
            
            # Extract all text
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            # Show first 3000 characters
            print(f"{'─'*100}")
            print("CONTENT PREVIEW (First 3000 characters):")
            print(f"{'─'*100}\n")
            print(full_text[:3000])
            
            if len(full_text) > 3000:
                print(f"\n... [Content continues for {len(full_text) - 3000} more characters] ...\n")
            
            # Show last 1000 characters
            if len(full_text) > 4000:
                print(f"{'─'*100}")
                print("CONTENT END (Last 1000 characters):")
                print(f"{'─'*100}\n")
                print(full_text[-1000:])
            
            print(f"\n{'─'*100}")
            print(f"Total characters extracted: {len(full_text)}")
            print(f"{'─'*100}\n")
            
            return full_text
            
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

if __name__ == "__main__":
    print("\n" + "="*100)
    print(" "*35 + "PDF CONTENT READER")
    print("="*100)
    
    # PDF files
    pdf1 = "Zee- MOVIE RECOMMENDER SYSTEM.pdf"
    pdf2 = "zee-movie-recommender-system.pdf"
    
    # Read first PDF
    print("\n\n" + "🔵 "*50)
    print("READING FIRST PDF")
    print("🔵 "*50)
    text1 = analyze_pdf(pdf1)
    
    # Read second PDF
    print("\n\n" + "🟢 "*50)
    print("READING SECOND PDF")
    print("🟢 "*50)
    text2 = analyze_pdf(pdf2)
    
    print("\n\n" + "="*100)
    print("✅ FINISHED READING BOTH PDFs!")
    print("="*100)
    
    # Save full content to separate files
    if text1:
        with open("pdf1_full_content.txt", "w", encoding="utf-8") as f:
            f.write(text1)
        print(f"\n📝 Full content of PDF 1 saved to: pdf1_full_content.txt")
    
    if text2:
        with open("pdf2_full_content.txt", "w", encoding="utf-8") as f:
            f.write(text2)
        print(f"📝 Full content of PDF 2 saved to: pdf2_full_content.txt")
