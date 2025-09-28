# 🏥 AI Health Assistant

An AI-powered health assistant built with **Streamlit** and **Google Gemini API (via LangChain)**.
It helps users by analyzing their symptoms (via text or voice input), suggesting possible doctor specialties, prevention tips, and showing nearby doctors on an interactive map.

---

## 🚀 Features

* 🗣️ **Symptom Input** via text or voice
* 🤖 **AI Suggestions** using Gemini (LangChain wrapper)
* 🩺 Suggests **relevant doctor specialties**
* 🛡️ Provides **basic prevention & safety tips**
* 📍 Shows **nearby doctors on an interactive map** (from dataset / location-based)
* 💾 Uses a **CSV dataset of doctors in Pakistan** (expandable for other regions)

---

## 📂 Project Structure

```
ai-health-assistant/
│── app.py              # Main Streamlit app
│── doctors.csv     # Doctors dataset
│── requirements.txt    # Python dependencies
│── .env                # API keys (not pushed to GitHub)
```

---

## ⚙️ Installation & Setup

1. **Clone the repo**

```bash
git clone https://github.com/YOUR-USERNAME/ai-health-assistant.git
cd ai-health-assistant
```

2. **Create virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Add API key**
   Create a `.env` file in the root folder and add:

```
GEMINI_API_KEY=your_google_gemini_api_key
```

5. **Run the app**

```bash
streamlit run app.py
```

---

## 🌍 Deployment (Streamlit Cloud)

1. Push repo to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) → New App.
3. Connect your GitHub repo and select `app.py` as entry point.
4. Add API key in **Secrets**:

```toml
GEMINI_API_KEY="your_actual_api_key"
```

5. Get a live link like:

```
https://your-app-name.streamlit.app
```

---

## 📊 Example Doctor Dataset (`data/doctors.csv`)

```csv
name,specialty,lat,lng,city
Dr. Ayesha Khan,Cardiologist,24.8607,67.0011,Karachi
Dr. Bilal Ahmed,Neurologist,33.6844,73.0479,Islamabad
Dr. Sana Malik,Dermatologist,31.5204,74.3587,Lahore
Dr. Kamran Ali,Pediatrician,34.0151,71.5249,Peshawar
Dr. Fatima Zahra,General Physician,30.1575,71.5249,Multan
```

---

## 🛡️ Disclaimer

This project is for **educational and informational purposes only**.
It does **NOT replace medical advice**. Always consult a licensed doctor for medical concerns.

---
