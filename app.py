import streamlit as st
from pathlib import Path
import os
from agents.transcript_agent import TranscriptAgent
from agents.journalist_agent import JournalistAgent
from agents.editor_agent import EditorAgent
from agents.seo_agent import SEOAgent
from agents.social_media_agent import SocialMediaAgent
from utils.config import load_config

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="AI Content Generator",
    page_icon="🤖",
    layout="wide"
)

# Create necessary directories
for dir in ["agents", "data", "configs", "utils", "styles"]:
    Path(dir).mkdir(exist_ok=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    # Load custom CSS
    local_css("styles/main.css")

    # Header section with gradient background
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0; background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%); color: white; border-radius: 12px; margin-bottom: 2rem;'>
            <h1 style='color: white;'>AI Content Generator</h1>
            <p style='font-size: 1.2rem;'>Transform YouTube videos into engaging content using AI</p>
        </div>
    """, unsafe_allow_html=True)

    # Create two columns for input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url_input = st.text_input("🎥 Enter YouTube URL", placeholder="https://youtube.com/...")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
        generate_button = st.button("🚀 Generate Content", use_container_width=True)

    # Optional transcript input with expander
    with st.expander("📝 Or paste transcript directly"):
        transcript_input = st.text_area("", placeholder="Paste your transcript here...", height=150)
    
    if generate_button and (url_input or transcript_input):
        with st.spinner("🔄 Processing your content..."):
            # Initialize agents
            transcript_agent = TranscriptAgent()
            journalist_agent = JournalistAgent()
            editor_agent = EditorAgent()
            seo_agent = SEOAgent()
            social_media_agent = SocialMediaAgent()

            # Process flow
            if url_input:
                transcript = transcript_agent.fetch_from_url(url_input)
            else:
                transcript = transcript_input

            # Get SEO recommendations first
            with st.status("🔍 Analyzing content for SEO...") as status:
                seo_data = seo_agent.analyze(transcript)
                status.update(label="✅ SEO analysis complete!", state="complete")
            
            # Generate article
            with st.status("✍️ Writing article...") as status:
                article = journalist_agent.write_article(transcript, seo_data)
                status.update(label="✅ Article written!", state="complete")
            
            # Edit article
            with st.status("📝 Editing content...") as status:
                edited_article = editor_agent.edit(article)
                status.update(label="✅ Editing complete!", state="complete")
            
            # Generate social media content
            with st.status("📱 Creating social media posts...") as status:
                social_content = social_media_agent.generate_posts(edited_article, seo_data)
                status.update(label="✅ Social media content ready!", state="complete")

            # Results section
            st.markdown("""
                <div style='background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%); padding: 2px; border-radius: 12px; margin: 2rem 0;'>
                    <div style='background: white; padding: 1.5rem; border-radius: 11px;'>
                        <h2 style='margin-top: 0;'>Generated Content</h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Create tabs for different outputs
            tab1, tab2, tab3 = st.tabs(["📝 Article", "🎯 SEO Analysis", "📱 Social Media"])
            
            with tab1:
                st.markdown(f"### {seo_data['title']}")
                st.write(edited_article)
            
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 🎯 Target Keywords")
                    for kw in seo_data['keywords']:
                        st.markdown(f"- {kw}")
                with col2:
                    st.markdown("### 📊 TLDR Points")
                    for point in seo_data['tldr_points']:
                        st.markdown(f"- {point}")
                st.markdown("### 📝 Meta Description")
                st.info(seo_data['meta_description'])
            
            with tab3:
                if isinstance(social_content, dict):
                    for platform, post in social_content.items():
                        with st.expander(f"📱 {platform.title()} Post"):
                            st.write(post)

            # Detailed outputs in expandable sections
            st.markdown("""
                <div style='background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%); padding: 2px; border-radius: 12px; margin: 2rem 0;'>
                    <div style='background: white; padding: 1.5rem; border-radius: 11px;'>
                        <h2 style='margin-top: 0;'>Detailed Agent Outputs</h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            
            with col1:
                with st.expander("🎥 Transcript"):
                    st.code(transcript, language="markdown")
                
                with st.expander("✍️ Original Draft"):
                    st.write(article)
            
            with col2:
                with st.expander("🔍 Raw SEO Data"):
                    st.json(seo_data)
                
                with st.expander("📊 Content Analytics"):
                    st.markdown("### Content Statistics")
                    st.markdown(f"- **Word Count**: {len(edited_article.split())}")
                    st.markdown(f"- **Reading Time**: {len(edited_article.split()) // 200} minutes")
                    st.markdown(f"- **Keywords Used**: {len(seo_data['keywords'])}")

    else:
        if generate_button:
            st.error("Please provide either a YouTube URL or paste a transcript")
        
        # Show example/placeholder content
        st.markdown("""
            <div style='text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 12px; margin-top: 2rem;'>
                <h3>🚀 Get Started</h3>
                <p>Enter a YouTube URL above or paste your transcript to begin generating content!</p>
                <p style='color: #666; font-size: 0.9rem;'>Our AI agents will help you create SEO-optimized content and social media posts.</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
