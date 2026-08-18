# import os
# import json
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from app.services.orchestrator import orchestrator

# router = APIRouter(prefix="/api/v1/chat", tags=["AI Conversational Core Engine Channel"])

# class QueryRequestSchema(BaseModel):
#     user_query: str
#     chat_history: list = []

# @router.post("/query")
# async def process_portfolio_query(payload: QueryRequestSchema):
#     # 1. Execute query against the live LLaMA 3.3 70B framework
#     orchestrator_result = await orchestrator.execute_query(
#         user_query=payload.user_query,
#         history=payload.chat_history
#     )

#     if orchestrator_result["status"] == "error":
#         raise HTTPException(status_code=500, detail=orchestrator_result["message"])

#     raw_text = orchestrator_result.get("text_content", "")
#     tool_calls = orchestrator_result.get("tool_executions", [])
    
#     ui_directives = []
#     data_store_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data-store")

#     # Lowercase clean the user query for fuzzy substring matches downstream
#     clean_query = payload.user_query.lower()

#     # 2. TRIGGER INTERCEPT MATRIX
#     if tool_calls:
#         for tool in tool_calls:
#             func_name = tool["function_name"]
#             arguments = tool["arguments"]

#             # ==== GENERIC CASE 1: Project Retrieval Engine Layer ====
#             if func_name == "search_projects":
#                 model_keywords = arguments.get("keywords", [])
                
#                 # Filter out useless conversational padding tokens
#                 clean_keywords = [
#                     k.lower() for k in model_keywords 
#                     if k.lower() not in ["project", "projects", "work", "portfolio", "all", "show", "me"]
#                 ]
                
#                 try:
#                     with open(os.path.join(data_store_path, "projects.json"), "r", encoding="utf-8") as f:
#                         db_projects = json.load(f).get("projects", [])
                    
#                     matched_ids = []
#                     for proj in db_projects:
#                         # Extract all searchable tokens for this specific project item
#                         proj_id = proj["id"].lower()
#                         proj_name = proj["name"].lower()
#                         keywords_pool = [k.lower() for k in proj.get("routing_keywords", [])]
                        
#                         # --- THE FUZZY ENGINE LOGIC ---
#                         # Target checks match if:
#                         # a) Recruiter query explicitly mentions project id/name strings tokens
#                         # b) Model extracted pure explicit technologies matching keywords_pool
#                         # c) Clean keywords array became empty (meaning general/all search intent query)
#                         is_match = (
#                             proj_id in clean_query or 
#                             proj_name in clean_query or
#                             not clean_keywords or
#                             any(kw in keywords_pool for kw in clean_keywords) or
#                             any(kw in clean_query for kw in keywords_pool)
#                         )
                        
#                         if is_match:
#                             matched_ids.append(proj["id"])
                    
#                     if matched_ids:
#                         ui_directives.append({
#                             "action_type": "SHOW_PROJECTS",
#                             "payload": {
#                                 "project_ids": list(set(matched_ids)),  # Enforce uniqueness tags
#                                 "technologies": clean_keywords
#                             }
#                         })
#                 except Exception as e:
#                     raw_text += f"\n[Backend Notice: Project generic lookup pipeline error: {str(e)}]"

#             # ==== GENERIC CASE 2: Experience / Employment Timeline Layer ====
#             elif func_name == "get_professional_experience":
#                 target_company = arguments.get("company_id", None)
                
#                 try:
#                     with open(os.path.join(data_store_path, "experience.json"), "r", encoding="utf-8") as f:
#                         db_exp = json.load(f).get("professional_experience", [])
                    
#                     matched_ids = []
#                     for exp in db_exp:
#                         exp_id = exp["id"].lower()
#                         org_name = exp.get("organization", "").lower()
                        
#                         # Fuzzy structural verification logic checks
#                         is_exp_match = (
#                             target_company is None or 
#                             str(target_company).lower() in ["all", "none", "null", "work", "history"] or
#                             exp_id in clean_query or 
#                             org_name in clean_query or 
#                             str(target_company).lower() in exp_id
#                         )
                        
#                         if is_exp_match:
#                             matched_ids.append(exp["id"])
                    
