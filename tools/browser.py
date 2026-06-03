from playwright.sync_api import sync_playwright
class BrowserTool:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir="./data/browser_data",
            headless=False
        )
        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()
    
    def navigate(self,url):
        self.page.goto(url)
        

    def click(self,text):
        self.page.get_by_text(text).click()
        

    def type(self,selector,text):
        self.page.type(selector, text)
    
    def press(self,key):
        self.page.keyboard.press(key)
        

def observe(self):

    title = self.page.title()

    url = self.page.url

    text = self.page.locator("body").inner_text()

    buttons = []

    for button in self.page.locator("button").all():
        button_text = button.inner_text().strip()

        if button_text:
            buttons.append(button_text)

    links = []

    for link in self.page.locator("a").all():
        link_text = link.inner_text().strip()

        if link_text:
            links.append(link_text)

    inputs = []

    for inp in self.page.locator("input").all():

        placeholder = inp.get_attribute("placeholder")

        if placeholder:
            inputs.append(placeholder)

    return {
        "title": title,
        "url": url,
        "text": text,
        "buttons": buttons,
        "links": links,
        "inputs": inputs
    }