from playwright.sync_api import sync_playwright, Playwright, expect

def test_open_homepage_mobile_iPhone13(playwright: Playwright):
    iphone_13 = playwright.devices['iPhone 13']
    browser = playwright.webkit.launch(headless=True)
    context = browser.new_context(**iphone_13)
    page = context.new_page()
    page.goto("https://ovcharski.com/shop/")
    expect(page).to_have_title("Automation Demo Site – Website for demo purposes.")
    context.close()
    browser.close()

def test_open_homepage_mobile_GalaxyS9(playwright: Playwright):
    galaxy_s9 = playwright.devices['Galaxy S9+']
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(**galaxy_s9)
    page = context.new_page()
    page.goto("https://ovcharski.com/shop/")
    expect(page).to_have_title("Automation Demo Site – Website for demo purposes.")
    context.close()
    browser.close()

# Run the tests using the synchronous Playwright context manager
if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_open_homepage_mobile_iPhone13(playwright)
        test_open_homepage_mobile_GalaxyS9(playwright)