#                     if matched_ids:
#                         ui_directives.append({
#                             "action_type": "SHOW_EXPERIENCE",
#                             "payload": {
#                                 "experience_ids": list(set(matched_ids))
#                             }
#                         })
#                 except Exception as e:
#                     raw_text += f"\n[Backend Notice: Experience generic lookup pipeline error: {str(e)}]"

#     # ==== FALLBACK STEP: Conversational Integrity Protection ====
#     # If LLaMA 3.3 didn't fire a specific structural tool call but the user query text 
#     # directly infers clear intent markers, we inject the action commands programmatically!
#     if not ui_directives:
#         if any(w in clean_query for w in ["project", "projects", "work", "portfolio", "built", "repo", "github"]):
#             try:
#                 with open(os.path.join(data_store_path, "projects.json"), "r", encoding="utf-8") as f:
#                     all_ids = [p["id"] for p in json.load(f).get("projects", [])]
#                 ui_directives.append({
#                     "action_type": "SHOW_PROJECTS",
#                     "payload": { "project_ids": all_ids, "technologies": [] }
#                 })
#             except:
#                 pass
#         elif any(w in clean_query for w in ["experience", "jobs", "company", "work history", "tamar", "niit"]):
#             try:
#                 with open(os.path.join(data_store_path, "experience.json"), "r", encoding="utf-8") as f:
#                     all_exp_ids = [e["id"] for e in json.load(f).get("professional_experience", [])]
#                 ui_directives.append({
#                     "action_type": "SHOW_EXPERIENCE",
#                     "payload": { "experience_ids": all_exp_ids }
#                 })
#             except:
#                 pass

#     # 3. Compile ultimate clean secure response output envelope
#     return {
#         "status": "success",
#         "meta": {
#             "engine": "llama-3.3-70b-versatile via Groq Resilient Fuzzy Core",
#             "tools_triggered": len(tool_calls) > 0 or len(ui_directives) > 0
#         },
#         "response": {
#             "text_content": raw_text,
#             "ui_directives": ui_directives
#         }
#     }







# import os
# import json
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from app.services.orchestrator import orchestrator

# router = APIRouter(prefix="/api/v1/chat", tags=["AI Conversational Core Engine Channel"])

# class QueryRequestSchema(BaseModel):
#     user_query: str
#     chat_history: list = []

# @router.post("/query")
# async def process_portfolio_query(payload: QueryRequestSchema):
#     orchestrator_result = await orchestrator.execute_query(
#         user_query=payload.user_query,
#         history=payload.chat_history
#     )

#     if orchestrator_result["status"] == "error":
#         raise HTTPException(status_code=500, detail=orchestrator_result["message"])

#     raw_text = orchestrator_result.get("text_content", "")
#     tool_calls = orchestrator_result.get("tool_executions", [])
    
#     ui_directives = []
#     data_store_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data-store")
#     clean_query = payload.user_query.lower()

#     # Pre-load all database stores instantly for rich payload text generation
#     try:
#         with open(os.path.join(data_store_path, "profile.json"), "r", encoding="utf-8") as f:
#             profile_db = json.load(f).get("profile", {})
#         with open(os.path.join(data_store_path, "experience.json"), "r", encoding="utf-8") as f:
#             exp_file = json.load(f)
#             exp_db = exp_file.get("professional_experience", [])
#             edu_db = exp_file.get("education_history", [])
#             cert_db = exp_file.get("certifications", [])
#         with open(os.path.join(data_store_path, "skills.json"), "r", encoding="utf-8") as f:
#             skills_db = json.load(f).get("skills_catalog", {})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database load mapping failure: {str(e)}")

#     # ---- IDENTITY SECURITY GUARDRAIL ----
#     # If the recruiter asks about your name, identity, or basic credentials, bypass standard LLM defaults
#     if any(w in clean_query for w in ["your name", "who are you", "who is this", "introduce yourself"]):
#         if not any(w in clean_query for w in ["about yourself", "profile"]):
#             return {
#                 "status": "success",
#                 "meta": {"engine": "Hardcoded Identity Guardrail", "tools_triggered": False},
#                 "response": {
#                     "text_content": f"I am Aryan Mishra, an AI Engineer specializing in Computer Vision, Intelligent Document Processing (IDP), and Localized LLM architectures. I am currently driving production pipelines at Tamar Software.",
#                     "ui_directives": []
#                 }
#             }

