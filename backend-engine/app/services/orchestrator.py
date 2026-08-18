# import os
# import json
# import traceback
# from groq import Groq
# from app.config import settings
# from app.services.tools.definitions import PORTFOLIO_TOOLS
# from app.services.data_service import data_store_service

# class PortfolioOrchestrator:
#     """
#     The advanced multi-turn cognitive brain of the portfolio. Powered by Meta LLaMA 3.3 70B Versatile.
#     Implements a robust structured message array compilation for OpenAI/Groq specs compatibility.
#     """
#     def __init__(self):
#         self.client = Groq(api_key=settings.GROQ_API_KEY)
#         self.model = "llama-3.3-70b-versatile" 
#         self.base_data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data-store")
#         self.system_context_prompt = self._compile_engineering_system_prompt()

#     def _compile_engineering_system_prompt(self) -> str:
#         try:
#             profile = data_store_service.get_profile()
#             projects = data_store_service.get_projects()
#             skills = data_store_service.get_skills_catalog()
            
#             # Extract experience and academics separately to avoid context blindspots
#             exp_file = data_store_service.get_experience_records()
#             professional_history = exp_file.get("professional_experience", [])
#             academic_history = exp_file.get("education_history", [])
#             certifications_list = exp_file.get("certifications", [])

#             system_instructions = (
#                 "You are the absolute virtual AI Clone tracking the real physical identity of Aryan Mishra, an expert AI Engineer.\n"
#                 "CRITICAL CORE PERSONA RULE: Always respond in the FIRST PERSON ('I', 'ME', 'MY'). Never say 'I am an AI assistant'. You ARE Aryan Mishra.\n\n"
#                 "CRITICAL QUERY-TO-TOOL ROUTING CONTRACT:\n"
#                 "1. EDUCATION / DEGREE / BCA / UNIVERSITY PLACEMENTS:\n"
#                 "   - If the user query contains 'education', 'degree', 'university', 'bca', 'academic', or 'college', you MUST NOT call any tool functions. Respond directly using text from the ACADEMIC HISTORY data block below.\n\n"
#                 "2. CHATBOT PROFILE INTRODUCTIONS:\n"
#                 "   - General profile introductory queries like 'tell me about yourself', 'who are you', or general personal introductions MUST be answered directly using PROFILE text data.\n\n"
#                 "3. ENTERPRISE WORK EXPERIENCE:\n"
#                 "   - Only execute the 'get_professional_experience' tool if the recruiter explicitly targets a corporate role timeline, job history, or employment responsibilities at entities like Tamar Software or NIIT.\n\n"
#                 "4. TECHNICAL PROJECT REPOSITORIES:\n"
#                 "   - Questions inspecting projects, source code examples, or repositories MUST use and execute 'search_projects'.\n\n"
#                 "==========================================================\n"
#                 "========= ARYAN MISHRA KNOWLEDGE CORE LAYER DATA =========\n"
#                 f"PROFILE DETAILED OVERVIEW: {json.dumps(profile)}\n"
#                 f"PROJECTS REPOSITORIES CATALOG: {json.dumps(projects)}\n"
#                 f"TECHNICAL SKILLS CLUSTERS: {json.dumps(skills)}\n"
#                 f"PROFESSIONAL WORK HISTORY: {json.dumps(professional_history)}\n"
#                 f"ACADEMIC HISTORY & UNIVERSITY DEGREE: {json.dumps(academic_history)}\n"
#                 f"PROFESSIONAL CREDENTIAL CERTIFICATIONS: {json.dumps(certifications_list)}\n"
#                 "==========================================================\n"
#             )
#             return system_instructions
#         except Exception as e:
#             return f"System prompt hydration failed: {str(e)}"

#     async def execute_query(self, user_query: str, history: list = None) -> dict:
#         if history is None:
#             history = []

#         messages = [{"role": "system", "content": self.system_context_prompt}]
        
#         # Unpack chat history memory records securely into standard primitive formats
#         for msg in history:
#             try:
#                 if isinstance(msg, dict):
#                     role_str = msg.get("role") or msg.get("sender") or "user"
#                     clean_role = "assistant" if role_str in ["assistant", "avatar", "bot"] else "user"
#                     content_str = msg.get("content") or msg.get("text") or ""
#                     if content_str.strip():
#                         messages.append({"role": clean_role, "content": content_str})
#             except Exception:
#                 continue
            
