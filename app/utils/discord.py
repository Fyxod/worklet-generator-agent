import requests
import traceback

WEBHOOK_URL = 'https://discord.com/api/webhooks/1367095291425198183/Y0xGJuZqlesBRJKsXDiVdFcU33zV7mf5aD9E-oWvmXh8Kg-QQBxxRPwvm2ihYyeXT-7d'  # Replace with your webhook URL
USER_ID_1 = '1187313073057435708'  # Replace with first user's Discord ID
USER_ID_2 = '1187313073057435708'  # Replace with second user's Discord ID

def notify_discord_on_error(message: str, error: Exception):
    error_trace = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
    
    mentions = f"<@{USER_ID_1}> <@{USER_ID_2}>"
    payload = {
        "content": (
            f"{mentions} ❗ **Error Notification**\n"
            f"**Context:** {message}\n"
            f"```{error_trace[:1600]}```"
        )
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            print(f"Failed to send webhook: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to send error to Discord: {e}")

notify_discord_on_error("")