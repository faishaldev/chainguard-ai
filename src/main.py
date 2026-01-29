import json
import sys
import argparse
from .models import InputPayload
from .detector import Detector
from .scorer import Scorer
from .explainer import Explainer

def main():
    parser = argparse.ArgumentParser(description="ChainGuard AI - Fraud & Bot Detection Agent")
    parser.add_argument("input_file", help="Path to the JSON input file")
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as f:
            data = json.load(f)
        
        payload = InputPayload(**data)
        
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
