import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

prompt = """
Generate 300 careers across ALL domains:

Technology
Commerce
Finance
Business
Medicine
Engineering
Arts
Humanities
Law
Government
Creative fields

Each career must include:

career
skills
personality
salary
demand
category

Return ONLY valid JSON.

Example format:

[
 {
  "career": "Chartered Accountant",
  "skills": ["Accounting","Finance","Taxation"],
  "personality": ["Analytical","Detail Oriented"],
  "salary": "8L-30L",
  "demand": "High",
  "category": "Commerce"
 }
]
"""

data = {
    "model": "openai/gpt-4o-mini",
    "messages": [
        {"role": "user", "content": prompt}
    ]
}

response = requests.post(url, headers=headers, json=data)

result = response.json()

if "choices" not in result or len(result["choices"]) == 0:
    print("No choices in response:", result)
    exit(1)

content = result["choices"][0]["message"]["content"]

content = content.replace("```json","").replace("```","")

careers = json.loads(content)

with open("careers.json","w") as f:
    json.dump(careers,f,indent=4)

print("✅ careers.json generated with multiple domains")