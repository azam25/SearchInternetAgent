# 🔍 SearchInternetAgent - Streamlit Chatbot

A professional, AI-powered internet search chatbot built with Streamlit, featuring an Anthropic-inspired design theme.

## ✨ Features

- **🤖 AI Answer**: Get intelligent responses using three query types:
  - 🎯 **Precise**: 2-3 line concise answers
  - 🔍 **Deep Search**: Comprehensive reports with sections
  - 📊 **Presentation**: Slide-ready content format

- **🌐 Web Context**: Extract only scraped web content without AI processing

- **🔗 Source Attribution**: Each response section includes:
  - Source icon (🔗) for easy identification
  - Hover tooltip showing source and URL
  - Click to open source URL in new browser tab

- **🎨 Professional UI**: Clean, modern design inspired by Anthropic's website theme

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## 🏗️ Architecture

```
User Input → Query Type Selection → SearchInternetAgent → Response Processing → UI Display
```

### Components

- **Frontend**: Streamlit with custom CSS styling
- **Backend**: SearchInternetAgent library integration
- **Search Engine**: Google Custom Search API
- **AI Processing**: Claude 3.5 Sonnet via LLM server
- **Content Processing**: BeautifulSoup for web scraping
- **Semantic Matching**: Sentence transformers for relevance scoring

## 🎯 Usage Guide

### 1. Select Query Type

Choose from the sidebar:
- **Precise**: For quick, concise answers
- **Deep Search**: For comprehensive analysis
- **Presentation**: For slide-ready content

### 2. Ask Questions

Type your query in the input field and choose:
- **🤖 AI Answer**: Get AI-processed responses with source attribution
- **🌐 Web Context**: Get raw scraped web content only

### 3. View Results

Each response includes:
- **Content**: The main answer or information
- **Source Icon**: Click to open source URL
- **Hover Tooltip**: Shows source name and URL on hover

## 🎨 Design Features

### Color Scheme
- **Primary**: Dark gray (#1a1a1a) - Professional and modern
- **Accent**: Blue (#007cba) - Trustworthy and engaging
- **Background**: Clean white with subtle shadows
- **Borders**: Light gray (#e1e5e9) for subtle separation

### UI Elements
- **Gradient Headers**: Professional dark gradient with white text
- **Rounded Corners**: Modern 15px border radius
- **Hover Effects**: Smooth transitions and hover states
- **Responsive Design**: Mobile-friendly layout
- **Loading Animations**: Professional loading indicators

## ⚙️ Configuration

### Environment Variables

The app automatically uses the configuration from your SearchInternetAgent library:
- Google Custom Search API credentials
- LLM server configuration
- Model parameters and settings

### Customization

You can modify the theme by editing the CSS variables in the `streamlit_app.py` file:

```css
:root {
    --primary-color: #1a1a1a;
    --accent-color: #007cba;
    --background-light: #ffffff;
    /* ... more variables */
}
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Error**: Ensure SearchInternetAgent library is properly installed
2. **API Errors**: Check your Google Search API and LLM server credentials
3. **Styling Issues**: Clear browser cache and restart Streamlit

### Debug Mode

Run with debug information:
```bash
streamlit run streamlit_app.py --logger.level debug
```

## 📱 Responsive Design

The app automatically adapts to different screen sizes:
- **Desktop**: Full layout with sidebar and centered content
- **Tablet**: Optimized spacing and touch-friendly buttons
- **Mobile**: Stacked layout with full-width elements

## 🚀 Performance Features

- **Parallel Processing**: Concurrent web searches and content fetching
- **Connection Pooling**: HTTP session reuse for efficiency
- **Smart Caching**: Embedding and result caching
- **Lazy Loading**: Content loads as needed

## 🛡️ Security Features

- **Input Validation**: Query sanitization and validation
- **Error Handling**: Graceful degradation and user-friendly messages
- **Rate Limiting**: Built-in protection against abuse
- **Secure API**: Environment variable configuration

## 📊 Response Format

### AI Answer Response Structure
```json
{
  "text": "The global AI market is valued at $391 billion in 2024",
  "source": "Grand View Research",
  "url": "https://www.grandviewresearch.com/ai-market"
}
```

### Web Context Response
Raw scraped text content from web sources without AI processing.

## 🔄 Chat History

- **Persistent**: Chat history maintained during session
- **Clear Option**: Easy way to reset conversation
- **Timestamp**: Each message includes timestamp
- **Export**: Chat history can be exported (future feature)

## 🌟 Future Enhancements

- [ ] Chat history export functionality
- [ ] Advanced filtering options
- [ ] Custom prompt templates
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Integration with other AI models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the SearchInternetAgent library. Please refer to the main project license.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the main SearchInternetAgent documentation
3. Open an issue on GitHub
4. Contact the development team

---

**Built with ❤️ using Streamlit and SearchInternetAgent**
