# AI Agent App

A boilerplate AI agent application with FastAPI backend and Next.js frontend providing a simple chat interface for users to interact with multiple AI agents including OpenAI GPT, Google Gemini, and Anthropic Claude.

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
│   │       ├── ai_service_manager.py
│   │       ├── openai_ai_service.py
│   │       ├── gemini_ai_service.py
│   │       ├── anthropic_ai_service.py
│   │       └── dummy_ai_service.py
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

- **Multi-AI Support**: Choose between OpenAI GPT, Google Gemini, Anthropic Claude, or Mock AI
- **Dynamic Service Switching**: Change AI providers at runtime via API
- **Smart Fallback System**: Automatically falls back to available services
- **Chat Endpoint**: POST `/chat` for AI agent interactions
- **Service Management**: Endpoints to check and switch AI services
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
- **At least one AI API Key** (OpenAI, Google Gemini, or Anthropic)

## AI Services Setup

### OpenAI GPT

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key

### Google Gemini

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key for configuration

### Anthropic Claude

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key

## Setup Instructions

### Backend Setup

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

5. **Configure AI Services** (at least one required):
   Edit `.env` and add your API keys:

   ```env
   # Choose your preferred AI service
   AI_SERVICE=openai  # or gemini, anthropic, dummy
   
   # OpenAI Configuration
   OPENAI_API_KEY=your_actual_openai_api_key_here
   OPENAI_MODEL=gpt-4o
   
   # Google Gemini Configuration  
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   GEMINI_MODEL=gemini-pro
   
   # Anthropic Configuration
   ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here
   ANTHROPIC_MODEL=claude-3-sonnet-20240229
   ```

6. Run the development server:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

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

## AI Service Configuration

The application supports multiple AI services with easy switching:

### Service Selection

| Service | Environment Variable | Default Model |
|---------|---------------------|---------------|
| OpenAI | `AI_SERVICE=openai` | `gpt-4o` |
| Google Gemini | `AI_SERVICE=gemini` | `gemini-pro` |
| Anthropic | `AI_SERVICE=anthropic` | `claude-3-sonnet-20240229` |
| Mock (Development) | `AI_SERVICE=dummy` | N/A |

### Configuration Options

| Provider | Configuration Variables |
|----------|------------------------|
| **OpenAI** | `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_TEMPERATURE` |
| **Gemini** | `GEMINI_API_KEY`, `GEMINI_MODEL`, `GEMINI_TEMPERATURE`, `GEMINI_MAX_OUTPUT_TOKENS` |
| **Anthropic** | `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`, `ANTHROPIC_TEMPERATURE`, `ANTHROPIC_MAX_TOKENS` |

### Smart Fallback System

The application automatically handles service failures:

1. **Primary**: Uses your configured `AI_SERVICE`
2. **Fallback**: Tries other configured services if primary fails
3. **Final Fallback**: Uses mock service for development

## API Documentation

### Core Chat Endpoint

#### POST `/chat`

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

### Service Management Endpoints

#### GET `/chat/services`

Get available AI services and current active service.

**Response:**

```json
{
  "current_service": "openai",
  "available_services": ["openai", "gemini", "anthropic", "dummy"]
}
```

#### POST `/chat/services/switch/{service_name}`

Switch to a different AI service.

**Response:**

```json
{
  "success": true,
  "message": "Successfully switched to GEMINI service",
  "current_service": "gemini"
}
```

### Health Check Endpoints

#### GET `/chat/health`

Enhanced health check with AI service information.

**Response:**

```json
{
  "status": "healthy",
  "service": "chat",
  "ai_service": "openai",
  "available_services": ["openai", "gemini", "dummy"]
}
```

## Development

### Backend Development

- API documentation is available at `http://localhost:8000/docs` (Swagger UI)
- Add new routes in `app/routes/`
- Modify AI service logic in `app/services/`
- The system automatically falls back to mock responses if no AI services are configured

### Adding New AI Services

1. Create a new service class in `app/services/` following the existing pattern
2. Implement the required methods: `process_message()`, `get_conversation_history()`, `clear_conversation()`
3. Add the service to `AIServiceManager._create_service()`
4. Update environment configuration

### Frontend Development

- Components are located in `src/components/`
- API calls are handled in `src/services/api.ts`
- Type definitions are in `src/types/`

## Production Deployment

### Backend

- Set environment variables for production
- Use a production ASGI server like Gunicorn with Uvicorn workers
- Configure proper CORS settings
- Ensure at least one AI service API key is securely set
- Implement authentication if needed

### Frontend

- Run `npm run build` to create production build
- Deploy to platforms like Vercel, Netlify, or similar
- Configure environment variables for production API endpoint

## Costs and Usage

**Important**: This application uses AI APIs which are paid services. Please be aware of:

- **API usage costs** vary by provider (OpenAI, Google, Anthropic)
- **Rate limits** imposed by each AI service
- **Monitor usage** in respective dashboards
- **Consider implementing additional rate limiting** for production use

### Cost Comparison (Approximate)

- **OpenAI GPT-4**: ~$0.03-0.06 per 1K tokens
- **Google Gemini Pro**: ~$0.0005 per 1K tokens
- **Anthropic Claude**: ~$0.008-0.024 per 1K tokens

## Troubleshooting

### AI Service Issues

- **Service switching fails**: Check if API key is configured for target service
- **All services fail**: Verify API keys are correct and accounts have sufficient credits
- **Rate limit errors**: Check usage limits in provider dashboards
- **Check logs** for detailed error messages

### Development Issues

- Ensure both backend and frontend are running
- Check that environment variables are properly set
- Verify network connectivity between frontend and backend
- Use `/chat/services` endpoint to check available services

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
