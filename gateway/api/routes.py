from fastapi import APIRouter

from gateway.models.request import AnalyzeRequest
from gateway.models.response import AnalyzeResponse
from gateway.services.gateway_service import GatewayService

router = APIRouter()

gateway_service = GatewayService()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):

    risk_report = gateway_service.analyze(request.prompt)

    return AnalyzeResponse(
        status="success",
        risk=risk_report
    )


@router.get("/health")
def health():

    return {
        "status": "healthy"
    }


@router.get("/version")
def version():

    return {
        "version": "1.0.0"
    }