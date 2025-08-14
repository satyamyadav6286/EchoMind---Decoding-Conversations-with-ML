from fpdf import FPDF
import os
import base64
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('logo.png', 10, 8, 25)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'EchoMind - Chat Analysis Report', 0, 0, 'C')
        # Line break
        self.ln(20)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

def create_pdf_report(analysis_data, output_path='chat_analysis_report.pdf'):
    """
    Create a PDF report from the analysis data
    
    Args:
        analysis_data (dict): Dictionary containing analysis results
        output_path (str): Path to save the PDF file
        
    Returns:
        str: Path to the generated PDF file
    """
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Set font for the title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Chat Analysis Report', 0, 1, 'C')
    pdf.ln(10)
    
    # Add analysis date
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'R')
    pdf.ln(5)
    
    # Add basic statistics
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Basic Statistics', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    # Create a table for statistics
    col_width = pdf.w / 2.5
    row_height = pdf.font_size * 2
    
    stats = [
        ['Total Messages', analysis_data.get('total_messages', 'N/A')],
        ['Total Words', analysis_data.get('total_words', 'N/A')],
        ['Media Shared', analysis_data.get('media_shared', 'N/A')],
        ['Links Shared', analysis_data.get('links_shared', 'N/A')],
        ['Most Active User', analysis_data.get('most_active_user', 'N/A')],
        ['Most Active Day', analysis_data.get('most_active_day', 'N/A')],
        ['Most Active Hour', analysis_data.get('most_active_hour', 'N/A')],
    ]
    
    for row in stats:
        pdf.cell(col_width, row_height, str(row[0]), border=1)
        pdf.cell(col_width, row_height, str(row[1]), border=1)
        pdf.ln(row_height)
    
    # Add analysis sections
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Analysis Details', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    # Add word cloud image if available
    if 'wordcloud_path' in analysis_data and os.path.exists(analysis_data['wordcloud_path']):
        pdf.image(analysis_data['wordcloud_path'], x=10, y=pdf.get_y(), w=180)
        pdf.ln(100)  # Adjust based on image height
    
    # Add most common words
    if 'common_words' in analysis_data and analysis_data['common_words']:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Most Common Words', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        for i, (word, count) in enumerate(analysis_data['common_words'].items(), 1):
            pdf.cell(0, 10, f'{i}. {word}: {count}', 0, 1)
    
    # Add emoji analysis
    if 'top_emojis' in analysis_data and analysis_data['top_emojis']:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Top Emojis', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        for i, (emoji, count) in enumerate(analysis_data['top_emojis'].items(), 1):
            pdf.cell(0, 10, f'{i}. {emoji}: {count} times', 0, 1)
    
    # Save the PDF
    pdf.output(output_path, 'F')
    return output_path

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """
    Generates a link to download a file
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href
