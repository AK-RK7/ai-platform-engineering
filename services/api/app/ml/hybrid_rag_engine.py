import os
from typing import List, Dict, Any

class ECRIPHybridRAGEngine:
    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k

    def reciprocal_rank_fusion(self, dense_results: List[Dict], sparse_results: List[Dict]) -> List[Dict]:
        """Merges dense and sparse results using RRF (k=60)."""
        fusion_scores = {}
        
        for rank, item in enumerate(dense_results):
            doc_id = item["id"]
            fusion_scores[doc_id] = fusion_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))
            
        for rank, item in enumerate(sparse_results):
            doc_id = item["id"]
            fusion_scores[doc_id] = fusion_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))
            
        sorted_docs = sorted(fusion_scores.items(), key=lambda x: x[1], reverse=True)
        return [{"id": doc_id, "score": score} for doc_id, score in sorted_docs]

    def hallucination_guard(self, llm_response_claims: List[str], retrieved_subgraph_nodes: List[str]) -> Dict[str, Any]:
        """Validates LLM claims against graph-grounded citations to prevent hallucinations."""
        untraceable_claims = []
        valid_claims = []
        
        node_set = set(retrieved_subgraph_nodes)
        for claim in llm_response_claims:
            # Check if claim maps to graph node references or citations
            if any(node_id in claim for node_id in node_set):
                valid_claims.append(claim)
            else:
                untraceable_claims.append(claim)
                
        is_safe = len(untraceable_claims) == 0
        return {
            "status": "passed" if is_safe else "flagged_untraceable",
            "valid_claims_count": len(valid_claims),
            "untraceable_claims": untraceable_claims,
            "guard_message": "All claims grounded in graph citations." if is_safe else "Hallucination guard triggered: untraceable claims detected."
        }