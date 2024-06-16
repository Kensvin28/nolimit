import requests
import sys
import re
import json
from datetime import datetime
from content_parser import ContentParser

def get_title(html):
    """Get title from span in h1"""
    pattern = r'<span class="mw-page-title-main">([^<]+)<'
    title = re.findall(pattern, html)[0]
    return title

def get_link(html):
    """Get links inside content (.div.mw-content-ltr.mw-parser-output)"""
    parser = ContentParser()
    parser.feed(html)
    parser.close()
    links = parser.get_links()
    return links

def get_content(html):
    """Get content (text inside p, li, h2, h3, h4)"""
    parser = ContentParser()
    parser.feed(html)
    parser.close()
    content = parser.get_data()
    return content

def get_category(html):
    """Get category"""
    pattern = r'<div id="mw-normal-catlinks"[^>]*>(.*?)</div>'
    div_content = re.search(pattern, html).group(1)
    category_pattern = r'<a\s+href="\/wiki\/Category:[^"]*".*?>([^<]*)<\/a>'
    categories = re.findall(category_pattern, div_content)
    if len(categories) == 0:
        categories = ""
    categories = ", ".join(categories)
    return categories

def get_created_at(html):
    """Get created_at"""
    pattern = r'<li id="footer-info-lastmod"[^>]*>(.*?)<'
    created_at = re.search(pattern, html).group(1)
    # Get date
    date = re.search(r'(\d+\s+\w+\s+\d+)', created_at).group(1)
    # Get time
    time = re.search(r'(\d+:\d+)', created_at).group(1)
    created_at = datetime.strptime(date + " " + time, "%d %B %Y %H:%M").strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return created_at

if __name__ == "__main__":
    args = sys.argv
    if args[-1].startswith("http://"):
        proxy = args[-1]
    else:
        proxy = None
    phrase_list = args[1].split()
    if len(phrase_list) > 1:
        phrase = "_".join(phrase_list)
    else:
        phrase = args[1]
    print(f"Scraping {phrase}...")
    r = requests.get(f"https://en.wikipedia.org/wiki/{phrase}", proxies={"http": proxy, "https": proxy})

    if r.status_code != 200:
        print(f"Error {r.status_code}")
        exit()
    
    html = r.text

    title = get_title(html)
    links = get_link(html)
    content = get_content(html)
    categories = get_category(html)
    created_at = get_created_at(html)

    res = {"title": title, "link": links, "content": content, "createdAt": created_at, "category": categories}

    print(f"Successfully scraped {phrase}.")
    # Read json and append to json list
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    data = []
    data.append(res)
    with open("data.json", "w+") as f:
        json.dump(data, f)

