# Music Genre Classifier Expert System

A simple but powerful expert system that classifies music genres based on user-provided attributes. This project uses a **Prolog** knowledge base for its inference engine and a **Python Streamlit** application for an interactive web interface.



## Description

This application serves as a demonstration of a classic expert system. A user describes a song by providing characteristics such as its release year, tempo (BPM), vocal style, and instrumentation. This information is then asserted as temporary facts into a Prolog knowledge base. A set of predefined rules in the knowledge base evaluates these facts to infer the most likely music genre(s), complete with confidence scores and reasoning.

The core technologies used are:
* **Prolog (SWI-Prolog):** For the knowledge base and the rule-based inference engine.
* **Python:** As the backend server and for interfacing with Prolog.
* **pyswip:** A Python library that enables communication between Python and SWI-Prolog.
* **Streamlit:** To create a fast, interactive, and user-friendly web UI.

---

## Features

* **Interactive UI:** A clean web interface built with Streamlit for easy input of song attributes.
* **Rule-Based Logic:** Genre classification is handled by a declarative Prolog knowledge base, making the rules easy to read and modify.
* **Ranked Results:** Displays all matching genres, sorted by a confidence score.
* **Clear Reasoning:** Each recommendation comes with a simple explanation of why the rule was triggered.
* **Dynamic Knowledge Base:** User inputs are temporarily added to the Prolog database for each query and then retracted, ensuring a clean state for every classification.

---

## Installation & How to Run

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

You must install SWI-Prolog and Python 3 on your system first.

* **SWI-Prolog:** This is the engine that runs the `.pl` knowledge base.
    * [Download SWI-Prolog here](https://www.swi-prolog.org/download/stable).
    * **Important:** During installation, make sure you check the option to add `swipl` to your system's PATH. This allows `pyswip` to find and communicate with it.

* **Python:** This project requires Python 3.8 or newer.
    * [Download Python here](https://www.python.org/downloads/).

### 2. Project Setup

**Clone the repository:**
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

**Create a Python virtual environment (recommended):**
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

The required Python packages are listed in `requirements.txt`.

**Create a file named `requirements.txt`** in the root of your project and add the following lines:
```
streamlit
pyswip
```

**Now, install these packages using pip:**
```bash
pip install -r requirements.txt
```

### 4. Run the Application

Once the setup is complete, you can run the Streamlit app with a single command:
```bash
streamlit run app.py
```
Your web browser should automatically open a new tab with the running application. If not, the terminal will provide a local URL (usually `http://localhost:8501`) that you can visit.

---

## File Structure

```
.
├── app.py              # The main Python file containing the Streamlit UI and backend logic.
├── music_kb.pl         # The Prolog knowledge base with facts and classification rules.
├── requirements.txt    # A list of required Python packages for pip.
└── README.md          
```