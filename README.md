# 🚇 Crowd Prediction

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)](https://reactjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-5.0+-47A248.svg)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

*A sophisticated full-stack platform for real-time crowd monitoring, intelligent forecasting, and comprehensive analytics for transit operators.*

[📖 Overview](#-overview) • [✨ Features](#-features) • [🏗️ Architecture](#️-architecture) • [🚀 Quick Start](#-quick-start) • [📊 API Documentation](#-api-documentation) • [🤝 Contributing](#-contributing) • [📄 License](#-license)

</div>
I 
---

## 🌟 Overview

**Crowd Prediction** is an advanced transit analytics platform that revolutionizes crowd management through intelligent data collection and predictive modeling. The system empowers transit operators with real-time insights, enabling data-driven decisions to optimize service quality and passenger experience.

Built with cutting-edge technologies and modern architectural patterns, this platform seamlessly integrates real-time reporting, machine learning predictions, and comprehensive analytics into a cohesive, scalable solution.

## ✨ Features

### 🔄 Real-time Capabilities
- **Live Crowd Reporting** - Instant crowd level submissions from mobile and web interfaces
- **Dynamic Updates** - Real-time data synchronization across all connected clients
- **Live Dashboards** - Interactive visualizations updating in real-time

### 🤖 Intelligent Predictions
- **Machine Learning Models** - Advanced algorithms for accurate crowd forecasting
- **Short-term Predictions** - 15-60 minute crowd level predictions
- **Historical Analysis** - Trend analysis and pattern recognition

### 📈 Analytics & Insights
- **Interactive Dashboards** - Comprehensive analytics with drill-down capabilities
- **Heat Maps** - Visual crowd density representations
- **Trend Analysis** - Historical data analysis with actionable insights
- **Custom Reports** - Configurable reporting for different stakeholder needs

### 🔐 Security & Authentication
- **JWT Authentication** - Secure token-based user authentication
- **Role-based Access** - Granular permissions for different user types
- **Data Encryption** - End-to-end data protection
- **API Security** - Comprehensive security measures for all endpoints

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (MongoDB)     │
│                 │    │                 │    │                 │
│ • Single Page   │    │ • REST API      │    │ • Document      │
│   Application   │    │ • Async I/O     │    │   Database      │
│ • Real-time UI  │    │ • ML Pipeline   │    │ • Flexible      │
│ • Responsive    │    │ • Caching       │    │   Schema        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🛠️ Tech Stack

#### Backend
- **Framework:** FastAPI (High-performance async web framework)
- **Language:** Python 3.7+
- **Database:** MongoDB (NoSQL for flexible data models)
- **ORM:** Motor (Async MongoDB driver)
- **Web Server:** Uvicorn (ASGI server)
- **Real-time:** WebSockets (for live updates)
- **Data Validation:** Pydantic
- **Task Queue:** Celery with Redis (for background tasks)
- **Data Processing:** Pandas, NumPy
- **Authentication:** JWT with OAuth2
- **ML Framework:** Scikit-learn, TensorFlow (for predictions)
- **Caching:** Redis (for improved performance)
- **API Documentation:** OpenAPI/Swagger

#### Frontend
- **Framework:** React 18+ (Modern component-based UI)
- **Build Tool:** Create React App
- **Styling:** CSS3 with CSS Modules
- **State Management:** React Context API
- **Charts:** Chart.js, D3.js (for data visualization)
- **Real-time:** WebSocket integration

#### DevOps & Tools
- **Version Control:** Git with GitFlow workflow
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Code Quality:** Pre-commit hooks, ESLint, Black
- **Testing:** Pytest, Jest, React Testing Library

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.7+** - [Download](https://python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **MongoDB 5.0+** - [Download](https://www.mongodb.com/try/download/community)
- **Git** - [Download](https://git-scm.com/downloads)

### 🔧 Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/abhrajyoti-01/Crowd_prediction.git
cd Crowd_prediction
```

#### 2. Backend Setup
```bash
# Navigate to backend directory
cd Backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your MongoDB connection string and credentials

# Initialize database with sample data
python init_db.py

# Start development server
python server.py
# Or alternatively: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Frontend Setup
```bash
# Navigate to frontend directory (new terminal)
cd Frontend

# Install dependencies
npm install

# Start development server
npm start
# Frontend will be available at http://localhost:3000
```

#### 4. Access the Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## 📊 API Documentation

### 🔌 REST API Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/auth/login` | POST | User authentication | ❌ |
| `/api/auth/register` | POST | User registration | ❌ |
| `/api/stations` | GET | Retrieve all stations | ✅ |
| `/api/stations/{id}` | GET | Get station details | ✅ |
| `/api/crowd-reports` | POST | Submit crowd report | ✅ |
| `/api/predictions/{station_id}` | GET | Get predictions | ✅ |
| `/api/analytics/stations` | GET | Analytics data | ✅ |

### 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

```bash
# Login to get token
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Use token in subsequent requests
curl -X GET "http://localhost:8000/api/stations" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🧪 Testing

### Backend Testing
```bash
cd Backend
pytest tests/ -v --cov=app --cov-report=html
```

### Frontend Testing
```bash
cd Frontend
npm test -- --coverage --watchAll=false
```

### Integration Testing
```bash
# Run both frontend and backend tests
./scripts/test-all.sh
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🚀 Getting Started with Development

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch: `git checkout -b feature/amazing-feature`
4. **Make** your changes
5. **Test** thoroughly
6. **Commit** your changes: `git commit -m 'Add amazing feature'`
7. **Push** to the branch: `git push origin feature/amazing-feature`
8. **Open** a Pull Request

### 📝 Development Guidelines

- Follow [PEP 8](https://pep8.org/) for Python code
- Use [ESLint](https://eslint.org/) configuration for JavaScript
- Write comprehensive tests for new features
- Update documentation for API changes
- Use conventional commit messages

### 🐛 Reporting Issues

- Use the [GitHub issue tracker](https://github.com/abhrajyoti-01/Crowd_prediction/issues)
- Include detailed reproduction steps
- Add appropriate labels (bug, enhancement, documentation)
- Be respectful and constructive

## 📁 Project Structure

```
Crowd_prediction/
├── Backend/                 # Python FastAPI backend
│   ├── app/                # Main application package
│   │   ├── api/           # API route handlers
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utility functions
│   ├── tests/             # Backend tests
│   └── requirements.txt   # Python dependencies
├── Frontend/              # React frontend
│   ├── src/              # Source code
│   │   ├── components/   # React components
│   │   ├── services/     # API services
│   │   └── utils/        # Utility functions
│   ├── public/           # Static assets
│   └── package.json      # Node dependencies
└── docs/                 # Documentation
    ├── API.md           # API documentation
    └── ARCHITECTURE.md  # Architecture guide
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Abhrajyoti Nath

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

### 👨‍💻 Core Contributors
- **Abhrajyoti Nath** - *Project Lead & Full-Stack Developer*
  - GitHub: [@abhrajyoti-01](https://github.com/abhrajyoti-01)
  - LinkedIn: [Abhrajyoti Nath](https://linkedin.com/in/abhrajyoti-nath)

### 🔧 Technologies & Libraries
- [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework
- [React](https://reactjs.org/) - User interface library
- [MongoDB](https://www.mongodb.com/) - NoSQL document database
- [Chart.js](https://chartjs.org/) - Data visualization
- [JWT](https://jwt.io/) - Authentication standard

### 🌟 Inspiration
This project draws inspiration from modern transit systems and smart city initiatives worldwide, aiming to contribute to more efficient and passenger-friendly public transportation.

---

<p align="center">

**Made by [Surajit](https://github.com/Surajit09636) | [Arijit](https://github.com/arijit-rapai-sarkar)**

**Contributed with ❤️ by [Abhra](https://github.com/abhrajyoti-01)**

[⭐ Star this repo](https://github.com/abhrajyoti-01/Crowd_prediction) • [🐛 Report issues](https://github.com/abhrajyoti-01/Crowd_prediction/issues) • [📖 Documentation](https://github.com/abhrajyoti-01/Crowd_prediction/wiki)

</p>
