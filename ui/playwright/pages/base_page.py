class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url.rstrip('/'))

    def get_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title

    def to_be_visible(self, selector: str) -> bool:
        return self.page.locator(selector).to_be_visible()

