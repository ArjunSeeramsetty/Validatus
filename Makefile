.PHONY: help install test start stop clean docker-up docker-down

help: ## Show this help message
	@echo "Validatus Platform - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	@echo "Installing backend dependencies..."
	cd backend && python -m venv venv && \
	venv\Scripts\activate && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Dependencies installed successfully!"

test: ## Test the backend setup
	@echo "Testing backend setup..."
	cd backend && python test_setup.py

start: ## Start development servers
	@echo "Starting Validatus Platform in development mode..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "Use 'make stop' to stop all services"
	@start cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
	@start cmd /k "cd frontend && npm run dev"

stop: ## Stop all development servers
	@echo "Stopping development servers..."
	@taskkill /f /im python.exe 2>nul || echo "No Python processes found"
	@taskkill /f /im node.exe 2>nul || echo "No Node processes found"

clean: ## Clean up generated files
	@echo "Cleaning up..."
	@rmdir /s /q backend\venv 2>nul || echo "No venv directory found"
	@rmdir /s /q frontend\node_modules 2>nul || echo "No node_modules directory found"
	@del /q backend\__pycache__\* 2>nul || echo "No __pycache__ files found"
	@echo "✅ Cleanup completed!"

docker-up: ## Start all services with Docker
	@echo "Starting Validatus Platform with Docker..."
	docker-compose up -d
	@echo "✅ Services started! Access at:"
	@echo "  Backend: http://localhost:8000"
	@echo "  Frontend: http://localhost:3000"

docker-down: ## Stop all Docker services
	@echo "Stopping Docker services..."
	docker-compose down
	@echo "✅ Services stopped!"

docker-logs: ## View Docker service logs
	docker-compose logs -f

build: ## Build Docker images
	@echo "Building Docker images..."
	docker-compose build
	@echo "✅ Images built successfully!"

dev: ## Start development environment
	@echo "Starting development environment..."
	@make install
	@make test
	@make start

prod: ## Start production environment
	@echo "Starting production environment..."
	@make docker-up
	@echo "Production services started!"
