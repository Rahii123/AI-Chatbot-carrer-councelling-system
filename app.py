from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from dotenv import load_dotenv
import sys

# -------------------------- Load .env --------------------------
load_dotenv()

# -------------------------- Flask --------------------------
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)

# -------------------------- Check Dependencies --------------------------
def check_dependencies():
    missing_deps = []
    
    # Check core dependencies
    try:
        import langchain_community
    except ImportError:
        missing_deps.append("langchain-community")
    
    try:
        import langchain_google_genai
    except ImportError:
        missing_deps.append("langchain-google-genai")
    
    try:
        import langchain_groq
    except ImportError:
        missing_deps.append("langchain-groq")
    
    try:
        import faiss
    except ImportError:
        missing_deps.append("faiss-cpu")
    
    return missing_deps

# Check dependencies on startup
missing_deps = check_dependencies()
if missing_deps:
    print(f"⚠️ Missing dependencies: {', '.join(missing_deps)}")
    print("Some features may not work properly.")

# -------------------------- Database --------------------------
try:
    from database import CareerCounselingDB
    db = CareerCounselingDB()
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"❌ Database import failed: {e}")
    DATABASE_AVAILABLE = False
    # Create a simple mock database class
    class MockDB:
        def create_user(self, *args, **kwargs): return 1
        def verify_user(self, *args, **kwargs): return {'id': 1, 'username': 'test'}
        def get_user_by_id(self, *args, **kwargs): return {'username': 'test'}
        def save_message(self, *args, **kwargs): pass
        def get_chat_history(self, *args, **kwargs): return []
        def get_user_sessions(self, *args, **kwargs): return []
        def create_session(self, *args, **kwargs): return 'test-session'
        def update_user_profile(self, *args, **kwargs): pass
    db = MockDB()

# -------------------------- AI Setup --------------------------
def setup_ai_components():
    """Setup AI components with fallbacks"""
    model = None
    embed_model = None
    vector_store = None
    retriever = None
    
    try:
        # Try to import LangChain components
        from langchain_community.vectorstores import FAISS
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_groq import ChatGroq
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        from langchain_core.prompts import PromptTemplate
        
        print("✅ LangChain components imported successfully")
        
        # Initialize Groq model
        if os.getenv("GROQ_API_KEY"):
            model = ChatGroq(
                model_name="llama-3.1-8b-instant",
                groq_api_key=os.getenv("GROQ_API_KEY"),
                temperature=0.1
            )
            print("✅ Groq model initialized")
        else:
            print("❌ GROQ_API_KEY not found")
            
        # Initialize embeddings
        if os.getenv("GOOGLE_API_KEY"):
            embed_model = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
            print("✅ Google embeddings initialized")
        else:
            print("❌ GOOGLE_API_KEY not found")
            
        # Setup FAISS vector store
        index_path = "vectorsdata/academic_index"
        pdf_path = "academicdisciplinesoutline.pdf"
        
        if embed_model and os.path.exists(pdf_path):
            try:
                if os.path.exists(index_path):
                    vector_store = FAISS.load_local(
                        index_path, 
                        embeddings=embed_model,
                        allow_dangerous_deserialization=True
                    )
                    print("✅ FAISS vector store loaded")
                else:
                    # Create new vector store
                    documents = PyPDFLoader(pdf_path).load()
                    chunks = RecursiveCharacterTextSplitter(
                        chunk_size=2000, 
                        chunk_overlap=400
                    ).split_documents(documents)
                    vector_store = FAISS.from_documents(chunks, embed_model)
                    vector_store.save_local(index_path)
                    print("✅ FAISS vector store created and saved")
            except Exception as e:
                print(f"❌ FAISS setup failed: {e}")
        
        if vector_store:
            retriever = vector_store.as_retriever(search_kwargs={"k": 3})
            print("✅ Retriever initialized")
            
    except Exception as e:
        print(f"❌ AI setup failed: {e}")
    
    return model, embed_model, vector_store, retriever

# Initialize AI components
model, embed_model, vector_store, retriever = setup_ai_components()

