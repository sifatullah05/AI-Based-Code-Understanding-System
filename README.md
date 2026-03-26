## GitHub Source Code Analyzer
An AI-powered tool that analyzes GitHub repositories and answers questions about Python code using natural language.

## Table of Contents
Overview
Tech Stack
Prerequisites
Installation
Project Structure
Usage
API Endpoints
How It Works
Troubleshooting
License

## Overview

GitHub Source Code Analyzer is a RAG (Retrieval-Augmented Generation) based system that:

🔗 Clones GitHub repositories and extracts Python code
✂️ Splits code into manageable chunks
🧠 Converts code into embeddings and stores in a vector database
🔍 Retrieves relevant code context based on user queries
💬 Generates human-like answers using an AI model

## Tech Stack
## Backend
Technology	Purpose
FastAPI	REST API Framework
LangChain	RAG Pipeline Builder
ChromaDB	Vector Database
Groq	LLM (model="openai/gpt-oss-20b")
HuggingFace	Code Embeddings Model

## Frontend
Technology	Purpose
React.js	UI Framework
TailwindCSS	Styling
Axios	HTTP Client
React Toastify	Notifications

## Prerequisites
Make sure you have installed:

Python 3.10+
Node.js 16+
Git
Groq API Key

## Installation
1️⃣ Clone the Repository
git clone [https://github.com/your-username/code-analyzer.git](https://github.com/sifatullah05/AI-Based-Code-Understanding-System)

cd code-analyzer
2️⃣ Fastapi Setup
pip install -r requirements.txt

Create a .env file:

GROQ_API_KEY=your_api_key_here

Run the backend:

uvicorn app:app --reload
3️⃣ Frontend Setup
cd frontend
npm install
npm run dev

## Usage
1. Open the frontend in your browser
2. Enter a GitHub repository URL
3. Ask questions about the code
4. Get AI-generated answers instantly

## How It Works
1. Repository is cloned from GitHub
2. Python files are extracted and split into chunks
3. Embeddings are generated using HuggingFace model
4. Stored in ChromaDB vector database
5. Relevant chunks retrieved using similarity search
6. Answer generated using Groq LLM

## Troubleshooting
❌ Common Issues
## Module not found
→ Run pip install -r requirements.txt
## Frontend not starting
→ Run npm install again
## API key error
→ Check your .env file

## License
This project is licensed under the MIT License.

## Acknowledgments
LangChain for RAG framework
Groq for LLM API
HuggingFace for embeddings
Meta for test repository
