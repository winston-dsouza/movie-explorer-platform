# 🎬 Movie Explorer Platform

A full-stack web application for exploring movies, actors, directors, and genres. Built with **FastAPI** (Python) backend and **Angular 17** frontend, featuring a modern, responsive design with Bootstrap 5.

## 📸 Features

### Core Features
- 🎥 **Browse Movies**: Explore a rich collection of movies with detailed information
- 🔍 **Advanced Filtering**: Filter by genre, director, actor, and release year
- 🔎 **Smart Search**: Search for movies, actors, and directors
- ❤️ **Favorites**: Save your favorite movies for quick access
- ⏰ **Watch Later**: Create a watch list for future viewing
- 👥 **Actor Profiles**: View actor details and filmography
- 🎬 **Director Profiles**: View director details and filmography

### Technical Highlights
- **RESTful API** with automatic OpenAPI/Swagger documentation
- **Responsive Design** with Bootstrap 5 and custom CSS
- **Local Storage** for favorites and watch later functionality
- **Docker Support** for easy deployment
- **Clean Architecture** with separation of concerns
- **Type Safety** with TypeScript and Pydantic

## 🏗️ Architecture

```
movie-explorer-platform/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configurations
│   │   ├── crud/           # CRUD operations
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── main.py         # Application entry point
│   ├── Dockerfile
│   ├── requirements.txt
│   └── seed_data.py        # Database seeder
├── frontend/               # Angular Frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── models/     # TypeScript interfaces
│   │   │   ├── services/   # Angular services
│   │   │   ├── pages/      # Page components
│   │   │   └── app.routes.ts
│   │   └── environments/
│   ├── Dockerfile
│   ├── package.json
│   └── angular.json
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/movie-explorer-platform.git
cd movie-explorer-platform
```

2. **Start the application with Docker Compose**
```bash
docker-compose up --build
```

3. **Access the application**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run database seeder**
```bash
python seed_data.py
```

5. **Start the backend server**
```bash
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
ng serve
```

4. **Access the application**
- Frontend: http://localhost:4200
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📖 API Documentation

The API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs
- OpenAPI Spec: http://localhost:8000/openapi.json

### Main API Endpoints

#### Movies
- `GET /api/movies` - List all movies with filtering options
- `GET /api/movies/{id}` - Get movie details
- `GET /api/movies/search` - Search movies
- `POST /api/movies` - Create a new movie
- `PUT /api/movies/{id}` - Update movie
- `DELETE /api/movies/{id}` - Delete movie

#### Actors
- `GET /api/actors` - List all actors
- `GET /api/actors/{id}` - Get actor details with filmography
- `GET /api/actors/search` - Search actors
- `POST /api/actors` - Create a new actor
- `PUT /api/actors/{id}` - Update actor
- `DELETE /api/actors/{id}` - Delete actor

#### Directors
- `GET /api/directors` - List all directors
- `GET /api/directors/{id}` - Get director details with filmography
- `GET /api/directors/search` - Search directors
- `POST /api/directors` - Create a new director
- `PUT /api/directors/{id}` - Update director
- `DELETE /api/directors/{id}` - Delete director

#### Genres
- `GET /api/genres` - List all genres
- `GET /api/genres/{id}` - Get genre details
- `POST /api/genres` - Create a new genre
- `PUT /api/genres/{id}` - Update genre
- `DELETE /api/genres/{id}` - Delete genre

## 🎨 Frontend Features

### Pages
1. **Movie List**: Browse all movies with filters and search
2. **Movie Detail**: View complete movie information and cast
3. **Actor List**: Browse all actors with search
4. **Actor Detail**: View actor profile and filmography
5. **Director List**: Browse all directors with search
6. **Director Detail**: View director profile and filmography
7. **Favorites**: View and manage favorite movies
8. **Watch Later**: Manage your watch list

### User Features
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Local Storage**: Persists favorites and watch later across sessions
- **Real-time Updates**: Immediate UI updates when adding/removing favorites
- **Loading States**: Proper loading indicators for all async operations
- **Error Handling**: User-friendly error messages

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **SQLite** - Lightweight database (can be replaced with PostgreSQL)
- **Uvicorn** - ASGI server

### Frontend
- **Angular 17** - Modern web application framework
- **TypeScript** - Type-safe JavaScript
- **Bootstrap 5** - CSS framework for responsive design
- **Bootstrap Icons** - Icon library
- **RxJS** - Reactive programming library

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Web server for frontend

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test

# Run with coverage
npm run test:ci

# Run in watch mode
npm run test:watch
```

### E2E Tests
```bash
cd frontend
ng e2e
```

## 📝 Environment Variables

### Backend
Create a `.env` file in the `backend` directory:
```env
DATABASE_URL=sqlite:///./movie_explorer.db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Frontend
Environment files are located in `frontend/src/environments/`:
- `environment.ts` - Development configuration
- `environment.prod.ts` - Production configuration

## 🚢 Deployment

### Using Docker Compose

```bash
docker-compose up -d
```

The application will be available at:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Winston** - Full Stack Developer

##  Support

For support, email winstondsouza688@gmail.com or open an issue in the repository.
