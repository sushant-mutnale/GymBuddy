# 🏋️ GymBuddy - AI-Powered Gym Partner Matching App

An intelligent gym partner matching application that uses **collaborative filtering** to recommend compatible workout partners based on preferences, goals, and workout patterns.

## 🎯 Features (Planned)

- **AI-Powered Matching**: Uses collaborative filtering algorithms to find compatible gym partners
- **User Profiles**: Create detailed profiles with workout preferences, fitness goals, and schedules
- **Smart Recommendations**: Get personalized partner suggestions based on your gym habits
- **Chat System**: Connect and communicate with potential gym partners
- **Workout Tracking**: Log and share workouts with your matched partners

## 🏗️ Project Structure

```
GYMBUDDY/
├── backend/                 # Python FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── config.py       # Configuration settings
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── routers/        # API route handlers
│   │   ├── services/       # Business logic
│   │   └── ml/             # Machine learning & recommendation engine
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
│
├── frontend/               # React/Next.js Frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Application pages
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API service calls
│   │   └── styles/         # CSS/styling files
│   ├── public/             # Static assets
│   └── package.json        # Node dependencies
│
├── docs/                   # Documentation
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run the server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **Scikit-learn** - ML for collaborative filtering

### Frontend
- **React/Next.js** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

*Built with ❤️ for fitness enthusiasts*
