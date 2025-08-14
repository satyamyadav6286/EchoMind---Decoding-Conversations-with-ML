from fpdf import FPDF
import os
import base64
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO
import tempfile

class PDF(FPDF):
    def header(self):
        # Logo
        try:
            self.image('logo.png', 10, 8, 25)
        except:
            # If logo fails to load, continue without it
            pass
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

def create_visualization_charts(df, selected_user, helper_module):
    """Create visualization charts and return as image files"""
    charts = {}
    
    try:
        # Set style for better looking charts
        plt.style.use('default')
        sns.set_palette("husl")
        
        # 1. Monthly Timeline
        timeline = helper_module.monthly_timeline(selected_user, df)
        if not timeline.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            timeline.plot(kind='line', ax=ax, color='#4f46e5', linewidth=2)
            ax.set_title('Monthly Message Activity', fontsize=14, fontweight='bold')
            ax.set_xlabel('Month')
            ax.set_ylabel('Number of Messages')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Save to bytes
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            charts['monthly_timeline'] = img_buffer
            plt.close()
        
        # 2. Daily Activity
        daily_timeline = helper_module.daily_timeline(selected_user, df)
        if not daily_timeline.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            daily_timeline.plot(kind='area', ax=ax, color='#7c3aed', alpha=0.7)
            ax.set_title('Daily Message Activity', fontsize=14, fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('Number of Messages')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            charts['daily_timeline'] = img_buffer
            plt.close()
        
        # 3. Weekly Activity
        busy_day = helper_module.week_activity_map(selected_user, df)
        if not busy_day.empty:
            fig, ax = plt.subplots(figsize=(8, 6))
            busy_day.plot(kind='bar', ax=ax, color='#4f46e5')
            ax.set_title('Most Active Day of Week', fontsize=14, fontweight='bold')
            ax.set_xlabel('Day of Week')
            ax.set_ylabel('Number of Messages')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            charts['weekly_activity'] = img_buffer
            plt.close()
        
        # 4. Monthly Activity
        busy_month = helper_module.month_activity_map(selected_user, df)
        if not busy_month.empty:
            fig, ax = plt.subplots(figsize=(8, 6))
            busy_month.plot(kind='bar', ax=ax, color='#7c3aed')
            ax.set_title('Most Active Month', fontsize=14, fontweight='bold')
            ax.set_xlabel('Month')
            ax.set_ylabel('Number of Messages')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            charts['monthly_activity'] = img_buffer
            plt.close()
        
        # 5. Most Common Words (if available)
        most_common_df = helper_module.most_common_words(selected_user, df)
        if not most_common_df.empty and len(most_common_df) > 0:
            fig, ax = plt.subplots(figsize=(10, 8))
            top_words = most_common_df.head(15)
            y_pos = np.arange(len(top_words))
            ax.barh(y_pos, top_words[1], color='#10b981')
            ax.set_yticks(y_pos)
            ax.set_yticklabels(top_words[0])
            ax.set_xlabel('Frequency')
            ax.set_title('Most Common Words', fontsize=14, fontweight='bold')
            ax.invert_yaxis()
            plt.tight_layout()
            
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            charts['common_words'] = img_buffer
            plt.close()
        
        # 6. Emoji Analysis (if available)
        emoji_df = helper_module.emoji_helper(selected_user, df)
        if not emoji_df.empty and len(emoji_df) > 0:
            fig, ax = plt.subplots(figsize=(8, 6))
            top_emojis = emoji_df.head(10)
            ax.bar(range(len(top_emojis)), top_emojis[1], color='#f59e0b')
            ax.set_title('Top Emojis Used', fontsize=14, fontweight='bold')
            ax.set_xlabel('Emoji')
            ax.set_ylabel('Frequency')
            ax.set_xticks(range(len(top_emojis)))
            ax.set_xticklabels(top_emojis[0], fontsize=12)
            plt.tight_layout()
            
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            charts['emoji_analysis'] = img_buffer
            plt.close()
            
    except Exception as e:
        print(f"Error creating charts: {e}")
    
    return charts

def create_pdf_report(df, selected_user, num_messages, words, num_media_messages, num_links):
    """
    Create a PDF report from the analysis data with visualizations
    
    Args:
        df: DataFrame containing chat data
        selected_user: User selected for analysis
        num_messages: Total number of messages
        words: Total number of words
        num_media_messages: Number of media messages
        num_links: Number of links shared
        
    Returns:
        BytesIO: PDF buffer
    """
    from io import BytesIO
    import helper

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Set font for the title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'EchoMind - Chat Analysis Report', 0, 1, 'C')
    pdf.ln(10)

    # Add analysis date and user info
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'R')
    pdf.cell(0, 10, f'Analysis for: {selected_user}', 0, 1, 'R')
    pdf.ln(5)

    # Calculate additional statistics
    total_days = (df['date'].max() - df['date'].min()).days + 1 if len(df) > 0 else 0
    avg_messages_per_day = num_messages / total_days if total_days > 0 else 0
    avg_words_per_message = words / num_messages if num_messages > 0 else 0
    media_ratio = (num_media_messages/num_messages*100) if num_messages > 0 else 0

    # Add basic statistics
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Basic Statistics', 0, 1)
    pdf.set_font('Arial', '', 10)

    # Create a table for statistics
    col_width = pdf.w / 2.5
    row_height = pdf.font_size * 2

    stats = [
        ['Total Messages', f'{num_messages:,}'],
        ['Total Words', f'{words:,}'],
        ['Media Shared', f'{num_media_messages:,}'],
        ['Links Shared', f'{num_links:,}'],
        ['Total Days', f'{total_days}'],
        ['Avg Messages/Day', f'{avg_messages_per_day:.1f}'],
        ['Avg Words/Message', f'{avg_words_per_message:.1f}'],
        ['Media Ratio', f'{media_ratio:.1f}%'],
    ]

    for row in stats:
        pdf.cell(col_width, row_height, str(row[0]), border=1)
        pdf.cell(col_width, row_height, str(row[1]), border=1)
        pdf.ln(row_height)

    # Create visualizations
    charts = create_visualization_charts(df, selected_user, helper)
    
    # Add visualizations to PDF
    if charts:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Visual Analysis', 0, 1, 'C')
        pdf.ln(5)
        
        # Add charts
        for chart_name, chart_buffer in charts.items():
            try:
                # Save chart to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                    tmp_file.write(chart_buffer.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Add chart to PDF
                pdf.set_font('Arial', 'B', 12)
                chart_title = chart_name.replace('_', ' ').title()
                pdf.cell(0, 10, chart_title, 0, 1)
                pdf.ln(2)
                
                # Add image (centered, max width 180mm)
                pdf.image(tmp_file_path, x=10, y=None, w=180)
                pdf.ln(5)
                
                # Clean up temporary file
                os.unlink(tmp_file_path)
                
            except Exception as e:
                print(f"Error adding chart {chart_name}: {e}")
                continue

    # Add analysis sections
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Analysis Details', 0, 1)
    pdf.set_font('Arial', '', 10)

    # Add project information
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Project Information', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, 'EchoMind - Decoding Conversations with Machine Learning', 0, 1)
    pdf.cell(0, 10, 'Developed by: Satyam Govind Yadav & Arunkumar Gupta', 0, 1)
    pdf.ln(5)

    # Add insights section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Key Insights', 0, 1)
    pdf.set_font('Arial', '', 10)

    insights = []
    if avg_messages_per_day > 50:
        insights.append("High daily message activity detected")
    if media_ratio > 20:
        insights.append("High media sharing activity")
    if avg_words_per_message > 10:
        insights.append("Detailed conversations with longer messages")
    if total_days > 30:
        insights.append("Long-term conversation analysis")

    if insights:
        for insight in insights:
            pdf.cell(0, 10, f'- {insight}', 0, 1)
    else:
        pdf.cell(0, 10, '- Standard conversation patterns observed', 0, 1)

    # Add footer
    pdf.add_page()
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, 'Report generated by EchoMind - Advanced Conversation Analysis Platform', 0, 1, 'C')
    pdf.cell(0, 10, 'Made with love by Satyam Govind Yadav & Arunkumar Gupta', 0, 1, 'C')

    # Return PDF as BytesIO buffer (ensure non-empty)
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    from io import BytesIO as _BytesIO
    buffer = _BytesIO(pdf_bytes)
    buffer.seek(0)
    return buffer

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """
    Generates a link to download a file
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href
