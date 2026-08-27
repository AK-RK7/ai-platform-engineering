from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

class ComplianceGraphState(TypedDict):
    query: str
    tenant_id: str
    selected_instructions: List[str]
    gap_findings: List[Dict[str, Any]]
    max_severity: str
    approval_required: bool
    status: str

def orchestrator_node(state: ComplianceGraphState) -> ComplianceGraphState:
    """Orchestrator plans analysis and selects adaptive instructions."""
    state["selected_instructions"] = ["instr_gdpr_32_security", "instr_breach_notification"]
    state["status"] = "planning_complete"
    return state

def gap_mapper_node(state: ComplianceGraphState) -> ComplianceGraphState:
    """Identifies gaps between controls and regulatory obligations."""
    # Simulated gap analysis results from knowledge graph traversal
    findings = [
        {"id": "gap-001", "obligation": "Article 32", "severity": "CRITICAL", "description": "Missing encryption at rest."},
        {"id": "gap-002", "obligation": "Article 33", "severity": "MEDIUM", "description": "Documentation incomplete."}
    ]
    state["gap_findings"] = findings
    
    # Determine max severity
    severities = [f["severity"] for f in findings]
    if "CRITICAL" in severities:
        state["max_severity"] = "CRITICAL"
        state["approval_required"] = True
    elif "HIGH" in severities:
        state["max_severity"] = "HIGH"
        state["approval_required"] = True
    else:
        state["max_severity"] = "MEDIUM"
        state["approval_required"] = False
        
    state["status"] = "mapping_complete"
    return state

def human_approval_gate_router(state: ComplianceGraphState) -> str:
    """Routes execution based on whether human-in-the-loop approval is mandatory."""
    if state["approval_required"]:
        return "wait_for_human_approval"
    return "finalize_remediation"

def human_approval_node(state: ComplianceGraphState) -> ComplianceGraphState:
    """Pauses workflow for CCO or Senior Compliance Manager sign-off."""
    state["status"] = "pending_human_approval"
    return state

def remediation_node(state: ComplianceGraphState) -> ComplianceGraphState:
    """Generates remediation tasks and policy update templates post-approval."""
    state["status"] = "remediation_planned"
    return state

def build_ecrip_agent_workflow() -> StateGraph:
    workflow = StateGraph(ComplianceGraphState)
    
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("gap_mapper", gap_mapper_node)
    workflow.add_node("human_approval", human_approval_node)
    workflow.add_node("remediation", remediation_node)
    
    workflow.set_entry_point("orchestrator")
    workflow.add_edge("orchestrator", "gap_mapper")
    
    workflow.add_conditional_edges(
        "gap_mapper",
        human_approval_gate_router,
        {
            "wait_for_human_approval": "human_approval",
            "finalize_remediation": "remediation"
        }
    )
    
    workflow.add_edge("human_approval", "remediation")
    workflow.add_edge("remediation", END)
    
    return workflow