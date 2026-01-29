# agents.md
## Agent: ChainGuard AI — Fraud & Bot Detection Agent (MVP)

---

## 1. Agent Purpose

ChainGuard AI is an off-chain analysis agent designed to detect potentially fraudulent or automated (bot-like) behavior in Web3 ecosystems by analyzing on-chain transaction patterns and producing explainable, human-readable summaries.

The agent does not block transactions or provide legal or financial judgments. Its role is detection, explanation, and risk signaling.

---

## 2. Problem Context

Web3 networks face persistent issues such as:
- Automated bot activity
- Spam and wash trading
- Exploit attempts using repeated contract calls

Raw blockchain data is difficult to interpret quickly, especially when identifying *why* an activity is suspicious rather than just *that* it is suspicious.

---

## 3. Agent Responsibilities

The ChainGuard AI agent is responsible for:
- Ingesting normalized on-chain transaction data
- Detecting suspicious or bot-like patterns using rule-based heuristics
- Scoring risk levels in an explainable way
- Generating clear AI explanations for flagged behavior
- Supporting visualization and investigation workflows

---

## 4. Input Specification

### Input Payload
```json
{
  "entity_type": "wallet | contract",
  "entity_id": "0x...",
  "chain": "polygon",
  "transactions": [
    {
      "hash": "0x...",
      "from": "0x...",
      "to": "0x...",
      "value": "0.0",
      "gas_used": 220000,
      "timestamp": 1700000000,
      "method": "swapExactTokensForTokens"
    }
  ]
}
