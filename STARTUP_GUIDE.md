# Validatus Platform Startup Guide

This guide will help you get the Validatus Platform up and running on your local machine.

## Prerequisites

- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- **Docker** and **Docker Compose** installed (for full deployment)
- **API Keys** for OpenAI and Tavily (for production use)

## Quick Start (Development Mode)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test the setup
python test_setup.py

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Verify Installation

- Backend API: `http://localhost:8000/health`
- Frontend: `http://localhost:3000`
- API Documentation: `http://localhost:8000/docs`

## Full Deployment with Docker

### 1. Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit with your API keys
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 2. Start All Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Access Services

- **Backend API**: `http://localhost:8000`
- **Frontend**: `http://localhost:3000`
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`

## Testing the Platform

### 1. Backend Testing

```bash
cd backend
python test_setup.py
```

### 2. API Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test analysis creation
curl -X POST "http://localhost:8000/api/v1/analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Should we enter the B2B SaaS market?",
    "context": {
      "industry": "Technology",
      "geography": ["North America"],
      "company_stage": "startup",
      "target_audience": "B2B SaaS companies"
    }
  }'
```

### 3. Frontend Testing

1. Open `http://localhost:3000` in your browser
2. Fill out the analysis form
3. Submit and monitor progress
4. View results and recommendations

## Troubleshooting

### Common Issues

#### Backend Import Errors
- Ensure you're in the correct directory (`backend/`)
- Check that virtual environment is activated
- Verify all `__init__.py` files exist

#### Frontend Build Errors
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version compatibility
- Verify all dependencies in `package.json`

#### Docker Issues
- Ensure Docker and Docker Compose are running
- Check port conflicts (8000, 3000, 5432, 6379)
- Verify `.env` file configuration

### Logs and Debugging

```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# Database logs
docker-compose logs postgres

# Redis logs
docker-compose logs redis
```

## Development Workflow

### 1. Making Changes

- Backend changes: Server auto-reloads with `--reload` flag
- Frontend changes: Vite hot-reloads automatically
- Database changes: Restart PostgreSQL container

### 2. Adding New Features

1. Update models in `backend/app/models/`
2. Add business logic in `backend/app/services/`
3. Create new agents in `backend/app/agents/`
4. Add scoring frameworks in `backend/app/scoring/`
5. Update frontend components in `frontend/src/components/`

### 3. Testing Changes

```bash
# Backend testing
cd backend
python -m pytest tests/

# Frontend testing
cd frontend
npm test
```

## Production Deployment

### 1. Environment Variables

Ensure all production environment variables are set:
- `OPENAI_API_KEY`
- `TAVILY_API_KEY`
- `DATABASE_URL`
- `REDIS_URL`
- `SECRET_KEY`

### 2. Security Considerations

- Use HTTPS in production
- Implement proper authentication
- Rate limiting
- Input validation
- CORS configuration

### 3. Scaling

- Use production-grade databases (PostgreSQL)
- Implement Redis for caching
- Add load balancers
- Monitor performance metrics

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the README.md for detailed documentation
3. Check the API documentation at `/docs` endpoint
4. Review the code structure and comments

## Next Steps

Once the platform is running:

1. **Configure API Keys**: Add your OpenAI and Tavily API keys
2. **Test Analysis**: Run a sample strategic analysis
3. **Customize Framework**: Modify the analytical structure for your needs
4. **Add Data Sources**: Integrate additional research data sources
5. **Deploy**: Move to production environment

---

**Happy analyzing! 🚀**
