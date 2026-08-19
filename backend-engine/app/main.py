import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.router import router as chat_core_router

app = FastAPI(
    title="AI Portfolio Core Engine",
    description="Asynchronous Hybrid Query Router & AI Orchestrator Pipeline Services",
    version="1.0.0"
)

# ──────────────────────────────────────────────────────────────────
# 🛡️ M08 PRODUCTION CORS GUARD POLICY: WHITELIST ACCESS SEGREGATION
# ──────────────────────────────────────────────────────────────────
# Hardening the origin arrays. Replaces loose open configuration boundaries.
# ──────────────────────────────────────────────────────────────────
# 🛡️ M08 PRODUCTION CORS GUARD POLICY: WHITELIST ACCESS SEGREGATION
# ──────────────────────────────────────────────────────────────────
ALLOWED_PRODUCTION_ORIGINS = [
    "http://localhost:3000",       
    "http://127.0.0.1:3000",
    # 🔥 INJECTED GLOBAL DOMAIN: Allows your live Vercel dashboard browser canvas to safely handshake with the API!
    "https://vercel.app"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_PRODUCTION_ORIGINS,  # Strict origin whitelist lock
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],         # Tight method gate mapping - Blocks DELETE, PUT, GET for exploit protections
    allow_headers=["Content-Type", "Authorization"], # Explicit headers filtering mapping bounds
)

# ──────────────────────────────────────────────────────────────────
# 🛠️ DIAGNOSTIC GATEWAY: FORCE PRINT FULL PYTHON TRACEBACK ON 500
# ──────────────────────────────────────────────────────────────────
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        print("\n" + "="*80)
        print("🚨 CRITICAL BACKEND EXCEPTION ENCOUNTERED:")
        print("="*80)
        # Force print the exact file name and line number that crashed right into the console
        traceback.print_exc()
        print("="*80 + "\n")
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Internal pipeline exception: {str(exc)}",
                "traceback_hint": "Inspect the active Python console to debug the line source block."
            }
        )

app.include_router(chat_core_router)

@app.get("/api/v1/health", tags=["Infrastructure System Diagnostics"])
async def health_check():
    return {
        "status": "healthy",
        "engine": "active",
        "cors_integrity": "secured_origins_whitelist_active",
        "environment": settings.ENVIRONMENT
    }
