from app.graph.workflow import workflow


with open(
    "transcripts/clean_call.txt",
    "r",
    encoding="utf-8"
) as f:

    transcript = f.read()


result = workflow.invoke({
    "transcript": transcript
})


print("\n========== FINAL QA REPORT ==========")
print(result["report"])