<p align="center">
  <img src="assets/logo.png" alt="FinanceAI Logo" width="180">
</p>


<h1 align="center">
  FinanceAI
  <span style="font-size: 0.6em; font-weight: normal;">
     — AI-Powered Financial Analysis Platform
  </span>
</h1>

## DEMO


## CONTENTS

1. [About This Project](#about-this-project)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Architecture](#architecture)
6. [How It Works](#how-it-works)
7. [Local Installation (without Docker)](#local-installation-without-docker)
8. [Quick Installation with Docker](#quick-installation-with-docker)
9. [Usage](#usage)
10. [User Interface](#user-interface)
11. [Known Limitations](#known-limitations)
12. [Future Improvements](#future-improvements)
13. [Author](#author)

## ABOUT THIS PROJECT
This project began entirely for my own personal interests,
and as it progressed, I kept adding new features with growing enthusiasm until
it finally reached a point where I could present it here. 

Ever since I can remember, I’ve been a bit of a tightwad, 
and as I was thinking, ***“I wish my banking app had a tab that did some
kind of analysis so I could track my spending from there.”***, then it
suddenly occurred to me that I study computer engineering.

I really enjoyed working on this project. Since I started it to meet my own needs,
I believe I designed its features entirely from the user’s perspective,
and I still enjoy using it today.

## FEATURES

- 📈 View the trend of your annual expenses in a single chart.
- 📊 See where you spend the most money based on the automatic categorizations created for you.
- 🎯 Compare your monthly expenses with those of the previous month and see how you're doing.
- 🖥️ Let the app track your spending at unfamiliar locations and predict it for you.
- 🤖 You can consult the Finance Assistant chatbot —customized with your data— on any topic, and request any kind of analysis.


## TECH STACK

| Category              | Technologies       |
|-----------------------|--------------------|
| 🐍 Language           | Python             |
| 🧠 AI                 | Google Gemini API  |
| 🤖 Machine Learning   | scikit-learn       |
| 🎨 UI                 | Streamlit          |
| 📊 Data Processing    | Pandas             |
| 📈 Data Visualization | Plotly             |
| 📦 Database           | SQLite, SQLAlchemy |
| 🔧 Version Control    | Git                |
| 🐋 Containerization   | Docker             |


## PROJECT STRUCTURE

```text
src/
├── application/      # Business logic and application services
├── config/           # Application configuration
├── data/             # Source datasets
├── domain/           # Entities and interfaces
├── infrastructure/
│   ├── data/         # Data ingestion pipeline
│   ├── database/     # SQLite & SQLAlchemy
│   ├── llm/          # Gemini client
│   ├── ml/           # ML classifier
│   └── nlp/          # Text vectorization
└── presentation/
    ├── components/   # Reusable Streamlit components
    └── views/        # Application pages              
```

## ARCHITECTURE

### Clean Architecture

```mermaid
flowchart TD

U[User]

P[Presentation Layer]

A[Application Layer]

D[Domain Layer]

I[Infrastructure Layer]

DB[(SQLite)]

AI[Gemini API]

ML[ML Classifier]

U --> P
P --> A
A --> D
D --> I

I --> DB
I --> AI
I --> ML

```

### AI Assistant Flow

This diagram illustrates the end-to-end workflow of the AI Assistant. When a user submits a question, the request is processed by the application layer, which retrieves the necessary financial data from the database according to the function call collected from Gemini API. When Gemini API creates the final response after making the call, the generated response is returned to the Streamlit interface and presented to the user.

```mermaid
flowchart TD

U[User] --> UI[AI Assistant]
    UI --> AI[AI Service]

    AI --> LLM[Gemini API]

    LLM -->|Function Call| F{Select Function}

    F --> FS[Financial Service]

    FS --> TS[Transaction Service]
    TS --> R[Transaction Repository]
    R --> DB[(SQLite Database)]

    DB --> R
    R --> TS
    TS --> FS
    FS --> F

    FS -->|Function Result| LLM

    LLM -->|Final Response| AI
    AI --> UI
    UI --> U
```

## HOW IT WORKS

### Data Pipeline
ml ve database de burda

### AI Assistant Flow

### Transaction Categorization / ML Pipeline

### State Management & Dynamic UI
session_state şeyleri. dosya yokken napıyorum, gemini api key nasıl istiyorum...

## LOCAL INSTALLATION (WITHOUT DOCKER)
### Prerequisites
- Python 3.9 or higher
- Git

### Step 1: Clone the Repository
Open your terminal and run the following commands to clone the project and navigate into the directory:
```bash
git clone https://github.com/iremnaz-d/FinanceAI.git
```
```bash
cd FinanceAI
```

### Step 2: Create and activate a virtual environment (Recommended)
It is highly recommended to use a virtual environment to avoid conflicts with other packages.

#### For Windows
```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

#### For macOS/Linux
```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
Install the required Python packages using ``pip``:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
Start the Streamlit server by running the main application file:

```bash
streamlit run src/presentation/run_app.py
```




## QUICK INSTALLATION WITH DOCKER

You can use Docker to run the project on your local machine in an isolated
environment without dealing with any Python dependencies.

### Step 1: Clone the Project
```bash
git clone https://github.com/iremnaz-d/FinanceAI.git
```
```bash
cd FinanceAI
```

### Step 2: Build The Docker Image

Build the application's Docker image by running the following command in the project's 
root directory(where the Dockerfile is located). 
(This process may take 1-2 minutes depending on your computer's speed)
```bash
docker build -t finance_ai .
```

### Step 3: Run App

Use the following command to start the application.

Important Note: When the application runs, the database will be automatically created
under the `src` folder. The `-v` (volume) parameter in the command below ensures that
the database inside Docker is synchronized with your local machine. 
This way, your data will not be lost even if you stop Docker.

#### For Mac/Linux/Git Bash
```bash
docker run -p 8501:8501 -v "$(pwd)/src:/app/src" finance_ai
```

#### For Windows PowerShell
```PowerShell
docker run -p 8501:8501 -v "${PWD}/src:/app/src" finance_ai
```

#### For Windows CMD
```DOS
docker run -p 8501:8501 -v "%cd%/src:/app/src" finance_ai
```

### Step 4: Access to UI

Once the container is running successfully, 
open your web browser and go to the following address:
```text
http://localhost:8501
```

## USAGE

After installing and launching the application as described in the [Installation](#local-installation-without-docker) section, 
the user interface will guide you through the process so you'll know exactly what to do.

But if you'd still like some suggestions:

### Load & Prepare Your Data (Optional)
The app will open with a **sample dataset already loaded** (I’m sharing all the transactions I’ve made with my Ziraat 
card with you; whoever is reading this, I trust you’re a good person—please don’t let me down).

If you want to upload your own data (I think only data from Ziraat will work),
make sure the file is in ``.xlsx`` format and **doesn’t contain any formatting**, such as images.
You can upload your file from the ``📁 Data Management`` tab.

### Explore the Analysis
- From the ``🏠 Homepage`` tab, you can **select a month** and view that month's summary:

    + A graphical and percentage-based **comparison of last month** and the month you selected
  
    + **Top 5 expenses** of that month
  
    + You can **view the AI's predictions** for uncategorized expenses for that month:
        * You can **correct predictions** you think are wrong with the correct answers—my ``ML model``
          will be retrained based on your feedback!
        * If you'd like, you can **add a new category** or **delete an existing one**.
      

- In the ``📊 Chart Analysis`` tab, you can see the ups and downs of your annual spending and how much you’ve spent 
in each category; if you’d like, you can have my ML model **predict** the *“Other”* category.


- On the ``💳 My Transactions`` tab, you can view all your transactions, filter them by month and category, 
and delete a transaction if you wish.

### Ask Questions

You can go to the ``🤖 AI Assistant`` tab and ask any questions you like. Here are a few questions you can ask:
- Where have I been drinking coffee the most over the past 6 months?


- Final exams ended toward the end of June—can you tell from my spending?


- What do you think were my excessive expenses this past March?


- Why are you so funny? The developer must be a really nice person.


- Could you compare my spending this April with my spending before April? I kind of lost track of things back then...

❗ Since you'll be running the project externally, the system will ask you for your own Gemini API key.
If you don't have one, don't worry—you'll be redirected to a website where you can get one for free!


## USER INTERFACE

### 🏠 Homepage

![FinanceAI Demo](assets/homepage_gif.gif)

### 💳 My Transactions

### 📊 Chart Analysis

### 🤖 AI Assistant

### 📁 Data Management


## KNOWN LIMITATIONS

- **File Type**: Only accepts ``.xlsx`` files as datasets. I didn’t expand this restriction because
I would need a different dataset to do so. Additionally, due to limitations in the `pandas` library, 
the file must not contain any formatting (e.g., images) —it should consist solely of text.


- **Same IDs**: Only when sending money to another person, the data that appears in the bank account is in 
sets of two or three entries (one for the amount sent, the others for the amounts withdrawn to send the money),
all under the same IDs. I had trouble importing all of these account transactions with the same IDs into the
database. Fortunately, this issue doesn’t cause major problems during data analysis.


## FUTURE IMPROVEMENTS
login 
search bar for my transactions descriptions

## AUTHOR

**İrem Naz Durgut**


Computer Engineering Student @ Dokuz Eylül University

- **e-mail**: iremnazdurgut4@gmail.com
- [GitHub](https://github.com/iremnaz-d)
- [LinkedIn](https://www.linkedin.com/in/iremnazdurgut)


