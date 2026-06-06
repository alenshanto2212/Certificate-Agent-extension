import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

# 1. Initialize the FastAPI Web Framework
app = FastAPI(title="AI Career Scout API Engine")

# 2. Fix Security Rules (CORS) 
# This tells your Python server to allow connections coming from your Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows your extension to talk to the backend safely
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure your Gemini API Key directly from your local environment
# (Make sure GEMINI_API_KEY is set in your system environment variables!)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/generate")
async def generate_blueprint(query: str = Query(..., description="The user tracking keywords or history data")):
    """
    This endpoint listens live at http://127.0.0.1:8000/generate?query=KEYWORDS
    """
    print(f"📡 Incoming Request! Received user browsing footprint: {query}")
    
    try:
        # Initialize your preferred high-speed model
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # 3. Dynamic context prompt engineering
        prompt = f"""
        You are an advanced Real-Time AI Career Scout Agent. 
        A user has been browsing the web, and their tracking logs/interests have captured this raw context data:
        "{query}"

        Analyze what technology or technical field they are trying to master right now. 
        Select 2-3 specific global tech targets matching this interest (e.g., if they are looking at React, focus on Web Development platforms like Google Skillshop or foundational vendor portals).
        
        Generate a highly structured, premium HTML portfolio template matching a dark theme ecosystem. 
        Include:
        1. A targeted track review summarizing what skills they need to focus on next.
        2. A curated course pathway map using real global certification targets.
        3. A custom Upwork freelance strategy blueprint tailored to those exact skills.

        CRITICAL REQUIREMENT: Do not output markdown, do not write ```html tags, and do not include <html> or <body> tags. 
        Output ONLY the raw internal HTML block content (e.g., <div>, <h3>, <ul>, <p>, <a>) using sharp emerald-green inline styles for action buttons, ready to be immediately injected onto a web dashboard.
        """

        # 4. Generate the blueprint layout live
        response = model.generate_content(prompt)
        ai_generated_html = response.text.strip()
        
        # 5. Return the package straight back to the extension dashboard tab
        return {"status": "success", "html_blueprint": ai_generated_html}

    except Exception as e:
        print(f"❌ Generation Error: {str(e)}")
        return {
            "status": "error", 
            "html_blueprint": f"<p style='color: #ef4444;'>AI Generation Engine hit an operational fault: {str(e)}</p>"
        }