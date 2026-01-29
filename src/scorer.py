from typing import List, Dict, Any

class Scorer:
    SEVERITY_WEIGHTS = {
        "low": 10,
        "medium": 30,
        "high": 60,
        "critical": 90
    }

    def calculate_score(self, findings: List[Dict[str, Any]]) -> int:
        score = 0
        for finding in findings:
            severity = finding.get("severity", "low")
            score += self.SEVERITY_WEIGHTS.get(severity, 10)
        
        # Cap score at 100
        return min(score, 100)
