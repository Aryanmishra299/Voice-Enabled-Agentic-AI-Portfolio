"use client";

import { useState, useRef, useEffect } from "react";
import { Terminal as TerminalIcon, Cpu, Github, Linkedin, Mail, Code, Briefcase, Award, ShieldCheck, Zap } from "lucide-react";

interface ChatMessageContract {
  sender: "user" | "avatar";
  text: string;
}

type PortfolioSection = "projects" | "experiences" | "skills" | "academics" | "contact";

export default function AINativePortfolioDashboard() {
  const [promptInput, setPromptInput] = useState("");
  const [conversationHistory, setConversationHistory] = useState<ChatMessageContract[]>([
    { sender: "avatar", text: "System Boot Sequence Completed. Core Logic Active. Hello Recruiter! I am Aryan Mishra. Welcome to my engineering dashboard. Feel free to ask about my projects, experiences, technical skills, or academics." }
  ]);
  const [networkLoading, setNetworkLoading] = useState(false);
  const [activeSection, setActiveSection] = useState<PortfolioSection>("projects");
  const [isClientMounted, setIsClientMounted] = useState(false);
  const loggingConsoleEndRef = useRef<HTMLDivElement>(null);
// Around Line 22 inside frontend-client/app/page.tsx:
  const [isListening, setIsListening] = useState(false); // 🎤 ADDED: Microphone state manager


  // Database models configuration
  const projectsMockDatabase = [
    {
      id: "intelligent-ocr-idp",
      name: "Intelligent OCR & Document Processing System",
      technologies: ["Python", "OpenCV", "PaddleOCR"],
      short_summary: "Advanced image preprocessing with OpenCV to deskew and denoise low-res inputs before executing PaddleOCR text localization chunks.",
      metrics: "Improved text extraction accuracy by ~25-30% on noisy layouts."
    },
    {
      id: "ai-document-assistant-rag",
      name: "AI Document Assistant (RAG-based GenAI System)",
      technologies: ["Python", "LangChain", "ChromaDB", "FastAPI"],
      short_summary: "Combined PaddleOCR and OpenCV for initial extraction, passing parsed vectors to LangChain RAG pipes with ChromaDB backend store.",
      metrics: "Significantly reduced manual search efforts via structured context injection."
    },
    {
      id: "customer-churn-prediction",
      name: "Customer Churn Prediction Pipeline",
      technologies: ["Python", "Scikit-Learn", "Pandas", "NumPy", "Matplotlib"],
      short_summary: "Executed clean feature engineering and data preprocessing via Pandas and NumPy, routing matrix shapes to Scikit-Learn classification wrappers.",
      metrics: "Optimized classification confidence metrics and model reliability profiles."
    },
    {
      id: "ai-model-api-deployment",
      name: "AI Model API Deployment Engine",
      technologies: ["Python", "FastAPI", "Uvicorn"],
      short_summary: "Constructed asynchronous FastAPI gateways processing structured JSON tokens for instant inference integration layers.",
      metrics: "Enables robust real-time low-latency inference processing across decoupled endpoints."
    }
  ];

  const experienceMockDatabase = [
    {
      id: "tamar-software",
      organization: "Tamar Software (Noida / Remote)",
      role: "AI Engineer",
      timeline: "June 2026 - Present",
      responsibilities: [
        "Architected open-source OCR engine optimized for high-throughput workflows.",
        "Developed conversational AI systems featuring custom state-management logic chatbot architectures."
      ]
    },
    // Locate this block inside data-store/experience.json:
    {
    "id": "niit-associate",
    "organization": "NIIT (Gurgaon / On-site)", 
    "role": "Associate",
    "timeline": "Jan 2026 - April 2026",
    "responsibilities": [
        "Processed structured datasets by building custom python parsing scripts and managing data integrity.",
        "Designed data automation workflows to streamline operational processing bottlenecks."
    ]
    },

    {
      id: "freelance-contractor",
      organization: "Technical Contractor & Freelance System Engineer",
      role: "AI Engineer",
      timeline: "Sept 2025 - Feb 2026",
      responsibilities: [
        "Designed OCR systems capable of handling heavily noisy, low-resolution layouts.",
        "Improved text extraction accuracy by 25-30% on noisy unformatted document streams."
      ]
    },
    {
      id: "planet-spark",
      organization: "PlanetSpark (Gurgaon / On-site)",
      role: "Business Operations & Data Analyst",
      timeline: "June 2025 - Dec 2025",
      responsibilities: [
        "Analyzed user engagement data to identify behavioral trends and improve retention strategies.",
        "Delivered data-driven insights that enhanced decision-making and operational efficiency."
      ]
    }
  ];

  const skillsMockCategories = [
    { title: "Programming", content: "Python, SQL, Java" },
    { title: "AI/ML & Libraries", content: "OpenCV, PaddleOCR, Scikit-learn, NumPy, Pandas, Matplotlib, TensorFlow / PyTorch (Working Knowledge), LangChain" },
    { title: "Generative AI & NLP", content: "LLMs, RAG, Prompt Engineering" },
    { title: "Vector DB", content: "ChromaDB" },
    { title: "Domains", content: "Computer Vision, OCR, Machine Learning, NLP, Feature Engineering" },
    { title: "Tools & Deployment", content: "FastAPI (Working Knowledge), REST APIs, Git, GitHub, Jupyter Notebook, VS Code, AZURE, AWS" }
  ];

  const educationMockDatabase = [
    {
      institution: "Shri Ramswaroop Memorial University",
      degree: "Bachelor of Computer Application (BCA)",
      timeline: "2022 - 2025",
      performance_metric: "8.12 CGPA"
    }
  ];

  const certificationsMockList = [
    "Machine Learning Specialization",
    "Computer Vision Advanced Certification",
    "Generative AI & LLM Systems Orchestration"
  ];

  useEffect(() => {
    setIsClientMounted(true);
  }, []);

  useEffect(() => {
    loggingConsoleEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversationHistory]);

  // ──────────────────────────────────────────────────────────────────
  // 🎙️ THE MASTER AUDIO CORE TRIGGER: LIVE SYNCHRONOUS VOICE ENGINE
  // ──────────────────────────────────────────────────────────────────
  const speakAvatarStatement = (textToSpeak: string) => {
    if (typeof window === "undefined" || !window.speechSynthesis) return;

    // Instantly cancel any previously ongoing speech streams to prevent overlapping tracks
    window.speechSynthesis.cancel();

    // Clean up markdown markers and syntax pointers before processing vocal audio
    const cleanSpokenString = textToSpeak
      .replaceAll("***", "")
      .replaceAll("**", "")
      .replaceAll("›", "")
      .replaceAll("🔹", "")
      .replace(/\[.*?\]/g, ""); // Strips metadata fallback logs brackets strings

    const vocalUtterance = new SpeechSynthesisUtterance(cleanSpokenString);

    // Fetch browser-native premium voice profiles (Targeting English Natural Profiles)
        // 🛡️ RE-ENGINEERED: STRICT INDIAN MALE PROFESSIONAL VOICE SELECTOR MATRIX
    const availableVoices = window.speechSynthesis.getVoices();
    
    // Priority 1: Direct Indian English Profile match (e.g., Microsoft Ravi, Google en-IN Male)
    let targetedProfileVoice = availableVoices.find(
      (v) => (v.lang === "en-IN" || v.lang.startsWith("en-IN")) && 
             (v.name.toLowerCase().includes("ravi") || v.name.toLowerCase().includes("male") || v.name.toLowerCase().includes("google"))
    );

    // Priority 2: Fallback to any active Indian English voice index if exact male signature isn't named
    if (!targetedProfileVoice) {
      targetedProfileVoice = availableVoices.find((v) => v.lang.startsWith("en-IN"));
    }

    // Priority 3: Safe generic clear English fallback if the device operating system completely lacks en-IN packs
    if (!targetedProfileVoice) {
      targetedProfileVoice = availableVoices.find((v) => v.lang.startsWith("en-GB") && v.name.toLowerCase().includes("male")) || 
                             availableVoices.find((v) => v.lang.startsWith("en-US") && v.name.toLowerCase().includes("male"));
    }

    if (targetedProfileVoice) {
      vocalUtterance.voice = targetedProfileVoice;
    }


    vocalUtterance.rate = 1.05;  // Elite, professional interview response pacing speed configuration
    vocalUtterance.pitch = 1.0;  // Balanced natural human pitch tone metrics
    
    window.speechSynthesis.speak(vocalUtterance);
  };

    // ──────────────────────────────────────────────────────────────────
  // 🎤 ADDED INTERACTION: LIVE RECRUITER SPEECH-TO-TEXT LISTENER HOOK
  // ──────────────────────────────────────────────────────────────────
  const toggleVoiceListeningInput = () => {
    if (typeof window === "undefined") return;

    // Check cross-browser Webkit validation standards guards
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      alert("⚠️ API Fault: Your current browser does not natively support HTML5 Voice Speech Recognition.");
      return;
    }

    // Instantly stop if microphone is already engaged
    if (isListening) {
      setIsListening(false);
      return;
    }

    const recognitionInstance = new SpeechRecognition();
    recognitionInstance.continuous = false; // Capture a single turn sawal safely
    recognitionInstance.lang = "en-US";     // Match global corporate accent benchmarks
    recognitionInstance.interimResults = false;

    recognitionInstance.onstart = () => {
      setIsListening(true);
    };

    recognitionInstance.onerror = (err: any) => {
      console.error("Microphone hardware error:", err);
      setIsListening(false);
    };

    recognitionInstance.onend = () => {
      setIsListening(false);
    };

    recognitionInstance.onresult = (event: any) => {
      const rawVocalTranscript = event.results[0][0].transcript;
      if (rawVocalTranscript.strip !== "") {
        // Set the converted text directly inside the input textbox state channel! ✅
        setPromptInput(rawVocalTranscript);
      }
    };

    recognitionInstance.start();
  };


  // ──────────────────────────────────────────────────────────────────
  // ⚡ DYNAMIC MARKDOWN PARSER LAYER FOR EXTRA READABILITY INDENTATIONS
  // ──────────────────────────────────────────────────────────────────
    // Overwrite with this fail-safe string cleaning definition:
  const formatTerminalText = (rawText: string) => {
    if (!rawText) return null;

    // HOTFIX: Instantly replace triple asterisks with double asterisks to guarantee zero clutter text tags
    const cleanedText = rawText.replaceAll("***", "**");
    const layoutLines = cleanedText.split("\n");


    return layoutLines.map((line, lIdx) => {
      let trimmed = line.trim();
      if (!trimmed) return <div key={lIdx} className="h-2" />; // Add a clean padding spacer row

      // Check if the current line acts as a numbered list item or a standard bullet indicator
      const isBulletPattern = trimmed.startsWith("*") || trimmed.startsWith("-") || /^\d+\./.test(trimmed);
      
      // Clean up markdown bullet indicators from text display arrays
      if (trimmed.startsWith("*") || trimmed.startsWith("-")) {
        trimmed = trimmed.substring(1).trim();
      }

      // Intercept inline bold headers declarations `**Header:**`
      const boldSegments = trimmed.split("**");
      
      return (
        <div 
          key={lIdx} 
          className={`font-mono text-xs leading-relaxed transition-all tracking-wide ${
            isBulletPattern ? "pl-4 border-l border-green-500/10 my-2 py-0.5 bg-slate-900/10 rounded" : "my-1"
          }`}
        >
          {isBulletPattern && <span className="text-green-400 mr-2 font-bold font-mono">›</span>}
          {boldSegments.map((segment, sIdx) => {
            // Alternate indexing detects matching strings inside markdown stars constraints blocks
            const isBoldNode = sIdx % 2 === 1;
            return (
              <span 
                key={sIdx} 
                className={isBoldNode ? "text-white font-bold tracking-wide uppercase border-b border-slate-800 pb-[1px]" : "text-slate-300"}
              >
                {segment}
              </span>
            );
          })}
        </div>
      );
    });
  };

  const dispatchRecruiterPrompt = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!promptInput.trim() || networkLoading) return;

    const targetedQuery = promptInput.trim();
    setPromptInput("");
    setNetworkLoading(true);

    setConversationHistory((prev) => [...prev, { sender: "user", text: targetedQuery }]);

    try {
      const backendEndpoint = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
      
      const formattedHistoryForLLM = conversationHistory.map((msg) => ({
        role: msg.sender === "user" ? "user" : "assistant",
        content: msg.text
      }));

      const networkResponse = await fetch(`${backendEndpoint}/api/v1/chat/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_query: targetedQuery,
          chat_history: formattedHistoryForLLM
        }),
      });

      if (!networkResponse.ok) {
        setConversationHistory((prev) => [
          ...prev,
          { sender: "avatar", text: `⚠️ System Processing Error: Backend returned HTTP status ${networkResponse.status}. Check Python console logs.` }
        ]);
        setNetworkLoading(false);
        return;
      }

      const dataResult = await networkResponse.json();
      const outputTextContent = dataResult.response?.text_content || "Unable to generate an analytical context response parameters.";

      // 🔥 CRITICAL TRIGGER: Execute voice synthesis instantly right as text data arrives!
      speakAvatarStatement(outputTextContent);

      setConversationHistory((prev) => [
        ...prev,
        {
          sender: "avatar",
          text: outputTextContent
        }
      ]);

    } catch (err) {
      setConversationHistory((prev) => [
        ...prev,
        { sender: "avatar", text: "⚠️ Network Disconnect: Unable to securely connect over server endpoint channel." }
      ]);
    } finally {
      setNetworkLoading(false);
    }
  };

  if (!isClientMounted) {
    return <div className="min-h-screen bg-slate-950 text-slate-500 font-mono p-8 flex items-center justify-center">Initializing Cognitive Portfolio Shell...</div>;
  }

  return (
    <main className="min-h-screen p-4 md:p-8 max-w-7xl mx-auto flex flex-col gap-6 selection:bg-green-500 selection:text-slate-950" suppressHydrationWarning>
      
      {/* HEADER META IDENTITY MATRIX BAR */}

      <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center p-6 bg-slate-900/50 border border-slate-800 rounded-xl backdrop-blur-sm gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            Aryan Mishra <span className="text-xs px-2 py-0.5 bg-green-500/10 text-green-400 border border-green-500/20 rounded">AI Engineer</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">Computer Vision • Intelligent Document Processing • Localized ML Architectures</p>
        </div>
        <div className="flex gap-3 text-slate-400">
          <a href="https://github.com/Aryanmishra299" target="_blank" className="hover:text-green-400 transition-colors"><Github className="w-5 h-5" /></a>
          <a href="https://linkedin.com" target="_blank" className="hover:text-green-400 transition-colors"><Linkedin className="w-5 h-5" /></a>
          <a href="mailto:aryantulikamishra@gmail.com" className="hover:text-green-400 transition-colors"><Mail className="w-5 h-5" /></a>
        </div>
      </header>

      {/* CHAT INTERFACE SECTION MONITOR */}
      <section className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        
        {/* AVATAR GLOW NODE FRAME */}
        <div className="lg:col-span-4 bg-slate-900/40 border border-slate-800 rounded-2xl p-6 flex flex-col items-center justify-center min-h-[300px] relative overflow-hidden backdrop-blur-sm">
          <div className="absolute top-4 left-4 flex items-center gap-1.5 text-xs text-slate-500">
            <Cpu className="w-3.5 h-3.5 text-green-500 animate-pulse" /> LIVE_AVATAR_NODE
          </div>
                      {/* ────────────────────────────────────────────────────────────────── */}
          {/* RE-ENGINEERED: ENLARGED PORTRAIT AVATAR ZONE WITH LIVE AUDIO GLOWS  */}
          {/* ────────────────────────────────────────────────────────────────── */}
          <div className={`w-48 h-48 rounded-full border-2 ${networkLoading ? 'border-green-400 shadow-[0_0_20px_rgba(34,197,94,0.4)]' : 'border-slate-800'} flex items-center justify-center bg-slate-950 overflow-hidden shadow-2xl relative transition-all duration-300`}>
            {networkLoading ? (
              /* Keeps the structural vocal analysis loops active during speech turns */
              <div className="absolute inset-0 bg-slate-950 flex flex-col items-center justify-center gap-1.5 animate-pulse">
                <span className="text-[9px] text-green-400 font-mono tracking-widest uppercase">[ VOCAL_SYNTHESIS ]</span>
                <div className="w-5 h-5 border-2 border-green-500 border-t-transparent rounded-full animate-spin"></div>
              </div>
            ) : (
              /* 👤 ENLARGED identity picture matrix layer. Applied 'object-top' to preserve head space elements */
              <img 
                src="/avatar.jpeg" 
                alt="Aryan Mishra AI Portfolio Avatar" 
                className="w-full h-full object-cover object-top grayscale brightness-95 opacity-90 hover:grayscale-0 hover:opacity-100 hover:scale-105 transition-all duration-500 ease-out"
                onError={(e) => {
                  e.currentTarget.style.display = 'none';
                  if (e.currentTarget.parentElement) {
                    const fallbackSpan = document.createElement('span');
                    fallbackSpan.className = 'text-4xl animate-pulse';
                    fallbackSpan.innerText = '👨‍💻';
                    e.currentTarget.parentElement.appendChild(fallbackSpan);
                  }
                }}
              />
            )}
          </div>


          <div className="mt-4 text-center">
                        <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">ARYAN MISHA</p>
            <p className={`text-xs mt-1 font-bold ${networkLoading ? 'text-green-400 animate-pulse' : 'text-slate-500'}`}>
              {networkLoading ? "Processing Inference Token Stream..." : "AI & COMPUTER VISION ENGINEER"}
            </p>
          </div>
        </div>

        {/* BASH MONITORS TERMINAL FRAME */}
        <div className="lg:col-span-8 bg-slate-950 border border-slate-800 rounded-2xl flex flex-col h-[400px] overflow-hidden shadow-xl">
          <div className="bg-slate-900/90 px-4 py-2.5 border-b border-slate-800 flex justify-between items-center text-xs text-slate-400">
            <span className="flex items-center gap-2 text-slate-300 font-bold"><TerminalIcon className="w-4 h-4 text-green-500" />Chat With Aryan-AI</span>
            <div className="flex gap-1.5">
              <span className="w-2 h-2 rounded-full bg-slate-800"></span>
              <span className="w-2 h-2 rounded-full bg-slate-800"></span>
              <span className="w-2 h-2 rounded-full bg-green-500/40"></span>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3 text-xs leading-relaxed text-slate-300">
            {conversationHistory.map((messageBlock, idx) => (
              <div key={idx} className={`flex flex-col gap-1 ${messageBlock.sender === "user" ? "items-end" : "items-start"}`}>
                <span className="text-[9px] text-slate-500 uppercase tracking-wider px-1">
                  {messageBlock.sender === "user" ? "You" : "Aryan"}
                </span>
                <div className={`max-w-[90%] rounded-xl px-4 py-2 border whitespace-pre-wrap ${
                messageBlock.sender === "user" 
                    ? "bg-slate-900 border-slate-800 text-slate-100" 
                    : "bg-green-950/10 border-green-900/40 text-green-400"
                }`}>

                  {messageBlock.text}
                </div>
              </div>
            ))}
            <div ref={loggingConsoleEndRef} />
          </div>

                    <form onSubmit={dispatchRecruiterPrompt} className="border-t border-slate-800 p-2.5 bg-slate-900/40 flex items-center gap-2">
            <span className="text-green-500 font-bold pl-1 text-xs">~</span>
            
            {/* INJECTED: DYNAMIC MIC CONSOLE CONTROL TOGGLE */}
            <button
              type="button"
              onClick={toggleVoiceListeningInput}
              className={`p-1 rounded transition-colors ${
                isListening 
                  ? "text-red-500 bg-red-500/10 border border-red-500/30 animate-pulse" 
                  : "text-slate-500 hover:text-green-400 bg-slate-900/40 border border-slate-800/80"
              }`}
              title="Speak your question directly"
            >
              🎤
            </button>

            <input
              type="text"
              value={promptInput}
              onChange={(e) => setPromptInput(e.target.value)}
              placeholder={isListening ? "[ LISTENING // SPEAK INTO MICROPHONE NOW... ]" : "Ask about my projects, experiences, technical skills, or academics..."}
              disabled={networkLoading || isListening}
              className="flex-1 bg-transparent border-0 outline-none text-slate-200 placeholder:text-slate-600 disabled:placeholder:text-red-400 text-xs py-1 disabled:opacity-50 font-mono"
            />

            
            <button
              type="button"
              onClick={() => {
                const initText = "System logs flushed. Core Logic Active. Hello Recruiter! I am Aryan Mishra. Welcome to my engineering dashboard. Feel free to ask about my projects, experiences, technical skills, or academics.";
                // Triggers real-time vocal audio speech reset feedback turn
                speakAvatarStatement(initText);
                setConversationHistory([{ sender: "avatar", text: initText }]);
              }}

              className="bg-slate-800 hover:bg-slate-700 text-slate-400 font-mono px-2.5 py-1 rounded-md text-xs transition-colors"
            >
              clear
            </button>

            <button
              type="submit"
              disabled={networkLoading || !promptInput.trim()}
              className="bg-green-500 hover:bg-green-400 disabled:bg-slate-800 text-slate-950 disabled:text-slate-600 font-bold px-3 py-1 rounded-md text-xs tracking-wider uppercase transition-colors"
            >
              {networkLoading ? "Sending..." : "Execute"}
            </button>
          </form>
        </div>
      </section>

      {/* ────────────────────────────────────────────────────────────────── */}
      {/* 🛠️ STEP 4 DETACHED INTERACTIVE DECOUPLED PORTFOLIO TABS SECTION     */}
      {/* ────────────────────────────────────────────────────────────────── */}
      <section className="mt-4 p-6 bg-slate-900/30 border border-slate-800 rounded-2xl backdrop-blur-sm shadow-xl">
        <div className="flex flex-wrap gap-2 border-b border-slate-800/80 pb-3">
          {[
            ["projects", "Projects"],
            ["experience", "Experiences"],
            ["skills", "Technical Skills"],
            ["education", "Academic"],
            ["contact", "Contact"]
          ].map(([key, label]) => (
            <button
              key={key}
              onClick={() => setActiveSection(key as PortfolioSection)}
              className={`px-4 py-2 rounded-lg text-xs font-mono transition-all font-semibold ${
                activeSection === key 
                  ? "bg-green-500 text-slate-950 font-bold shadow-md shadow-green-500/10" 
                  : "bg-slate-950/80 border border-slate-800 text-slate-400 hover:text-green-400 hover:border-green-500/20"
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        <div className="mt-6 font-mono text-xs">
          
          {/* STEP 5: RENDERING PROJECT SHIELD CARDS ONLY IN PROJECTS TAB */}
          {activeSection === "projects" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {projectsMockDatabase.map((proj) => (
                <div key={proj.id} className="p-5 bg-slate-950/60 border border-slate-800 hover:border-slate-700/60 rounded-xl transition-all flex flex-col justify-between gap-4 shadow-md">
                  <div>
                    <h3 className="text-white font-bold text-sm flex items-center gap-1.5"><Code className="w-4 h-4 text-green-400" /> {proj.name}</h3>
                    <p className="text-xs text-slate-400 mt-2.5 leading-relaxed">{proj.short_summary}</p>
                  </div>
                  <div className="flex flex-col gap-2 border-t border-slate-800/60 pt-2">
                    <div className="flex flex-wrap gap-1.5">
                      {proj.technologies.map((tech) => (
                        <span key={tech} className="text-[10px] bg-slate-900 border border-slate-800 text-slate-300 px-2 py-0.5 rounded-md font-medium">{tech}</span>
                      ))}
                    </div>
                    <div className="text-[11px] text-green-400 font-semibold flex items-center gap-1 mt-1"><Zap className="w-3.5 h-3.5" /> Metrics: {proj.metrics}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* STEP 6: RENDERING WORK HISTORY TIMELINE CARDS ONLY IN EXPERIENCE TAB */}
          {activeSection === "experiences" && (
            <div className="flex flex-col gap-4">
              {experienceMockDatabase.map((work) => (
                <div key={work.id} className="p-5 bg-slate-950/60 border border-slate-800 rounded-xl flex flex-col gap-3 shadow-md">
                  <div className="flex justify-between items-start gap-4 border-b border-slate-800/60 pb-2">
                    <div>
                      <h3 className="text-white font-bold text-sm flex items-center gap-1.5"><Briefcase className="w-4 h-4 text-green-400" /> {work.organization}</h3>
                      <p className="text-green-400 font-semibold text-xs mt-0.5">{work.role}</p>
                    </div>
                    <span className="text-[10px] bg-slate-900 border border-slate-800 text-slate-400 px-2 py-0.5 rounded-md">{work.timeline}</span>
                  </div>
                  <ul className="space-y-1.5 list-none mt-1">
                    {work.responsibilities.map((item, index) => (
                      <li key={index} className="text-xs text-slate-400 leading-relaxed flex items-start gap-1.5">
                        <span className="text-green-500">•</span> {item}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}

          {/* RENDERING TECH SKILLS MATRIX INSIDE SKILLS TAB */}
                    {/* RENDERING REAL-WORLD RESUME-MATCHING TECHNICAL INDEX INSIDE SKILLS TAB */}
          {activeSection === "skills" && (
            <div className="flex flex-col gap-5 font-mono text-xs max-w-4xl">
              <div className="flex items-center gap-2 px-1 text-[11px] text-slate-500 uppercase tracking-widest border-b border-slate-900 pb-2">
                <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
                <span>System Manifest: Verified Engineering Skills Inventory Loaded</span>
              </div>
              
              <div className="p-5 bg-slate-950/80 border border-slate-800 rounded-xl shadow-xl flex flex-col gap-4 relative overflow-hidden group hover:border-slate-700/60 transition-all">
                <div className="border-b border-slate-800 pb-2.5">
                  <h3 className="text-white font-bold text-sm tracking-wide uppercase flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-500 rounded-sm"></span> TECHNICAL SKILLS MATRIX
                  </h3>
                </div>

                {/* Structured High Density Rows Layout Section */}
                <div className="flex flex-col gap-4 leading-relaxed">
                  {[
                    { title: "Programming", content: "Python, SQL, Java" },
                    { title: "AI/ML & Libraries", content: "OpenCV, PaddleOCR, Scikit-learn, NumPy, Pandas, Matplotlib, TensorFlow / PyTorch (Working Knowledge), LangChain" },
                    { title: "Generative AI & NLP", content: "LLMs, RAG, Prompt Engineering" },
                    { title: "Vector DB", content: "ChromaDB" },
                    { title: "Domains", content: "Computer Vision, OCR, Machine Learning, NLP, Feature Engineering" },
                    { title: "Tools & Deployment", content: "FastAPI (Working Knowledge), REST APIs, Git, GitHub, Jupyter Notebook, VS Code, AZURE, AWS" }
                  ].map((row, rIdx) => (
                    <div key={rIdx} className="grid grid-cols-1 sm:grid-cols-12 gap-1 sm:gap-4 p-2.5 bg-slate-900/30 border border-slate-900 hover:bg-slate-900/60 hover:border-slate-800/80 rounded-lg transition-all flex items-start">
                      {/* Left Block: Bold Highlight Category Title Header */}
                      <div className="sm:col-span-3 text-green-400 font-bold tracking-wide uppercase border-r-0 sm:border-r border-slate-800/60 sm:pr-2">
                        {row.title}:
                      </div>
                      {/* Right Block: Safe text strings elements mapping content */}
                      <div className="sm:col-span-9 text-slate-300 font-medium">
                        {row.content}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}


          {/* RENDERING ACADEMICS AND CERTIFICATES INSIDE EDUCATION TAB */}
          {activeSection === "education" && (
            <div className="flex flex-col gap-4 max-w-3xl">
              {educationMockDatabase.map((edu, idx) => (
                <div key={idx} className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl flex flex-col gap-1 shadow-md">
                  <h3 className="text-white font-bold text-sm flex items-center gap-1.5"><Award className="w-4 h-4 text-green-400" /> {edu.institution}</h3>
                  <p className="text-xs text-slate-300 mt-1">{edu.degree} ({edu.timeline})</p>
                  <p className="text-xs text-green-400 font-semibold mt-1">🎯 Performance Index: {edu.performance_metric}</p>
                </div>
              ))}
              <div className="p-4 bg-slate-950/40 border border-slate-800 border-dashed rounded-xl flex flex-col gap-2.5">
                              <span className="text-xs font-bold text-slate-400 flex items-center gap-1.5 uppercase"><ShieldCheck className="w-4 h-4 text-green-400" /> Professional Credentials</span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-300">
                  {certificationsMockList.map((cert, cIdx) => (
                    <div key={cIdx} className="bg-slate-950 p-2 rounded-md border border-slate-800/80 flex items-center gap-1.5">🔹 {cert}</div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* RENDERING CONTACT INFO DATA CARD */}
          {activeSection === "contact" && (
            <div className="p-5 bg-slate-950/60 border border-slate-800 rounded-xl max-w-md flex flex-col gap-3 shadow-md">
              <h3 className="text-white font-bold text-sm uppercase tracking-wider border-b border-slate-800 pb-2 flex items-center gap-2">🌐 Initiate Handshake Channel</h3>
              <div className="text-slate-400 flex flex-col gap-2 text-xs">
                <div><span className="text-white font-bold font-mono">Location:</span> Lucknow, Uttar Pradesh, India</div>
                <div><span className="text-white font-bold font-mono">Secure Mail:</span> aryantulikamishra@gmail.com</div>
                <div><span className="text-white font-bold font-mono">Phone:</span> +91-9140909121</div>
                <div className="flex gap-2 border-t border-slate-800/60 pt-2.5 mt-1">
                  <a href="https://github.com/Aryanmishra299" target="_blank" className="text-green-400 hover:underline">GitHub Workspace</a>
                  <span className="text-slate-700">|</span>
                  <a href="https://www.linkedin.com/in/aryanmishra299/" target="_blank" className="text-green-400 hover:underline">LinkedIn Connection</a>
                </div>
              </div>
            </div>
          )}

        </div>
      </section>
    </main>
  );
}

