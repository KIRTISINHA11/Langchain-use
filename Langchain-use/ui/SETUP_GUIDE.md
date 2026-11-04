# 🚀 ZSearch React UI - Complete Setup Guide

## ⚡ Quick Start (5 minutes)

### 1. Backend Setup
```bash
cd "C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\ui\backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
echo GROQ_API_KEY=your_key > .env
python main.py
```
✅ Backend runs on `http://localhost:8000`

### 2. Frontend Setup
```bash
cd "C:\Users\Admin\Agentic AI Projects\AI\RAG\Langchain-use\ui\React-App"
npm install
npm start
```
✅ Frontend runs on `http://localhost:3000`

---

## 📋 Full Installation Guide

### Prerequisites
- Node.js 16+ - [Download](https://nodejs.org)
- Python 3.10+ - [Download](https://www.python.org)
- Git (optional)

### Step-by-Step Setup

#### Backend Configuration

```bash
# 1. Navigate to backend folder
cd Langchain-use/ui/backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file with API keys
# Create a file named '.env' in the backend folder:
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# 6. Run the backend
python main.py
```

#### Frontend Configuration

```bash
# 1. Navigate to React app
cd ../React-App

# 2. Install npm dependencies
npm install

# 3. Create .env file (optional, defaults to localhost:8000)
echo REACT_APP_API_URL=http://localhost:8000 > .env

# 4. Start development server
npm start
```

---

## 🎯 Features Overview

### 📄 File Upload
- Drag & drop PDF/CSV files
- Real-time upload progress
- Automatic document parsing
- Multi-document support

### 💬 Chat Interface
- Natural language Q&A
- Message history
- Source attribution
- Confidence scores
- Real-time updates

### 📊 Document Management
- View loaded documents
- Clear history
- Track upload status
- API health monitoring

---

## 🔌 API Integration

### Health Check
```bash
curl http://localhost:8000/health
```

### Upload Document
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/upload
```

### Query Documents
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
```

---

## 🛠️ Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is already in use
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port:
uvicorn main:app --port 8001
```

### React App Won't Connect to Backend
1. Verify backend is running on port 8000
2. Check CORS is enabled (it is by default)
3. Update `.env` if using different backend URL
4. Check browser console for errors

### Module Import Errors
```bash
# Make sure you're in the right directory
cd Langchain-use/ui/backend

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Slow Performance
- Use smaller PDF files initially
- Increase chunk size in ingestion
- Check system resources (RAM, disk)
- Consider using ChatGroq instead of OpenAI

---

## 📱 Mobile Compatibility

The React UI is fully responsive and works on:
- ✅ Desktop (1920x1080+)
- ✅ Tablet (768px+)
- ✅ Mobile (375px+)

---

## 🔐 Security Notes

### For Development
- Default CORS allows all origins
- No authentication required
- Files stored locally

### For Production
- Restrict CORS origins
- Add authentication
- Use HTTPS
- Store files securely
- Rate limit API endpoints

---

## 📦 Project Structure

```
Langchain-use/ui/
├── React-App/              # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css
│   │   └── components/
│   │       ├── FileUpload.js
│   │       ├── ChatInterface.js
│   │       └── QueryHistory.js
│   ├── package.json
│   └── .env
│
├── backend/                 # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
└── SETUP_GUIDE.md
```

---

## 🚀 Deployment Options

### Local Machine
- Development: `npm start` + `python main.py`
- Production: `npm run build` + `uvicorn main:app`

### Docker
```dockerfile
# Backend
FROM python:3.10
COPY ui/backend /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]

# Frontend
FROM node:18
COPY ui/React-App /app
WORKDIR /app
RUN npm install && npm run build
CMD ["npm", "start"]
```

### Cloud Platforms
- **Heroku**: Deploy backend, serve frontend
- **Vercel**: Deploy frontend
- **AWS/GCP**: Container services

---

## 💡 Pro Tips

1. **Enable Verbose Logging**
   - Backend: Check terminal output
   - Frontend: Open browser DevTools (F12)

2. **Test API Directly**
   - Use Postman or Insomnia
   - Test `/health` endpoint first
   - Verify `/upload` works before chat

3. **Optimize Chunking**
   - Smaller chunks: faster but less context
   - Larger chunks: slower but better answers
   - Start with 1000-2000 tokens

4. **Monitor Performance**
   - Track query response times
   - Monitor memory usage
   - Check disk space for embeddings

---

## 📞 Support

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Port already in use | Use different port or kill process |
| Module not found | Ensure correct directory, reinstall deps |
| Slow queries | Reduce chunk size, try different model |
| High memory usage | Clear documents, use smaller files |
| API timeout | Increase timeout in App.js |

---

**Ready to use ZSearch? Follow the Quick Start above! 🎉**