#     # 2. TRIGGER INTERCEPT MATRIX (Tool Calling Intercepts)
#     if tool_calls:
#         for tool in tool_calls:
#             func_name = tool["function_name"]
#             arguments = tool["arguments"]

#             # ---- MASTER CASE 1: FULL INTERVIEW PROFILE FLOW ----
#             if func_name == "get_professional_experience" and any(w in clean_query for w in ["yourself", "profile", "background", "history"]):
#                 ui_directives.append({
#                     "action_type": "SHOW_FULL_PROFILE",
#                     "payload": {
#                         "name": profile_db.get("name", "Aryan Mishra"),
#                         "role": profile_db.get("role", "AI Engineer"),
#                         "summary": profile_db.get("summary", ""),
#                         "education": edu_db,
#                         "current_experience": [e for e in exp_db if e["id"] == "tamar-software"],
#                         "skills": skills_db
#                     }
#                 })
#                 raw_text = (
#                     f"Hello! My name is Aryan Mishra, and I am an AI Engineer specializing in Computer Vision and Generative AI frameworks. "
#                     f"I completed my Bachelor of Computer Application (BCA) from Shri Ramswaroop Memorial University (2022-2025) with a CGPA of 8.12. "
#                     f"Currently, I am working at Tamar Software as an AI Engineer, where I architect open-source OCR engines and intelligent chatbot architectures. "
#                     f"I have compiled my complete professional matrix including academic history, active roles, and expert toolsets inside the console panel below for your evaluation."
#                 )

#             # ---- SUBSIDIARY CASE 2: Project Retrieval Engine ----
#             elif func_name == "search_projects":
#                 model_keywords = arguments.get("keywords", []) or []
#                 clean_keywords = [k.lower() for k in model_keywords if k.lower() not in ["project", "projects", "work", "portfolio", "all"]]
#                 try:
#                     with open(os.path.join(data_store_path, "projects.json"), "r", encoding="utf-8") as f:
#                         db_projects = json.load(f).get("projects", [])
#                     matched_ids = []
#                     for proj in db_projects:
#                         if not clean_keywords or any(kw in [tk.lower() for tk in proj.get("routing_keywords", [])] for kw in clean_keywords):
#                             matched_ids.append(proj["id"])
#                     if matched_ids:
#                         ui_directives.append({
#                             "action_type": "SHOW_PROJECTS",
#                             "payload": { "project_ids": list(set(matched_ids)), "technologies": clean_keywords }
#                         })
#                         if not raw_text.strip():
#                             raw_text = "I have extracted the core AI and Computer Vision project modules from my engineering repositories. You can review the layouts directly inside the terminal interface."
#                 except Exception as e: raw_text += f"\n[Project lookup error: {str(e)}]"

#             # ---- SUBSIDIARY CASE 3: Isolated Company Timeline ----
#             elif func_name == "get_professional_experience":
#                 target_company = arguments.get("company_id", None)
#                 matched_ids = []
#                 for exp in exp_db:
#                     if target_company is None or str(target_company).lower() in exp["id"].lower():
#                         matched_ids.append(exp["id"])
#                 if matched_ids:
#                     ui_directives.append({
#                         "action_type": "SHOW_EXPERIENCE",
#                         "payload": { "experience_ids": list(set(matched_ids)) }
#                     })
#                     if not raw_text.strip():
#                         raw_text = "Extracting the specific enterprise timeline milestones records from my experience logs store:"

#             # ---- SUBSIDIARY CASE 4: Isolated Education Records ----
#             elif func_name in ["get_education_and_certifications", "get_education"]:
#                 ui_directives.append({
#                     "action_type": "SHOW_EDUCATION",
#                     "payload": { "education": edu_db, "certifications": cert_db }
#                 })
#                 if not raw_text.strip():
#                     raw_text = "Here are the verified records of my academic history, university degree performance index, and specialized machine learning credentials."