#         messages.append({"role": "user", "content": user_query})

#         try:
#             # PASS 1: Capturing tool intents parameters from LLaMA
#             completion = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=messages,
#                 tools=PORTFOLIO_TOOLS,  
#                 tool_choice="auto",     
#                 temperature=0.2,        
#                 max_tokens=800
#             )
            
#             response_message = completion.choices[0].message
#             tool_calls = response_message.tool_calls
#             tool_calls_payload = []
            
#             # --- 🛠️ MILESTONE M06 HOOK PASS: BULLETPROOF DUAL-PASS TOOL RECURSION ---
#             if tool_calls:
#                 # Standard explicit list tracking arrays parsing
#                 tool_calls_list = []
#                 for tc in tool_calls:
#                     func_name = tc.function.name
#                     arguments = json.loads(tc.function.arguments) if isinstance(tc.function.arguments, str) else (tc.function.arguments or {})
                    
#                     tool_calls_payload.append({
#                         "id": tc.id,
#                         "function_name": func_name,
#                         "arguments": arguments
#                     })
                    
#                     tool_calls_list.append({
#                         "id": tc.id,
#                         "type": "function",
#                         "function": {
#                             "name": func_name,
#                             "arguments": json.dumps(arguments) if isinstance(arguments, dict) else str(arguments)
#                         }
#                     })
                
#                 # Append initial message object structured contract safely
#                 messages.append({
#                     "role": "assistant",
#                     "content": response_message.content or "",
#                     "tool_calls": tool_calls_list
#                 })
                
#                 # Hydrate database feedback nodes one by one
#                 for tc in tool_calls:
#                     func_name = tc.function.name
#                     tool_content_feedback = ""
#                     if func_name == "get_professional_experience":
#                         exp_file = data_store_service.get_experience_records()
#                         tool_content_feedback = json.dumps(exp_file.get("professional_experience", []))
#                     elif func_name == "search_projects":
#                         tool_content_feedback = json.dumps(data_store_service.get_projects())
#                     elif func_name == "get_technical_skills":
#                         tool_content_feedback = json.dumps(data_store_service.get_skills_catalog())
                        
#                     messages.append({
#                         "role": "tool",
#                         "tool_call_id": tc.id,
#                         "name": func_name,
#                         "content": tool_content_feedback
#                     })
                
#                 # RE-FIRE SECOND CONTEXT PASS: Fetch organic first-person answer text safely
#                 second_completion = self.client.chat.completions.create(
#                     model=self.model,
#                     messages=messages,
#                     temperature=0.2,
#                     max_tokens=500
#                 )
#                 final_text = second_completion.choices.message.content
#             else:
#                 final_text = response_message.content

#             print("\n" + "="*80)
#             print("🧠 MODEL RESPONSE DEBUG - LOOP CONNECTED & TYPE SAFE")
#             print("="*80)
#             print(f"CONTENT: {final_text}")
#             print(f"TOOL CALLS COUNT: {len(tool_calls_payload) if tool_calls_payload else 0}")
#             print("="*80 + "\n")

#             return {
#                 "status": "success",
#                 "text_content": final_text if final_text else "",
#                 "tool_executions": tool_calls_payload
#             }
#         except Exception as e:
#             print("\n" + "=" * 80)
#             print("🚨 ORCHESTRATOR EXCEPTION CRASH STACK")
#             print("=" * 80)
#             traceback.print_exc()
#             print("=" * 80 + "\n")
#             return {
#                 "status": "error",
#                 "message": f"Groq LPU Versatile multi-turn process failure: {str(e)}"
#             }

# orchestrator = PortfolioOrchestrator()




# import os
# import json
# import traceback
# from groq import Groq
# from app.config import settings
# from app.services.tools.definitions import PORTFOLIO_TOOLS
# from app.services.data_service import data_store_service

# class PortfolioOrchestrator:
#     """
#     The advanced contextual cognitive brain of the portfolio. Powered by Meta LLaMA 3.3 70B Versatile.
#     Implements a fail-safe single-turn aggregated transaction mapping window to guarantee 100% 
#     Groq API compliance and eliminate conversational pipeline choke-points.
#     """
#     def __init__(self):
#         self.client = Groq(api_key=settings.GROQ_API_KEY)
#         self.model = "llama-3.3-70b-versatile" 
#         self.base_data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data-store")
#         self.system_context_prompt = self._compile_engineering_system_prompt()

