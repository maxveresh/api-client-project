from playwright.sync_api import sync_playwright

def test_playwright_works():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.google.com")
        assert 'Google' in page.title()
        browser.close()
