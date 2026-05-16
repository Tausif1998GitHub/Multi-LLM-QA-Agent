from pydantic import BaseModel
from typing import List


class QAReport(BaseModel):

    call_id: str

    llm_used: str

    fallback_triggered: bool

    fallback_reason: str

    policy_violations: List[str]

    policies_retrieved: List[str]

    sentiment: dict

    qa_score: int

    score_reasoning: str

    flag_for_review: bool