#     def _compile_engineering_system_prompt(self) -> str:
#         try:
#             profile = data_store_service.get_profile()
#             projects = data_store_service.get_projects()
#             skills = data_store_service.get_skills_catalog()
            
#             exp_file = data_store_service.get_experience_records()
#             professional_history = exp_file.get("professional_experience", [])
#             academic_history = exp_file.get("education_history", [])
#             certifications_list = exp_file.get("certifications", [])

#             system_instructions = (
#                 "You are the absolute virtual AI Clone tracking the real physical identity of Aryan Mishra, an expert AI Engineer.\n"
#                 "CRITICAL CORE PERSONA RULE: Always respond in the FIRST PERSON ('I', 'ME', 'MY'). Never say 'I am an AI assistant'. You ARE Aryan Mishra.\n\n"
#                 "CRITICAL QUERY-TO-TOOL ROUTING CONTRACT:\n"
#                 "1. EDUCATION / DEGREE / BCA / UNIVERSITY PLACEMENTS:\n"
#                 "   - If the user query contains 'education', 'degree', 'university', 'bca', 'academic', or 'college', you MUST NOT call any tool functions. Respond directly using text from the ACADEMIC HISTORY data block below.\n\n"
#                 "2. CHATBOT PROFILE INTRODUCTIONS:\n"
#                 "   - General profile introductory queries like 'tell me about yourself', 'who are you', or general personal introductions MUST be answered directly using PROFILE text data.\n\n"
#                 "3. ENTERPRISE WORK EXPERIENCE:\n"
#                 "   - Only execute the 'get_professional_experience' tool if the recruiter explicitly targets a corporate role timeline, job history, or employment responsibilities at entities like Tamar Software or NIIT.\n\n"
#                 "4. TECHNICAL PROJECT REPOSITORIES:\n"
#                 "   - Questions inspecting projects, source code examples, or repositories MUST use and execute 'search_projects'.\n\n"
#                 "==========================================================\n"
#                 "========= ARYAN MISHRA KNOWLEDGE CORE LAYER DATA =========\n"
#                 f"PROFILE DETAILED OVERVIEW: {json.dumps(profile)}\n"
#                 f"PROJECTS REPOSITORIES CATALOG: {json.dumps(projects)}\n"
#                 f"TECHNICAL SKILLS CLUSTERS: {json.dumps(skills)}\n"
#                 f"PROFESSIONAL WORK HISTORY: {json.dumps(professional_history)}\n"
#                 f"ACADEMIC HISTORY & UNIVERSITY DEGREE: {json.dumps(academic_history)}\n"
#                 f"PROFESSIONAL CREDENTIAL CERTIFICATIONS: {json.dumps(certifications_list)}\n"
#                 "==========================================================\n"
#             )
#             return system_instructions
#         except Exception as e:
#             return f"System prompt hydration failed: {str(e)}"

#     async def execute_query(self, user_query: str, history: list = None) -> dict:
#         if history is None:
#             history = []

#         messages = [{"role": "system", "content": self.system_context_prompt}]
        
#         # --- SAFE STATELESS CONTEXT AGGREGATOR ENGINE ---
#         # Extracts the immediate preceding exchange turn text to preserve semantic memory 
#         # while keeping the underlying API message array stateless and perfectly type-safe.
#         context_hint_str = ""
#         if history and len(history) >= 2:
#             try:
#                 # Safely pull the last user query and assistant response text blocks
#                 last_user_turn = history[-2] if isinstance(history[-2], dict) else {}
#                 last_ai_turn = history[-1] if isinstance(history[-1], dict) else {}
                
#                 u_text = last_user_turn.get("content") or last_user_turn.get("text") or ""
#                 ai_text = last_ai_turn.get("content") or last_ai_turn.get("text") or ""
                
#                 if u_text.strip() or ai_text.strip():
#                     context_hint_str = f"[Previous Conversation Context - Recruiter asked: '{u_text}'. You replied: '{ai_text}']\n"
#             except Exception:
#                 pass
            
