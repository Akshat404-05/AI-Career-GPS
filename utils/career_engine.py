import json
import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# ------------------------------------------------
# Load Career Database
# ------------------------------------------------

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# ------------------------------------------------
# Generic AI Caller
# ------------------------------------------------

def call_ai(prompt):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(BASE_URL, headers=headers, json=data)

        result = response.json()

        # DEBUG (helps see what OpenRouter returns)
        print("AI RESPONSE:", result)

        # if API returns error
        if "choices" not in result:
            return ""

        if len(result["choices"]) == 0:
            return ""

        content = result["choices"][0]["message"]["content"]

        # Clean up markdown formatting if the AI returns a code block
        content = content.replace("```json","").replace("```","").strip()

        # Validate JSON structure
       
            
        return content

    except Exception as e:
        print("AI CALL FAILED:", e)
        return ""

    
def load_careers():
    with open("careers.json","r") as f:
        return json.load(f)

# ------------------------------------------------
# Career Matching Algorithm
# ------------------------------------------------

def match_careers(user_skills, user_personality):
    careers = load_careers()
    results = []

    # Lowercase user inputs for better matching
    u_skills = [s.lower() for s in user_skills]
    u_pers = [p.lower() for p in user_personality]

    for career in careers:
        c_skills = [s.lower() for s in career.get("skills", [])]
        c_pers = [p.lower() for p in career.get("personality", [])]

        # Calculate exact overlap
        skill_overlap = len(set(u_skills) & set(c_skills))
        pers_overlap = len(set(u_pers) & set(c_pers))

        # Denominator: How many traits does the career actually require?
        total_career_requirements = len(c_skills) + len(c_pers)
        
        # Avoid division by zero
        if total_career_requirements == 0:
            continue

        # Calculate a true match percentage (0 to 100)
        match_percentage = ((skill_overlap + pers_overlap) / total_career_requirements) * 100

        # Optional: Add a slight bonus for High Demand, but don't let it overpower the score
        demand = career.get("demand", "Medium")
        if demand == "High":
            match_percentage += 5  # 5% bonus
        elif demand == "Low":
            match_percentage -= 5  # 5% penalty

        # Cap at 100%
        match_percentage = min(100.0, round(match_percentage, 1))

        # Only recommend careers where they have at least *some* match (e.g., > 10%)
        if match_percentage > 10:
            results.append((career["career"], match_percentage))

    # Sort descending
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:10]

# ------------------------------------------------
# AI Profile Analyzer
# ------------------------------------------------

def analyze_user_profile(text):
    prompt = f"""
Analyze the student's description below.

{text}

Extract skills and personality traits.

Recognize domains like:
Technology
Commerce
Finance
Medicine
Engineering
Arts
Humanities
Law
Government

Return ONLY valid JSON:

{{
 "skills": [],
 "personality": [],
 "subjects": [],
 "domains": []
}}
"""
    return call_ai(prompt)

# ------------------------------------------------
# Career Explanation
# ------------------------------------------------

def explain_career(career, skills, personality):
    prompt = f"""
Explain why the career "{career}" is suitable.

Student skills:
{skills}

Personality:
{personality}

Keep explanation under 120 words.
"""
    return call_ai(prompt)

# ------------------------------------------------
# Career Roadmap Generator
# ------------------------------------------------

def generate_roadmap(career):
    prompt = f"""
Create a 5 step roadmap to become a {career}.

Steps should be practical and beginner friendly.
"""
    return call_ai(prompt)

# ------------------------------------------------
# Skill Gap Detection
# ------------------------------------------------

def detect_skill_gap(career, user_skills):
    prompt = f"""
A student wants to become a {career}.

Current skills:
{user_skills}

Identify:
1. Skills they already have
2. Skills they must improve
"""
    return call_ai(prompt)

# ------------------------------------------------
# Career Demand Analysis
# ------------------------------------------------

def analyze_career_demand(career):
    prompt = f"""
Explain the demand for the career {career}.

Include:
• Current job demand
• Future outlook
• Industries hiring
"""
    return call_ai(prompt)

# ------------------------------------------------
# Salary Prediction
# ------------------------------------------------

def predict_salary(career, skills):
    prompt = f"""
Estimate salary for a {career} in India.

Include:
• Entry level salary
• Mid level salary
• Senior salary
"""
    return call_ai(prompt)

# ------------------------------------------------
# Job Market Analysis
# ------------------------------------------------

def job_market_analysis(career):
    prompt = f"""
Analyze the job market for {career}.

Include:
• hiring sectors
• growth trend
• job availability
"""
    return call_ai(prompt)

# ------------------------------------------------
# AI Career Counselor
# ------------------------------------------------
def career_chat(conversation_history):
    # 1. Setup the messages
    messages = [
        {"role": "system", "content": "You are an expert AI career counselor. Provide detailed, actionable advice including skills required, roadmaps, and salary expectations in India."}
    ]
    
    # 2. Add the user's chat history
    if isinstance(conversation_history, list):
        messages.extend(conversation_history)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": messages
    }

    try:
        response = requests.post(BASE_URL, headers=headers, json=data)
        result = response.json()
        
        # 3. The absolute simplest extraction (No nested logic)
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            return content
            
        # 4. Fallbacks only if 'choices' genuinely doesn't exist
        if "error" in result:
            return f"⚠️ API Error: {result['error']}"

            
        return "🚨 Could not extract answer. Please try again."

    except Exception as e:
        return f"🚨 System Error: {e}"
def generate_interview_question(history):
    prompt = f"""
You are an AI career counselor.

Based on the conversation history below, ask the next
best question to understand the student's interests,
skills, and personality.

Conversation history:
{history}

Ask ONE short question only.
"""
    result = call_ai(prompt)

    if not result:
        return "What subjects or activities do you enjoy the most?"

    return result

# ------------------------------------------------
# RIASEC Personality Scoring
# ------------------------------------------------

def calculate_riasec_profile(text):
    prompt = f"""
Analyze this student description and score RIASEC personality traits.

{text}

Return ONLY valid JSON.
Do not explain anything.

Example format:

{{
"Realistic": 0,
"Investigative": 0,
"Artistic": 0,
"Social": 0,
"Enterprising": 0,
"Conventional": 0
}}
"""
    riasec_json = call_ai(prompt)
    try:
        json.loads(riasec_json)
    except:
        return '{{"Realistic": 50,"Investigative": 50,"Artistic": 50,"Social": 50,"Enterprising": 50,"Conventional": 50}}'
    return riasec_json

# ------------------------------------------------
# Global Career Demand Heatmap Data
# ------------------------------------------------

def global_career_demand(career):
    prompt = f"""
Estimate global demand for the career: {career}

Return JSON with demand score (0-100) for:
USA
India
Germany
Canada
Australia
UK
Singapore

Example format:

{{
 "USA": 90,
 "India": 85,
 "Germany": 70,
 "Canada": 75,
 "Australia": 65,
 "UK": 80,
 "Singapore": 60
}}
"""
    return call_ai(prompt)

def build_career_graph():
    careers = load_careers()
    nodes = []
    edges = []

    for career in careers:
        career_name = career["career"]
        career_skills = career.get("skills", [])

        nodes.append(career_name)

        for skill in career_skills:
            edges.append((skill, career_name))
            nodes.append(skill)

    return list(set(nodes)), edges