#     # 3. FALLBACK FUZZY PATTERN INTERCEPTOR (If LLaMA bypasses tool choice parameters)
#     if not ui_directives:
#         if any(w in clean_query for w in ["yourself", "profile", "background", "history"]):
#             ui_directives.append({
#                 "action_type": "SHOW_FULL_PROFILE",
#                 "payload": {
#                     "name": profile_db.get("name", "Aryan Mishra"),
#                     "role": profile_db.get("role", "AI Engineer"),
#                     "summary": profile_db.get("summary", ""),
#                     "education": edu_db,
#                     "current_experience": [e for e in exp_db if e["id"] == "tamar-software"],
#                     "skills": skills_db
#                 }
#             })
#             raw_text = (
#                 f"Hello! I am Aryan Mishra, an AI Engineer. I completed my BCA from Shri Ramswaroop Memorial University with an 8.12 CGPA. "
#                 f"Currently, I am working at Tamar Software building enterprise-grade OCR and conversational chatbot systems. "
#                 f"I have initialized my complete interview-profile directive inside the dashboard interface below."
#             )
#         elif any(w in clean_query for w in ["project", "projects", "work", "portfolio"]):
#             try:
#                 with open(os.path.join(data_store_path, "projects.json"), "r", encoding="utf-8") as f:
#                     all_ids = [p["id"] for p in json.load(f).get("projects", [])]
#                 ui_directives.append({ "action_type": "SHOW_PROJECTS", "payload": { "project_ids": all_ids, "technologies": [] } })
#                 raw_text = "Displaying all matched software and architecture project pipelines repository nodes."
#             except: pass
#         elif any(w in clean_query for w in ["experience", "jobs", "company", "work history"]):
#             ui_directives.append({ "action_type": "SHOW_EXPERIENCE", "payload": { "experience_ids": [e["id"] for e in exp_db] } })
#             raw_text = "Loading the complete structural work optimization history matrix from the data layers."
#         elif any(w in clean_query for w in ["education", "degree", "university", "bca", "certifications"]):
#             ui_directives.append({ "action_type": "SHOW_EDUCATION", "payload": { "education": edu_db, "certifications": cert_db } })
#             raw_text = "Loading academic credentials timeline tracks parameters."

#     if not raw_text.strip():
#         raw_text = f"I am Aryan Mishra. Let's discuss metrics regarding my deep computer vision OCR work, custom LangChain architectures, or enterprise roles."

#     return {
#         "status": "success",
#         "meta": {
#             "engine": "llama-3.3-70b-versatile via Full Interview Persona Engine",
#             "tools_triggered": len(ui_directives) > 0
#         },
#         "response": {
#             "text_content": raw_text,
#             "ui_directives": ui_directives}

#         }



# import os
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from app.services.orchestrator import orchestrator
# from app.services.data_service import data_store_service

# router = APIRouter(prefix="/api/v1/chat", tags=["AI Conversational Core Engine Channel"])

# class QueryRequestSchema(BaseModel):
#     user_query: str
#     chat_history: list = []

# @router.post("/query")
# async def process_portfolio_query(payload: QueryRequestSchema):
#     orchestrator_result = await orchestrator.execute_query(
#         user_query=payload.user_query,
#         history=payload.chat_history
#     )

#     if orchestrator_result["status"] == "error":
#         raise HTTPException(status_code=500, detail=orchestrator_result["message"])

#     raw_text = orchestrator_result.get("text_content", "")
#     tool_calls = orchestrator_result.get("tool_executions", [])
    
#     ui_directives = []
#     clean_query = payload.user_query.lower()

#     try:
#         exp_file = data_store_service.get_experience_records()
#         exp_db = exp_file.get("professional_experience", []) or []
#         edu_db = exp_file.get("education_history", []) or []
#         cert_db = exp_file.get("certifications", []) or []
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Data store connection fault: {str(e)}")

#     # 1. TRIGGER ACTION INJECTION INTERCEPTS OVER SECURE BOUNDARY
#     if any(w in clean_query for w in ["education", "degree", "university", "bca", "academic", "college", "graduation", "studies"]):
#         ui_directives.append({
#             "action_type": "SHOW_EDUCATION",
#             "payload": { "education": edu_db, "certifications": cert_db }
#         })

#     if tool_calls:
#         for tool in tool_calls:
#             if not isinstance(tool, dict):
#                 continue
#             func_name = tool.get("function_name")
#             arguments = tool.get("arguments", {}) or {}

#             if func_name == "search_projects":
#                 ui_directives.append({
#                     "action_type": "SHOW_PROJECTS",
#                     "payload": { "projects_data": data_store_service.get_projects() }
#                 })

