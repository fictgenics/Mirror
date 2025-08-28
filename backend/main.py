from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from dotenv import load_dotenv
import os

from api.routes import trending_router
from core.config import settings

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Mirror - Trending Topics Analyzer",
    description="Analyze trending topics across GitHub, X (Twitter), and Reddit",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trending_router, prefix="/api/v1")

# Mount static files (only if frontend is built)
try:
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
except RuntimeError:
    print("Warning: Frontend static files not found. Run 'npm run build' in frontend directory to serve the web interface.")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main application"""
    try:
        with open("frontend/build/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mirror - Trending Topics Analyzer</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                .container { text-align: center; }
                .api-info { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }
                .endpoint { background: #e3f2fd; padding: 10px; margin: 10px 0; border-radius: 4px; }
                code { background: #f1f1f1; padding: 2px 6px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 Mirror - Trending Topics Analyzer</h1>
                <p>Backend API is running successfully! 🚀</p>
                
                <div class="api-info">
                    <h2>📡 API Endpoints</h2>
                    <div class="endpoint">
                        <strong>Health Check:</strong> <code>GET /health</code>
                    </div>
                    <div class="endpoint">
                        <strong>Platforms:</strong> <code>GET /api/v1/trending/platforms</code>
                    </div>
                    <div class="endpoint">
                        <strong>Example Queries:</strong> <code>GET /api/v1/trending/example-queries</code>
                    </div>
                    <div class="endpoint">
                        <strong>Analyze Trends:</strong> <code>POST /api/v1/trending/analyze</code>
                    </div>
                    <div class="endpoint">
                        <strong>Quick Analysis:</strong> <code>POST /api/v1/trending/quick-analysis</code>
                    </div>
                </div>
                
                <div class="api-info">
                    <h2>🔧 Next Steps</h2>
                    <p>To use the web interface:</p>
                    <ol style="text-align: left; display: inline-block;">
                        <li>Open another terminal</li>
                        <li>Navigate to the frontend directory: <code>cd frontend</code></li>
                        <li>Install dependencies: <code>npm install</code></li>
                        <li>Start development server: <code>npm start</code></li>
                    </ol>
                </div>
                
                <div class="api-info">
                    <h2>📚 API Documentation</h2>
                    <p><a href="/docs" target="_blank">Interactive API Docs (Swagger UI)</a></p>
                    <p><a href="/redoc" target="_blank">ReDoc Documentation</a></p>
                </div>
            </div>
        </body>
        </html>
        """)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Mirror API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
