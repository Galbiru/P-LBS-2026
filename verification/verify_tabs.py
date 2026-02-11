import os
import sys
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get absolute path to index.html
        cwd = os.getcwd()
        file_path = f"file://{cwd}/index.html"

        print(f"Loading {file_path}")
        page.goto(file_path)

        # Click start button
        print("Clicking start button...")
        page.click("#start-btn")

        # Wait for main view
        print("Waiting for main view...")
        page.wait_for_selector("#main-view", state="visible")

        # Wait a bit for animations to finish (confetti, fade in)
        page.wait_for_timeout(2000)

        # Count user cards
        cards = page.query_selector_all(".user-card")
        count = len(cards)
        print(f"Found {count} user cards.")

        # Take screenshot
        print("Taking screenshot...")
        page.screenshot(path="verification/tabs_screenshot.png", full_page=True)

        browser.close()

        if count != 16:
            print(f"FAIL: Expected 16 cards, found {count}")
            sys.exit(1)
        else:
            print("SUCCESS: Found 16 cards.")

if __name__ == "__main__":
    run()
