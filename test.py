from tools.browser import BrowserTool

browser = BrowserTool()

try:
    print("STEP 1: Open YouTube")
    browser.navigate("https://www.youtube.com")

    browser.page.wait_for_timeout(2000)

    obs = browser.observe()

    print("TITLE:", obs["title"])
    print("URL:", obs["url"])

    # --------------------------
    # STEP 2: Search
    # --------------------------

    print("\nSTEP 2: Search dhurandhar song")

    search_id = obs["inputs"][0]["element_id"]

    browser.type(
        element_id=search_id,
        text="dhurandhar song"
    )

    browser.press("Enter")

    browser.page.wait_for_timeout(2000)

    obs = browser.observe()

    print("TITLE:", obs["title"])
    print("URL:", obs["url"])

    print("\nTOP LINKS:")
    for link in obs["links"]:
        print(link["text"])

    # --------------------------
    # STEP 3: Open first video
    # --------------------------

    print("\nSTEP 3: Open first video")

    first_video = None

    for link in obs["links"]:
        if "Sign in" not in link["text"] and \
           "Home" not in link["text"] and \
           "Shorts" not in link["text"]:
            first_video = link["element_id"]
            break

    if first_video is None:
        raise Exception("No video found")

    browser.click(element_id=first_video)

    browser.page.wait_for_timeout(2000)

    obs = browser.observe()

    print("TITLE:", obs["title"])
    print("URL:", obs["url"])

    # --------------------------
    # STEP 4: Go back
    # --------------------------

    print("\nSTEP 4: Go Back")

    browser.page.go_back()

    browser.page.wait_for_timeout(2000)

    obs = browser.observe()

    print("TITLE:", obs["title"])
    print("URL:", obs["url"])

    print("\nTOP LINKS AFTER BACK:")
    for link in obs["links"]:
        print(link["text"])

    print("\nTEST COMPLETED")

finally:
    browser.close()