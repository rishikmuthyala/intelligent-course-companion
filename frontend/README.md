# Intelligent Course Companion - Frontend

## Overview

React-based frontend for the Intelligent Course Companion, providing a clean interface for course Q&A using AI.

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast builds and HMR
- **Tailwind CSS** for styling
- **Axios** for API calls

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Copy the example environment file and update if needed:

```bash
cp env.example .env
```

The default configuration points to `http://localhost:8000` for the backend API.

### 3. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### 4. Build for Production

```bash
npm run build
```

## Project Structure

```
/frontend
├── src/
│   ├── components/        # React components
│   │   ├── DashboardPage.tsx    # Main course listing page
│   │   ├── ChatPage.tsx         # Q&A interface
│   │   ├── CourseCard.tsx       # Course display card
│   │   ├── ChatWindow.tsx       # Message history display
│   │   └── MessageInput.tsx     # User input component
│   ├── services/          # API services
│   │   └── api.ts         # Backend API calls
│   ├── types/             # TypeScript types
│   │   └── index.ts       # Shared type definitions
│   ├── App.tsx            # Main app component
│   ├── main.tsx           # Entry point
│   └── index.css          # Global styles with Tailwind
├── public/                # Static assets
├── tailwind.config.js     # Tailwind configuration
├── postcss.config.js      # PostCSS configuration
├── vite.config.ts         # Vite configuration
└── package.json           # Dependencies and scripts
```

## Features

### Dashboard Page
- Lists all available courses
- Shows course statistics (transcript count)
- Quick navigation to course chat

### Chat Page
- Real-time Q&A interface
- Message history with timestamps
- Source chunk citations
- Loading indicators

### Components

1. **DashboardPage**: Main landing page with course grid
2. **ChatPage**: Full Q&A interface for a selected course
3. **CourseCard**: Individual course display with stats
4. **ChatWindow**: Scrollable message history
5. **MessageInput**: Text input with send functionality

## API Integration

The frontend connects to the backend API endpoints:

- `GET /courses` - Fetch available courses
- `POST /sync` - Trigger data synchronization
- `GET /sync/status` - Check sync progress
- `POST /query/{course_id}` - Send questions and receive answers

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Styling

The project uses Tailwind CSS with custom configuration:
- Custom color palette (primary colors)
- Custom animations (fade-in, slide-up)
- Responsive design utilities
- Custom scrollbar styles

## Next Steps

To implement the course listing functionality:

1. Update `DashboardPage` to fetch courses from the API
2. Map through courses and render `CourseCard` components
3. Handle navigation to `ChatPage` with selected course
4. Implement loading and error states