#         # Compile an aggregated single-turn user prompt tracking memory lines
#         aggregated_user_prompt = f"{context_hint_str}Current Recruiter Query: {user_query}"
#         messages.append({"role": "user", "content": aggregated_user_prompt})

#         try:
#             # PASS 1: Capturing tool intents parameters from LLaMA safely
#             completion = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=messages,
#                 tools=PORTFOLIO_TOOLS,  
#                 tool_choice="auto",     
#                 temperature=0.2,        
#                 max_tokens=800
#             )
            
#             response_message = completion.choices[0].message
#             tool_calls = response_message.tool_calls
#             tool_calls_payload = []
            
#             # --- DUAL-PASS TOOL RECURSION INTEGRATION ---
#             if tool_calls:
#                 serialized_tool_calls = []
#                 for tc in tool_calls:
#                     args_dict = json.loads(tc.function.arguments) if isinstance(tc.function.arguments, str) else (tc.function.arguments or {})
                    
#                     tool_calls_payload.append({
#                         "id": tc.id,
#                         "function_name": tc.function.name,
#                         "arguments": args_dict
#                     })
                    
#                     serialized_tool_calls.append({
#                         "id": tc.id,
#                         "type": "function",
#                         "function": {
#                             "name": tc.function.name,
#                             "arguments": json.dumps(args_dict)
#                         }
#                     })

#                 messages.append({
#                     "role": "assistant",
#                     "content": "",
#                     "tool_calls": serialized_tool_calls
#                 })
                
#                 for tc in tool_calls:
#                     func_name = tc.function.name
#                     tool_content_feedback = ""
#                     if func_name == "get_professional_experience":
#                         exp_file = data_store_service.get_experience_records()
#                         tool_content_feedback = json.dumps(exp_file.get("professional_experience", []))
#                     elif func_name == "search_projects":
#                         tool_content_feedback = json.dumps(data_store_service.get_projects())
#                     elif func_name == "get_technical_skills":
#                         tool_content_feedback = json.dumps(data_store_service.get_skills_catalog())
                        
#                     messages.append({
#                         "role": "tool",
#                         "tool_call_id": tc.id,
#                         "name": func_name,
#                         "content": tool_content_feedback
#                     })
                
#                 second_completion = self.client.chat.completions.create(
#                     model=self.model,
#                     messages=messages,
#                     temperature=0.2,
#                     max_tokens=500
#                 )
#                 final_text = second_completion.choices[0].message.content
#             else:
#                 final_text = response_message.content

#             print("\n" + "="*80)
#             print("🧠 MODEL RESPONSE DEBUG - CONVERSATION SESSION LOOP ACTIVE & IMMUNE")
#             print("="*80)
#             print(f"CONTENT: {final_text}")
#             print(f"TOOL CALLS COUNT: {len(tool_calls_payload) if tool_calls_payload else 0}")
#             print("="*80 + "\n")

#             return {
#                 "status": "success",
#                 "text_content": final_text if final_text else "",
#                 "tool_executions": tool_calls_payload
#             }
#         except Exception as e:
#             print("\n" + "=" * 80)
#             print("🚨 ORCHESTRATOR EXCEPTION CRASH STACK")
#             print("=" * 80)
#             traceback.print_exc()
#             print("=" * 80 + "\n")
#             return {
#                 "status": "error",
#                 "message": f"Groq LPU Versatile multi-turn process failure: {str(e)}"
#             }

# orchestrator = PortfolioOrchestrator()





# import json
# import traceback
# from groq import Groq

# from app.config import settings
# from app.services.data_service import data_store_service


# class PortfolioOrchestrator:
#     """
#     Deterministic portfolio orchestration layer.

#     Flow:
#         User Query
#             ↓
#         Intent Detection
#             ↓
#         Local JSON Data Selection
#             ↓
#         Context-Hydrated LLaMA Completion
#             ↓
#         Natural First-Person Response

#     No RAG.
#     No vector database.
#     No embeddings.
#     No LLM function/tool calling.
#     """

#     def __init__(self):
#         self.client = Groq(api_key=settings.GROQ_API_KEY)
#         self.model = "llama-3.3-70b-versatile"

#     # =========================================================
#     # INTENT DETECTION
#     # =========================================================

#     def _detect_intent(self, query: str, history: list) -> str:

