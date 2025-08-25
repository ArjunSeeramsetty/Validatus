# Validatus Platform

A LangGraph-Orchestrated Decision Intelligence Platform that transforms scattered insights into strategic clarity.

## Overview

Validatus Platform is a comprehensive strategic decision intelligence system that addresses the "decision spaghetti" problem faced by enterprise strategy teams. By leveraging multiple AI research agents and strategic scoring frameworks, it provides real-time, cross-validated insights across five critical business segments.

## Key Features

- **Research-First Architecture**: Live market research instead of stale data warehouses
- **Multi-Agent Research**: Specialized AI agents for different research domains
- **Comprehensive Scoring**: 100+ analytical layers with strategic frameworks
- **Real-Time Analysis**: 60-90 second end-to-end analysis completion
- **Strategic Weighting**: Business-important factors receive higher weight in scoring
- **Multiple Data Sources**: Redundancy and validation across research providers

## Architecture

### Backend (Python/FastAPI)
- **LangGraph Orchestration**: Stateful workflow management
- **Research Agents**: Specialized AI agents for different domains
- **Scoring Engine**: Strategic framework implementations
- **API Layer**: RESTful endpoints with real-time status updates

### Frontend (React/TypeScript)
- **Modern UI**: Clean, intuitive dashboard interface
- **Real-Time Updates**: Live progress tracking and status updates
- **Responsive Design**: Mobile and desktop optimized
- **State Management**: Zustand for efficient state handling

## Five-Segment Analytical Framework

1. **CONSUMER**: Demand, behavior, loyalty, perception, engagement
2. **MARKET**: Size, trends, competition, regulations, risks
3. **PRODUCT**: Features, innovation, value, resilience, quality
4. **BRAND**: Awareness, equity, positioning, messaging, monetization
5. **EXPERIENCE**: UX design, customer journey, support, loyalty, engagement

## Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API Key
- Tavily API Key

### Environment Setup
```bash
# Create environment file
cp .env.example .env

# Add your API keys
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

### Launch Platform
```bash
# Start all services
docker-compose up -d

# Access the platform
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Development Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## API Usage

### Start Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Should we enter the electric vehicle market in Europe?",
    "context": {
      "industry": "Automotive",
      "geography": ["Europe"],
      "company_stage": "startup",
      "target_audience": "B2B customers"
    }
  }'
```

### Check Status
```bash
curl "http://localhost:8000/api/v1/analysis/{analysis_id}/status"
```

### Get Results
```bash
curl "http://localhost:8000/api/v1/analysis/{analysis_id}/results"
```

## Research Agents

- **MarketResearchAgent**: Market size, trends, industry reports
- **ConsumerInsightsAgent**: Sentiment, behavior, social media
- **CompetitorAnalysisAgent**: Competitive landscape, positioning
- **TrendAnalysisAgent**: Emerging trends, technological shifts
- **PricingResearchAgent**: Pricing strategies, market pricing

## Scoring Frameworks

- **Sentiment Analysis**: Consumer perception and sentiment
- **Porter's Five Forces**: Competitive intensity analysis
- **PESTLE Analysis**: Macro-environmental factors
- **Market Sizing**: TAM, SAM, SOM, CAGR calculations
- **Competitive Analysis**: Positioning and differentiation
- **Innovation Scoring**: Innovation and disruption metrics

## Project Structure

```
Validatus/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── agents/         # Research agents
│   │   ├── core/           # Core models and workflow
│   │   ├── scoring/        # Scoring frameworks
│   │   └── utils/          # Utility functions
│   ├── main.py             # FastAPI application
│   └── requirements.txt    # Python dependencies
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── stores/         # State management
│   │   └── services/       # API services
│   └── package.json        # Node dependencies
└── docker-compose.yml      # Service orchestration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the GitHub repository.

## Roadmap

- [ ] Enhanced visualization components
- [ ] Historical analysis tracking
- [ ] Team collaboration features
- [ ] Advanced scoring algorithms
- [ ] Integration with business intelligence tools
- [ ] Mobile application
- [ ] Multi-language support
