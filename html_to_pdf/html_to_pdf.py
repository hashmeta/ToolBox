import os
from bs4 import BeautifulSoup
from fpdf import FPDF

# Function to convert HTML to plain text
def html_to_text(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator='\n')
    return text

# Function to sanitize text for FPDF compatibility
def sanitize_text(text):
    # Replace unsupported characters with a placeholder or remove them
    sanitized = []
    for char in text:
        if ord(char) < 128:  # ASCII characters
            sanitized.append(char)
        else:
            sanitized.append('?')  # Replace with a placeholder
    return ''.join(sanitized)

# Function to convert a text file to PDF
def text_to_pdf(input_file, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()  # Start with a new page

    page_map = {}  # Store filename and starting page number
    current_page = 1  # Start from page 1

    # Convert text file to PDF, keeping track of pages
    pdf.set_font("Arial", size=12)

    with open(input_file, 'r', encoding='utf-8') as file:
        current_file = None
        
        for line in file:
            # If the identifier for a new page is found, add a new page in the PDF
            if '---NEW PAGE---' in line:
                pdf.add_page()
                current_page += 1
                current_file = None  # Reset current file since we're on a new page
            else:
                if current_file is None:
                    current_file = line.strip().strip('*')  # Get the current filename
                    page_map[current_file] = current_page  # Map the file to the current page
                else:
                    sanitized_line = sanitize_text(line)
                    pdf.multi_cell(0, 10, txt=sanitized_line)
        
        # Add a new page for the index
        pdf.add_page()
        pdf.set_font("Arial", size=16, style='B')
        pdf.cell(200, 10, txt="Index (Table of Contents)", ln=True, align='C')
        pdf.ln(10)  # Line break

        pdf.set_font("Arial", size=12)
        for file_name, page_no in page_map.items():
            pdf.cell(0, 10, f"{file_name} .......... Page {page_no}", ln=True)
    
    # Output the PDF to the specified file
    pdf.output(output_pdf)

if __name__ == '__main__':
    html_folder = 'New_Folder_With_Items'  # Replace with your folder path
    output_file_txt = 'combined.txt'
    
    # Get HTML files and sort them alphabetically
    html_files = sorted([f for f in os.listdir(html_folder) if f.endswith('.html')])
    
    # Combine all HTML files into one text file, adding identifier for new pages
    with open(output_file_txt, 'w', encoding='utf-8') as txt_file:
        for filename in html_files:
            file_path = os.path.join(html_folder, filename)
            text_content = html_to_text(file_path)
            
            # Write filename, then new lines, then the content, and identifier for a new page
            txt_file.write(f"**{filename}**\n\n{text_content}\n\n---NEW PAGE---\n\n")
    
    # Create PDF from the combined text file
    output_pdf = "output.pdf"
    text_to_pdf(output_file_txt, output_pdf)
    
    # Delete the text file after PDF creation
    if os.path.exists(output_file_txt):
        os.remove(output_file_txt)
        print(f"Deleted temporary file: {output_file_txt}")
    else:
        print(f"File {output_file_txt} not found.")