#         text = query.lower().strip()

#         # -----------------------------------------------------
#         # 1. EDUCATION
#         # -----------------------------------------------------
#         education_keywords = [
#             "education",
#             "educational",
#             "degree",
#             "bca",
#             "bachelor",
#             "university",
#             "college",
#             "academic",
#             "graduation",
#             "graduate",
#             "studies",
#             "cgpa"
#         ]

#         if any(keyword in text for keyword in education_keywords):
#             return "education"

#         # -----------------------------------------------------
#         # 2. PROFESSIONAL EXPERIENCE
#         # -----------------------------------------------------
#         experience_keywords = [
#             "professional experience",
#             "work experience",
#             "work history",
#             "employment",
#             "job history",
#             "career history",
#             "previous job",
#             "previous jobs",
#             "company",
#             "companies",
#             "tamar",
#             "niit",
#             "role",
#             "roles",
#             "responsibilities",
#             "worked",
#             "experience"
#         ]

#         if any(keyword in text for keyword in experience_keywords):
#             return "experience"

#         # -----------------------------------------------------
#         # 3. PROJECTS
#         # -----------------------------------------------------
#         project_keywords = [
#             "project",
#             "projects",
#             "built",
#             "build",
#             "developed",
#             "development",
#             "repository",
#             "repositories",
#             "repo",
#             "github",
#             "portfolio projects",
#             "what have you built"
#         ]

#         if any(keyword in text for keyword in project_keywords):
#             return "projects"

#         # -----------------------------------------------------
#         # 4. TECHNICAL SKILLS
#         # -----------------------------------------------------
#         skill_keywords = [
#             "technical skills",
#             "skills",
#             "skillset",
#             "tech stack",
#             "technology",
#             "technologies",
#             "programming languages",
#             "programming",
#             "frameworks",
#             "databases",
#             "tools",
#             "machine learning skills",
#             "ai skills"
#         ]

#         if any(keyword in text for keyword in skill_keywords):
#             return "skills"

#         # -----------------------------------------------------
#         # 5. GENERAL PROFILE
#         # -----------------------------------------------------
#         profile_keywords = [
#             "tell me about yourself",
#             "about yourself",
#             "who are you",
#             "introduce yourself",
#             "about you",
#             "your profile",
#             "background"
#         ]

#         if any(keyword in text for keyword in profile_keywords):
#             return "profile"

#         # -----------------------------------------------------
#         # 6. FOLLOW-UP QUERY
#         #
#         # Example:
#         # User: Tell me about your experience
#         # AI: ...
#         # User: Yes, kindly provide it.
#         #
#         # The second query has no useful keyword.
#         # Therefore we inspect the previous user message.
#         # -----------------------------------------------------

#         followup_keywords = [
#             "yes",
#             "yes please",
#             "please",
#             "provide it",
#             "tell me more",
#             "more details",
#             "give me more",
#             "elaborate",
#             "go ahead",
#             "sure",
#             "kindly provide",
#             "please provide"
#         ]

#         if any(keyword in text for keyword in followup_keywords):
#             previous_intent = self._detect_previous_intent(history)

#             if previous_intent:
#                 return previous_intent

#         # -----------------------------------------------------
#         # DEFAULT
#         # -----------------------------------------------------
#         return "profile"

#     # =========================================================
#     # PREVIOUS INTENT DETECTION
#     # =========================================================

#     def _detect_previous_intent(self, history: list) -> str | None:

#         if not history:
#             return None

#         # Search backwards for the most recent user message.
#         for message in reversed(history):

#             if not isinstance(message, dict):
#                 continue

#             role = (
#                 message.get("role")
#                 or message.get("sender")
#                 or ""
#             ).lower()

#             if role not in ["user", "recruiter"]:
#                 continue

#             previous_text = (
#                 message.get("content")
#                 or message.get("text")
#                 or ""
#             )

#             if not previous_text.strip():
#                 continue

#             return self._detect_intent(
#                 previous_text,
#                 []
#             )

#         return None

#     # =========================================================
#     # DATA CONTEXT BUILDER
#     # =========================================================

#     def _build_context(self, intent: str) -> dict:

#         if intent == "education":

#             experience_data = data_store_service.get_experience_records()

