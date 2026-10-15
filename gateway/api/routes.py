from fastapi import APIRouter, Depends

from gateway.api.dependencies import get_gateway_service
from gateway.models.request import AnalyzeRequest, MultiTurnRequest
from gateway.models.response import AnalyzeResponse
from gateway.services.gateway_service import GatewayService
from gateway.services.memory_service import SessionMemory

router = APIRouter()
session_memory = SessionMemory()

# Route 1: Stateless Single Prompt Defense
@router.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_single(
    request: AnalyzeRequest,
    gateway_service: GatewayService = Depends(get_gateway_service),
):
    risk_report = gateway_service.analyze(request.prompt)
    return AnalyzeResponse(status="success", risk=risk_report)

# ============================================================================
# 2. MULTI-TURN CRESCENDO GATEWAY (Stateful - Session Velocity Tracking)
# ============================================================================
@router.post("/api/analyze/multi-turn", response_model=AnalyzeResponse)
def analyze_multi_turn_crescendo(
    request: MultiTurnRequest,
    gateway_service: GatewayService = Depends(get_gateway_service),
):
    # 1. Base inspection for the current turn
    risk_report = gateway_service.analyze(request.prompt)
    current_risk = risk_report.risk_score

    # 2. Record this turn in the isolated session bucket
    history = session_memory.add_turn(request.session_id, current_risk)

    # 3. Dual-Logic Context Drift Detection
    if len(history) == 3:
        r0, r1, r2 = history[0], history[1], history[2]
        
        # Logic 1: Strict Monotonic Escalation 
        # (Must continuously increase AND both Turn 2 and Turn 3 must be > 50%)
        strict_escalation = (r0 < r1 < r2) and (r1 > 50.0) and (r2 > 50.0)
        
        # Logic 2: Overall Trajectory Drift 
        # (Catches minor dips between turns if overall jump is >= 25% and final is >= 50%)
        overall_drift = r2 - r0
        trajectory_drift = (r2 >= 50.0) and (overall_drift >= 25.0)
        
        # Trigger block if EITHER condition is met
        if strict_escalation or trajectory_drift:
            risk_report.decision = "BLOCK"
            risk_report.decision_reason = "MULTI_TURN_ESCALATION_DETECTED"
            risk_report.risk_level = "HIGH"

            if not getattr(risk_report, "top_risk_factors", None):
                risk_report.top_risk_factors = []

            # Append Context_Drift as the top primary risk factor
            risk_report.top_risk_factors.insert(
                0,
                {
                    "feature": "Context_Drift",
                    "contribution": 25.0,
                },
            )

    return AnalyzeResponse(status="success", risk=risk_report)