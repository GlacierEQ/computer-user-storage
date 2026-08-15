from dataclasses import dataclass
from typing import List

@dataclass
class QueryPlan:
    query: str
    execution_steps: List[str]
    estimated_cost: float
    parallelizable: bool
    cacheable: bool
    cache_ttl: int = 1800
    
    def estimate_improvement(self) -> float:
        reduction = 0.0
        if self.cacheable:
            reduction += 0.40
        if self.parallelizable:
            reduction += 0.25
        reduction += (1.0 - self.estimated_cost) * 0.20
        return min(reduction, 0.65)

class QueryOptimizer:
    def __init__(self)
        self.optimization_rules = {
            "mesh_health": {"cacheable": True, "ttl": 300, "parallel": False},
            "evidence_lookup": {"cacheable": True, "ttl": 3600, "parallel": True},
            "token_balance": {"cacheable": True, "ttl": 60, "parallel": False},
            "case_timeline": {"cacheable": True, "ttl": 1800, "parallel": True}
        }
        self.stats = {"optimizations_applied": 0}
    
    def optimize(self, query: str, query_type: str = None) -> QueryPlan:
        rules = self.optimization_rules.get(query_type or \"generic\", {})
        steps = [\"parse_query\", \"check_cache\", \"analyze_complexity\", \"execute\"]
        cost = 0.5 * (0.3 if rules.get(\"cacheable\") else 1.0)
        
        plan = QueryPlan(
            query=query,
            execution_steps=steps,
            estimated_cost=cost,
            parallelizable=rules.get(\"parallel\", False),
            cacheable=rules.get(\"cacheable\", False),
            cache_ttl=rules.get(\"ttl\", 1800)
        )
        self.stats[\"optimizations_applied\"] += 1
        return plan

OPTIMIZER = QueryOptimizer()

def optimize_query(query: str, query_type: str = None) -> QueryPlan:
    return OPTIMIZER.optimize(query, query_type)
