from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all CORS (for development/testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Calendly MCP Server is running"}

@app.get("/.well-known/ai-plugin.json")
async def serve_ai_plugin():
    return {
        "schema_version": "v1",
        "name_for_human": "Calendly MCP Server",
        "name_for_model": "calendly",
        "description_for_human": "Schedule and manage events with Calendly.",
        "description_for_model": "Use this tool to create, update, and cancel Calendly meetings, event types, and users.",
        "auth": {
            "type": "bearer"
        },
        "api": {
            "type": "openapi",
            "url": "https://calendly-mcp-server-production.up.railway.app/.well-known/openapi.json",
            "is_user_authenticated": True
        },
        "logo_url": "https://avatars.githubusercontent.com/u/2226605?s=48",
        "contact_email": "you@example.com",
        "legal_info_url": "https://yourdomain.com/legal"
    }

@app.get("/.well-known/openapi.json")
async def serve_openapi():
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Calendly MCP API",
            "version": "1.0.0"
        },
        "paths": {
            "/event_types": {
                "get": {
                    "summary": "List Event Types",
                    "responses": {
                        "200": {
                            "description": "A list of event types"
                        }
                    }
                }
            }
        }
    }

@app.get("/.well-known/oauth-authorization-server")
async def oauth_server_info():
    return {
        "issuer": "https://calendly-mcp-server-production.up.railway.app",
        "authorization_endpoint": "https://auth.calendly.com/oauth/authorize",
        "token_endpoint": "https://auth.calendly.com/oauth/token",
        "scopes_supported": ["read", "write"],
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "token_endpoint_auth_methods_supported": ["client_secret_basic"]
    }

@app.post("/register")
async def register_user():
    return {"status": "registered"}

@app.get("/sse")
async def sse_not_supported():
    raise HTTPException(status_code=404, detail="SSE not supported")

@app.options("/{rest_of_path:path}")
async def handle_preflight(rest_of_path: str, request: Request):
    return JSONResponse(status_code=200, content={"message": "CORS preflight OK"})

@app.post("/")
async def catch_post_root():
    raise HTTPException(status_code=404, detail="Root POST not implemented")
