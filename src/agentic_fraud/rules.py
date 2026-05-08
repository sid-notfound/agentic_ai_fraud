HIGH_RISK_COUNTRIES = {"Russia", "Nigeria", "UAE"}
HIGH_RISK_TYPES = {"Crypto Transfer", "Wire Transfer"}


def apply_rules(transaction: dict) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []

    amount = float(transaction.get("amount_usd", 0))
    country = str(transaction.get("country", ""))
    txn_type = str(transaction.get("transaction_type", ""))
    risk_flag = str(transaction.get("risk_flag", ""))

    if amount >= 20000:
        score += 30
        reasons.append("Large-value transfer above 20,000 USD.")
    elif amount >= 10000:
        score += 15
        reasons.append("Moderately large transfer above 10,000 USD.")

    if country in HIGH_RISK_COUNTRIES:
        score += 20
        reasons.append(f"High-risk geography detected: {country}.")

    if txn_type in HIGH_RISK_TYPES:
        score += 15
        reasons.append(f"Higher-risk transaction type: {txn_type}.")

    if risk_flag and risk_flag.lower() != "normal":
        score += 25
        reasons.append(f"Upstream indicator flagged as {risk_flag}.")

    return score, reasons

