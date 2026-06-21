import sys
import os
import json

# Add W5 src to path to import ConfidenceScorer
w5_src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../W5/src"))
if w5_src_path not in sys.path:
    sys.path.append(w5_src_path)

from agent.confidence_score import ConfidenceScorer

def run_proposed_agentic_rag():
    scorer = ConfidenceScorer()
    
    # Mock data to calculate scores for the Proposed Agentic RAG
    sensor_score = scorer.calculate_sensor_quality_score(missing_values_ratio=0.1, noise_level=0.15, delay_ms=200)
    rag_score = scorer.calculate_rag_relevance_score(query_similarity=0.95, context_usefulness=0.89)
    rule_score = scorer.calculate_rule_consistency_score(rules_passed=5, total_rules=5)
    historical_score = scorer.calculate_historical_stability_score(failure_rate_past_24h=0.05)
    
    # Generate agent output incorporating data quality and RAG metrics
    output = scorer.generate_agent_output(
        status="Warning",
        detected_issue="Abnormal temperature spike detected in Sensor Unit Alpha.",
        recommendation="Initiate auxiliary cooling system for Unit Alpha.",
        explanation="Temperature data indicates a rapid increase exceeding 15% of the normal operating range. Retrieved historical context suggests initiating the auxiliary cooling system resolves this issue without halting production. All safety rules are met.",
        evidence={
            "sensor_id": "alpha-temp-01",
            "current_value": 85.4,
            "historical_average": 72.0,
            "retrieved_doc_ids": ["doc-104", "doc-299"]
        },
        sensor_score=sensor_score,
        rag_score=rag_score,
        rule_score=rule_score,
        historical_score=historical_score,
        threshold=0.75
    )
    
    return output

if __name__ == "__main__":
    result = run_proposed_agentic_rag()
    print(json.dumps(result, indent=2))
