# My AI-Based Portfolio: Voice-Activated Agentic Core Engine 🎙️🤖

[![FastAPI Engine](https://shields.io)](https://tiangolo.com)
[![Next.js 15 Canvas](https://shields.io)](https://nextjs.org)
[![Groq Hardware Accelerations](https://shields.io)](https://groq.com)
[![LLaMA Core Intelligence](https://shields.io)](https://meta.ai)

Welcome to **My AI-Based Portfolio Dashboard**. This is a production-grade, asynchronous full-stack agentic ecosystem designed to serve as an intelligent, conversational digital twin of **Aryan Mishra, AI Engineer**. 

Unlike standard portfolio web layouts or basic keyword-matching bots, this architecture combines a **Deterministic Intent-Routing Middleware Gateway** with single-pass LLM text completions to deliver an error-immune, contextual, and high-performance recruiter experience.

---

## 🚀 Key Architectural Breakthroughs & Features

### 1. Hands-Free Dual-Voice Handshake (Speech-to-Text & Text-to-Speech)
* **Voice Recruiter Input (STT):** Recruiters can engage a hands-free console by tapping the integrated microphone button. The system leverages browser-native HTML5 Web Speech Recognition APIs to capture vocal frequencies and map transcripts directly into the query state with sub-millisecond processing.
* **Strict Indian Male Voice Engine (TTS):** When data packets arrive from the backend, a customized HTML5 Web Speech Synthesis pipeline overrides default operating system profiles, strictly enforcing a clear, professional, corporate-grade **Indian Male English Accent (`en-IN`)** driving an energetic, structured interview pacing tempo.

### 2. Symmetrical Separated Layout Matrix (Generative Text + Static Bento Tabs)
* **Textual Conversational Core:** The chat terminal box focuses strictly on executing high-accuracy, first-person candidate narrative dialogue tracking context strings without leaking raw JSON brackets or cluttering the interface viewport.
* **Decoupled Bento Tabs Section:** Volatile JSON rendering schemas for **Projects, Experiences, Technical Skills, Academics, and Contacts** are decoupled entirely onto static, state-managed dashboard tabs. Recruiters can seamlessly switch panels with 0% runtime type-exception risks.

### 3. Hardened Production Security Boundaries
* **Pydantic Validation Firewall:** The incoming router endpoint payload is tightly guarded against data injections or empty trace arrays, forcing strict data-type compliance contracts (`user_query` is constrained between 1 to 500 characters).
* **CORS Origin Whitelisting:** Wildcard restrictions (`*`) are fully decommissioned. The app enforces a strict whitelist array layer, blocking malicious script crawlers, and allows only trusted loopback addresses and verified deployment mirrors.
* **API Failure Recovery Gateway:** If external cloud resources face momentary latency or timeouts, an explicit `try/except` fallback boundary intercepts the crash, rendering a graceful user recovery recommendation.

---

## 🧬 System Topography & Data Flows

```text
    [ Recruiter Vocal / Text Query ]
                   │
                   ▼ Dispatched from Next.js Dashboard Client (:3000)
    [ FastAPI Route Endpoint Gateway (:8000) ]
                   │
                   ▼ Pydantic Input Firewall Constraints Validated ✅
    [ Deterministic Intent Classifier ]
                   │
                   ├──> [ regex scanning / keyword checks ] ──> Maps Target Aspect Tag
                   ▼
    [ PortfolioOrchestrator Service Engine ]
                   ├──> Loads specific JSON Context on Demand (Profile, Projects, Skills, etc.)
                   └──> Packs data matrix & fires Single-Pass request to Groq Cloud Hardware Array
                   │
                   ▼ Meta LLaMA 3.3 70B evaluates facts and generates 1st-Person text content
    [ Sanitized Server-Side Response Pre-Processor ]
                   └──> Strips out raw markdown symbols (***, **) at python levels
                   │
                   ▼ Returns Clean HTTP 200 OK JSON Packet: { "text_content": "..." }
    [ Next.js Client Terminal View Canvas ]
                   ├──> Typography highlighted with clean shell bullet indicators (›)
                   └──> Native audio speaker nodes trigger real-time lipsync vocal track!
```

---

## 🛠️ The Technical Stack Catalog

* **Presentation Layer:** Next.js 15 (App Router Core), React 19, TypeScript Framework, Tailwind CSS Engine, Lucide Icons Framework, HTML5 Web Speech APIs Core.
* **Microservices Layer:** Python 3.10, FastAPI Framework, Uvicorn ASGI Server, Pydantic Data Validations V2, WatchFiles Trackers.
* **Cognitive Processing Array:** Meta LLaMA 3.3 70B Versatile, Groq Cloud SDK Client, Decoupled JSON Data-Store Layer.

---

## 📦 Local Workspace Operations Manual

### Prerequisites
* Ensure your Windows host environment has **Node.js (v18+)** and **Python 3.10+** configured natively inside system path tracks.

### 1. Booting the FastAPI Backend Microservice
Navigate to the engine directory, spin up a secure python virtual shell environment, and establish dependency locks:
```bash
cd backend-engine
python -m venv venv
.\venv\Scripts\activate

# Install production-hardened dependencies
pip install -r requirements.txt

# Create your localized secret environment token file
# Add: GROQ_API_KEY=gsk_your_real_host_token_string_here
echo GROQ_API_KEY=your_key_here > .env

# Launch the asynchronous server instance
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Launching the Next.js Client Dashboard
Open a parallel system terminal pane window, shift to the client repository, and launch the dev bundler:
```bash
cd frontend-client
npm install

# Initialize your local public environment URL reference variable
echo NEXT_PUBLIC_BACKEND_URL=http://localhost:8000 > .env.local

# Run the live hot-reload server canvas
npm run dev
```
Open your favorite browser client tab and map straight onto **`http://localhost:3000`** to trigger the AI Portfolio Agent!

---

## 🛡️ Production & Cloud Deployment Roadmap

This application's architecture is fully decoupled, production-hardened, and cloud-ready for immediate hosting deployment:
* **The `.gitignore` Shield:** Ensured zero direct exposure of keys; `.env` profiles are excluded globally to completely insulate host variables.
* **The Docker Configuration Layer:** Includes multi-stage optimized frontend `Dockerfile` blocks andpersistent database storage volumes shared arrays setups ready for automated deployment grids.
