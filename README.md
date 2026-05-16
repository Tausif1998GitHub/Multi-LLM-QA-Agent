# 📞 Multi LLM Call QA Agent

An AI powered customer support Quality Assurance system built using LangGraph, Groq hosted LLMs, FAISS based Retrieval Augmented Generation, and Streamlit.

The application analyzes customer support call transcripts, retrieves relevant company policies, detects policy violations, scores agent performance, and generates explainable QA reports with dynamic execution tracing and multi LLM fallback orchestration.

---

# Features

* Multi LLM fallback orchestration
* LangGraph workflow execution
* FAISS powered policy retrieval
* Semantic policy search using Sentence Transformers
* Dynamic execution tracing with timestamps
* Retry and fallback observability
* Structured QA scoring
* Customer sentiment analysis
* Streamlit based interactive UI
* Runtime metrics and execution logs

---

# Tech Stack

| Layer                  | Technologies          |
| ---------------------- | --------------------- |
| Frontend               | Streamlit             |
| Workflow Orchestration | LangGraph             |
| LLM Providers          | Groq                  |
| Embeddings             | Sentence Transformers |
| Vector Database        | FAISS                 |
| Language               | Python                |
| Environment Management | dotenv                |

---

# System Architecture

> Add the System Architecture image here

```md
<img width="1738" height="2300" alt="System Architecture Multiagent jpg" src="https://github.com/user-attachments/assets/dc92a7c7-9839-473d-b011-4caa8db80dbe" />

```

---

# LangGraph Workflow

> Add the LangGraph Workflow image here

```md
<img width="1384" height="2889" alt="Lang-Graph  workflow jpg" src="https://github.com/user-attachments/assets/c859e5de-b83c-47da-a462-a990cfb9ea0b" />

```

---

# Multi LLM Fallback Flow

> Add the LLM Fallback Flow image here

```md
<img width="1686" height="2372" alt="LLM Fallback flow jpg" src="https://github.com/user-attachments/assets/69434122-a0ea-4ffc-9555-4692cc97ef16" />

```

---

# Project Workflow

The application follows a multi stage AI workflow:

1. User submits a customer support transcript through Streamlit UI

2. LangGraph orchestrates the workflow execution

3. Transcript is cleaned and normalized

4. Relevant policies are retrieved using FAISS similarity search

5. Policy violations and sentiment signals are analyzed

6. QA score is calculated

7. Multi LLM orchestrator generates reasoning and report

8. Dynamic execution traces and logs are displayed

9. Final structured QA report is generated

---

# Multi LLM Routing

The system uses a resilient fallback strategy for LLM inference.

| Priority   | Model                   |
| ---------- | ----------------------- |
| Primary    | llama 3.3 70b versatile |
| Fallback 1 | qwen3 32b               |
| Fallback 2 | gpt oss 20b             |

If one model fails or times out, the system automatically routes inference to the next available model.

---

# Dynamic Execution Trace

The system provides runtime observability including:

* Node level execution trace
* Timestamps
* Execution duration
* Retry visibility
* Fallback tracking
* LLM execution logs

Example:

```text
✅ retrieve_policies
Timestamp: 20:46:31
Duration: 0.18 sec

🔄 llama-3.3-70b retry
Timestamp: 20:46:33

✅ generate_report
Timestamp: 20:46:35
Duration: 2.7 sec
```

---

# Folder Structure

```text
multi-llm-qa-agent/
│
├── app/
│   ├── graph/
│   ├── llms/
│   ├── rag/
│   └── utils/
│
├── policies/
│
├── transcripts/
│
├── ui/
│
├── tests/
│
├── .env
├── requirements.txt
├── main.py
└── README.md
```

---

# Installation

## 1. Clone Repository

```bash
git clone <your-repository-url>
cd multi-llm-qa-agent
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Running the Application

Start Streamlit:

```bash
streamlit run ui/streamlit_app.py
```

---

# Sample Output

The application generates:

* QA score
* Policy violations
* Retrieved policies
* LLM reasoning
* Runtime metrics
* Execution traces
* Retry logs
* Review recommendation

---

# Example Use Cases

* Customer support QA automation
* Telecom call analysis
* Contact center compliance monitoring
* AI workflow orchestration demos
* Multi LLM reliability experiments
* Explainable AI systems

---

# Future Improvements

* Real time speech to text integration
* Audio call ingestion
* Redis caching
* Docker deployment
* Human feedback loop
* Analytics dashboard
* Role based access
* Persistent vector database
* Kubernetes deployment

---

# Screenshots

> Add application screenshots here

```md
<img width="1782" height="933" alt="SS-1" src="https://github.com/user-attachments/assets/10af0429-b2f6-47ae-adc6-c16eb947daaf" />

<img width="1831" height="962" alt="SS-2" src="https://github.com/user-attachments/assets/0664867f-d678-467a-b53e-88819697cb72" />

<img width="1816" height="843" alt="SS-3" src="https://github.com/user-attachments/assets/3358c9f9-65a1-4873-ba5c-11dab4aaf434" />

```

---

# Author

Sk Tausif Rahman,
Data Scientist

---

# License

MIT License
