from fastapi import Header, HTTPException

from config.settings import settings


async def validate_webhook_secret(
    x_telegram_bot_api_secret_token: str | None = Header(None),
) -> None:
    if x_telegram_bot_api_secret_token == settings.TELEGRAM_BOT_WEBHOOK_SECRET:
        return

    raise HTTPException(status_code=403, detail="Permissio Denied")


def remove_buttons_with_callback(reply_markup: dict) -> dict:
    original_keyboard = reply_markup["inline_keyboard"]

    new_keyboard = []
    for row in original_keyboard:
        filtered_buttons = []
        for button in row:
            if "callback_data" in button:
                continue

            filtered_buttons.append(button)

        new_keyboard.append(filtered_buttons)

    reply_markup["inline_keyboard"] = new_keyboard
    return reply_markup
