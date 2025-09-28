from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from dotenv import load_dotenv
import speech_recognition as sr

# --------------------------
# Load environment variables
# --------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="AI Health Assistant", page_icon="💊")
st.title("AI Health Assistant 🏥")

# --------------------------
# Initialize Gemini model
# --------------------------
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7
)

# --------------------------
# Voice input function
# --------------------------
# def get_voice_input():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Listening... Please speak now.")
#         audio = r.listen(source, timeout=5)
#         try:
#             text = r.recognize_google(audio)
#             return text
#         except:
#             st.error("Could not recognize voice")
#             return ""

# --------------------------
# Session state for history
# --------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------
# Symptom input
# # --------------------------
# voice_input_btn = st.button("Use Voice Input")
# if voice_input_btn:
#     symptom = get_voice_input()
# else:
symptom = st.text_input("Enter your symptoms:")

# --------------------------
# Load doctors CSV
# --------------------------
doctors_df = pd.read_csv("doctors.csv")

# --------------------------
# Expanded CSV specialties + keyword mapping
# --------------------------
csv_specialties = [
    "Cardiologist", "Neurologist", "Dermatologist", "Pediatrician",
    "General Physician", "Orthopedic", "ENT Specialist", 
    "Gastroenterologist", "Psychiatrist", "Ophthalmologist",
    "Preventive Medicine", "Nutritionist", "Physiotherapist", "Family Physician"
]

keyword_map = {
    "heart": "Cardiologist",
    "brain": "Neurologist",
    "skin": "Dermatologist",
    "child": "Pediatrician",
    "general": "General Physician",
    "bone": "Orthopedic",
    "ear nose throat": "ENT Specialist",
    "stomach": "Gastroenterologist",
    "mental": "Psychiatrist",
    "eye": "Ophthalmologist",
    "preventive": "Preventive Medicine",
    "nutrition": "Nutritionist",
    "physio": "Physiotherapist",
    "family": "Family Physician"
}

# --------------------------
# Generate AI analysis
# --------------------------
if st.button("Get Doctors") and symptom:
    prompt = f"""
You are a medical assistant. Based on the symptoms provided, do the following:

SYMPTOMS:
{symptom}

TASKS:
1. Suggest relevant doctor specialties for these symptoms.
2. Recommend preventive or safety measures the user can take (e.g., lifestyle, diet, exercises, routine check-ups).
3. Give practical advice on maintaining general health.
4. Keep all advice simple and beginner-friendly.

IMPORTANT:
- Do NOT provide any medical prescriptions or diagnosis.
- Focus only on specialties and guidance.
- If the user shows signs of common health risks, suggest preventive measures.
"""
    with st.spinner("Analyzing symptoms..."):
        result = model.invoke(prompt)
        response_text = result.content
        st.session_state.history.append(response_text)

    # --------------------------
    # Extract specialties from AI output
    # --------------------------
    mapped_specialties = []

    # Exact match with CSV specialties
    for s in csv_specialties:
        if s.lower() in response_text.lower():
            mapped_specialties.append(s)

    # Keyword mapping for variations
    for keyword, specialty in keyword_map.items():
        if keyword.lower() in response_text.lower():
            mapped_specialties.append(specialty)

    mapped_specialties = list(set(mapped_specialties))  # remove duplicates

    st.subheader("Suggested Doctor Specialties:")
    st.write(", ".join(mapped_specialties) if mapped_specialties else "No specialties found")

    # --------------------------
    # Filter doctors
    # --------------------------
    if mapped_specialties:
        filtered_doctors = doctors_df[doctors_df["Specialty"].isin(mapped_specialties)]
    else:
        filtered_doctors = pd.DataFrame()  # empty if no match

    st.subheader("Nearby Doctors:")
    if not filtered_doctors.empty:
        st.dataframe(
         filtered_doctors[["Name", "Specialty", "Distance"]],
         hide_index=True
        )
    else:
        st.info("No doctors found for these specialties.")

    # --------------------------
    # Map view
    # --------------------------
    if not filtered_doctors.empty:
        st.subheader("Map View")
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=filtered_doctors["lat"].mean(),
                longitude=filtered_doctors["lng"].mean(),
                zoom=12
            ),
            layers=[
                # OSM Tile Layer
                pdk.Layer(
                    "TileLayer",
                    data=None,
                    get_tile_data=None,
                    min_zoom=0,
                    max_zoom=19,
                    tile_size=256,
                    url="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
                ),
                # Doctors Scatterplot
                pdk.Layer(
                    "ScatterplotLayer",
                    data=filtered_doctors,
                    get_position='[lng, lat]',
                    get_fill_color='[255,0,0,160]',
                    get_radius=200,
                    pickable=True
                )
            ]
        ))

    # --------------------------
    # Chat history / AI advice
    # --------------------------
    st.subheader("AI Advice / Preventive Measures 📝")
    st.text_area("Advice", value=response_text, height=350)

    st.subheader("Chat History 🗂️")
    for i, res in enumerate(st.session_state.history, 1):
        with st.expander(f"Analysis {i}"):
            st.write(res)

