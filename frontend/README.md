# Third Eye - Next.js Frontend

Modern, presentable frontend built with Next.js, TypeScript, and Tailwind CSS.

## Features

- ⚡ Next.js 15 with App Router
- 🎨 Tailwind CSS for styling
- 🔷 TypeScript for type safety
- 🎭 Glassmorphism UI design
- 🌈 Gradient accents and animations
- 📱 Fully responsive
- 🔍 Real-time detection results
- 📋 License plate recognition display

## Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Start development server:**
```bash
npm run dev
```

3. **Open in browser:**
```
http://localhost:3000
```

## Backend Integration

Make sure the Flask backend is running on `http://localhost:5000`

To start the backend:
```bash
cd ../backend
venv\Scripts\activate
python app.py
```

## Build for Production

```bash
npm run build
npm start
```

## Environment Variables

Create a `.env.local` file for custom API URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Tech Stack

- **Framework**: Next.js 15
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Image Optimization**: Next/Image

## UI Design

The interface features:
- Dark theme with gradient backgrounds
- Glassmorphism cards with backdrop blur
- Animated elements and smooth transitions
- Responsive grid layouts
- Custom scrollbar styling
- Interactive drag-and-drop upload
- Real-time status indicators
