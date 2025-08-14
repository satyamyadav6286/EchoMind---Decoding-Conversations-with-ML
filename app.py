import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import json
import base64
import tempfile
import os
from datetime import datetime
import uuid
import pandas as pd
from io import BytesIO
from fpdf import FPDF
from pdf_utils import create_pdf_report, get_binary_file_downloader_html

# Set page configuration
st.set_page_config(
    page_title="EchoMind - Decoding Conversations with ML",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
local_css("style.css")

# Header Section
st.markdown("""
    <div class="main-header">
        <h1>🧠 EchoMind</h1>
        <p>Decoding Conversations with Machine Learning</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h3 style="color: #4f46e5; margin-bottom: 0.5rem;">🧠 EchoMind</h3>
        <p style="color: #b8b8b8; font-size: 0.9rem;">Conversation Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["🏠 Home", "📊 Upload & Analyze", "ℹ️ About"],
        icons=["house", "cloud-upload", "info-circle"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#1a1a2e"},
            "icon": {"color": "#4f46e5", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#16213e", "color": "#ffffff"},
            "nav-link-selected": {"background-color": "#4f46e5"},
        }
    )

def get_share_buttons():
    """Generate HTML for social sharing buttons"""
    current_url = "https://echomind.streamlit.app"  # Replace with your actual URL when deployed
    share_text = "Check out EchoMind - Decoding Conversations with Machine Learning!"
    
    twitter_url = f"https://twitter.com/intent/tweet?url={current_url}&text={share_text}"
    linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={current_url}"
    
    return f"""
    <div class="share-buttons">
        <a href="{twitter_url}" target="_blank" class="share-btn" title="Share on Twitter">
            <img src="https://img.icons8.com/ios/24/000000/twitter--v1.png" alt="Twitter"/>
        </a>
        <a href="{linkedin_url}" target="_blank" class="share-btn" title="Share on LinkedIn">
            <img src="https://img.icons8.com/ios/24/000000/linkedin.png" alt="LinkedIn"/>
        </a>
        <a href="#" id="copyLinkBtn" class="share-btn" title="Copy link to clipboard">
            <img src="https://img.icons8.com/ios/24/000000/link--v1.png" alt="Copy link"/>
        </a>
    </div>
    <script>
    document.getElementById('copyLinkBtn').addEventListener('click', function(e) {{
        e.preventDefault();
        navigator.clipboard.writeText('{current_url}').then(function() {{
            const icon = document.querySelector('#copyLinkBtn img');
            const originalSrc = icon.src;
            icon.src = 'https://img.icons8.com/ios/24/4CAF50/checkmark--v1.png';
            setTimeout(() => {{
                icon.src = originalSrc;
            }}, 2000);
        }});
    }});
    </script>
    """

def footer():
    """Render the footer with team info and social links"""
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>🧠 EchoMind</h3>
                <p>Advanced conversation analysis platform powered by Machine Learning. Gain deep insights from your chat data with beautiful visualizations and comprehensive analytics.</p>
                """ + get_share_buttons() + """
            </div>
            <div class="footer-section">
                <h4>👥 Project Team</h4>
                <div class="team-member">
                    <p>Satyam Govind Yadav</p>
                    <div class="member-links">
                        <a href="https://github.com/satyamyadav6286" target="_blank" title="GitHub">
                            <img src="https://img.icons8.com/ios-filled/20/000000/github.png" alt="GitHub"/>
                        </a>
                        <a href="https://linkedin.com/in/satyamyadav" target="_blank" title="LinkedIn">
                            <img src="https://img.icons8.com/ios-filled/20/000000/linkedin.png" alt="LinkedIn"/>
                        </a>
                    </div>
                </div>
                <div class="team-member">
                    <p>Arunkumar Gupta</p>
                    <div class="member-links">
                        <a href="https://github.com/arungupta" target="_blank" title="GitHub">
                            <img src="https://img.icons8.com/ios-filled/20/000000/github.png" alt="GitHub"/>
                        </a>
                        <a href="https://linkedin.com/in/arungupta" target="_blank" title="LinkedIn">
                            <img src="https://img.icons8.com/ios-filled/20/000000/linkedin.png" alt="LinkedIn"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="footer-section">
                <h4>🔗 Quick Links</h4>
                <ul style="list-style: none; padding: 0; color: #b8b8b8;">
                    <li style="margin-bottom: 0.5rem;">🏠 Home</li>
                    <li style="margin-bottom: 0.5rem;">📊 Upload & Analyze</li>
                    <li style="margin-bottom: 0.5rem;">ℹ️ About</li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; """ + str(datetime.now().year) + """ EchoMind. Made with ❤️ by Satyam Govind Yadav & Arunkumar Gupta</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Home Page
if selected == "🏠 Home":
    st.markdown("""
    <div class="welcome-section">
        <h2>Welcome to EchoMind</h2>
        <p>Your advanced conversation analysis platform powered by Machine Learning. Gain deep insights from your chat data with beautiful visualizations and comprehensive analytics.</p>
        
        <div class="features-grid">
            <div class="feature-card">
                <h3>📊 Conversation Analytics</h3>
                <p>Get detailed statistics and visualizations of your chat data including message counts, word frequency, and activity patterns.</p>
            </div>
            <div class="feature-card">
                <h3>🔍 Sentiment Analysis</h3>
                <p>Understand the emotional tone of your conversations with advanced sentiment analysis algorithms.</p>
            </div>
            <div class="feature-card">
                <h3>📈 Trend Analysis</h3>
                <p>Track conversation patterns and trends over time with interactive timeline visualizations.</p>
            </div>
            <div class="feature-card">
                <h3>📝 Word Cloud</h3>
                <p>Visual representation of the most frequently used words in your conversations.</p>
            </div>
            <div class="feature-card">
                <h3>😊 Emoji Analysis</h3>
                <p>Discover the most used emojis and understand emotional expressions in your chats.</p>
            </div>
            <div class="feature-card">
                <h3>📱 Activity Heatmap</h3>
                <p>Visualize when conversations are most active with detailed hourly and daily heatmaps.</p>
            </div>
        </div>
        
        <div class="cta-section">
            <h3>Ready to get started?</h3>
            <p>Upload your chat data and unlock powerful insights today!</p>
            <a href="#upload" class="btn btn-primary">📤 Upload Chat Data</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Upload & Analyze Page
elif selected == "📊 Upload & Analyze":
    st.markdown("""
    <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 2rem; margin-bottom: 2rem;">
        <h2 style="color: var(--text-primary); margin-bottom: 1rem;">📊 Upload & Analyze Your Chat</h2>
        <p style="color: var(--text-secondary);">Upload your exported chat file to begin comprehensive analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a chat file", type=['txt'], key="file_uploader")
    
    if uploaded_file is not None:
        st.success("✅ File uploaded successfully!")
        
        # Show file details
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": f"{uploaded_file.size / 1024:.2f} KB"}
        st.json(file_details)
        
        # Process the file
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

        # Fetch unique users
        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")
        
        # Sidebar for analysis options
        st.sidebar.markdown("### 📋 Analysis Options")
        selected_user = st.sidebar.selectbox("Select User for Analysis", user_list)
        
        if st.sidebar.button("🚀 Show Analysis", type="primary"):
            # Stats Area with cards
            st.markdown("### 📊 Chat Statistics")
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>Total Messages</h3>
                    <h2>{num_messages:,}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>Total Words</h3>
                    <h2>{words:,}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>Media Shared</h3>
                    <h2>{num_media_messages:,}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>Links Shared</h3>
                    <h2>{num_links:,}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Timeline visualization
            st.markdown("### 📅 Timeline Analysis")
            
            # Monthly Timeline
            st.markdown("#### 📈 Monthly Activity")
            timeline = helper.monthly_timeline(selected_user, df)
            fig = px.line(timeline, x='time', y='message', 
                         title='Monthly Message Count',
                         labels={'time': 'Month', 'message': 'Number of Messages'},
                         template='plotly_dark')
            fig.update_traces(line=dict(color='#4f46e5', width=3))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(showgrid=False, color='#b8b8b8'),
                            yaxis=dict(showgrid=True, gridcolor='#374151', color='#b8b8b8'),
                            font=dict(color='#ffffff'))
            st.plotly_chart(fig, use_container_width=True)

            # Daily Timeline
            st.markdown("#### 📊 Daily Activity")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig = px.area(daily_timeline, x='only_date', y='message',
                         title='Daily Message Count',
                         labels={'only_date': 'Date', 'message': 'Number of Messages'},
                         template='plotly_dark')
            fig.update_traces(fill='tozeroy', line=dict(color='#7c3aed', width=2))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(showgrid=False, color='#b8b8b8'),
                            yaxis=dict(showgrid=True, gridcolor='#374151', color='#b8b8b8'),
                            font=dict(color='#ffffff'))
            st.plotly_chart(fig, use_container_width=True)
            
            # Activity Map
            st.markdown("### 📊 Activity Map")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📅 Most Active Day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig = px.bar(busy_day, x=busy_day.index, y=busy_day.values,
                            labels={'x': 'Day of Week', 'y': 'Number of Messages'},
                            color_discrete_sequence=['#4f46e5'],
                            template='plotly_dark')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                xaxis=dict(showgrid=False, color='#b8b8b8'),
                                yaxis=dict(showgrid=True, gridcolor='#374151', color='#b8b8b8'),
                                font=dict(color='#ffffff'))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 📆 Most Active Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig = px.bar(busy_month, x=busy_month.index, y=busy_month.values,
                            labels={'x': 'Month', 'y': 'Number of Messages'},
                            color_discrete_sequence=['#7c3aed'],
                            template='plotly_dark')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                xaxis=dict(showgrid=False, color='#b8b8b8'),
                                yaxis=dict(showgrid=True, gridcolor='#374151', color='#b8b8b8'),
                                font=dict(color='#ffffff'))
                st.plotly_chart(fig, use_container_width=True)
            
            # Weekly Activity Heatmap
            st.markdown("#### 🔥 Weekly Activity Heatmap")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig = px.imshow(user_heatmap,
                          labels=dict(x="Hour of Day", y="Day of Week", color="Messages"),
                          x=[f"{h:02d}:00" for h in range(24)],
                          y=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                          color_continuous_scale='Viridis',
                          template='plotly_dark')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(showgrid=False, color='#b8b8b8'),
                            yaxis=dict(showgrid=False, color='#b8b8b8'),
                            font=dict(color='#ffffff'))
            st.plotly_chart(fig, use_container_width=True)
            
            # Finding the busiest users in the group (Group level only)
            if selected_user == 'Overall':
                st.markdown("### 👥 User Activity")
                x, new_df = helper.most_busy_users(df)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🏆 Most Active Users")
                    fig = px.bar(x=x.index, y=x.values,
                                labels={'x': 'User', 'y': 'Number of Messages'},
                                color=x.values,
                                color_continuous_scale='Bluered',
                                template='plotly_dark')
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    xaxis=dict(showgrid=False, color='#b8b8b8'),
                                    yaxis=dict(showgrid=True, gridcolor='#374151', color='#b8b8b8'),
                                    font=dict(color='#ffffff'),
                                    showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### 📊 User Activity Distribution")
                    st.dataframe(new_df.style.background_gradient(cmap='Blues'),
                               use_container_width=True)

            # Word Cloud Analysis
            st.markdown("### 📝 Word Cloud")
            st.markdown("Visual representation of the most frequently used words in the conversation.")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(df_wc, interpolation='bilinear')
            ax.axis('off')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            
            # Most Common Words
            st.markdown("### 📊 Most Common Words")
            most_common_df = helper.most_common_words(selected_user, df)
            
            if not most_common_df.empty:
                fig = px.bar(most_common_df.head(20), 
                            x=most_common_df[1].head(20), 
                            y=most_common_df[0].head(20),
                            orientation='h',
                            labels={'x': 'Frequency', 'y': 'Words'},
                            color=most_common_df[1].head(20),
                            color_continuous_scale='Viridis',
                            template='plotly_dark')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                xaxis=dict(showgrid=False, color='#b8b8b8'),
                                yaxis=dict(showgrid=True, gridcolor='#374151', color='#b8b8b8'),
                                font=dict(color='#ffffff'),
                                showlegend=False,
                                height=600)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough data to display common words.")
            
            # Emoji Analysis
            st.markdown("### 😊 Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)
            
            if not emoji_df.empty and len(emoji_df) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🎯 Top Emojis Used")
                    st.dataframe(emoji_df.head(10).style.background_gradient(cmap='YlOrRd'),
                               use_container_width=True)
                
                with col2:
                    st.markdown("#### 📊 Emoji Distribution")
                    if len(emoji_df) >= 5:
                        fig = px.pie(emoji_df.head(5), 
                                   values=emoji_df[1].head(5), 
                                   names=emoji_df[0].head(5),
                                   hole=0.5,
                                   color_discrete_sequence=px.colors.sequential.RdBu,
                                   template='plotly_dark')
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        fig.update_layout(showlegend=False,
                                        margin=dict(t=0, b=0, l=0, r=0),
                                        font=dict(color='#ffffff'))
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Not enough emoji data for visualization")
            else:
                st.info("No emoji data available for analysis.")
            
            # Download PDF Report
            st.markdown("### 📄 Download Report")
            if st.button("📥 Generate PDF Report", type="primary"):
                pdf_buffer = create_pdf_report(df, selected_user, num_messages, words, num_media_messages, num_links)
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_buffer.getvalue(),
                    file_name=f"echomind_report_{selected_user}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
            
            # Add footer to the analysis page
            footer()

# About Page
elif selected == "ℹ️ About":
    st.markdown("""
    <div class="about-section">
        <h2>About EchoMind</h2>
        <p>EchoMind is an advanced conversation analysis platform that helps you gain deep insights from your chat data using Machine Learning and Data Visualization techniques. Our platform provides comprehensive analytics to understand conversation patterns, sentiment, and engagement metrics.</p>
        
        <h3>🚀 Key Features</h3>
        <ul class="feature-list">
            <li>📊 Detailed conversation statistics and analytics</li>
            <li>📅 Timeline analysis of message frequency</li>
            <li>📈 Activity patterns and trends visualization</li>
            <li>📝 Interactive word cloud generation</li>
            <li>😊 Comprehensive emoji analysis</li>
            <li>👥 User activity comparison (for group chats)</li>
            <li>🔥 Activity heatmaps for time-based insights</li>
            <li>📄 PDF report generation and download</li>
        </ul>
        
        <h3>📋 How to Use</h3>
        <ol style="color: var(--text-secondary); line-height: 1.6;">
            <li>Export your WhatsApp chat (without media)</li>
            <li>Navigate to the 'Upload & Analyze' page</li>
            <li>Upload your chat file (.txt format)</li>
            <li>Select user for analysis (or choose 'Overall' for group analysis)</li>
            <li>Explore the comprehensive insights and visualizations</li>
            <li>Download your analysis report in PDF format</li>
        </ol>
        
        <div class="team-section">
            <h3>👥 Project Team</h3>
            <div class="team-members">
                <div class="team-member">
                    <h4 style="color: var(--text-primary); margin-bottom: 0.5rem;">Satyam Govind Yadav</h4>
                    <p style="color: var(--text-secondary); margin: 0;">Lead Developer & ML Engineer</p>
                    <div class="member-links" style="margin-top: 1rem;">
                        <a href="https://github.com/satyamyadav6286" target="_blank" title="GitHub">
                            <img src="https://img.icons8.com/ios-filled/20/000000/github.png" alt="GitHub"/>
                        </a>
                        <a href="https://linkedin.com/in/satyamyadav" target="_blank" title="LinkedIn">
                            <img src="https://img.icons8.com/ios-filled/20/000000/linkedin.png" alt="LinkedIn"/>
                        </a>
                    </div>
                </div>
                <div class="team-member">
                    <h4 style="color: var(--text-primary); margin-bottom: 0.5rem;">Arunkumar Gupta</h4>
                    <p style="color: var(--text-secondary); margin: 0;">UI/UX Designer & Developer</p>
                    <div class="member-links" style="margin-top: 1rem;">
                        <a href="https://github.com/arungupta" target="_blank" title="GitHub">
                            <img src="https://img.icons8.com/ios-filled/20/000000/github.png" alt="GitHub"/>
                        </a>
                        <a href="https://linkedin.com/in/arungupta" target="_blank" title="LinkedIn">
                            <img src="https://img.icons8.com/ios-filled/20/000000/linkedin.png" alt="LinkedIn"/>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <h3>🛠️ Technology Stack</h3>
        <ul style="color: var(--text-secondary); line-height: 1.6;">
            <li><strong>Frontend:</strong> Streamlit, HTML/CSS, JavaScript</li>
            <li><strong>Backend:</strong> Python, Pandas, NumPy</li>
            <li><strong>Machine Learning:</strong> Natural Language Processing, Sentiment Analysis</li>
            <li><strong>Visualization:</strong> Plotly, Matplotlib, Seaborn</li>
            <li><strong>Data Processing:</strong> Text preprocessing, Emoji analysis, Word cloud generation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Add footer to the about page
    footer()
