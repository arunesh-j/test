from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
import platform

app = FastAPI(
    title="Docker Test Server",
    description="A FastAPIs servers for testing Docker deployment",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docker Test Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .status { background: #d4edda; padding: 10px; border-radius: 4px; margin: 20px 0; }
            .info { background: #e2e3e5; padding: 15px; border-radius: 4px; margin: 10px 0; }
            pre { background: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐳 Docker Test Server Running!</h1>
            <div class="status">
                <strong>✅ Server Status:</strong> Running successfully on port 8000
            </div>
            <div class="info">
                <h3>Server Information:</h3>
                <p><strong>Framework:</strong> FastAPI with Uvicorn</p>
                <p><strong>Python Version:</strong> 3.11</p>
                <p><strong>Workers:</strong> 4</p>
                <p><strong>Host:</strong> 0.0.0.0:8000</p>
            </div>
            <div class="info">
                <h3>Available Endpoints:</h3>
                <ul>
                    <li><a href="/">/</a> - This welcome page</li>
                    <li><a href="/healthz">/healthz</a> - Health check endpoint</li>
                    <li><a href="/info">/info</a> - System information</li>
                    <li><a href="/docs">/docs</a> - API documentation (Swagger UI)</li>
                    <li><a href="/redoc">/redoc</a> - Alternative API documentation</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Server is running"}

@app.get("/info")
async def server_info():
    """Get server and system information"""
    return {
        "message": "Docker Test Server",
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "architecture": platform.machine(),
        "user": os.getenv("USER", "unknown"),
        "working_directory": os.getcwd(),
        "environment_variables": {
            "DD_TRACE_SAMPLING_RULES": os.getenv("DD_TRACE_SAMPLING_RULES"),
            "DD_PATCH_MODULES": os.getenv("DD_PATCH_MODULES"),
            "PATH": os.getenv("PATH", "")[:100] + "..." if len(os.getenv("PATH", "")) > 100 else os.getenv("PATH", "")
        }
    }

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {
        "message": "Hello from Docker!",
        "status": "success",
        "container": "running",
        "framework": "FastAPI"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)