#             return {
#                 "education_history": experience_data.get(
#                     "education_history",
#                     []
#                 ),
#                 "certifications": experience_data.get(
#                     "certifications",
#                     []
#                 )
#             }

#         if intent == "experience":

#             experience_data = data_store_service.get_experience_records()

#             return {
#                 "professional_experience": experience_data.get(
#                     "professional_experience",
#                     []
#                 )
#             }

#         if intent == "projects":

#             return {
#                 "projects": data_store_service.get_projects()
#             }

#         if intent == "skills":

#             return {
#                 "skills_catalog": data_store_service.get_skills_catalog()
#             }

#         if intent == "profile":

#             return {
#                 "profile": data_store_service.get_profile()
#             }

#         return {}

#     # =========================================================
#     # SYSTEM PROMPT
#     # =========================================================

#     def _build_system_prompt(
#         self,
#         intent: str,
#         context: dict
#     ) -> str:

#         return f"""
# You are Aryan Mishra's AI portfolio representative.

# You must answer as Aryan Mishra in first person.

# PERSONA RULES:
# - Always use "I", "my", and "me".
# - Never say "I am an AI assistant".
# - Never pretend to be a generic chatbot.
# - Never invent facts.
# - Never create companies, projects, degrees, technologies,
#   responsibilities, dates, or achievements that are not present
#   in the supplied portfolio data.

# CURRENT INTENT:
# {intent}

# AUTHORITATIVE PORTFOLIO DATA:
# {json.dumps(context, indent=2, ensure_ascii=False)}

# ANSWERING RULES:

# 1. Use ONLY the authoritative portfolio data above.
# 2. Give a natural recruiter-friendly answer.
# 3. If the recruiter asks about education, discuss the education data.
# 4. If the recruiter asks about professional experience,
#    discuss the professional experience data.
# 5. If the recruiter asks about projects,
#    discuss the projects data.
# 6. If the recruiter asks about technical skills,
#    discuss the skills catalog.
# 7. If the recruiter asks a follow-up question,
#    continue naturally from the current intent.
# 8. Do not mention JSON, databases, routing, context,
#    orchestration, tools, RAG, or internal architecture.
# 9. Do not say that information is unavailable if it exists
#    in the supplied portfolio data.
# 10. Keep the response concise but sufficiently detailed for a recruiter.

# Return ONLY the natural conversational answer.
# """

#     # =========================================================
#     # MAIN EXECUTION
#     # =========================================================

#     async def execute_query(
#         self,
#         user_query: str,
#         history: list = None
#     ) -> dict:

#         if history is None:
#             history = []

#         try:

#             # -------------------------------------------------
#             # STEP 1: Determine what recruiter wants
#             # -------------------------------------------------

#             intent = self._detect_intent(
#                 user_query,
#                 history
#             )

#             # -------------------------------------------------
#             # STEP 2: Load only relevant local data
#             # -------------------------------------------------

#             selected_context = self._build_context(intent)

#             # -------------------------------------------------
#             # DEBUG: Verify data before LLaMA call
#             # -------------------------------------------------

#             print("\n" + "=" * 80)
#             print("🧭 DETERMINISTIC PORTFOLIO ROUTER")
#             print("=" * 80)
#             print(f"USER QUERY : {user_query}")
#             print(f"INTENT     : {intent}")
#             print("CONTEXT LOADED:")
#             print(json.dumps(
#                 selected_context,
#                 indent=2,
#                 ensure_ascii=False
#             ))
#             print("=" * 80 + "\n")

#             # -------------------------------------------------
#             # STEP 3: Build authoritative LLaMA prompt
#             # -------------------------------------------------

#             system_prompt = self._build_system_prompt(
#                 intent,
#                 selected_context
#             )

#             messages = [
#                 {
#                     "role": "system",
#                     "content": system_prompt
#                 }
#             ]

#             # -------------------------------------------------
#             # STEP 4: Add small conversational context
#             #
#             # We don't need to send the entire conversation.
#             # Only recent turns are useful here.
#             # -------------------------------------------------

#             recent_history = []

#             for message in history[-4:]:

#                 if not isinstance(message, dict):
#                     continue

#                 role = (
#                     message.get("role")
#                     or message.get("sender")
#                     or ""
#                 ).lower()

