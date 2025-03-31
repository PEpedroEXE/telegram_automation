import asyncio
import datetime
import os
import requests
from telethon import TelegramClient, events
from bs4 import BeautifulSoup

API_ID = 123456  
API_HASH = "your_api_hash"
SESSION_NAME = "telegram_multitool"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Auto-Reply to Messages
@client.on(events.NewMessage)
async def auto_reply(event):
    if event.is_private:  # Reply only to private messages
        await event.reply("🤖 I'm a bot! How can I assist you?")

# Save Messages to a File
@client.on(events.NewMessage)
async def save_messages(event):
    with open("messages_log.txt", "a", encoding="utf-8") as file:
        file.write(f"[{event.date}] {event.chat_id}: {event.raw_text}\n")

# Keyword Alerts
keywords = ["alert", "important", "urgent"]

@client.on(events.NewMessage)
async def keyword_alert(event):
    message = event.raw_text.lower()
    for keyword in keywords:
        if keyword in message:
            await client.send_message("me", f"🔔 Alert: '{keyword}' found in chat {event.chat_id}")

# Scheduled Reminders
async def scheduled_reminder():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == "09:00":  # Change time as needed
            await client.send_message("me", "🌞 Good morning! Don't forget your tasks.")
        await asyncio.sleep(60)  # Check every minute

# Export Chat History
async def export_chat(chat_username, output_file="chat_history.txt"):
    messages = await client.get_messages(chat_username, limit=100)
    with open(output_file, "w", encoding="utf-8") as file:
        for msg in messages:
            file.write(f"[{msg.date}] {msg.sender_id}: {msg.text}\n")
    print(f"✅ Chat history saved to {output_file}")

# Download Media from Chats
@client.on(events.NewMessage)
async def download_media(event):
    if event.media:
        folder = "downloads"
        os.makedirs(folder, exist_ok=True)
        file_path = await event.download_media(folder)
        print(f"✅ Media saved to {file_path}")

# Fetch Daily Weather (OpenWeatherMap API)
async def get_weather():
    API_KEY = "your_openweather_api_key"
    CITY = "New York"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    
    response = requests.get(url).json()
    temp = response["main"]["temp"]
    desc = response["weather"][0]["description"]
    
    await client.send_message("me", f"🌤 Weather Update: {CITY}\nTemperature: {temp}°C\nCondition: {desc}")

# Fetch Latest News (Scraping Example)
async def get_news():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = [a.text for a in soup.find_all("a", class_="storylink")[:5]]

    news_message = "📰 Latest News:\n" + "\n".join(headlines)
    await client.send_message("me", news_message)

# Start the Bot
async def main():
    await client.start()
    print("✅ Telegram Multi-Tool Bot is running...")

    # Run background tasks
    asyncio.create_task(scheduled_reminder())
    asyncio.create_task(get_weather())
    asyncio.create_task(get_news())

    await client.run_until_disconnected()

asyncio.run(main())
