from typing import TypedDict
from langgraph.graph import StateGraph
import time
from datetime import datetime

# =========================================================
# STATE DEFINITION
# =========================================================

class AgentState(TypedDict):

    transcript: str

    cleaned_transcript: str

    retrieved_policies: list

    violations: list

    sentiment: str

    score: int

    report: dict

    llm_used: str

    fallback_triggered: bool

    fallback_reason: str

    llm_logs: list

    execution_trace: list


# =========================================================
# TRACE HELPER
# =========================================================

def create_trace_entry(
    node_name,
    status,
    start_time
):

    return {

        "node": node_name,

        "status": status,

        "timestamp":
            datetime.now().strftime("%H:%M:%S"),

        "duration":
            round(time.time() - start_time, 4)
    }


# =========================================================
# NODE 1
# =========================================================

def transcribe_and_clean(state):

    start_time = time.time()

    cleaned = state["transcript"].strip()

    trace = state.get(
        "execution_trace",
        []
    )

    trace.append(

        create_trace_entry(
            "transcribe_and_clean",
            "success",
            start_time
        )
    )

    return {

        "cleaned_transcript": cleaned,

        "execution_trace": trace
    }


# =========================================================
# NODE 2
# =========================================================

def retrieve_policies(state):

    start_time = time.time()

    from app.rag.vector_store import PolicyVectorStore

    store = PolicyVectorStore()

    policies = store.search(
        state["cleaned_transcript"]
    )

    trace = state.get(
        "execution_trace",
        []
    )

    trace.append(

        create_trace_entry(
            "retrieve_policies",
            "success",
            start_time
        )
    )

    return {

        "retrieved_policies": policies,

        "execution_trace": trace
    }


# =========================================================
# NODE 3
# =========================================================

def analyze_signals(state):

    start_time = time.time()

    from app.utils.helpers import (
        analyze_sentiment,
        detect_policy_violations
    )

    sentiment = analyze_sentiment(
        state["cleaned_transcript"]
    )

    violations = detect_policy_violations(
        state["cleaned_transcript"],
        state["retrieved_policies"]
    )

    trace = state.get(
        "execution_trace",
        []
    )

    trace.append(

        create_trace_entry(
            "analyze_signals",
            "success",
            start_time
        )
    )

    return {

        "sentiment": sentiment,

        "violations": violations,

        "execution_trace": trace
    }


# =========================================================
# NODE 4
# =========================================================

def score_call(state):

    start_time = time.time()

    score = 100

    score -= len(
        state["violations"]
    ) * 30

    if score < 0:
        score = 0

    trace = state.get(
        "execution_trace",
        []
    )

    trace.append(

        create_trace_entry(
            "score_call",
            "success",
            start_time
        )
    )

    return {

        "score": score,

        "execution_trace": trace
    }


# =========================================================
# NODE 5
# =========================================================

def generate_report(state):

    start_time = time.time()

    from app.llms.orchestrator import LLMOrchestrator

    orchestrator = LLMOrchestrator()

    trace = state.get(
        "execution_trace",
        []
    )

    # =====================================================
    # CLEAN VIOLATIONS
    # =====================================================

    violations_text = (

        ", ".join(
            state["violations"]
        )

        if len(state["violations"]) > 0

        else "No policy violations detected."
    )

    # =====================================================
    # PROMPT
    # =====================================================

    prompt = f"""
You are a QA evaluation assistant.

Analyze this customer support transcript.

Transcript:
{state['cleaned_transcript']}

Detected Policy Violations:
{violations_text}

Retrieved Policies:
{state['retrieved_policies']}

IMPORTANT:
Only discuss the policy violations already detected.
Do NOT invent new violations.
Do NOT mention policies that were not violated.

Generate:
1. Short QA reasoning
2. Customer sentiment
3. Overall QA quality summary

Keep the response concise and professional.
"""

    # =====================================================
    # LLM ANALYSIS
    # =====================================================

    llm_result = orchestrator.analyze(
        prompt
    )

    # =====================================================
    # ADD RETRY TRACES
    # =====================================================

    for log in llm_result["logs"]:

        if log["status"] == "retry":

            trace.append({

                "node":
                    f"{log['model']} retry",

                "status":
                    "retry",

                "timestamp":
                    log["timestamp"],

                "duration":
                    0
            })

    # =====================================================
    # ADD FINAL NODE TRACE
    # =====================================================

    trace.append(

        create_trace_entry(
            "generate_report",
            "success",
            start_time
        )
    )

    # =====================================================
    # FINAL REPORT
    # =====================================================

    report = {

        "call_id": "C001",

        "llm_used":
            llm_result["llm_used"],

        "fallback_triggered":
            llm_result["fallback_triggered"],

        "fallback_reason":
            llm_result["fallback_reason"],

        "policy_violations":
            state["violations"],

        "policies_retrieved":
            state["retrieved_policies"],

        "sentiment": {

            "customer":
                "Derived from LLM analysis",

            "agent":
                "neutral"
        },

        "qa_score":
            state["score"],

        "score_reasoning":
            llm_result["response"],

        "flag_for_review":
            state["score"] <= 70,

        "llm_logs":
            llm_result["logs"],

        "execution_trace":
            trace
    }

    return {

        "report": report,

        "llm_used":
            llm_result["llm_used"],

        "fallback_triggered":
            llm_result["fallback_triggered"],

        "fallback_reason":
            llm_result["fallback_reason"],

        "llm_logs":
            llm_result["logs"],

        "execution_trace":
            trace
    }


# =========================================================
# BUILD GRAPH
# =========================================================

graph = StateGraph(AgentState)

# =========================================================
# ADD NODES
# =========================================================

graph.add_node(
    "transcribe_and_clean",
    transcribe_and_clean
)

graph.add_node(
    "retrieve_policies",
    retrieve_policies
)

graph.add_node(
    "analyze_signals",
    analyze_signals
)

graph.add_node(
    "score_call",
    score_call
)

graph.add_node(
    "generate_report",
    generate_report
)

# =========================================================
# ENTRY POINT
# =========================================================

graph.set_entry_point(
    "transcribe_and_clean"
)

# =========================================================
# EDGES
# =========================================================

graph.add_edge(
    "transcribe_and_clean",
    "retrieve_policies"
)

graph.add_edge(
    "retrieve_policies",
    "analyze_signals"
)

graph.add_edge(
    "analyze_signals",
    "score_call"
)

graph.add_edge(
    "score_call",
    "generate_report"
)

# =========================================================
# COMPILE
# =========================================================

workflow = graph.compile()