import sys
import time

from playwright.sync_api import sync_playwright


def main():
    # "http://10.81.1.15:3000/d/ceeb3b75-9f23-4be5-95af-73b4441d812d/wordcloud-dnsquery?orgId=1"
    # noc_img1.png
    args = sys.argv
    url = args[1]
    path = args[2]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        page = browser.new_page()
        page.goto(url)
        username_field = page.locator('input[name="user"]')
        password_field = page.locator('input[name="password"]')

        username_field.fill("admin")
        password_field.fill("")
        # page.screenshot(path="gra_shin_1.png")
        page.get_by_text("Log in").click()
        # page.screenshot(path="gra_shin_2.png")
        page.goto(url)
        # page.screenshot(path="gra_shin_3.png")
        time.sleep(5)
        page.screenshot(path=path)
        browser.close()


if __name__ == "__main__":
    main()
