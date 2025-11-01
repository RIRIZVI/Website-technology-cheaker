import requests
from bs4 import BeautifulSoup

def detect_technology(url):
    try:
        response = requests.get(url)
        html = response.text.lower()

        # Simple keyword-based detection
        if "wp-content" in html:
            tech = "WordPress"
        elif "shopify" in html:
            tech = "Shopify"
        elif "drupal" in html:
            tech = "Drupal"
        elif "joomla" in html:
            tech = "Joomla"
        elif "react" in html or "jsx" in html:
            tech = "React / Next.js"
        elif "vue" in html:
            tech = "Vue.js"
        elif "laravel" in html:
            tech = "Laravel (PHP Framework)"
        elif "django" in html:
            tech = "Django (Python Framework)"
        else:
            tech = "Could not detect (Maybe custom site)"

        print(f"\n🔍 Website: {url}")
        print(f"🧩 Detected Technology: {tech}\n")

    except Exception as e:
        print("❌ Error:", e)

# Example:
url = input("Enter website URL (e.g. https://example.com): ")
detect_technology(url)