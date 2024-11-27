# YouTube Content Generator 🎥 ✍️

An AI-powered content generation system that transforms YouTube videos into engaging articles, SEO-optimized content, and social media posts.

## 🚀 Features

- **YouTube Transcript Processing**: Automatically fetch and process video transcripts
- **SEO Optimization**: Generate SEO-friendly titles, meta descriptions, and keywords
- **Article Generation**: Create well-structured articles in NYT style
- **Content Editing**: Polish and refine generated content
- **Social Media Integration**: Generate platform-specific social media posts
- **Modern UI**: Beautiful, responsive Streamlit interface

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/keemsmile/YOUTUBEWRITER.git
cd YOUTUBEWRITER
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
set OPENAI_API_KEY=your_api_key_here
```

## 🎮 Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Enter a YouTube URL or paste a transcript
3. Click "Generate Content"
4. View the generated article, SEO analysis, and social media posts

## 🔧 System Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for YouTube transcript fetching

## 📦 Dependencies

- openai==1.33.0
- swarm==0.1.0
- youtube-transcript-api==0.6.1
- streamlit==1.29.0
- langchain==0.0.339
- beautifulsoup4==4.12.2
- requests==2.31.0
- python-slugify==8.0.1

## 🤖 Agent Architecture

The system uses multiple specialized AI agents:

1. **TranscriptAgent**: Fetches and processes YouTube transcripts
2. **SEOAgent**: Analyzes content and generates SEO recommendations
3. **JournalistAgent**: Writes the main article
4. **EditorAgent**: Polishes and refines the content
5. **SocialMediaAgent**: Creates platform-specific social posts

## 🎨 UI Features

- Modern, gradient-based design
- Responsive layout
- Dark mode support
- Progress indicators
- Expandable sections for detailed outputs
- Content analytics

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
