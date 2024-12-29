# Project Setup and Deployment

## POSTGRES and MAILHOG are REQUIRED for dev purposes

This project uses Docker Compose for managing services in different environments. It includes a development environment with necessary containers and a deployment environment for running the application with all services.

## Docker Compose Files

### 1. `docker-compose.yml` (Development)
This file is used for setting up the development environment. It starts the containers needed for development, including:

- **PostgreSQL** - Database service.
- **Mailhog** - A test mail server used for capturing emails sent during development.

### 2. `docker-compose-deployment.yml` (Deployment)
This file is used for starting the application with all services in containers for production or deployment purposes. It includes all the services required for the application, including Traefik for routing and service discovery.

## Web Server Configuration

- **Traefik** - The web server is configured using Traefik as a reverse proxy. This ensures that the app and its associated services are properly routed.

### Accessing Services

- **Backend**: The application backend can be accessed via `influencers.localhost`.
- **Mailhog**: To view receiving emails during development, access Mailhog via `mailhog.localhost`.
- **Traefik UI**: The Traefik UI, used for managing routing and configurations, is accessible at `traefik.localhost`.

## Setting Up Development Environment

1. Clone this repository to your local machine.
2. Navigate to the project directory and run the following command to start the development containers:

   ```bash
   docker-compose -f docker-compose-deployment.yml up --build -d
