# SmartOps Frontend

Vue 3 + Vite application for text summarization and task prioritization.

## Features

- **Text Summarization**: Upload or paste text to get a 5-sentence summary
- **Task Extraction**: Extract and prioritize actionable items from text
- Clean, simple UI with responsive design

## Setup

### Prerequisites

- Node.js 16+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

### Running the Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

Build output will be in the `dist/` folder.

## Usage

1. Make sure the backend is running at `http://localhost:8000`
2. Paste or type text into the text area
3. Click "Summarize" to get a 5-sentence summary
4. Click "Extract & Prioritize Tasks" to see prioritized action items

## Project Structure

```
smartops-frontend/
├── src/
│   ├── components/
│   │   ├── SummaryList.vue      # Displays summary
│   │   └── TaskTable.vue        # Displays prioritized tasks
│   ├── services/
│   │   └── api.ts               # API service layer
│   ├── App.vue                  # Main application component
│   └── main.js                  # Application entry point
├── public/                       # Static assets
├── index.html                    # HTML entry point
├── vite.config.js               # Vite configuration
└── package.json                 # Dependencies
```

## Backend Connection

The frontend connects to the backend at `http://localhost:8000`. This is configured in `src/services/api.ts`.
