# Movie Explorer Platform Makefile

.PHONY: help build up down restart logs clean

# Default target
help:
	@echo "Movie Explorer Platform - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make build        - Build Docker images"
	@echo "  make up           - Start all services"
	@echo "  make down         - Stop all services"
	@echo "  make restart      - Restart all services"
	@echo "  make logs         - View logs from all services"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Remove all containers and volumes"

# Development commands
build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down:
	docker-compose down

restart: down up

logs:
	docker-compose logs -f

# Cleanup
clean:
	docker-compose down -v
	@echo "All containers and volumes removed!"
