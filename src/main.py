import json
import sys
import argparse
import os
from .models import InputPayload
from .detector import Detector
from .scorer import Scorer
from .explainer import Explainer
from .fetcher import Fetcher

def main():
    parser = argparse.ArgumentParser(description="ChainGuard AI - Fraud & Bot Detection Agent")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input_file", help="Path to the JSON input file")
    group.add_argument("--address", help="Wallet address to analyze (requires POLYGONSCAN_API_KEY)")
    
    parser.add_argument("--chain", default="polygon", help="Blockchain network (default: polygon)")
    
    args = parser.parse_args()

    try:
        if args.input_file:
            with open(args.input_file, 'r') as f:
                data = json.load(f)
            payload = InputPayload(**data)
        else:
            # Live data mode
            if not os.getenv("POLYGONSCAN_API_KEY"):
                print("Error: POLYGONSCAN_API_KEY environment variable is required for live data.")
                sys.exit(1)
            
            print(f"Fetching transactions for {args.address} on {args.chain}...")
            fetcher = Fetcher()
            payload = fetcher.fetch_transactions(args.address, args.chain)
            print(f"Analyze {len(payload.transactions)} transactions...")

        detector = Detector()
        findings = detector.analyze(payload)
        
        scorer = Scorer()
        risk_score = scorer.calculate_score(findings)
        
        explainer = Explainer()
        explanation = explainer.generate_explanation(findings, risk_score)
        
        output = {
            "entity_id": payload.entity_id,
            "risk_score": risk_score,
            "findings": findings,
            "explanation": explanation
        }
        
        print(json.dumps(output, indent=2))
        
    except json.JSONDecodeError:
        print("Error: Invalid JSON file.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
