from playwright.sync_api import Page, expect

def test_open_homepage(page: Page) -> None:
    page.goto("https://ovcharski.com/shop/")
    expect(page.get_by_text("Welcome to the store")).to_be_visible()
    expect(page.locator("#post-84")).to_contain_text("Welcome to the store")
    expect(page.locator("#colophon")).to_contain_text("© Automation Demo Site 2025 Built with WooCommerce.")
    
    # Take a regular screenshot (visible viewport only)
    page.screenshot(path="screenshots/homepage.png")
    
    # Take a full-page screenshot
    page.screenshot(path="screenshots/homepage_full.png", full_page=True)