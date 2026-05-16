# Multi LLM Call QA Agent

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

<img src="https://github.com/user-attachments/assets/c72850d8-3d92-4c45-84de-49fd5dbad4fb"
     alt="System Architecture"
     width="500"/>


---

# LangGraph Workflow



<img src="https://github.com/user-attachments/assets/3cb0d317-f197-40bf-92af-2f2945941e21"
     alt="LangGraph Workflow"
     width="500"/>

# Multi LLM Fallback Flow


<img src="https://github.com/user-attachments/assets/9531c126-d8ff-4391-9390-9daeb3cafbe8"
     alt="LLM Fallback Flow"
     width="500"/>

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

Interface for Uploading the transcript

<img width="1782" height="933" alt="SS-1" src="https://github.com/user-attachments/assets/ac6c6ef0-715c-4443-ac40-2aedcfc262de" />


Image of LangGraph Executive trace
<img width="1831" height="962" alt="SS-2" src="https://github.com/user-attachments/assets/055a09dd-e60a-45c8-b828-13f972823558" />

Final JSON Report output

<img width="1816" height="843" alt="SS-3" src="https://github.com/user-attachments/assets/90a7d8ab-f320-468d-b5ca-d70ef5129759" />

---

# Author

Sk Tausif Rahman,
Data Scientist

---

# License

MIT License
