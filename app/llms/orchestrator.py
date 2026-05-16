import os
import random
import time

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from datetime import datetime

# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =========================================================
# MODEL CONFIGURATION
# =========================================================

PRIMARY_MODEL = "llama-3.3-70b-versatile"

FALLBACK_MODEL_1 = "qwen/qwen3-32b"

FALLBACK_MODEL_2 = "openai/gpt-oss-20b"

# =========================================================
# ORCHESTRATOR
# =========================================================

class LLMOrchestrator:

    def __init__(self):

        self.logs = []

    # =====================================================
    # INVOKE MODEL
    # =====================================================

    def invoke_model(
        self,
        model_name,
        prompt
    ):

        llm = ChatGroq(

            model=model_name,

            groq_api_key=GROQ_API_KEY
        )

        response = llm.invoke(prompt)

        return response.content

    # =====================================================
    # FAILURE SIMULATION
    # =====================================================

    def simulate_failure(
        self,
        probability=0.2
    ):

        if random.random() < probability:

            raise TimeoutError(
                "Simulated API timeout"
            )

    # =====================================================
    # CLEAN RESPONSE
    # =====================================================

    def clean_response(self, response):

        if response is None:

            return "Empty LLM response."

        response = response.strip()

        # ================================================
        # REMOVE THINK TAGS
        # ================================================

        if "<think>" in response:

            response = (

                response
                .split("</think>")[-1]
                .strip()
            )

        return response

    # =====================================================
    # MAIN ANALYSIS METHOD
    # =====================================================

    def analyze(self, prompt):

        models = [

            PRIMARY_MODEL,

            FALLBACK_MODEL_1,

            FALLBACK_MODEL_2
        ]

        fallback_reason = None

        # =================================================
        # TRY EACH MODEL
        # =================================================

        for index, model in enumerate(models):

            model_start = time.time()

            try:

                print(
                    f"\n[ORCHESTRATOR] TRYING MODEL: {model}"
                )

                # =========================================
                # SIMULATE FAILURE ONLY FOR PRIMARY
                # =========================================

                if index == 0:

                    self.simulate_failure(
                        probability=0.2
                    )

                # =========================================
                # INVOKE MODEL
                # =========================================

                response = self.invoke_model(

                    model,

                    prompt
                )

                response = self.clean_response(
                    response
                )

                duration = round(

                    time.time() - model_start,

                    2
                )

                # =========================================
                # SUCCESS LOG
                # =========================================

                self.logs.append({

                    "model": model,

                    "status": "success",

                    "timestamp":
                        datetime.now().strftime(
                            "%H:%M:%S"
                        ),

                    "duration":
                        f"{duration} sec"
                })

                print(
                    f"[ORCHESTRATOR] SUCCESS: {model}"
                )

                return {

                    "response": response,

                    "llm_used": model,

                    "fallback_triggered":
                        index != 0,

                    "fallback_reason":
                        fallback_reason,

                    "logs": self.logs
                }

            # =============================================
            # FAILURE HANDLING
            # =============================================

            except Exception as e:

                duration = round(

                    time.time() - model_start,

                    2
                )

                print(
                    f"[ORCHESTRATOR] FAILED: {model}"
                )

                fallback_reason = str(e)

                # =========================================
                # RETRY LOG
                # =========================================

                self.logs.append({

                    "model": model,

                    "status": "retry",

                    "reason": str(e),

                    "timestamp":
                        datetime.now().strftime(
                            "%H:%M:%S"
                        ),

                    "duration":
                        f"{duration} sec"
                })

        # =================================================
        # ALL MODELS FAILED
        # =================================================

        return {

            "response":
                (
                    "LLM analysis unavailable "
                    "because all fallback models failed."
                ),

            "llm_used": None,

            "fallback_triggered": True,

            "fallback_reason":
                "All models failed.",

            "logs": self.logs
        }