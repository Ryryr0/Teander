# :fire: Teander

**Microservices-based** API consisting of two services:

- Auth
- Profiles

# :triangular_ruler: Architecture

Both services use **REST API** principles. The project uses **Docker** and **Docker Compose** to manage the services and their infrastructure.  
**Nginx** is used as an *API gateway* and *load balancer* for routing and scaling.

#
### Auth Service

The Auth service handles registration, authentication, issuing **JWT** tokens with *RS256*, and managing core user data. It uses the following technologies:

- :rocket: **FastAPI** framework as the base;

- **PostgreSQL** as the primary relational database for persistent storage (*SQLAlchemy* is used for interactions);

- **Apache Kafka** as a message broker for asynchronous communication between services (e.g., user registration events, user data updates).

#
### Profiles Service

The Profiles service manages profile data. It uses the following technologies:

- :rocket: **FastAPI** framework as the base;

- **PostgreSQL** as the primary relational database for persistent storage (*SQLAlchemy* is used for interactions);

- **Redis** as an in-memory cache to improve response times and reduce database load;

- **Apache Kafka** as a message broker for asynchronous communication between services (e.g., user registration events, user data updates).

# :gear: Usage

The project contains all the required files such as `.env`, keys, etc. You just need to run:

```bash
docker compose up --build -d
```

After startup, the project will be available at:

```arduino
http://localhost:8000/
```

You’ll find a simple main page where you can choose the service you’re interested in and use the FastAPI-generated Swagger UI to test the API.