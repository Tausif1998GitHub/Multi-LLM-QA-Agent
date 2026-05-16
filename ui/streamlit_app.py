import sys
import os
import time

# =========================================================
# FIX PYTHON PATH
# =========================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st

from app.graph.workflow import workflow

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="LLM Call QA Agent",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("Multi-LLM Call QA Agent")

st.markdown(
    """
AI-powered customer support QA system using:

- LangGraph Workflow Orchestration
- Multi-LLM Fallback Routing
- FAISS Vector Retrieval
- Structured QA Scoring
"""
)

st.divider()

# =========================================================
# SAMPLE TRANSCRIPT BUTTONS
# =========================================================

col1, col2 = st.columns(2)

with col1:

    if st.button("Load Bad Call"):

        with open(
            "transcripts/bad_call.txt",
            "r",
            encoding="utf-8"
        ) as f:

            st.session_state[
                "sample_transcript"
            ] = f.read()

with col2:

    if st.button("Load Clean Call"):

        with open(
            "transcripts/clean_call.txt",
            "r",
            encoding="utf-8"
        ) as f:

            st.session_state[
                "sample_transcript"
            ] = f.read()

# =========================================================
# TRANSCRIPT INPUT
# =========================================================

st.subheader("Transcript Input")

transcript = st.text_area(
    "Paste customer support transcript",
    value=st.session_state.get(
        "sample_transcript",
        ""
    ),
    height=300
)

st.divider()

# =========================================================
# RUN ANALYSIS
# =========================================================

if st.button("Run QA Analysis"):

    if transcript.strip() == "":

        st.warning(
            "Please enter a transcript."
        )

    else:

        with st.spinner(
            "Running QA workflow..."
        ):

            # ============================================
            # START TIMER
            # ============================================

            start = time.time()

            result = workflow.invoke({

                "transcript": transcript
            })

            report = result["report"]

            # ============================================
            # END TIMER
            # ============================================

            end = time.time()

            execution_time = round(
                end - start,
                2
            )

        # ================================================
        # SUCCESS
        # ================================================

        st.success("Analysis Completed")

        st.info(
            f"Execution Time: {execution_time} seconds"
        )

        st.divider()

        # =================================================
        # EXECUTION TRACE
        # =================================================

        st.subheader(
            "Dynamic LangGraph Execution Trace"
        )

        trace = report.get(
            "execution_trace",
            []
        )

        if len(trace) == 0:

            st.warning(
                "No execution trace available."
            )

        else:

            for step in trace:

                icon = "✅"

                if step["status"] == "failed":

                    icon = "❌"

                elif step["status"] == "retry":

                    icon = "🔄"

                st.markdown(
                    f"""
### {icon} {step['node']}

- **Timestamp:** `{step['timestamp']}`
- **Duration:** `{step['duration']} sec`
"""
                )

                st.divider()

        # =================================================
        # LLM ORCHESTRATION
        # =================================================

        st.subheader("LLM Orchestration")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "LLM Used",
                report["llm_used"]
            )

        with col2:

            st.metric(
                "Fallback Triggered",
                str(
                    report[
                        "fallback_triggered"
                    ]
                )
            )

        with col3:

            st.metric(
                "QA Score",
                report["qa_score"]
            )

        # =================================================
        # FALLBACK STATUS
        # =================================================

        if report["fallback_triggered"]:

            st.warning(
                "Fallback Routing Activated"
            )

        else:

            st.success(
                "Primary Model Used"
            )

        fallback_reason = (

            report["fallback_reason"]

            if report["fallback_reason"]

            else "No fallback required."
        )

        st.info(
            f"Fallback Reason: {fallback_reason}"
        )

        # =================================================
        # EXECUTION LOGS
        # =================================================

        with st.expander(
            "View LLM Execution Logs"
        ):

            st.json(
                report["llm_logs"]
            )

        st.divider()

        # =================================================
        # RETRIEVED POLICIES
        # =================================================

        st.subheader(
            "Retrieved Policies"
        )

        for policy in report[
            "policies_retrieved"
        ]:

            clean_policy = (

                policy
                .replace("\n", " ")
                .replace(":", " -", 1)
            )

            st.success(clean_policy)

        st.divider()

        # =================================================
        # POLICY VIOLATIONS
        # =================================================

        st.subheader(
            "Policy Violations"
        )

        if len(
            report["policy_violations"]
        ) == 0:

            st.success(
                "No policy violations detected."
            )

        else:

            for violation in report[
                "policy_violations"
            ]:

                st.error(violation)

        st.divider()

        # =================================================
        # QA SCORE
        # =================================================

        st.subheader("QA Score")

        score = report["qa_score"]

        if score >= 80:

            st.success(
                f"QA Score: {score}"
            )

        elif score >= 60:

            st.warning(
                f"QA Score: {score}"
            )

        else:

            st.error(
                f"QA Score: {score}"
            )

        st.divider()

        # =================================================
        # LLM QA REASONING
        # =================================================

        st.subheader(
            "LLM QA Reasoning"
        )

        st.write(
            report["score_reasoning"]
        )

        st.divider()

        # =================================================
        # REVIEW STATUS
        # =================================================

        st.subheader(
            "Review Status"
        )

        if report["flag_for_review"]:

            st.error(
                "Flagged For Review"
            )

        else:

            st.success(
                "No Review Needed"
            )

        st.divider()

        # =================================================
        # STRUCTURED JSON REPORT
        # =================================================

        st.subheader(
            "Structured JSON Report"
        )

        display_report = report.copy()

        display_report[
            "score_reasoning"
        ] = (

            display_report[
                "score_reasoning"
            ]
            .replace('"', "'")[:300]

            + "..."
        )
        if display_report["fallback_reason"] is None:
            display_report["fallback_reason"] = (
                "No fallback required."
            )
        st.json(display_report)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Built using LangGraph, Groq LLMs, FAISS, and Streamlit"
)