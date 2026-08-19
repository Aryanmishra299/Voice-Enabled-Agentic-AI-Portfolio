import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.orchestrator import orchestrator

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["AI Conversational Core Engine Channel"]
)

# ──────────────────────────────────────────────────────────────────
# 🛡️ M07 REQUEST VALIDATION FIREWALL: ENFORCING DATA INPUT CONTRACTS
# ──────────────────────────────────────────────────────────────────
class QueryRequestSchema(BaseModel):
    # Enforces explicit string type constraint bounds on incoming recruiter data text queries
    user_query: str = Field(
        ..., 
        min_length=1, 
        max_length=500, 
        description="The incoming query token from the recruiter client browser window panel."
    )
    # Replaces loose mutable list default definitions with a safe default_factory list array guard
    chat_history: list[dict] = Field(
        default_factory=list, 
        description="The continuous conversational multi-turn logs state storage history tracking buffer."
    )

# ============================================================
# DETERMINISTIC INTENT ROUTER (Preserved 100% Intact)
# ============================================================
def detect_intent(query: str) -> str:
    q = query.lower().strip()
    
    # --------------------------------------------------------
    # EDUCATION
    # --------------------------------------------------------
    education_keywords = [
        "education", "degree", "bca", "university", "college", 
        "graduation", "academic", "studies", "certification", "certifications"
    ]
    if any(keyword in q for keyword in education_keywords):
        return "education"
        
    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------
    experience_keywords = [
        "professional experience", "work experience", "work history", 
        "employment", "career", "job experience", "companies worked", "where have you worked"
    ]
    if any(keyword in q for keyword in experience_keywords):
        return "experience"
        
    # --------------------------------------------------------
    # PROJECTS
    # --------------------------------------------------------
    project_keywords = [
        "project", "projects", "built", "developed", 
        "portfolio projects", "what have you built"
    ]
    if any(keyword in q for keyword in project_keywords):
        return "projects"
        
    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------
    skills_keywords = [
        "skills", "technical skills", "tech stack", "technologies", 
        "technology", "programming languages", "tools", "frameworks"
    ]
    if any(keyword in q for keyword in skills_keywords):
        return "skills"
        
    # --------------------------------------------------------
    # PROFILE / CONTACT / ABOUT
    # --------------------------------------------------------
    profile_keywords = [
        "tell me about yourself", "about yourself", "who are you", 
        "introduce yourself", "your profile", "your background"
    ]
    if any(keyword in q for keyword in profile_keywords):
        return "profile"
        
    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------
    return "general"

# ============================================================
# CHAT ENDPOINT (Hardened with Failure Boundary Recoveries)
# ============================================================
@router.post("/query")
async def process_portfolio_query(payload: QueryRequestSchema):
    intent = detect_intent(payload.user_query)
    
    try:
        # Pipeline dispatches token variables data downstream into the orchestrator securely
        orchestrator_result = await orchestrator.execute_query(
            user_query=payload.user_query,
            intent=intent,
            history=payload.chat_history
        )
    except Exception as api_exception_trace:
        # 🚨 M07 API FAILURE GATEWAY INTERCEPTED: Catches unhandled cloud rate limits or timeouts anomalies
        print(f"\n🚨 [M07 API FAILURE GATEWAY INTERCEPTED]: {str(api_exception_trace)}\n")
        return {
            "status": "success",
            "meta": {
                "engine": "M07 Emergency Failover Bypass Core Recovery Route",
                "intent": intent
            },
            "response": {
                "text_content": "I am tracking your query logs, but my cognitive API inference gateway is currently facing temporary network communication timeouts or heavy traffic load parameters. Please use the interactive workspace dashboard tabs right below to explore my projects, experiences, and technical skills directly!"
            }
        }

    # Internal error status handler node guard layer
    if orchestrator_result.get("status") == "error":
        return {
            "status": "success",
            "meta": {
                "engine": "Orchestrator Internal Validation Recovery Route",
                "intent": intent
            },
            "response": {
                "text_content": "I am fully ready to assist. Let's discuss details regarding my deep computer vision OCR work, custom GenAI pipelines, or previous roles trajectories. You can also explore my real-world credentials inside the dashboard tabs below."
            }
        }

    raw_text = orchestrator_result.get("text_content", "")

    # Clean server-side text post-processing formatting layer sanitization
    sanitized_text = raw_text.replace("***", "").replace("**", "")

    if not sanitized_text.strip():
        sanitized_text = "I have successfully compiled my profile layers matrix data records response parameters index."

    return {
        "status": "success",
        "meta": {
            "engine": "openai/gpt-oss-120b Decoupled Core Engine Pipeline",
            "intent": intent
        },
        "response": {
            "text_content": sanitized_text
        }
    }
