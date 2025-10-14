# Crypto Test Admin - Backend API

FastAPI backend for managing cryptocurrency API test cases.

## Setup

### 1. Install Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update database credentials if needed.

### 3. Run the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Test Cases
- `GET /api/cases` - List all test cases (with filters)
- `GET /api/cases/{id}` - Get single test case
- `POST /api/cases` - Create test case
- `PUT /api/cases/{id}` - Update test case
- `DELETE /api/cases/{id}` - Delete test case

### Data Sets
- `GET /api/cases/{case_id}/datasets` - List data sets for a case
- `GET /api/datasets/{id}` - Get single data set
- `POST /api/datasets` - Create data set
- `PUT /api/datasets/{id}` - Update data set
- `DELETE /api/datasets/{id}` - Delete data set

### Environments
- `GET /api/environments` - List all environments

### Metadata
- `GET /api/services` - Get all service names
- `GET /api/modules` - Get all module names
- `GET /api/components` - Get all component names

## Database

Connects to the same PostgreSQL database used by the test execution framework.

Tables:
- `api_auto_cases` - Test case definitions
- `case_data_sets` - Test data sets
- `test_environments` - Environment configurations
