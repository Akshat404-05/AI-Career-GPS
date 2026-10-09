import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import requests
import networkx as nx

from streamlit_lottie import st_lottie

from utils.career_engine import (
    match_careers,
    explain_career,
    generate_roadmap,
    detect_skill_gap,
    analyze_career_demand,
    career_chat,
    job_market_analysis,
    predict_salary,
    analyze_user_profile,
    generate_interview_question,
    calculate_riasec_profile,
    global_career_demand,
)
TOTAL_QUESTIONS = 7

# ------------------------------------------------
# Page Setup
# ------------------------------------------------

st.set_page_config(
    page_title="AI Career GPS",
    page_icon="🚀",
    layout="wide"
)

# ------------------------------------------------
# Animation Loader
# ------------------------------------------------

def load_lottie(url):
    r = requests.get(url)
    return r.json()

lottie_ai = load_lottie(
    "https://assets5.lottiefiles.com/packages/lf20_kyu7xb1v.json"
)

# ------------------------------------------------
# Title Section
# ------------------------------------------------

st.title("🚀 AI Career GPS")

st_lottie(lottie_ai, height=200)

st.markdown("""
### Discover Your Ideal Career Path Using AI

This AI system analyzes:

✔ Your interests  
✔ Your personality  
✔ Your natural skills  
✔ Global career demand  

Then recommends the best careers for you.
""")

# ------------------------------------------------
# SESSION STATE INIT
# ------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""

if "answers" not in st.session_state:
    st.session_state.answers = []

if "current_question" not in st.session_state:
    st.session_state.current_question = generate_interview_question("")


# ------------------------------------------------
# ANSWER HANDLER FUNCTION
# ------------------------------------------------

def handle_answer():
    answer = st.session_state.user_answer_input

    if answer:
        st.session_state.answers.append(answer)

        st.session_state.chat_history += f"""
    Q: {st.session_state.current_question}
    A: {answer}
    """

        if len(st.session_state.answers) < TOTAL_QUESTIONS:
            st.session_state.current_question = generate_interview_question(
                st.session_state.chat_history
            )

        # clear input
        st.session_state.user_answer_input = ""


# ------------------------------------------------
# AI INTERVIEW UI
# ------------------------------------------------

st.header("🤖 AI Career Interview")

# Interview progress bar
st.progress(len(st.session_state.answers) / TOTAL_QUESTIONS)

st.write(st.session_state.current_question)

st.text_input(
    "Your answer",
    key="user_answer_input"
)

st.button(
    "Submit Answer",
    on_click=handle_answer
)

# ------------------------------------------------
# AFTER 7 QUESTIONS → ANALYZE PROFILE
# ------------------------------------------------