# -------------------------- RAG Pipeline --------------------------
def get_ai_response(question):
    """Get AI response with comprehensive error handling"""
    if not model:
        return "AI service is not available. Please check your API keys and dependencies."
    
    try:
        # Simple prompt without RAG if retriever is not available
        if not retriever:
            prompt = f"""You are a helpful career counselor assistant. 
Answer the following question about career guidance:

Question: {question}

Answer:"""
            response = model.invoke(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        
        # Use RAG if available
        docs = retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        prompt = f"""You are a helpful and knowledgeable career counselor assistant.
Answer questions based on the context provided.

Context:
{context}

Question:
{question}

Answer:"""
        
        response = model.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
        
    except Exception as e:
        print(f"❌ Error in get_ai_response: {e}")
        return "I apologize, but I'm having trouble processing your question. Please try again."

# -------------------------- Flask Routes --------------------------
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name', '')
        
        if DATABASE_AVAILABLE:
            user_id = db.create_user(username, email, password, full_name)
            if user_id:
                session['user_id'] = user_id
                session['username'] = username
                session['full_name'] = full_name
                return redirect(url_for('dashboard'))
            return render_template('signup.html', error='Username or email already exists')
        else:
            # Mock authentication for demo
            session['user_id'] = 1
            session['username'] = username
            session['full_name'] = full_name
            return redirect(url_for('dashboard'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if DATABASE_AVAILABLE:
            user = db.verify_user(username, password)
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['full_name'] = user.get('full_name') or user.get('username')
                user_sessions = db.get_user_sessions(user['id'])
                if user_sessions:
                    session['session_id'] = user_sessions[0]['session_id']
                else:
                    session['session_id'] = db.create_session(user['id'])
                return redirect(url_for('dashboard'))
            return render_template('login.html', error='Invalid username or password')
        else:
            # Mock authentication for demo
            session['user_id'] = 1
            session['username'] = username
            session['full_name'] = username
            session['session_id'] = 'demo-session'
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_info = {
        'username': session.get('username', 'User'),
        'full_name': session.get('full_name', 'User')
    }
    
    sessions = []
    if DATABASE_AVAILABLE:
        sessions = db.get_user_sessions(session['user_id'])
    
    return render_template('dashboard.html', 
                         username=user_info['username'],
                         full_name=user_info['full_name'],
                         sessions=sessions)

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'session_id' not in session:
        if DATABASE_AVAILABLE:
            session['session_id'] = db.create_session(session['user_id'])
        else:
            session['session_id'] = 'demo-session'
    
    user_info = {
        'username': session.get('username', 'User'),
        'full_name': session.get('full_name', 'User')
    }
    
    return render_template('chat.html', 
                         username=user_info['username'], 
                         full_name=user_info['full_name'])

@app.route('/api/chat', methods=['POST'])
def api_chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({"error": "Message is empty"}), 400
    
    session_id = session.get('session_id')
    user_id = session['user_id']
    
    # Save user message
    if DATABASE_AVAILABLE:
        db.save_message(session_id, user_id, 'user', user_message)
    
    # Get AI response
    ai_response = get_ai_response(user_message)
    
    # Save AI response
    if DATABASE_AVAILABLE:
        db.save_message(session_id, user_id, 'assistant', ai_response)
    
    return jsonify({'response': ai_response, 'session_id': session_id})

@app.route('/api/suggested-questions')
def suggested_questions():
    questions = [
        "What are the career options after FSC Pre-Medical?",
        "Which fields have the highest growth potential in healthcare?",
        "How can I transition from medical to business fields?",
        "What are the scope and salary of data science in healthcare?"
    ]
    return jsonify(questions)

@app.route('/api/history')
def api_history():
    if 'user_id' not in session:
        return jsonify([])
    
    if DATABASE_AVAILABLE:
        session_id = session.get('session_id')
        user_id = session['user_id']
        history = db.get_chat_history(session_id, user_id)
        return jsonify(history)
    else:
        return jsonify([])

@app.route('/api/sessions')
def api_sessions():
    if 'user_id' not in session:
        return jsonify([])
    
    if DATABASE_AVAILABLE:
        user_id = session['user_id']
        sessions = db.get_user_sessions(user_id)
        return jsonify(sessions)
    else:
        return jsonify([{'session_id': 'demo-session', 'created_at': '2024-01-01'}])

@app.route('/api/user-profile')
def api_user_profile():
    if 'user_id' not in session:
        return jsonify({}), 401
    
    return jsonify({
        'username': session.get('username', 'User'),
        'full_name': session.get('full_name', 'User'),
        'educational_background': '',
        'interests': []
    })

@app.route('/api/update-profile', methods=['POST'])
def api_update_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if DATABASE_AVAILABLE:
        data = request.get_json(force=True)
        educational_background = data.get('educational_background', '')
        interests = data.get('interests', [])
        db.update_user_profile(session['user_id'], educational_background, interests)
    
    return jsonify({'success': True})

# -------------------------- Run Flask --------------------------
if __name__ == '__main__':
    print("🚀 Starting Career Counselor Application...")
    print(f"✅ Flask: Available")
    print(f"✅ Database: {'Available' if DATABASE_AVAILABLE else 'Mock (for demo)'}")
    print(f"✅ AI Model: {'Available' if model else 'Not available - check API keys'}")
    print(f"✅ Vector Store: {'Available' if vector_store else 'Not available'}")
    
    app.run(debug=True)