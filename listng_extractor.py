import json
import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def extract_jobposting_jsonld(html: str):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")

    def iter_candidates(data):
        # JSON-LD can be dict, list, or contain @graph
        if isinstance(data, dict) and "@graph" in data:
            for item in data["@graph"]:
                yield item
        elif isinstance(data, list):
            for item in data:
                yield item
        elif isinstance(data, dict):
            yield data

    for s in scripts:
        raw = s.string
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue

        for obj in iter_candidates(data):
            if not isinstance(obj, dict):
                continue
            t = obj.get("@type")
            # sometimes @type can be list
            if t == "JobPosting" or (isinstance(t, list) and "JobPosting" in t):
                return obj

    return None


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text("\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch_html_requests(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-CA,en;q=0.9",
    }
    r = requests.get(url, headers=headers, timeout=15)
    # If blocked, raise with context
    if r.status_code in (403, 429):
        raise requests.HTTPError(f"Blocked with status {r.status_code}", response=r)
    r.raise_for_status()
    return r.text


def fetch_html_playwright(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        # some sites hydrate after load
        page.wait_for_timeout(1500)
        html = page.content()
        browser.close()
        return html


def extract_job(url: str):
    # 1) try cheap fetch
    html = None
    fetch_method = None

    try:
        html = fetch_html_requests(url)
        fetch_method = "requests"
    except Exception as e:
        # 2) fallback to browser fetch
        html = fetch_html_playwright(url)
        fetch_method = "playwright"

    # 3) parse JSON-LD if available
    job = extract_jobposting_jsonld(html)
    if job:
        hiring = job.get("hiringOrganization")
        company = hiring.get("name") if isinstance(hiring, dict) else None

        return {
            "fetch_method": fetch_method,
            "source": "jsonld",
            "title": job.get("title"),
            "company": company,
            "location": job.get("jobLocation"),
            "description_html": job.get("description"),
        }

    # 4) fallback: return extracted text
    return {
        "fetch_method": fetch_method,
        "source": "text",
        "text": html_to_text(html)[:12000],
    }


if __name__ == "__main__":
    url = "PUT URL HERE"
    print(extract_job(url))
