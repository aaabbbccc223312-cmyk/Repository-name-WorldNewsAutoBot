from bot import telegram_sender

message = """
🌍 <b>GLOBAL PULSE</b>

🚨 <b>BREAKING NEWS</b>

📰 Apple unveils a new AI feature.

📍 <b>Source:</b> Reuters

🔗 https://example.com
"""

await telegram_sender.broadcast(message)
