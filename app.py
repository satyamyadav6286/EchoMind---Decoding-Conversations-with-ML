import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
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
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page configuration
st.set_page_config(
    page_title="EchoMind - Decoding Conversations with ML",
    page_icon="💬",
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
    <div class="header">
        <h1>EchoMind</h1>
        <p class="subtitle">Decoding Conversations with Machine Learning</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/chat--v1.png", width=80)
    st.title("Navigation")
    
    selected = option_menu(
        menu_title=None,
        options=["Home", "Upload & Analyze", "About"],
        icons=["house", "cloud-upload", "info-circle"],
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#f8f9fa"},
            "icon": {"color": "orange", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#0d6efd"},
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
        <a href="{twitter_url}" target="_blank" class="share-btn">
            <img src="https://img.icons8.com/ios/24/000000/twitter--v1.png" alt="Share on Twitter"/>
        </a>
        <a href="{linkedin_url}" target="_blank" class="share-btn">
            <img src="https://img.icons8.com/ios/24/000000/linkedin.png" alt="Share on LinkedIn"/>
        </a>
        <a href="#" id="copyLinkBtn" class="share-btn" title="Copy link to clipboard">
            <img src="https://img.icons8.com/ios/24/000000/link--v1.png" alt="Copy link"/>
        </a>
    </div>
    <script>
    document.getElementById('copyLinkBtn').addEventListener('click', function(e) {{
        e.preventDefault();
        navigator.clipboard.writeText('{current_url}').then(function() {{
            // Change icon to checkmark temporarily
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
    st.markdown("---")
    st.markdown(f"""
    <div class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>EchoMind</h3>
                <p>Decoding Conversations with Machine Learning</p>
                {get_share_buttons()}
            </div>
            <div class="footer-section">
                <h4>Team Members</h4>
                <div class="team-member">
                    <p>Satyam Govind Yadav</p>
                    <div class="member-links">
                        <a href="https://github.com/satyamyadav" target="_blank" title="GitHub">
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
                <h4>Quick Links</h4>
                <ul class="footer-links">
                    <li><a href="#" onclick="document.querySelector('a[href^="#"][data-baseweb="tab"]').click(); return false;">Home</a></li>
                    <li><a href="#" onclick="document.querySelector('a[href^="#"][data-baseweb="tab"]:nth-child(2)').click(); return false;">Analyze</a></li>
                    <li><a href="#" onclick="document.querySelector('a[href^="#"][data-baseweb="tab"]:last-child').click(); return false;">About</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; {datetime.now().year} EchoMind. All rights reserved.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Home Page
if selected == "Home":
    st.markdown("""
    <div class="welcome-section">
        <h2>Welcome to EchoMind</h2>
        <p>Your advanced conversation analysis platform powered by Machine Learning. Gain deep insights from your chat data with beautiful visualizations and comprehensive analytics.</p>
        
        <div class="features">
            <div class="feature-card">
                <h3>📊 Conversation Analytics</h3>
                <p>Get detailed statistics and visualizations of your chat data.</p>
            </div>
            <div class="feature-card">
                <h3>🔍 Sentiment Analysis</h3>
                <p>Understand the emotional tone of your conversations.</p>
            </div>
            <div class="feature-card">
                <h3>📈 Trend Analysis</h3>
                <p>Track conversation patterns and trends over time.</p>
            </div>
        </div>
        
        <div class="cta">
            <h3>Ready to get started?</h3>
            <p>Upload your chat data and unlock powerful insights today!</p>
            <a href="#upload" class="btn btn-primary">Upload Chat</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Upload & Analyze Page
elif selected == "Upload & Analyze":
    st.header("Upload & Analyze Your Chat")
    st.write("Upload your exported chat file to begin analysis.")
    
    uploaded_file = st.file_uploader("Choose a file", type=['txt'], key="file_uploader")
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        # Show file details
        file_details = {"Filename":uploaded_file.name, "FileType":uploaded_file.type, "FileSize":uploaded_file.size}
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
        st.sidebar.header("Analysis Options")
        selected_user = st.sidebar.selectbox("Select User for Analysis", user_list)
        
        if st.sidebar.button("Show Analysis"):
            # Stats Area with cards
            st.markdown("### 📊 Chat Statistics")
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>Total Messages</h3>
                    <h2>{num_messages}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>Total Words</h3>
                    <h2>{words}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>Media Shared</h3>
                    <h2>{num_media_messages}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>Links Shared</h3>
                    <h2>{num_links}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Timeline visualization
            st.markdown("### 📅 Timeline Analysis")
            
            # Monthly Timeline
            st.markdown("#### Monthly Activity")
            timeline = helper.monthly_timeline(selected_user, df)
            fig = px.line(timeline, x='time', y='message', 
                         title='Monthly Message Count',
                         labels={'time': 'Month', 'message': 'Number of Messages'},
                         template='plotly_white')
            fig.update_traces(line=dict(color='#0d6efd', width=3))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=True, gridcolor='#f0f0f0'))
            st.plotly_chart(fig, use_container_width=True)

            # Daily Timeline
            st.markdown("#### Daily Activity")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig = px.area(daily_timeline, x='only_date', y='message',
                         title='Daily Message Count',
                         labels={'only_date': 'Date', 'message': 'Number of Messages'},
                         template='plotly_white')
            fig.update_traces(fill='tozeroy', line=dict(color='#0d6efd', width=2))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=True, gridcolor='#f0f0f0'))
            st.plotly_chart(fig, use_container_width=True)
            
            # Activity Map
            st.markdown("### 📊 Activity Map")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Most Active Day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig = px.bar(busy_day, x=busy_day.index, y=busy_day.values,
                            labels={'x': 'Day of Week', 'y': 'Number of Messages'},
                            color_discrete_sequence=['#6f42c1'])
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                xaxis=dict(showgrid=False),
                                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Most Active Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig = px.bar(busy_month, x=busy_month.index, y=busy_month.values,
                            labels={'x': 'Month', 'y': 'Number of Messages'},
                            color_discrete_sequence=['#fd7e14'])
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                xaxis=dict(showgrid=False),
                                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'))
                st.plotly_chart(fig, use_container_width=True)
            
            # Weekly Activity Heatmap
            st.markdown("#### Weekly Activity Heatmap")
            # Weekly Activity Heatmap
            st.markdown("#### Weekly Activity Heatmap")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig = px.imshow(user_heatmap,
                          labels=dict(x="Hour of Day", y="Day of Week", color="Messages"),
                          x=[f"{h:02d}:00" for h in range(24)],
                          y=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                          color_continuous_scale='Viridis')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=False))
            st.plotly_chart(fig, use_container_width=True)
            
            # Finding the busiest users in the group (Group level only)
            if selected_user == 'Overall':
                st.markdown("### 👥 User Activity")
                x, new_df = helper.most_busy_users(df)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Most Active Users")
                    fig = px.bar(x=x.index, y=x.values,
                                labels={'x': 'User', 'y': 'Number of Messages'},
                                color=x.values,
                                color_continuous_scale='Bluered')
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    xaxis=dict(showgrid=False),
                                    yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                                    showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### User Activity Distribution")
                    st.dataframe(new_df.style.background_gradient(cmap='Blues'),
                               use_container_width=True)

            # Word Cloud Analysis
            st.markdown("### 📝 Word Cloud")
            st.markdown("Visual representation of the most frequently used words in the conversation.")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(df_wc, interpolation='bilinear')
            ax.axis('off')
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
                            color_continuous_scale='Viridis')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                xaxis=dict(showgrid=False),
                                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
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
                    st.markdown("#### Top Emojis Used")
                    st.dataframe(emoji_df.head(10).style.background_gradient(cmap='YlOrRd'),
                               use_container_width=True)
                
                with col2:
                    st.markdown("#### Emoji Distribution")
                    if len(emoji_df) >= 5:
                        fig = px.pie(emoji_df.head(5), 
                                   values=emoji_df[1].head(5), 
                                   names=emoji_df[0].head(5),
                                   hole=0.5,
                                   color_discrete_sequence=px.colors.sequential.RdBu)
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        fig.update_layout(showlegend=False,
                                        margin=dict(t=0, b=0, l=0, r=0))
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Not enough emoji data for visualization")
            else:
                st.info("No emoji data available for analysis.")
            
            # Add footer to the analysis page
            footer()

# About Page
elif selected == "About":
    st.markdown("""
    <div class="about-section">
        <h2>About EchoMind</h2>
        <p>EchoMind is an advanced conversation analysis platform that helps you gain insights from your chat data using Machine Learning and Data Visualization.</p>
        
        <h3>Features</h3>
        <ul class="feature-list">
            <li>📊 Detailed conversation statistics and analytics</li>
            <li>📅 Timeline analysis of message frequency</li>
            <li>📈 Activity patterns and trends</li>
            <li>📝 Word cloud visualization</li>
            <li>😊 Emoji analysis</li>
            <li>👥 User activity comparison (for group chats)</li>
        </ul>
        
        <h3>How to Use</h3>
        <ol>
            <li>Export your WhatsApp chat (without media)</li>
            <li>Go to the 'Upload & Analyze' page</li>
            <li>Upload your chat file</li>
            <li>Explore the insights and visualizations</li>
        </ol>
        
        <div class="team-section">
            <h3>Project Team</h3>
            <div class="team-members">
                <div class="team-member">
                    <h4>Satyam Govind Yadav</h4>
                    <p>Lead Developer & ML Engineer</p>
                </div>
                <div class="team-member">
                    <h4>Arunkumar Gupta</h4>
                    <p>UI/UX Designer & Developer</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add footer to the about page
    footer()