#             elif func_name == "get_professional_experience":
#                 target_company = arguments.get("company_id", None) if isinstance(arguments, dict) else None
#                 matched_exp = []
#                 for exp in exp_db:
#                     exp_id = exp.get("id", "").lower()
#                     if target_company is None or str(target_company).lower() in ["all", "none", "work"] or str(target_company).lower() in exp_id:
#                         matched_exp.append(exp)
                
#                 if not matched_exp or any(w in clean_query for w in ["yourself", "profile"]):
#                     matched_exp = exp_db

#                 ui_directives.append({
#                     "action_type": "SHOW_EXPERIENCE",
#                     "payload": { "experience_data": matched_exp }
#                 })

#             elif func_name == "get_technical_skills":
#                 raw_skills = data_store_service.get_skills_catalog()
#                 lang_list = raw_skills.get("programming_and_databases", {}).get("tools", []) if isinstance(raw_skills.get("programming_and_databases"), dict) else []
#                 ai_list = raw_skills.get("ai_and_machine_learning", {}).get("tools", []) if isinstance(raw_skills.get("ai_and_machine_learning"), dict) else []
#                 back_list = raw_skills.get("backend_and_automation", {}).get("tools", []) if isinstance(raw_skills.get("backend_and_automation"), dict) else []

#                 formatted_categories = [
#                     {"name": "Programming Languages & DBs", "skills": lang_list},
#                     {"name": "Computer Vision & AI/ML Core", "skills": ai_list},
#                     {"name": "Backend & Cloud Frameworks", "skills": back_list}
#                 ]
#                 ui_directives.append({
#                     "action_type": "SHOW_SKILLS",
#                     "payload": { "categories": formatted_categories }
#                 })

#     # ---- 2. FUZZY STICKERS PROTECTION LAYER (Fallbacks matching rules) ----
#     if not ui_directives:
#         if any(w in clean_query for w in ["project", "projects", "work", "portfolio", "built", "repo", "github"]):
#             ui_directives.append({ "action_type": "SHOW_PROJECTS", "payload": { "projects_data": data_store_service.get_projects() } })
#         elif any(w in clean_query for w in ["experience", "jobs", "company", "work history", "yourself", "about"]):
#             ui_directives.append({ "action_type": "SHOW_EXPERIENCE", "payload": { "experience_data": exp_db } })
#         elif any(w in clean_query for w in ["skills", "tech stack", "languages", "technologies", "tools"]):
#             raw_s = data_store_service.get_skills_catalog()
#             lang_list = raw_s.get("programming_and_databases", {}).get("tools", []) if isinstance(raw_s.get("programming_and_databases"), dict) else []
#             ai_list = raw_s.get("ai_and_machine_learning", {}).get("tools", []) if isinstance(raw_s.get("ai_and_machine_learning"), dict) else []
#             back_list = raw_s.get("backend_and_automation", {}).get("tools", []) if isinstance(raw_s.get("backend_and_automation"), dict) else []
#             formatted_cat = [
#                 {"name": "Programming Languages & DBs", "skills": lang_list},
#                 {"name": "Computer Vision & AI/ML Core", "skills": ai_list},
#                 {"name": "Backend & Cloud Frameworks", "skills": back_list}
#             ]
#             ui_directives.append({ "action_type": "SHOW_SKILLS", "payload": { "categories": formatted_cat } })

#     if not raw_text.strip():
#         raw_text = "I have successfully fetched my profile metrics response data parameters index."

#     return {
#         "status": "success",
#         "meta": {"engine": "llama-3.3-70b-versatile Secure Isolation Pipeline", "tools_triggered": len(ui_directives) > 0},
#         "response": { "text_content": raw_text, "ui_directives": ui_directives }
#     }





# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel

# from app.services.orchestrator import orchestrator
# from app.services.data_service import data_store_service


# router = APIRouter(
#     prefix="/api/v1/chat",
#     tags=["AI Conversational Core Engine Channel"]
# )


# class QueryRequestSchema(BaseModel):
#     user_query: str
#     chat_history: list = []


# @router.post("/query")
# async def process_portfolio_query(
#     payload: QueryRequestSchema
# ):

