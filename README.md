# AI Career GPS 🚀

An AI-powered career guidance platform designed to help users explore career opportunities, understand their skill gaps, and plan their professional development.

## Overview

AI Career GPS aims to make career planning more personalized by combining user profile analysis, career matching, and AI-generated guidance.

## Features

- **Career recommendations:** Discover careers based on your skills and profile.
- **Skill gap analysis:** Identify skills to develop for your target career.
- **Personalized roadmaps:** Generate structured learning and career plans.
- **AI career assistant:** Ask questions about careers, skills, and job roles.
- **Career insights:** Explore career demand and salary-related information where supported by the application.
- **Interview preparation:** Generate practice interview questions.
- **Personality assessment:** Explore career preferences using the RIASEC framework.

*Note: Features listed above should be retained only if they are implemented in the current version of the project.*

## Tech Stack

- Python
- Streamlit
- AI model API integration
- JSON-based career data

## Project Structure


AI-Career-GPS/
├── app.py
├── careers.json
├── generate_careers.py
├── requirements.txt
└── utils/
    └── career_engine.py

## Getting Started

### 1. Clone the repository

git clone https://github.com/Akshat404-05/AI-Career-GPS.git
cd AI-Career-GPS


### 2. Create a virtual environment


python -m venv venv


Activate it on Windows:


.\venv\Scripts\Activate.ps1


### 3. Install dependencies


pip install -r requirements.txt


### 4. Configure your API key

Create a local `.env` file and configure the environment variables required by the application. Never commit API keys or credentials to GitHub.

### 5. Run the application


streamlit run app.py

## Security

Keep API keys, credentials, and other secrets out of source control. Use environment variables or a local `.env` file excluded by `.gitignore`.

## Future Improvements

- Improve career recommendation accuracy.
- Expand career and skills datasets.
- Enhance the user interface and visualizations.
- Add more career planning and interview preparation resources.

## Author

**Akshat Gupta**

GitHub: [@Akshat404-05](https://github.com/Akshat404-05)