#                 content = (
#                     message.get("content")
#                     or message.get("text")
#                     or ""
#                 )

#                 if role in ["user", "recruiter"]:
#                     clean_role = "user"
#                 elif role in ["assistant", "avatar", "bot"]:
#                     clean_role = "assistant"
#                 else:
#                     continue

#                 if content.strip():
#                     recent_history.append({
#                         "role": clean_role,
#                         "content": content
#                     })

#             messages.extend(recent_history)

#             # -------------------------------------------------
#             # STEP 5: Current recruiter query
#             # -------------------------------------------------

#             messages.append({
#                 "role": "user",
#                 "content": user_query
#             })

#             # -------------------------------------------------
#             # STEP 6: SINGLE LLaMA COMPLETION
#             # -------------------------------------------------

#             completion = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=messages,
#                 temperature=0.2,
#                 max_tokens=600
#             )

#             final_text = (
#                 completion.choices[0].message.content
#                 or ""
#             ).strip()

#             # -------------------------------------------------
#             # STEP 7: Final debug
#             # -------------------------------------------------

#             print("\n" + "=" * 80)
#             print("🧠 LLaMA RESPONSE")
#             print("=" * 80)
#             print(f"INTENT : {intent}")
#             print(f"CONTENT: {final_text}")
#             print("=" * 80 + "\n")

#             return {
#                 "status": "success",
#                 "intent": intent,
#                 "text_content": final_text,
#                 "tool_executions": []
#             }

#         except Exception as e:

#             print("\n" + "=" * 80)
#             print("🚨 ORCHESTRATOR EXCEPTION")
#             print("=" * 80)

#             traceback.print_exc()

#             print("=" * 80 + "\n")

#             return {
#                 "status": "error",
#                 "message": str(e)
#             }


# orchestrator = PortfolioOrchestrator()







import json
import traceback
from groq import Groq

from app.config import settings
from app.services.data_service import data_store_service


