# AI Career Counseling Chatbot 🤖🎓

A smart AI-powered career counseling system that provides personalized career guidance using Retrieval-Augmented Generation (RAG) technology.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![AI](https://img.shields.io/badge/AI-RAG_System-orange.svg)

## 🌟 Features

### 🤖 AI-Powered Counseling
- **Smart Career Guidance**: Get personalized career advice based on your educational background
- **RAG Technology**: Retrieval-Augmented Generation for accurate, context-aware responses
- **Multiple AI Providers**: Support for Groq (Llama) and Google AI models
- **PDF Knowledge Base**: Built-in career information from academic resources

### 💬 Interactive Chat Interface
- **Real-time Chat**: Smooth, responsive chat interface
- **Session Management**: Multiple chat sessions per user
- **Chat History**: Persistent conversation history
- **Suggested Questions**: Pre-defined career-related questions to get started

### 🔐 User Management
- **Secure Authentication**: User registration and login system
- **Profile Management**: Educational background and interests tracking
- **Session Security**: Isolated chat sessions for privacy

### 🛡️ Robust Architecture
- **Graceful Degradation**: Works even when components fail
- **Error Handling**: Comprehensive error management
- **Database Fallback**: Mock database for demo purposes
- **Dependency Checking**: Automatic validation of required packages

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ai-career-counselor.git
   cd ai-career-counselor
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file and add your API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Add Knowledge Base PDF**
   - Place your career guidance PDF file named `academicdisciplinesoutline.pdf` in the project root
   - Or modify the path in `app.py` to point to your PDF

6. **Run the Application**
   ```bash
   python app.py
   ```

7. **Access the Application**
   Open your browser and navigate to: `http://localhost:5000`

## 🔧 Configuration

### API Keys Setup

1. **Groq API Key** (for LLM responses):
   - Visit [Groq Cloud](https://console.groq.com/)
   - Create account and get API key
   - Add to `.env` as `GROQ_API_KEY`

2. **Google AI API Key** (for embeddings):
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Get API key for Embeddings API
   - Add to `.env` as `GOOGLE_API_KEY`

### Optional: Database Setup
The application uses SQLite by default. For production, you can modify `database.py` to use other databases like PostgreSQL.

## 📁 Project Structure

```
ai-career-counselor/
├── app.py                 # Main Flask application
├── database.py           # Database operations and models
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── academicdisciplinesoutline.pdf  # Knowledge base PDF
├── templates/           # HTML templates
│   ├── landing.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── chat.html
│   ├── about.html
│   └── contact.html
├── static/             # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
└── vectorsdata/        # FAISS vector store (auto-generated)
```

## 🏗️ Architecture

### Core Components

1. **Web Framework**: Flask for web interface and API
2. **AI Engine**: 
   - **LLM**: Groq (Llama 3.1 8B Instant) for response generation
   - **Embeddings**: Google Generative AI for text vectorization
   - **Vector Store**: FAISS for efficient similarity search
3. **Database**: SQLite with fallback to mock database
4. **RAG Pipeline**: 
   - Document loading and chunking
   - Vector embedding and storage
   - Context retrieval and response generation

### Key Features Implementation

- **Authentication System**: Session-based user management
- **Chat System**: Real-time messaging with persistence
- **AI Integration**: Flexible model provider architecture
- **Error Handling**: Comprehensive fallback mechanisms

## 🎯 Usage Guide

### For Students/Career Seekers
1. **Register/Login**: Create your account
2. **Set Up Profile**: Add your educational background and interests
3. **Start Chatting**: Ask career-related questions like:
   - "What career options are available after FSC Pre-Medical?"
   - "How can I transition from engineering to data science?"
   - "What are the highest-paying jobs in healthcare?"

### For Developers
The system provides RESTful APIs for extended functionality:

```python
# Example API usage
import requests

# Chat endpoint
response = requests.post('http://localhost:5000/api/chat', 
    json={'message': 'Career options in computer science?'},
    cookies=session_cookies
)
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/dashboard` | User dashboard |
| GET | `/chat` | Chat interface |
| POST | `/api/chat` | Send message to AI |
| GET | `/api/history` | Get chat history |
| GET | `/api/sessions` | Get user sessions |
| GET | `/api/suggested-questions` | Get sample questions |

## 🛠️ Development

### Adding New Features

1. **New AI Providers**:
   Modify `setup_ai_components()` in `app.py` to add support for additional LLM providers.

2. **Extended User Profile**:
   Update database schema in `database.py` and add corresponding form fields.

3. **Additional Knowledge Sources**:
   Add new document loaders in the RAG pipeline and update the vector store.

### Running Tests
```bash
# Add your test commands here
python -m pytest tests/
```

## 🚀 Deployment

### Local Production Setup
```bash
# Install production WSGI server
pip install gunicorn

# Run with production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Cloud Deployment
The application can be deployed on:
- **Heroku**: Add Procfile and required buildpacks
- **AWS Elastic Beanstalk**: Python platform
- **Google App Engine**: Standard Python environment
- **DigitalOcean App Platform**: Simple app deployment

## 📊 Performance

- **Response Time**: < 2 seconds for typical queries
- **Concurrent Users**: Supports multiple simultaneous sessions
- **Knowledge Base**: Scalable vector storage system
- **Memory Usage**: Optimized chunking and embedding

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request


## 🙏 Acknowledgments

- **Groq** for providing fast inference API
- **Google AI** for embedding models
- **LangChain** for the AI framework
- **FAISS** for vector similarity search
- **Flask** community for the web framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Rahii123/ai-career-counselor/issues) page
2. Create a new issue with detailed description
3. Contact: rahiiiraja123@gmail.com

## 🔮 Future Enhancements

- [ ] Resume parsing and analysis
- [ ] Skill gap analysis
- [ ] Job market trends integration
- [ ] Multi-language support
- [ ] Voice interface
- [ ] Mobile application
- [ ] Advanced analytics dashboard

---

<div align="center">

**Built with ❤️ for the future of career guidance**

*Star this repository if you find it helpful!*

</div>
