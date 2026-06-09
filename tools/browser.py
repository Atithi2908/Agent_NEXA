import json
import re

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
        self.element_id_map = {}

    def _escape_selector_value(self, value):
        """Safely escape quotes in attribute values for CSS selectors."""
        if not value:
            return value
        return value.replace('"', '\\"')

    def _build_aria_selector(self, aria_label):
        """Build a safe aria-label selector with proper escaping."""
        escaped = aria_label.replace('\\', '\\\\').replace('"', '\\"')
        return f'[aria-label="{escaped}"]'

    def navigate(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def click(self, selector=None, element_id=None):
        if element_id is not None:
            if element_id not in self.element_id_map:
                raise ValueError(f"Element ID {element_id} not found in mapping. Available IDs: {list(self.element_id_map.keys())}")
            selector = self.element_id_map[element_id]
        
        if selector is None:
            raise ValueError("Either 'selector' or 'element_id' must be provided")
        
        try:
            locator = self.page.locator(selector)
            count = locator.count()
            if count == 0:
                raise Exception(f"Element not found with selector: {selector}")
            locator.first.scroll_into_view_if_needed()
            locator.first.click()
            self.page.wait_for_load_state("networkidle")
        except Exception as e:
            raise Exception(f"Click failed for selector '{selector}': {str(e)}")

    def type(self, selector=None, element_id=None, text=""):
        if element_id is not None:
            if element_id not in self.element_id_map:
                raise ValueError(f"Element ID {element_id} not found in mapping. Available IDs: {list(self.element_id_map.keys())}")
            selector = self.element_id_map[element_id]
        
        if selector is None:
            raise ValueError("Either 'selector' or 'element_id' must be provided")
        
        try:
            self.page.type(selector, text)
        except Exception as e:
            raise Exception(f"Type failed for selector '{selector}': {str(e)}")

    def press(self, key):
        self.page.keyboard.press(key)
        self.page.wait_for_load_state("networkidle")

    def observe(self):

        title = self.page.title()
        url = self.page.url

        text = self.page.locator("body").inner_text()
        text = text[:500]

        buttons = []
        element_id = 1
        
        # Reset the element ID map for this observation
        self.element_id_map = {}

        for button in self.page.locator("button").all():

            button_text = button.inner_text().strip()

            if button_text:

                id_attr = button.get_attribute("id")
                aria = button.get_attribute("aria-label")
                
                if aria:
                    selector = self._build_aria_selector(aria)
                elif id_attr:
                    selector = f"#{id_attr}"
                else:
                    selector = f"text={button_text}"

                locator = self.page.locator(selector)
                try:
                    visible = locator.first.is_visible()
                except:
                    visible = False
                

                if visible:
                    buttons.append({
                        "element_id": element_id,
                        "type": "button",
                        "text": button_text,
                        "selector": selector
                    })
                    # Store mapping for LLM-generated actions
                    self.element_id_map[element_id] = selector
                    element_id += 1

            if len(buttons) >= 10:
                break

        # ---------------- LINKS ----------------

        links = []

        for link in self.page.locator("a").all():

            link_text = link.inner_text().strip()

            if link_text:

                id_attr = link.get_attribute("id")
                aria = link.get_attribute("aria-label")

                if id_attr:
                    selector = f"#{id_attr}"
                elif aria:
                    selector = self._build_aria_selector(aria)
                else:
                    selector = f"text={link_text}"

                # Check visibility and uniqueness
                locator = self.page.locator(selector)
                try:
                    visible = locator.first.is_visible()
                except:
                    visible = False
                
                unique = (locator.count() == 1)

                if visible:
                    links.append({
                        "element_id": element_id,
                        "type": "link",
                        "text": link_text,
                        "selector": selector
                    })
                    # Store mapping for LLM-generated actions
                    self.element_id_map[element_id] = selector
                    element_id += 1

            if len(links) >= 10:
                break

        # ---------------- INPUTS ----------------
        
        inputs = []

        for inp in self.page.locator("input").all():

            placeholder = inp.get_attribute("placeholder")

            if placeholder:

                id_attr = inp.get_attribute("id")
                aria = inp.get_attribute("aria-label")

                if id_attr:
                    selector = f"#{id_attr}"
                elif aria:
                    selector = self._build_aria_selector(aria)
                else:
                    selector = f'input[placeholder="{placeholder}"]'

                # Check visibility and uniqueness
                print(f"[DEBUG SELECTOR] {selector}")
                locator = self.page.locator(selector)
                try:
                    visible = locator.first.is_visible()
                except:
                    visible = False
            

                if visible:
                    inputs.append({
                        "element_id": element_id,
                        "type": "input",
                        "placeholder": placeholder,
                        "selector": selector
                    })
                    # Store mapping for LLM-generated actions
                    self.element_id_map[element_id] = selector
                    element_id += 1

            if len(inputs) >= 5:
                break

        return {
            "title": title,
            "url": url,
            "text": text,
            "buttons": buttons,
            "links": links,
            "inputs": inputs
        }

    def close(self):
        if self.context:
            try:
                self.context.close()
            except:
                pass

        if self.playwright:
            try:
                self.playwright.stop()
            except:
                pass