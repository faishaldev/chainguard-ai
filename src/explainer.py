from typing import List, Dict, Any

class Explainer:
    def generate_explanation(self, findings: List[Dict[str, Any]], risk_score: int) -> str:
        if not findings:
            return "No suspicious activity detected. The account appears to be behaving normally."
        
        reasons = []
        for f in findings:
            reasons.append(f"- {f['description']}")
            
        reasons_str = "\n".join(reasons)
        
        # Template-based "AI" explanation
        explanation = f"""
ChainGuard AI Assessment:
Risk Score: {risk_score}/100

Analysis detected potentially suspicious behavioral patterns:
{reasons_str}

Summary:
The observed activity triggers multiple risk indicators. users are advised to exercise caution.
"""
        return explanation.strip()
