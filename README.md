# 📧 Cold Email Generator

A powerful cold email automation tool built using **Groq**, **LangChain**, and **Streamlit**.

This tool allows users to enter a company’s **careers page URL**, automatically extract job listings, analyze job descriptions, and generate **highly personalized cold emails**.  
It also retrieves relevant portfolio links from a **vector database**, ensuring every outreach message is contextual and effective.

---

## 🚀 Example Scenario

- **TCS** is hiring for a *Principal Software Engineer*, investing significant time and effort into recruitment, onboarding, and training.  
- **Nike**, a software development company, can provide a dedicated engineer to support Nike.  
- **Rahul**, the business development executive at TCS, uses this tool to instantly generate a personalized cold email and reach out efficiently.

---

## 📸 Screenshot

<img width="1920" height="820" alt="Screenshot (841)" src="https://github.com/user-attachments/assets/a94ccea7-29d1-4c18-bc48-5642f608165c" />

---

## 🔑 Setup Instructions

### 1️⃣ Get Your Groq API Key  
Generate an API key here:  
**https://console.groq.com/keys**

Update the value of `GROQ_API_KEY` inside `app/.env`.

---

## ⚙️ Installation & Running the App

### **1. Create a virtual environment**
```bash
python -m venv venv
````

### **2. Activate the virtual environment**

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### **3. Install uv**

```bash
pip install uv
```

### **4. Sync dependencies**

```bash
uv sync
```

### **5. Run the Streamlit app**

```bash
streamlit run app/main.py
```


