def test_brave_api():
    api_key = os.environ.get("BRAVE_API_KEY")
    if not api_key:
        print("Brave Search API: SKIPPED - Missing BRAVE_API_KEY")
        return
    try:
        headers = {"X-Subscription-Token": api_key}
        params = {"q": "test query"}
        r = requests.get("https://api.search.brave.com/res/v1/web/search", headers=headers, params=params, timeout=5)
        r.raise_for_status()
        print("Brave Search API: SUCCESS")
    except Exception as e:
        print(f"Brave Search API: FAILURE - {e}")

def test_yandex_html():
    try:
        r = requests.get("https://yandex.com/search/?text=test+query", timeout=5)
        r.raise_for_status()
        if "yandex" in r.text.lower():
            print("Yandex Search HTML: SUCCESS")
        else:
            print("Yandex Search HTML: FAILURE - Unexpected content")
    except Exception as e:
        print(f"Yandex Search HTML: FAILURE - {e}")
import os
import requests
import subprocess
import json
from duckduckgo_search import DDGS

def test_duckduckgo_lite():
    try:
        r = requests.get("https://lite.duckduckgo.com/lite/", timeout=5)
        r.raise_for_status()
        print("DuckDuckGo Lite: SUCCESS")
    except Exception as e:
        print(f"DuckDuckGo Lite: FAILURE - {e}")

def test_duckduckgo_html():
    try:
        r = requests.get("https://html.duckduckgo.com/html/", timeout=5)
        r.raise_for_status()
        print("DuckDuckGo HTML: SUCCESS")
    except Exception as e:
        print(f"DuckDuckGo HTML: FAILURE - {e}")

def test_duckduckgo_api():
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text("test query", max_results=1))
            if results:
                print("DuckDuckGo Search API (duckduckgo_search): SUCCESS")
            else:
                print("DuckDuckGo Search API (duckduckgo_search): FAILURE - No results")
    except Exception as e:
        print(f"DuckDuckGo Search API (duckduckgo_search): FAILURE - {e}")


def test_duckduckgo_api_curl():
    """
    Test the DuckDuckGo Instant Answer API via the curl CLI.
    """
    try:
        # Using curl to call the Instant Answer API with recommended parameters
        cmd = [
            "curl", "-s", "-G", "https://api.duckduckgo.com",
            "-H", "Accept: application/json",
            "--data-urlencode", "q=python programming",
            "--data-urlencode", "format=json",
            "--data-urlencode", "no_html=1",
            "--data-urlencode", "skip_disambig=1",
            "--data-urlencode", "no_redirect=1"
        ]
        output = subprocess.check_output(cmd, timeout=30, stderr=subprocess.STDOUT).decode()
        data = json.loads(output)
        # Check for expected keys in the JSON response
        if "AbstractText" in data or "RelatedTopics" in data or "Results" in data:
            print("DuckDuckGo API via curl: SUCCESS")
        else:
            print("DuckDuckGo API via curl: FAILURE - Unexpected response structure")
    except Exception as e:
        print(f"DuckDuckGo API via curl: FAILURE - {e}")

def test_bing_api():
    api_key = os.environ.get("BING_API_KEY")
    if not api_key:
        print("Bing Search API: SKIPPED - Missing BING_API_KEY")
        return
    try:
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        params = {"q": "test query"}
        r = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params, timeout=5)
        r.raise_for_status()
        print("Bing Search API: SUCCESS")
    except Exception as e:
        print(f"Bing Search API: FAILURE - {e}")

def test_google_serpapi():
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        print("Google SerpAPI: SKIPPED - Missing SERPAPI_API_KEY")
        return
    try:
        params = {"q": "test query", "api_key": api_key, "engine": "google"}
        r = requests.get("https://serpapi.com/search", params=params, timeout=5)
        r.raise_for_status()
        print("Google SerpAPI: SUCCESS")
    except Exception as e:
        print(f"Google SerpAPI: FAILURE - {e}")

def test_qwant():
    try:
        params = {"q": "test query", "t": "web", "count": 1}
        r = requests.get("https://api.qwant.com/api/search/web", params=params, timeout=5)
        r.raise_for_status()
        print("Qwant Web Search: SUCCESS")
    except Exception as e:
        print(f"Qwant Web Search: FAILURE - {e}")

def test_startpage():
    try:
        r = requests.get("https://www.startpage.com/sp/search", params={"query": "test query"}, timeout=5)
        if "startpage" in r.text.lower():
            print("Startpage Search: SUCCESS")
        else:
            print("Startpage Search: FAILURE - Unexpected content")
    except Exception as e:
        print(f"Startpage Search: FAILURE - {e}")

if __name__ == "__main__":
    test_duckduckgo_lite()
    test_duckduckgo_html()
    test_duckduckgo_api()
    test_duckduckgo_api_curl()
    test_bing_api()
    test_google_serpapi()
    test_qwant()
    test_startpage()
    test_brave_api()
    test_yandex_html()
