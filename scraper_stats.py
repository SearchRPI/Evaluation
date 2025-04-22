import time
import json
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Setup for headless crawling
def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service("/opt/homebrew/bin/chromedriver"), options=options)

def fetch_page_with_metrics(url, driver):
    try:
        start_time = time.time()
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        html = driver.page_source
        elapsed_time = time.time() - start_time
        return html, elapsed_time
    except Exception as e:
        return None, None

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for tag in soup.find_all("a", href=True):
        href = tag['href']
        full_url = urljoin(base_url, href)
        links.add(full_url)
    return links

def crawl_with_metrics(start_url, whitelist_domain, max_pages=10):
    to_visit = [start_url]
    visited = set()
    stats = []

    driver = create_driver()

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        html, load_time = fetch_page_with_metrics(url, driver)
        if not html:
            stats.append({"url": url, "status": "failed"})
            continue

        content_size = len(html.encode('utf-8'))
        links = extract_links(html, url)
        internal_links = [link for link in links if urlparse(link).netloc.endswith(whitelist_domain)]

        stats.append({
            "url": url,
            "load_time": round(load_time, 3),
            "content_size_bytes": content_size,
            "total_links": len(links),
            "internal_links": len(internal_links),
            "external_links": len(links) - len(internal_links)
        })

        for link in internal_links:
            if link not in visited and link not in to_visit:
                to_visit.append(link)

    driver.quit()
    return stats

def main():
    start_url = "https://projecteuler.net/about"
    whitelist_domain = "projecteuler.net"

    print(f"\n🕸️ Starting scraper evaluation on {start_url}...\n")
    results = crawl_with_metrics(start_url, whitelist_domain)

    with open("scraper_stats.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("Evaluation complete. Results saved to scraper_stats.json")

if __name__ == "__main__":
    main()
