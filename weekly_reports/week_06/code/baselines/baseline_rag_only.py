import json

def run_rag_only(query: str, context: str):
    # Baseline RAG only, ignoring data quality
    output = {
        "status": "Warning",
        "detected_issue": "Abnormal temperature spike detected in Sensor Unit Alpha.",
        "rag_relevance_score": 0.92,
        # Notice missing sensor_quality_score, rule_consistency_score, historical_stability_score, final_confidence_score
        "recommendation": "Initiate auxiliary cooling system for Unit Alpha.",
        "explanation": "Based on retrieved documents, the temperature spike requires cooling. Ignored data quality metrics.",
        "evidence": {
            "sensor_id": "alpha-temp-01",
            "current_value": 85.4,
            "historical_average": 72.0,
            "retrieved_doc_ids": ["doc-104", "doc-299"]
        }
    }
    return output

if __name__ == "__main__":
    result = run_rag_only("Temperature spike in Unit Alpha", "Document 104, 299 context")
    print(json.dumps(result, indent=2))
