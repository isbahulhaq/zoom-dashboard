from flask import Flask
import asyncio
from playwright.async_api import async_playwright
import nest_asyncio

nest_asyncio.apply()
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Zoom Dashboard is Live on Render"

@app.route('/join')
def join_meeting():
    asyncio.run(run_zoom_bot())
    return "🤖 Joining Zoom meeting now..."

async def run_zoom_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-software-rasterizer"
            ]
        )
        context = await browser.new_context()
        page = await context.new_page()

        # 👇 Replace this with your actual Zoom Meeting Link
        meeting_url = "https://zoom.us/wc/join/1234567890"
        await page.goto(meeting_url)

        print("🎯 Zoom meeting page loaded!")

        # Optional: Enter Name Automatically
        try:
            await page.fill('input[name="username"]', "Render Bot 🚀")
        except:
            pass

        await asyncio.sleep(15)
        await browser.close()
        print("✅ Zoom meeting join script finished.")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
