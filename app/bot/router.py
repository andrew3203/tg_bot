import logging
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    status,
)
from app.bot.utils import remove_buttons_with_callback, validate_webhook_secret
from app.bot.app import process_event

router = APIRouter()


@router.post(
    "/webhook",
    dependencies=[Depends(validate_webhook_secret)],
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def tgbot_webhook_events(
    payload: dict,
    worker: BackgroundTasks,
) -> dict:
    logging.info(f"WORKS:::\npayload: {payload}\n")
    worker.add_task(func=process_event, **payload)

    # remove buttons with callback
    if "callback_query" in payload:
        cbqm = payload["callback_query"]["message"]
        if cbqm.get("reply_markup"):  # has buttons
            return {
                "method": "editMessageReplyMarkup",
                "chat_id": cbqm["chat"]["id"],
                "message_id": cbqm["message_id"],
                "reply_markup": remove_buttons_with_callback(cbqm["reply_markup"]),
            }

    return {"ok:": True}
