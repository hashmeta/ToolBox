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

# Function to convert a text file to PDF
def text_to_pdf(input_file, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            # If the identifier for a new page is found, add a new page in the PDF
            if '---NEW PAGE---' in line:
                pdf.add_page()
            else:
                # Replace unsupported characters and use utf-8 encoding
                line = line.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 10, txt=line)
    
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
    if os.path.exists(output_file_txt):
        os.remove(output_file_txt)
        print(f"Deleted temporary file: {output_file_txt}")
    else:
        print(f"File {output_file_txt} not found.")
