#  JSON schemas declaring function tools to the LLM 

# Unified system tooling definitions catalog array maps for Meta LLaMA 3.3 70B Engine
# Unified systems tooling arrays contract schemas for Meta LLaMA 3.3 70B
PORTFOLIO_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_projects",
            "description": "Triggers automatically when queries mention projects, repositories, codebases, or technical works to list specific records.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Search tags filtering categories from text (e.g. ['python', 'ocr'])."
                    }
                },
                "required": ["keywords"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_professional_experience",
            "description": "Triggers automatically when user queries inspect previous jobs history, workplace nodes, company data, or role timelines at places like Tamar Software or NIIT.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_id": {
                        "type": "string",
                        "description": "The target slug identifier mapping layout records (e.g. 'tamar-software')."
                    }
                },
                "required": ["company_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_technical_skills",
            "description": "Triggers automatically when a recruiter explicitly asks about your technical skills, tech stack, programming languages, databases, machine learning tools, or developer frameworks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter_category": {
                        "type": "string",
                        "description": "Filters standard category groups if requested. Defaults to 'all'.",
                        "enum": ["all", "languages", "ai_ml", "backend"]
                    }
                },
                "required": ["filter_category"]
            }
        }
    }
]
