# All
all: build up

# Build all service images
build:
	docker build -t consumer-flask ./consumers
	docker build -t my_flask ./flask

# Start all services
up:
	docker-compose up -d

# Stop and remove all services
down:
	docker-compose down

# Refresh Project
re: down all

.PHONY: build up down re