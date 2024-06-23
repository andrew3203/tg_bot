from fastapi import APIRouter


router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.post(
    "/crm",
    response_model=dict,
)
async def webhook_crm(data: dict) -> dict:
    return {"status": "ok"}
