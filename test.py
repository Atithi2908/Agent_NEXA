from tools.browser import BrowserTool


browser = BrowserTool()

print("Opening Google...")

browser.navigate("https://google.com")

obs = browser.observe()

print("\nOBSERVATION:")
print("-" * 50)

print("Title:")
print(obs["title"])

print("\nURL:")
print(obs["url"])

print("\nContent Length:")
print(len(obs["content"]))

input("\nPress Enter to continue...")

browser.type("textarea", "LangGraph")

browser.page.keyboard.press("Enter")

input("\nVerify search results and press Enter...")

obs = browser.observe()

print("\nUPDATED OBSERVATION:")
print("-" * 50)

print("Title:")
print(obs["title"])

print("\nURL:")
print(obs["url"])

print("\nContent Length:")
print(len(obs["content"]))