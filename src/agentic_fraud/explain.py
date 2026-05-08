import os


def build_explanation_prompt(transaction: dict, reasons: list[str], policies: list[str]) -> str:
    policy_context = "\n".join(f"- {p}" for p in policies[:3]) if policies else "- No policy excerpts retrieved."
    reason_text = "; ".join(reasons)
    return (
        "You are an AML analyst assistant. Explain this alert for an operations team.\n"
        f"Transaction: {transaction}\n"
        f"Detected reasons: {reason_text}\n"
        f"Retrieved policy context:\n{policy_context}\n"
        "Return a concise explanation and next action."
    )


def llm_provider_hint() -> str:
    if os.getenv("BEDROCK_MODEL_ID"):
        return "AWS Bedrock"
    if os.getenv("ANTHROPIC_API_KEY"):
        return "Claude API"
    return "local-rule-engine"