class PortfolioOrchestrator:
    """
    Conversational brain of the AI portfolio.

    Architecture:
        Deterministic Router
                ↓
        Relevant JSON Context
                ↓
        LLaMA 3.3 70B
                ↓
        Plain Conversational Response

    No RAG.
    No vector database.
    No tool calling.
    No UI directives.
    """

    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = "openai/gpt-oss-120b"

    # =========================================================
    # CONTEXT LOADING
    # =========================================================

    def _load_context_for_intent(self, intent: str) -> dict:
        """
        Loads only the portfolio data required for the current intent.
        """

        try:

            if intent == "education":
                experience_data = (
                    data_store_service.get_experience_records()
                )

                return {
                    "education_history": experience_data.get(
                        "education_history", []
                    ),
                    "certifications": experience_data.get(
                        "certifications", []
                    )
                }

            elif intent == "experience":

                experience_data = (
                    data_store_service.get_experience_records()
                )

                return {
                    "professional_experience": experience_data.get(
                        "professional_experience", []
                    )
                }

            elif intent == "projects":

                return {
                    "projects": data_store_service.get_projects()
                }

            elif intent == "skills":

                return {
                    "skills_catalog": (
                        data_store_service.get_skills_catalog()
                    )
                }

            elif intent in ["profile", "contact", "about"]:

                return {
                    "profile": data_store_service.get_profile()
                }

            elif intent == "general":

                return {
                    "profile": data_store_service.get_profile(),
                    "projects": data_store_service.get_projects(),
                    "skills_catalog": (
                        data_store_service.get_skills_catalog()
                    ),
                    "professional_experience": (
                        data_store_service
                        .get_experience_records()
                        .get("professional_experience", [])
                    ),
                    "education_history": (
                        data_store_service
                        .get_experience_records()
                        .get("education_history", [])
                    ),
                }

            return {}

        except Exception as e:

            print(
                f"⚠️ Context loading failure for intent "
                f"'{intent}': {str(e)}"
            )

            return {}

    # =========================================================
    # SYSTEM PROMPT
    # =========================================================
    def _build_system_prompt(
        self, intent: str, context: dict
    ) -> str:
        return f"""
You are Aryan Mishra's professional AI portfolio interview persona. 
You are representing Aryan Mishra in a live recruiter conversation.

================ PERSONA RULES ================
1. Speak in FIRST PERSON. Use:
   - I
   - my
   - me
   - I've
   - I built
   - I worked

2. Never say:
   - "the candidate"
   - "Aryan has..."
   - "the portfolio says..."
   - "the data says..."
   - "as an AI assistant..."

3. Do not pretend to have experience that is not present in the supplied portfolio context.
4. Use ONLY the supplied portfolio context for factual claims.
5. Do not invent:
   - companies, projects, technologies, metrics, education, certifications, job responsibilities, dates

6. Answer naturally like a professional AI Engineer during a technical interview.

7. STRICT INTERVIEW CONSTRAINTS:
   - Be highly concise, natural, and friendly. Do NOT dump the entire resume context list, all projects, or full tech stack arrays unless explicitly asked for a full breakdown.
   - If the intent is "general", "profile", or "about", respond with a sleek 2-3 sentence high-level summary overview stating your name, current title at Tamar Software, and a brief description of your core focus (Computer Vision/OCR).
   - If the recruiter asks a follow-up or cross-question, address ONLY that specific point conversationally without repeating preceding milestones summaries.

8. Do not output JSON.
9. Do not output UI directives.
10. Do not generate portfolio cards.
11. Do not repeat the entire portfolio unless the recruiter explicitly asks for the complete portfolio.

================ CURRENT INTENT ================
{intent}

================ TRUSTED PORTFOLIO CONTEXT ================
{json.dumps(context, indent=2)}

=================================================
Answer the recruiter's latest question directly.
"""


    # =========================================================
    # QUERY EXECUTION
    # =========================================================

    async def execute_query(
        self,
        user_query: str,
        intent: str = "general",
        history: list = None
    ) -> dict:

        if history is None:
            history = []

        try:

            # -------------------------------------------------
            # LOAD ONLY RELEVANT DATA
            # -------------------------------------------------

            context = self._load_context_for_intent(intent)

            print("\n" + "=" * 80)
            print("🧭 PORTFOLIO ORCHESTRATOR")
            print("=" * 80)

            print(f"USER QUERY : {user_query}")
            print(f"INTENT     : {intent}")

            print("CONTEXT LOADED:")
            print(
                json.dumps(
                    context,
                    indent=2,
                    ensure_ascii=False
                )
            )

            print("=" * 80 + "\n")

            # -------------------------------------------------
            # BUILD SYSTEM PROMPT
            # -------------------------------------------------

            system_prompt = self._build_system_prompt(
                intent=intent,
                context=context
            )

            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ]

            # -------------------------------------------------
            # MULTI-TURN HISTORY
            # -------------------------------------------------

            for msg in history:

                if not isinstance(msg, dict):
                    continue

                role = (
                    msg.get("role")
                    or msg.get("sender")
                    or ""
                )

                content = (
                    msg.get("content")
                    or msg.get("text")
                    or ""
                )

                if not content.strip():
                    continue

                if role in [
                    "assistant",
                    "avatar",
                    "bot"
                ]:
                    clean_role = "assistant"
                else:
                    clean_role = "user"

                messages.append(
                    {
                        "role": clean_role,
                        "content": content
                    }
                )

            # -------------------------------------------------
            # CURRENT USER QUERY
            # -------------------------------------------------

            messages.append(
                {
                    "role": "user",
                    "content": user_query
                }
            )

            # -------------------------------------------------
            # SINGLE LLM COMPLETION
            # -------------------------------------------------

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=600
            )

            final_text = (
                completion.choices[0]
                .message
                .content
                or ""
            ).strip()

            # -------------------------------------------------
            # DEBUG
            # -------------------------------------------------

            print("\n" + "=" * 80)
            print("🧠 LLaMA RESPONSE")
            print("=" * 80)

            print(f"INTENT : {intent}")
            print(f"CONTENT: {final_text}")

            print("=" * 80 + "\n")

            return {
                "status": "success",
                "text_content": final_text,
                "intent": intent
            }

        except Exception as e:

            print("\n" + "=" * 80)
            print("🚨 ORCHESTRATOR COMPLETION CRASH")
            print("=" * 80)

            traceback.print_exc()

            print("=" * 80 + "\n")

            return {
                "status": "error",
                "message": str(e)
            }


# =============================================================
# SINGLETON
# =============================================================

orchestrator = PortfolioOrchestrator()