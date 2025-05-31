# AI Agent App

A boilerplate AI agent application with FastAPI backend and Next.js frontend providing a simple chat interface for users to interact with an AI agent powered by OpenAI.

## Project Structure

```
├── README.md
├── prd.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routes/
│   │   │   └── chat.py
│   │   └── services/
│   │       └── ai_service.py
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── package.json
    ├── next.config.js
    ├── tsconfig.json
    ├── src/
    │   ├── app/
    │   │   ├── layout.tsx
    │   │   └── page.tsx
    │   ├── components/
    │   │   ├── ChatInterface.tsx
    │   │   ├── MessageInput.tsx
    │   │   ├── MessageHistory.tsx
    │   │   └── LoadingIndicator.tsx
    │   ├── services/
    │   │   └── api.ts
    │   └── types/
    │       └── chat.ts
    └── .env.local.example
```

## Features

### Backend (FastAPI)

- **Chat Endpoint**: POST `/chat` for AI agent interactions
- **OpenAI Integration**: Real AI responses using OpenAI's GPT models
- **Async Request Handling**: Non-blocking request processing
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **Request Validation**: Input validation using Pydantic models
- **Rate Limiting**: Basic rate limiting implementation
- **Conversation Management**: Maintains conversation history per session

### Frontend (Next.js)

- **Chat Interface**: Clean, responsive chat UI
- **Real-time Updates**: Immediate message display
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **TypeScript**: Full type safety
- **Responsive Design**: Mobile-friendly interface

## Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn
- **OpenAI API Key** (required for AI functionality)

## Setup Instructions

### 1. Get OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key (you'll need it for the backend setup)

### 2. Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create environment file:

   ```bash
   cp env_example .env
   ```

   Edit `.env` and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_actual_openai_api_key_here
   OPENAI_MODEL=gpt-4o
   OPENAI_TEMPERATURE=0.7
   ```

5. Run the development server:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Create environment file:

   ```bash
   cp env_local_example .env.local
   ```

   Edit `.env.local` and configure the backend API URL:

   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Run the development server:

   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## OpenAI Configuration

The application supports various OpenAI configuration options:

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key (required) | None |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o` |
| `OPENAI_TEMPERATURE` | Response creativity (0.0-2.0) | `0.7` |

### Fallback Mode

If the OpenAI API key is not configured or there's an issue with the OpenAI service, the application will automatically fall back to a mock AI service for development purposes.

## API Documentation

### POST `/chat`

Send a message to the AI agent.

**Request Body:**

```json
{
  "message": "Hello, how are you?",
  "conversation_id": "optional-uuid"
}
```

**Response:**

```json
{
  "response": "Hello! I'm doing well, thank you for asking.",
  "conversation_id": "uuid-for-conversation"
}
```

**Error Responses:**

- `400`: Bad Request - Invalid input
- `500`: Internal Server Error - Server or AI service error

## Development

### Backend Development

- API documentation is available at `http://localhost:8000/docs` (Swagger UI)
- Add new routes in `app/routes/`
- Modify AI service logic in `app/services/ai_service.py`
- The system automatically falls back to mock responses if OpenAI is unavailable

### Frontend Development

- Components are located in `src/components/`
- API calls are handled in `src/services/api.ts`
- Type definitions are in `src/types/`

## Production Deployment

### Backend

- Set environment variables for production
- Use a production ASGI server like Gunicorn with Uvicorn workers
- Configure proper CORS settings
- Ensure OpenAI API key is securely set
- Implement authentication if needed

### Frontend

- Run `npm run build` to create production build
- Deploy to platforms like Vercel, Netlify, or similar
- Configure environment variables for production API endpoint

## Costs and Usage

**Important**: This application uses OpenAI's API, which is a paid service. Please be aware of:

- API usage costs based on tokens consumed
- Rate limits imposed by OpenAI
- Monitor your usage in the OpenAI dashboard
- Consider implementing additional rate limiting for production use

## Troubleshooting

### OpenAI API Issues

- Verify your API key is correct and active
- Check your OpenAI account has sufficient credits
- Monitor API rate limits
- Check the logs for detailed error messages

### Development Issues

- Ensure both backend and frontend are running
- Check that environment variables are properly set
- Verify network connectivity between frontend and backend

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
