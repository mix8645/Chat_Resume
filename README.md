# Resume Chat Agent API 🤖

A FastAPI-based RAG (Retrieval-Augmented Generation) application that provides intelligent Q&A about resume information using LangChain, MongoDB Atlas Vector Search, and Anthropic Claude.

## 🚀 Features

- **FastAPI REST API** with Bearer Token authentication
- **RAG System** using LangChain for intelligent document retrieval
- **Vector Search** powered by MongoDB Atlas and Voyage AI embeddings
- **LLM Integration** using Anthropic Claude for natural language responses
- **Dockerized** deployment with multi-stage builds
- **Secure** API endpoints with token-based authentication

## 📋 Prerequisites

- Docker & Docker Compose
- MongoDB Atlas account with Vector Search index configured
- API Keys:
  - Voyage AI API Key
  - Anthropic API Key
  - MongoDB Atlas connection URI

## 🛠️ Technology Stack

- **Framework:** FastAPI 0.115.0
- **LLM:** Anthropic Claude (via langchain-anthropic)
- **Embeddings:** Voyage AI (voyage-3.5-lite)
- **Vector Database:** MongoDB Atlas Vector Search
- **Python:** 3.12.10
- **Dependency Management:** Poetry

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd Chat_Resume
```

### 2. Configure environment variables

Create a `.env` file in the root directory:
```env
# API Keys
VOYAGE_API_KEY=your_voyage_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
MONGODB_ATLAS_CLUSTER_URI=your_mongodb_connection_string

# API Token for Bearer Authentication
API_TOKEN=your-secret-token-here
```

### 3. Setup MongoDB Atlas Vector Search Index

Create a Vector Search index named `vector_index` on your `resume` collection:
```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1024,
      "similarity": "cosine"
    }
  ]
}
```

## 🐳 Docker Setup

### Docker Compose Configuration

**`docker-compose.yml`**
```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: my_langchain_app
    ports:
      - "8000:8000"
    environment:
      - VOYAGE_API_KEY=${VOYAGE_API_KEY}
      - MONGODB_ATLAS_CLUSTER_URI=${MONGODB_ATLAS_CLUSTER_URI}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - API_TOKEN=${API_TOKEN}
    restart: unless-stopped
```
## 🚦 Running the Application

### Using Docker Compose
```bash
# Build and start the container
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### Local Development (without Docker)
```bash
# Install dependencies
poetry install

# Run the server
poetry run uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

### Base URL
```
http://localhost:8000
```

### Public Endpoints

#### 1. Root Endpoint
```http
GET /
```

**Response:**
```json
{
  "message": "Resume Chat Agent API is running!",
  "version": "0.1.0",
  "endpoints": {
    "ask": "/ask (POST, requires Bearer token)",
    "health": "/health (GET, public)"
  }
}
```

#### 2. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

### Protected Endpoints (Requires Authentication)

#### 3. Ask Question
```http
POST /ask
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer your-secret-token-here
```

**Request Body:**
```json
{
  "question": "where is he graduate?"
}
```

**Response:**
```json
{
  "question": "where is he graduate?",
  "answer": "Based on the resume, Worachot Chanmueang graduated from..."
}
```

## 🧪 Testing

### Using cURL
```bash
# Health check
curl http://localhost:8000/health

# Ask question with authentication
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secret-token-here" \
  -d '{"question":"where is he graduate?"}'
```

### Using Postman

1. **Create new request**
2. **Set Method:** POST
3. **Set URL:** `http://localhost:8000/ask`
4. **Headers:**
   - `Content-Type`: `application/json`
   - `Authorization`: `Bearer your-secret-token-here`
5. **Body (raw JSON):**
```json
   {
     "question": "where is he graduate?"
   }
```
6. **Send**

### Using Swagger UI

Navigate to: `http://localhost:8000/docs`

1. Click **"Authorize"** 🔒
2. Enter your token: `your-secret-token-here`
3. Click **"Authorize"**
4. Test the `/ask` endpoint

## 📁 Project Structure
```
CHAT_RESUME/
├── golang/                         # Go application part (possibly a microservice)
│   ├── go.mod                      # Go dependencies management file
│   └── main.go                     # Main file to run the Go app
├── python/                  
│   ├── agent/              
│   │   ├── llm.py                  # LLM configuration (e.g., OpenAI, Anthropic)
│   │   ├── prompt.py               # Prompt templates file
│   │   └── rag_chain.py            # Logic for RAG (Retrieval-Augmented Generation)
│   ├── auth/                
│   │   └── security.py             # Security functions (e.g., API keys, JWT)
│   ├── controller/          
│   │   └── controller.py           # API controller code
│   ├── doc/                 
│   │   └── resume.txt              # Resume file used as data
│   ├── models/              
│   │   └── schemas.py              # Pydantic schemas for API data validation
│   └── tasks/
│   │   ├── chunks_generator.py     # Document chunking logic
│   │   └── vector_storage.py       # MongoDB vector store setup          
│   ├── app.py                      # Main file to run the Python app
│   ├── Dockerfile                  # File to build Docker image
│   ├── poetry.lock                 # Locked dependencies file (Poetry)
│   └── pyproject.toml              # Project configuration and dependencies file (Poetry)
├── .env                            # Environment variables file
├── .gitattributes                  # Git attributes configuration file
├── .gitignore                      # File specifying items Git should ignore
├── docker-compose.yml              # Docker Compose configuration file
└── README.md                       # Project explanation document
```

## 🔒 Security

- **Bearer Token Authentication:** All `/ask` requests require valid API token
- **Environment Variables:** Sensitive keys stored in `.env` file
- **Docker Isolation:** Application runs in isolated container
- **HTTPS Ready:** Can be deployed behind reverse proxy (nginx, Traefik)

## 🐛 Troubleshooting

### Issue: "Could not send request" in Postman
- Ensure Docker container is running: `docker ps`
- Check logs: `docker logs my_langchain_app`
- Try `localhost:8000` instead of `127.0.0.1:8000`

### Issue: "ModuleNotFoundError"
- Rebuild without cache: `docker-compose build --no-cache`
- Check PYTHONPATH is set correctly in Dockerfile

### Issue: "No relevant docs were retrieved"
- Verify MongoDB Atlas Vector Search index is **Active**
- Check index name matches code: `vector_index`
- Verify embedding dimensions: 1024 for voyage-3.5-lite

### Issue: Vector search returns empty results
- Ensure documents are uploaded to MongoDB
- Check index configuration (path: `embedding`, dimensions: 1024)
- Verify API keys are correct
- 
```

## 🚀 Deployment

### Production Considerations

1. **Use strong API tokens** (not "your-secret-token-here")
2. **Enable HTTPS** with reverse proxy
3. **Set up monitoring** (health checks, logs)
4. **Configure rate limiting** for API endpoints
5. **Use Docker secrets** instead of .env in production
6. **Set up CI/CD** pipeline for automated deployments

### Example Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Performance

- **Cold start:** ~2-3 seconds (document loading + vector store initialization)
- **Average response time:** 1-3 seconds per query
- **Concurrent requests:** Supports multiple simultaneous requests via FastAPI async

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

[Your License Here]

## 👥 Authors

- **Worachot Chanmueang** - Initial work

## 🙏 Acknowledgments

- LangChain for the RAG framework
- Anthropic for Claude API
- Voyage AI for embeddings
- MongoDB for vector search capabilities

---

**Status:** ✅ Production Ready  
**Version:** 0.1.0  
**Last Updated:** November 13, 2025
