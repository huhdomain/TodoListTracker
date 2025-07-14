# Todo List Application

## Overview

This is a simple todo list application built with Streamlit. It provides a basic task management system where users can add, toggle completion status, delete, and filter todo items. The application uses Streamlit's session state for data persistence during the session.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - A Python web framework for building interactive web applications
- **UI Components**: Native Streamlit components (st.title, st.write, etc.)
- **State Management**: Streamlit session state for maintaining todo data across interactions

### Backend Architecture
- **Language**: Python
- **Framework**: Streamlit (handles both frontend and backend logic)
- **Data Structure**: In-memory Python lists and dictionaries
- **Session Management**: Streamlit's built-in session state

### Data Storage
- **Primary Storage**: In-memory storage using Streamlit session state
- **Persistence**: Session-based only (data is lost when session ends)
- **Data Structure**: List of dictionaries with fields: id, text, completed, created_at

## Key Components

### Core Functions
1. **add_todo()**: Creates new todo items with UUID and timestamp
2. **toggle_todo()**: Switches completion status of existing todos
3. **delete_todo()**: Removes todos from the list
4. **filter_todos()**: Filters todos by completion status (all, completed, pending)
5. **main()**: Application entry point and UI setup

### Data Model
Each todo item contains:
- `id`: Unique UUID string identifier
- `text`: Task description
- `completed`: Boolean completion status
- `created_at`: Timestamp of creation

### State Management
- Uses Streamlit session state to maintain todos list
- Tracks filter state for UI filtering
- Implements st.rerun() for UI updates after state changes

## Data Flow

1. User inputs are captured through Streamlit components
2. Actions trigger corresponding functions (add, toggle, delete, filter)
3. Functions modify the session state
4. UI automatically updates via st.rerun() calls
5. Filtered results are displayed based on current filter state

## External Dependencies

- **streamlit**: Web framework for the entire application
- **uuid**: For generating unique identifiers
- **datetime**: For timestamp creation
- **typing**: For type hints (Dict, List, Any)

## Deployment Strategy

### Current State
- Single-file application (app.py)
- No database or external storage
- Session-based data persistence only

### Potential Enhancements
- Could be deployed on Streamlit Cloud, Heroku, or similar platforms
- Database integration would be needed for persistent storage
- The application structure is ready for extension with additional features

### Limitations
- Data is lost when the browser session ends
- No user authentication or multi-user support
- No data backup or recovery mechanisms