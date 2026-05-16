import os
import random
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =========================================================
# PRIMARY MODEL
# =========================================================

PRIMARY_MODEL = "llama-3.3-70b-versatile"

# =========================================================
# FALLBACK MODEL 1
# =========================================================

FALLBACK_MODEL_1 = "groq/compound-mini"

# =========================================================
# FALLBACK MODEL 2
# =========================================================

FALLBACK_MODEL_2 = "openai/gpt-oss-20b"

# =========================================================
# INVOKE MODEL
# =========================================================

def invoke_model(model_name, prompt):

    llm = ChatGroq(
        model=model_name,
        groq_api_key=GROQ_API_KEY
    )

    response = llm.invoke(prompt)

    return response.content

# =========================================================
# SIMULATE FAILURE
# =========================================================

def simulate_failure(probability=0.4):

    if random.random() < probability:
        raise TimeoutError("Simulated API timeout")

# =========================================================
# MAIN TEST
# =========================================================

print("\n========== STARTING MULTI-LLM FALLBACK TEST ==========\n")

PROMPT = "Say hello professionally in one sentence."

# =========================================================
# TRY PRIMARY
# =========================================================

try:

    print(f"TRYING PRIMARY MODEL: {PRIMARY_MODEL}\n")

    simulate_failure()

    response = invoke_model(PRIMARY_MODEL, PROMPT)

    print("PRIMARY SUCCESS:\n")
    print(response)

# =========================================================
# FALLBACK 1
# =========================================================

except Exception as primary_error:

    print("PRIMARY FAILED:\n")
    print(primary_error)

    try:

        print(f"\nTRYING FALLBACK 1: {FALLBACK_MODEL_1}\n")

        simulate_failure()

        response = invoke_model(FALLBACK_MODEL_1, PROMPT)

        print("FALLBACK 1 SUCCESS:\n")
        print(response)

    # =====================================================
    # FALLBACK 2
    # =====================================================

    except Exception as fallback1_error:

        print("FALLBACK 1 FAILED:\n")
        print(fallback1_error)

        try:

            print(f"\nTRYING FALLBACK 2: {FALLBACK_MODEL_2}\n")

            response = invoke_model(FALLBACK_MODEL_2, PROMPT)

            print("FALLBACK 2 SUCCESS:\n")
            print(response)

        except Exception as fallback2_error:

            print("FALLBACK 2 FAILED:\n")
            print(fallback2_error)

            print("\nALL MODELS FAILED.\n")

print("\n========== FALLBACK TEST COMPLETED ==========\n")