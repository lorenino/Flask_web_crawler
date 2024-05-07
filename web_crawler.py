import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import datetime
import os

def fetch(url):
    try:
        response = requests.get(url, timeout=10)
        return response if response.status_code == 200 else None
    except requests.RequestException:
        return None

def process_page(url, base_domain):
    response = fetch(url)
    found_links = set()
    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            parsed_url = urlparse(full_url)
            if parsed_url.netloc.endswith(base_domain) and not (parsed_url.query or parsed_url.fragment):
                if not parsed_url.path.lower().endswith(('.jpg', '.jpeg', '.pdf', '.png', '.gif', '.mp4', '.mp3', '.avi', '.mov', '.wmv')):
                    found_links.add(full_url)
    return found_links, url

def crawl_site(start_url, base_domain, max_workers=10):
    visited = set()
    to_visit = set([start_url])

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while to_visit:
            futures = {executor.submit(process_page, url, base_domain): url for url in to_visit if url not in visited}
            to_visit.clear()  # Clear immediately to prepare for next round of URLs
            for future in as_completed(futures):
                new_urls, url = future.result()
                visited.add(url)  # Mark this URL as visited
                to_visit.update(new_urls - visited)  # Add new URLs if they haven't been visited

    return visited

def save_data(visited_pages, output_dir, base_domain):
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(output_dir, f"visited_urls_{base_domain}_{timestamp}.xlsx")
    df = pd.DataFrame(sorted(visited_pages), columns=['URL'])
    df.to_excel(filename, index=False)
