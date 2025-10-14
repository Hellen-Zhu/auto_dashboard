# Crypto Test Admin - Frontend

Web UI for managing cryptocurrency API test cases.

## MVP Version - Pure HTML/JavaScript

This is a simplified MVP version using pure HTML, CSS, and vanilla JavaScript.
No build process or npm packages required!

## How to Run

### Option 1: Using Python HTTP Server

```bash
cd frontend
python3 -m http.server 3000
```

Then open: http://localhost:3000

### Option 2: Using Node.js HTTP Server

```bash
cd frontend
npx http-server -p 3000
```

Then open: http://localhost:3000

### Option 3: Direct File Open

Simply open `index.html` directly in your browser.

**Note**: If using direct file open, you may encounter CORS issues. Use Option 1 or 2 instead.

## Prerequisites

- Backend API must be running at http://localhost:8000
- Browser with JavaScript enabled

## Features

- ✅ View all test cases
- ✅ Filter by Service and Module
- ✅ Create new test case
- ✅ Edit existing test case
- ✅ Delete test case
- ✅ JSON editor for test steps

## Future Enhancements

For a production version, consider:
- React + TypeScript + Vite for better developer experience
- Ant Design components for richer UI
- React Router for multi-page navigation
- Data set management page
- Advanced JSON editor (Monaco Editor or similar)
- User authentication