#     # =========================================================
#     # STEP 1: Ask orchestrator for answer + deterministic intent
#     # =========================================================

#     orchestrator_result = await orchestrator.execute_query(
#         user_query=payload.user_query,
#         history=payload.chat_history
#     )

#     if orchestrator_result.get("status") == "error":

#         raise HTTPException(
#             status_code=500,
#             detail=orchestrator_result.get(
#                 "message",
#                 "Portfolio orchestration failed."
#             )
#         )

#     raw_text = orchestrator_result.get(
#         "text_content",
#         ""
#     )

#     intent = orchestrator_result.get(
#         "intent",
#         "profile"
#     )

#     # =========================================================
#     # STEP 2: Build frontend UI directives
#     # =========================================================

#     ui_directives = []

#     try:

#         # -----------------------------------------------------
#         # EDUCATION
#         # -----------------------------------------------------

#         if intent == "education":

#             experience_data = (
#                 data_store_service
#                 .get_experience_records()
#             )

#             ui_directives.append({
#                 "action_type": "SHOW_EDUCATION",
#                 "payload": {
#                     "education": experience_data.get(
#                         "education_history",
#                         []
#                     ),
#                     "certifications": experience_data.get(
#                         "certifications",
#                         []
#                     )
#                 }
#             })

#         # -----------------------------------------------------
#         # EXPERIENCE
#         # -----------------------------------------------------

#         elif intent == "experience":

#             experience_data = (
#                 data_store_service
#                 .get_experience_records()
#             )

#             ui_directives.append({
#                 "action_type": "SHOW_EXPERIENCE",
#                 "payload": {
#                     "experience_data": experience_data.get(
#                         "professional_experience",
#                         []
#                     )
#                 }
#             })

#         # -----------------------------------------------------
#         # PROJECTS
#         # -----------------------------------------------------

#         elif intent == "projects":

#             ui_directives.append({
#                 "action_type": "SHOW_PROJECTS",
#                 "payload": {
#                     "projects_data":
#                         data_store_service.get_projects()
#                 }
#             })

#         # -----------------------------------------------------
#         # SKILLS
#         # -----------------------------------------------------

#         elif intent == "skills":

#             raw_skills = (
#                 data_store_service
#                 .get_skills_catalog()
#             )

#             lang_list = (
#                 raw_skills
#                 .get("programming_and_databases", {})
#                 .get("tools", [])
#                 if isinstance(
#                     raw_skills.get(
#                         "programming_and_databases"
#                     ),
#                     dict
#                 )
#                 else []
#             )

#             ai_list = (
#                 raw_skills
#                 .get("ai_and_machine_learning", {})
#                 .get("tools", [])
#                 if isinstance(
#                     raw_skills.get(
#                         "ai_and_machine_learning"
#                     ),
#                     dict
#                 )
#                 else []
#             )

#             backend_list = (
#                 raw_skills
#                 .get("backend_and_automation", {})
#                 .get("tools", [])
#                 if isinstance(
#                     raw_skills.get(
#                         "backend_and_automation"
#                     ),
#                     dict
#                 )
#                 else []
#             )

#             ui_directives.append({
#                 "action_type": "SHOW_SKILLS",
#                 "payload": {
#                     "categories": [
#                         {
#                             "name": "Programming Languages & DBs",
#                             "skills": lang_list
#                         },
#                         {
#                             "name": "Computer Vision & AI/ML Core",
#                             "skills": ai_list
#                         },
#                         {
#                             "name": "Backend & Cloud Frameworks",
#                             "skills": backend_list
#                         }
#                     ]
#                 }
#             })

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=f"UI data preparation failed: {str(e)}"
#         )

#     # =========================================================
#     # STEP 3: Safety fallback
#     # =========================================================

#     if not raw_text.strip():

#         raw_text = (
#             "I can share more details about my "
#             "professional background, projects, "
#             "education, or technical skills."
#         )

#     # =========================================================
#     # STEP 4: Final API response
#     # =========================================================

#     return {
#         "status": "success",

#         "meta": {
#             "engine": "llama-3.3-70b-versatile",
#             "intent": intent,
#             "tools_triggered": False
#         },

#         "response": {
#             "text_content": raw_text,
#             "ui_directives": ui_directives
#         }
#     }


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
