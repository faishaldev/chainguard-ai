from typing import List, Dict, Any
from .models import InputPayload, Transaction

class Detector:
    def __init__(self):
        self.rules = [
            self._rule_high_frequency,
            self._rule_wash_trading,
            self._rule_repeated_contract_calls
        ]

    def analyze(self, payload: InputPayload) -> List[Dict[str, Any]]:
        findings = []
        for rule in self.rules:
            result = rule(payload)
            if result:
                findings.append(result)
        return findings

    def _rule_high_frequency(self, payload: InputPayload) -> Dict[str, Any]:
        """Detects high frequency transactions in a short window."""
        txs = sorted(payload.transactions, key=lambda x: x.timestamp)
        if len(txs) < 5:
            return None
        
        # Check for > 10 txs in 1 minute
        # Simplified: Check density
        duration = txs[-1].timestamp - txs[0].timestamp
        if duration > 0 and (len(txs) / duration) > (10 / 60): # > 10 tx per min
             return {
                "rule_id": "HIGH_FREQUENCY",
                "severity": "medium",
                "description": "Unusually high transaction frequency detected (potential bot).",
                "metadata": {"tx_rate_per_sec": len(txs) / duration}
            }
        return None

    def _rule_wash_trading(self, payload: InputPayload) -> Dict[str, Any]:
        """Detects circular flow of funds (simple implementation)."""
        # Placeholder for complex graph cycle detection
        # Simple check: Rapid back-and-forth between same addresses
        
        # For this MVP, let's just look for repeated (from, to) pairs
        # If > 50% of txs are between same two addresses
        if not payload.transactions:
            return None
            
        pairs = {}
        for tx in payload.transactions:
            key = tuple(sorted((tx.from_addr, tx.to_addr)))
            pairs[key] = pairs.get(key, 0) + 1
            
        for count in pairs.values():
            if count > len(payload.transactions) * 0.5 and count > 2:
                 return {
                    "rule_id": "WASH_TRADING_SUSPECT",
                    "severity": "high",
                    "description": "High concentration of transactions between same addresses.",
                    "metadata": {"repeated_pair_count": count}
                }
        return None

    def _rule_repeated_contract_calls(self, payload: InputPayload) -> Dict[str, Any]:
        """Detects repeated calls to the same method."""
        method_counts = {}
        for tx in payload.transactions:
            if tx.method:
                method_counts[tx.method] = method_counts.get(tx.method, 0) + 1
        
        for method, count in method_counts.items():
            if count > 5:
                 return {
                    "rule_id": "REPEATED_CONTRACT_CALLS",
                    "severity": "low",
                    "description": f"Repeated calls to method '{method}'.",
                    "metadata": {"method": method, "count": count}
                }
        return None
