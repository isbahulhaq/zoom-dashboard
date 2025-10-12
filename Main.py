import os
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
import nest_asyncio
import indian_names
import logging

# लॉगिंग सेटअप
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nest_asyncio.apply()

# ग्लोबल फ्लैग
running = True
print_lock = threading.Lock()

async def start(thread_name, wait_time, meetingcode, passcode):
    user = indian_names.get_full_name()
    with print_lock:
        logger.info(f"{thread_name} शुरू हुआ (यूजर: {user})!")

    async with async_playwright() as p:
        browser = None
        try:
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(f'https://zoom.us/wc/join/{meetingcode}', timeout=60000)
            await page.wait_for_load_state('networkidle')

            # कुकी बटन
            try:
                await page.click('button[id="onetrust-accept-btn-handler"]', timeout=5000)
                logger.info(f"{thread_name}: कुकीज स्वीकार की गईं।")
            except Exception:
                logger.warning(f"{thread_name}: कुकी बटन नहीं मिला।")

            # टर्म्स बटन
            try:
                await page.click('button[id="wc_agree1"]', timeout=5000)
                logger.info(f"{thread_name}: टर्म्स स्वीकार किए गए।")
            except Exception:
                logger.warning(f"{thread_name}: टर्म्स बटन नहीं मिला।")

            # यूजर नेम और पासकोड
            try:
                await page.wait_for_selector('input[type="text"]', timeout=30000)
                await page.fill('input[type="text"]', user)
                await page.fill('input[type="password"]', passcode)
                join_button = await page.wait_for_selector('button.preview-join-button', timeout=30000)
                await join_button.click()
                logger.info(f"{thread_name}: मीटिंग जॉइन हो गई।")
            except Exception as e:
                logger.error(f"{thread_name}: जॉइन करने में एरर: {e}")
                return

            # माइक बटन
            try:
                query = '//button[text()="Join Audio by Computer"]'
                await page.wait_for_selector(query, timeout=60000)
                mic_button = await page.query_selector(query)
                await mic_button.click()
                logger.info(f"{thread_name}: माइक ऑन हो गया।")
            except Exception as e:
                logger.error(f"{thread_name}: माइक ऑन करने में एरर: {e}")

            # वेट टाइम
            logger.info(f"{thread_name}: {wait_time} सेकंड तक रुक रहा है...")
            while running and wait_time > 0:
                await asyncio.sleep(1)
                wait_time -= 1
            logger.info(f"{thread_name}: समाप्त हुआ!")

        except Exception as e:
            logger.error(f"{thread_name}: अप्रत्याशित एरर: {e}")
        finally:
            if browser:
                await browser.close()
                logger.info(f"{thread_name}: ब्राउज़र बंद हो गया।")

async def run_meeting(meetingcode, passcode, num_users, timeout):
    global running
    wait_time = int(timeout)
    with ThreadPoolExecutor(max_workers=num_users) as executor:
        loop = asyncio.get_running_loop()
        tasks = []
        for i in range(num_users):
            task = loop.create_task(start(f'[Thread{i}]', wait_time, meetingcode, passcode))
            tasks.append(task)
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            running = False
            await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    try:
        asyncio.run(run_meeting("default", "default", 5, 3600))  # डिफॉल्ट वैल्यूज़
    except KeyboardInterrupt:
        pass