from fastapi import APIRouter, Depends

from gateway.api.dependencies import get_gateway_service
from gateway.models.request import AnalyzeRequest
from gateway.models.response import AnalyzeResponse
from gateway.services.gateway_service import GatewayService

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(
    request: AnalyzeRequest,
    gateway_service: GatewayService = Depends(get_gateway_service),
):

    risk_report = gateway_service.analyze(request.prompt)

    return AnalyzeResponse(
        status="success",
        risk=risk_report,
    )