import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =========================================================
# MODELS TO TEST
# =========================================================

MODELS = [
    "llama-3.3-70b-versatile",
    "groq/compound-mini",
    "openai/gpt-oss-20b"
]

# =========================================================
# TEST PROMPT
# =========================================================

PROMPT = "Say hello professionally in one sentence."

print("\n========== TESTING ALL MODELS ==========\n")

# =========================================================
# TEST EACH MODEL
# =========================================================

for model_name in MODELS:

    print(f"\n========== TESTING MODEL: {model_name} ==========\n")

    try:

        llm = ChatGroq(
            model=model_name,
            groq_api_key=GROQ_API_KEY
        )

        response = llm.invoke(PROMPT)

        print("SUCCESS:\n")
        print(response.content)

    except Exception as e:

        print("FAILED:\n")
        print(e)

print("\n========== ALL MODEL TESTS COMPLETED ==========\n")