if len(st.session_state.answers) >= 7:

    combined_text = " ".join(st.session_state.answers)

    riasec_raw = calculate_riasec_profile(combined_text)

    # clean formatting
    riasec_raw = riasec_raw.replace("```json","").replace("```","").strip()

    try:
        riasec = json.loads(riasec_raw)

    except:
        # fallback default values
        riasec = {
            "Realistic": 50,
            "Investigative": 50,
            "Artistic": 50,
            "Social": 50,
            "Enterprising": 50,
            "Conventional": 50
        }

    with st.spinner("AI analyzing your profile..."):
        profile = analyze_user_profile(combined_text)

    profile = profile.replace("```json","").replace("```","").strip()

    try:
        profile = json.loads(profile)
    except:
        profile = {}

    skills = profile.get("skills", [])
    personality = profile.get("personality", [])
    subjects = profile.get("subjects", [])
    domains = profile.get("domains", [])

    # Combine everything into one feature list
    user_features = skills + personality + subjects + domains

    st.success("✨ AI Profile Generated!")

    st.balloons()

    # ------------------------------------------------
    # METRICS
    # ------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Detected Skills", len(skills))

    with col2:
        st.metric("Personality Traits", len(personality))

    # ------------------------------------------------
    # SKILLS DISPLAY
    # ------------------------------------------------

    st.subheader("🛠 Skills Detected")

    for s in skills:
        st.success(s)

    # ------------------------------------------------
    # PERSONALITY PIE
    # ------------------------------------------------

    st.subheader("🧠 Personality Distribution")

    personality_df = pd.DataFrame({"Trait": personality})

    fig = px.pie(personality_df, names="Trait")

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------
    # RADAR CHART
    # ------------------------------------------------

    if skills:

        st.subheader("🛠 Skill Radar Chart")

        values = [5] * len(skills)

        radar = go.Figure()

        radar.add_trace(go.Scatterpolar(
            r=values,
            theta=skills,
            fill='toself'
        ))

        radar.update_layout(
            polar=dict(radialaxis=dict(range=[0,5], visible=True)),
            showlegend=False
        )

        st.plotly_chart(radar, use_container_width=True)

    # ------------------------------------------------
    # CAREER MATCHING
    # ------------------------------------------------

    results = match_careers(skills + subjects + domains, personality)

    career_names = [c for c, s in results]
    scores = [s for c, s in results]

    st.header("📊 Career Intelligence Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Careers Analyzed", len(results))

    with col2:
        st.metric("Detected Skills", len(skills))

    with col3:
        st.metric("Personality Traits", len(personality))

    st.header("🧠 Career Personality Profile (RIASEC)")

    riasec_df = pd.DataFrame({
        "Type": list(riasec.keys()),
        "Score": list(riasec.values())
    })

    fig = px.bar(
        riasec_df,
        x="Type",
        y="Score",
        color="Score",
        color_continuous_scale="Turbo"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header("📈 Career Match Scores")

    df = pd.DataFrame({
        "Career": career_names,
        "Score": scores
    })

    fig = px.bar(
        df,
        x="Career",
        y="Score",
        color="Score",
        text="Score",
        color_continuous_scale="Turbo"
    )

    fig.update_layout(
        xaxis_title="Career Path",
        yaxis_title="Match Score"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------
    # CAREER DISTRIBUTION PIE
    # ------------------------------------------------
    
    category_counts = pd.DataFrame({
        "Career": career_names,
        "Score": scores
    })

    fig = px.pie(
        category_counts,
        names="Career",
        values="Score",
        title="Career Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------
    # CAREER SKILL NETWORK
    # ------------------------------------------------

    st.header("🌌 Career Skill Network")

    G = nx.Graph()

    for career, score in results:
        G.add_node(career)

        for skill in skills:
            G.add_node(skill)
            G.add_edge(skill, career)

    pos = nx.spring_layout(G, seed=42)

    # EDGE TRACE
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color="#888"),
        hoverinfo="none",
        mode="lines"
    )

    # NODE TRACE
    node_x = []
    node_y = []
    node_text = []

    for node in G.nodes():
        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        marker=dict(size=18, color="#00FFAA")
    )

    fig = go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="black"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------
    # CAREER CARDS
    # ------------------------------------------------
    st.header("🎯 Top Career Matches")

    # Clean up the RIASEC raw output display (Hide the JSON)
    primary_trait = max(riasec, key=riasec.get)
    st.info(f"💡 Based on your answers, your primary RIASEC trait is **{primary_trait}**.")

    for career, score in results:
        with st.expander(f"🚀 {career} (Match Score: {score}%)"):
            st.progress(score / 100)
            
            # The Magic Button: Only run heavy LLM calls when the user explicitly clicks
            if st.button(f"Generate Deep Dive Analysis for {career}", key=f"btn_{career}"):
                with st.spinner("Generating customized roadmap and market analysis..."):
                    
                    # Now we do the heavy lifting safely
                    colA, colB = st.columns(2)
                    
                    with colA:
                        st.markdown("### 🎯 Why this fits you")
                        st.write(explain_career(career, skills, personality))
                        
                        st.markdown("### 📈 Career Roadmap")
                        st.write(generate_roadmap(career))
                        
                        st.markdown("### 🧠 Skill Gap")
                        st.write(detect_skill_gap(career, skills))

                    with colB:
                        st.markdown("### 📊 Career Demand")
                        st.write(analyze_career_demand(career))
                        
                        st.markdown("### 💼 Job Market Analysis")
                        st.write(job_market_analysis(career))
                        
                        st.markdown("### 💰 Salary Prediction (India)")
                        st.write(predict_salary(career, skills))

# ------------------------------------------------
# DYNAMIC SIDEBAR COUNSELOR
# ------------------------------------------------
st.sidebar.title("💬 AI Career Counselor")
st.sidebar.markdown("Ask follow-up questions about any career!")

# Initialize chat history in session state
if "sidebar_messages" not in st.session_state:
    st.session_state.sidebar_messages = []

# Display chat messages from history on app rerun
for message in st.session_state.sidebar_messages:
    with st.sidebar.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.sidebar.chat_input("Ask about a specific degree, skill, or job..."):
    
    # Display user message in chat message container
    st.sidebar.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.sidebar_messages.append({"role": "user", "content": prompt})

    # Get AI response
    with st.sidebar.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = career_chat(st.session_state.sidebar_messages)
            st.markdown(response)
            
    # Add assistant response to chat history
    st.session_state.sidebar_messages.append({"role": "assistant", "content": response})