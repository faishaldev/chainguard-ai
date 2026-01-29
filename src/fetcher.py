import os
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from .models import InputPayload, Transaction

load_dotenv()

class Fetcher:
    POLYGONSCAN_API_URL = "https://api.polygonscan.com/api"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("POLYGONSCAN_API_KEY")
        if not self.api_key:
            raise ValueError("POLYGONSCAN_API_KEY is not set in environment variables.")

    def fetch_transactions(self, address: str, chain: str = "polygon") -> InputPayload:
        if chain.lower() != "polygon":
            raise ValueError("Currently only 'polygon' chain is supported.")

        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": 1,
            "offset": 100, # Limit to 100 recent transactions for MVP performance
            "sort": "desc",
            "apikey": self.api_key
        }

        try:
            response = requests.get(self.POLYGONSCAN_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] != "1" and data["message"] != "No transactions found":
                raise ValueError(f"API Error: {data['message']} - {data['result']}")
                
            raw_txs = data.get("result", [])
            transactions = self._normalize_transactions(raw_txs)
            
            return InputPayload(
                entity_type="wallet", # Default assumption for address
                entity_id=address,
                chain=chain,
                transactions=transactions
            )

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to fetch transactions: {str(e)}")

    def _normalize_transactions(self, raw_txs: List[Dict[str, Any]]) -> List[Transaction]:
        normalized = []
        for tx in raw_txs:
            # Handle potential missing fields or format differences
            try:
                # PolygonScan returns string values for most numeric fields
                normalized.append(Transaction(
                    hash=tx.get("hash", ""),
                    from_addr=tx.get("from", ""),
                    to_addr=tx.get("to", ""),
                    value=tx.get("value", "0"),
                    gas_used=int(tx.get("gasUsed", 0)),
                    timestamp=int(tx.get("timeStamp", 0)),
                    method=tx.get("methodId", None) # PolygonScan uses methodId, input usually contains data. We'll verify if method name is available or just ID. 
                    # Note: PolygonScan often provides 'functionName' if verified, but standard 'txlist' might just give methodId or input.
                    # For simplicty in MVP, let's map methodId if functionName is missing or parse it.
                    # Actually, let's check if 'functionName' exists in standard txlist response from PolygonScan. It usually does for verified contracts.
                ))
                # Correction: methodId is the 4 bytes. functionName is human readable.
                # Let's try to use functionName if available and not empty, otherwise methodId.
                if "functionName" in tx and tx["functionName"]:
                     normalized[-1].method = tx["functionName"].split('(')[0] # clean up args
                elif "methodId" in tx:
                     normalized[-1].method = tx["methodId"]

            except (ValueError, TypeError):
                continue # Skip malformed transactions
                
        return normalized
