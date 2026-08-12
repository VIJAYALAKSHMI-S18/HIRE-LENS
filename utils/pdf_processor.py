import pymupdf as fitz  # PyMuPDF
import re
import io

def extract_text_from_pdf(pdf_bytes: bytes) -> dict:
    """
    Extracts structured text from PDF bytes using PyMuPDF.
    Returns metadata and cleaned text content.
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = len(doc)
        
        full_text = ""
        for page_num in range(page_count):
            page = doc[page_num]
            full_text += page.get_text("text") + "\n"
            
        doc.close()
        
        cleaned_text = clean_text(full_text)
        
        if not cleaned_text.strip():
            return {
                "success": False,
                "error": "The uploaded PDF appears to be empty or contains scanned images without extractable text.",
                "text": "",
                "pages": page_count
            }
            
        sections = extract_resume_sections(cleaned_text)
        
        return {
            "success": True,
            "text": cleaned_text,
            "raw_text": full_text,
            "pages": page_count,
            "sections": sections
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to parse PDF document: {str(e)}",
            "text": "",
            "pages": 0
        }

def clean_text(text: str) -> str:
    """Removes weird characters, normalizes line breaks and whitespace."""
    if not text:
        return ""
    # Normalize newline breaks
    text = re.sub(r'\r\n', '\n', text)
    # Remove consecutive spaces
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove non-printable control characters except standard whitespace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def extract_resume_sections(text: str) -> dict:
    """Detects standard resume section blocks."""
    text_lower = text.lower()
    
    sections = {
        "education": "",
        "experience": "",
        "projects": "",
        "skills": "",
        "certifications": ""
    }
    
    # Common section header keywords
    patterns = {
        "education": r'(?:education|academic background|qualification|academic history)',
        "experience": r'(?:work experience|employment|experience|professional history|career)',
        "projects": r'(?:projects|academic projects|key projects|personal projects)',
        "skills": r'(?:skills|technical skills|key competencies|core competencies|technologies)',
        "certifications": r'(?:certifications|licenses|courses|certificates|achievements)'
    }
    
    # Simple regex split approach
    lines = text.split('\n')
    current_section = None
    section_buffers = {k: [] for k in sections}
    
    for line in lines:
        line_clean = line.strip()
        matched_header = False
        
        for sec_key, pattern in patterns.items():
            if re.match(r'^(?:' + pattern + r')[:\s]*$', line_clean.lower()):
                current_section = sec_key
                matched_header = True
                break
                
        if not matched_header and current_section:
            section_buffers[current_section].append(line_clean)
            
    for k in sections:
        sections[k] = "\n".join(section_buffers[k])
        
    return sections
