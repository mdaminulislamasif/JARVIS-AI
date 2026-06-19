#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS Web Agent — Live Online Knowledge Engine
================================================
Gives JARVIS real-time internet knowledge by:
  1. DuckDuckGo Instant Answers (free, no API key)
  2. DuckDuckGo Web Search results (HTML scraping)
  3. Wikipedia summaries (free REST API)
  4. News search via GNews RSS feeds (free)

Usage:
    agent = JarvisWebAgent()
    result = agent.search_and_summarize("Python 3.13 new features")
    context = agent.build_context_for_ai("latest AI models 2025")
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import re
import time
import os
import threading
from datetime import datetime
from html.parser import HTMLParser


# ── HTML Tag Stripper ─────────────────────────────────────────────────────────
class _TagStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []

    def handle_data(self, data):
        self._parts.append(data)

    def get_text(self):
        return " ".join(self._parts)


def _strip_html(html: str) -> str:
    parser = _TagStripper()
    try:
        parser.feed(html)
        return re.sub(r'\s+', ' ', parser.get_text()).strip()
    except Exception:
        return re.sub(r'<[^>]+>', '', html).strip()


def _http_get(url: str, timeout: int = 8) -> str | None:
    """Simple HTTP GET with browser-like User-Agent to avoid blocks."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept": "application/json, text/html, */*",
                "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[WebAgent] HTTP error for {url[:60]}: {e}")
        return None


# ── JARVIS Web Agent ──────────────────────────────────────────────────────────
class JarvisWebAgent:
    """
    Live internet knowledge engine for JARVIS.
    No API keys required — uses free public endpoints.
    """

    DDG_API   = "https://api.duckduckgo.com/?q={q}&format=json&no_html=1&skip_disambig=1"
    DDG_SEARCH = "https://html.duckduckgo.com/html/?q={q}"
    WIKI_SEARCH = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={q}&format=json&srlimit=3"
    WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    GNEWS_RSS  = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"

    def __init__(self, log_callback=None):
        if log_callback:
            self.log = log_callback
        else:
            # Safe console logger that handles Windows CP1252 encoding
            import sys as _sys
            def _safe_log(msg):
                try:
                    print(f"[WebAgent] {msg}")
                except UnicodeEncodeError:
                    print(f"[WebAgent] {msg.encode('ascii', errors='replace').decode('ascii')}")
            self.log = _safe_log
        self._cache: dict[str, tuple[float, str]] = {}  # query -> (timestamp, result)
        self._cache_ttl = 300  # 5 minutes cache

    # ── Public API ────────────────────────────────────────────────────────────

    def ddg_instant(self, query: str) -> dict:
        """DuckDuckGo Instant Answers — fast, structured data."""
        url = self.DDG_API.format(q=urllib.parse.quote_plus(query))
        raw = _http_get(url)
        if not raw:
            return {}
        try:
            data = json.loads(raw)
            result = {}
            if data.get("AbstractText"):
                result["abstract"] = _strip_html(data["AbstractText"])
                result["source"]   = data.get("AbstractSource", "")
                result["url"]      = data.get("AbstractURL", "")
            if data.get("Answer"):
                result["answer"] = _strip_html(str(data["Answer"]))
            if data.get("Definition"):
                result["definition"] = _strip_html(data["Definition"])
            # Related topics
            topics = []
            for t in data.get("RelatedTopics", [])[:4]:
                if isinstance(t, dict) and t.get("Text"):
                    topics.append(_strip_html(t["Text"])[:150])
            if topics:
                result["related"] = topics
            return result
        except Exception as e:
            print(f"[WebAgent] DDG parse error: {e}")
            return {}

    def ddg_web_snippets(self, query: str, max_results: int = 5) -> list[dict]:
        """Scrape DuckDuckGo HTML search results for title + snippet."""
        url = self.DDG_SEARCH.format(q=urllib.parse.quote_plus(query))
        html = _http_get(url)
        if not html:
            return []

        results = []
        # Extract result blocks: <a class="result__a" href="...">TITLE</a>
        title_pat   = re.compile(r'class="result__a"[^>]*>(.*?)</a>', re.DOTALL)
        snippet_pat = re.compile(r'class="result__snippet"[^>]*>(.*?)</a>', re.DOTALL)
        url_pat     = re.compile(r'class="result__url"[^>]*>(.*?)</span>', re.DOTALL)

        titles   = [_strip_html(m.group(1)) for m in title_pat.finditer(html)]
        snippets = [_strip_html(m.group(1)) for m in snippet_pat.finditer(html)]
        urls     = [_strip_html(m.group(1)).strip() for m in url_pat.finditer(html)]

        for i in range(min(max_results, len(titles))):
            results.append({
                "title":   titles[i]   if i < len(titles)   else "",
                "snippet": snippets[i] if i < len(snippets) else "",
                "url":     urls[i]     if i < len(urls)      else "",
            })
        return results

    def wikipedia_summary(self, query: str) -> str | None:
        """Get Wikipedia page summary for a topic."""
        # First: find closest article title via search API
        search_url = self.WIKI_SEARCH.format(q=urllib.parse.quote_plus(query))
        raw = _http_get(search_url)
        if not raw:
            return None
        try:
            data = json.loads(raw)
            search_hits = data.get("query", {}).get("search", [])
            if not search_hits:
                return None
            title = search_hits[0]["title"]
        except Exception:
            return None

        # Fetch summary for that title
        summary_url = self.WIKI_SUMMARY.format(
            title=urllib.parse.quote(title, safe="")
        )
        raw = _http_get(summary_url)
        if not raw:
            return None
        try:
            data = json.loads(raw)
            extract = data.get("extract", "")
            if extract:
                # Limit to ~500 chars
                return extract[:600].strip()
        except Exception:
            pass
        return None

    def news_headlines(self, query: str, max_items: int = 5) -> list[str]:
        """Get news headlines from Google News RSS (free, no API key)."""
        url = self.GNEWS_RSS.format(q=urllib.parse.quote_plus(query))
        raw = _http_get(url, timeout=6)
        if not raw:
            return []
        items = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', raw)
        # Skip the first one (it's the feed title)
        return [_strip_html(h) for h in items[1:max_items+1]]

    # ── Main Agent Method ─────────────────────────────────────────────────────

    def search_and_summarize(self, query: str) -> str:
        """
        Full search: DDG instant + Wikipedia + web snippets.
        Returns a formatted context string ready to be injected into AI prompt.
        """
        cache_key = query.lower().strip()
        if cache_key in self._cache:
            ts, cached = self._cache[cache_key]
            if time.time() - ts < self._cache_ttl:
                return cached

        self.log(f"🌐 Searching: '{query}'")
        sections = [f"🌐 LIVE WEB KNOWLEDGE — Query: \"{query}\" [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"]
        sections.append("=" * 60)

        # 1. DuckDuckGo Instant Answer
        try:
            ddg = self.ddg_instant(query)
            if ddg:
                if ddg.get("answer"):
                    sections.append(f"📌 INSTANT ANSWER:\n{ddg['answer']}")
                if ddg.get("abstract"):
                    src = f" (Source: {ddg['source']})" if ddg.get("source") else ""
                    sections.append(f"📖 SUMMARY{src}:\n{ddg['abstract']}")
                if ddg.get("definition"):
                    sections.append(f"📚 DEFINITION:\n{ddg['definition']}")
                if ddg.get("related"):
                    sections.append("🔗 RELATED:\n" + "\n".join(f"  • {r}" for r in ddg["related"]))
        except Exception as e:
            self.log(f"DDG error: {e}")

        # 2. Wikipedia Summary
        try:
            wiki = self.wikipedia_summary(query)
            if wiki:
                sections.append(f"📚 WIKIPEDIA:\n{wiki}")
        except Exception as e:
            self.log(f"Wiki error: {e}")

        # 3. DuckDuckGo Web Snippets
        try:
            snippets = self.ddg_web_snippets(query, max_results=4)
            if snippets:
                lines = ["🔍 WEB RESULTS:"]
                for i, s in enumerate(snippets, 1):
                    if s.get("title") or s.get("snippet"):
                        lines.append(f"  [{i}] {s.get('title','')}")
                        if s.get("snippet"):
                            lines.append(f"      {s['snippet'][:200]}")
                        if s.get("url"):
                            lines.append(f"      🔗 {s['url']}")
                sections.append("\n".join(lines))
        except Exception as e:
            self.log(f"Snippets error: {e}")

        # 4. News Headlines
        try:
            news = self.news_headlines(query, max_items=4)
            if news:
                sections.append("📰 LATEST NEWS:\n" + "\n".join(f"  • {h}" for h in news))
        except Exception as e:
            self.log(f"News error: {e}")

        if len(sections) <= 2:
            result = f"[WebAgent] No online results found for: {query}"
        else:
            result = "\n\n".join(sections)

        self._cache[cache_key] = (time.time(), result)
        self.log(f"✅ Search complete — {len(sections)-2} sources found")
        return result

    def build_context_for_ai(self, query: str, code_context: str = "") -> str:
        """
        Build the complete AI prompt context:
        Web knowledge + optional code context.
        """
        web_data = self.search_and_summarize(query)
        parts = [web_data]
        if code_context.strip():
            parts.append(f"\n--- CODE CONTEXT ---\n{code_context[:2000]}")
        parts.append(f"\n--- QUESTION ---\n{query}")
        return "\n".join(parts)

    def search_threaded(self, query: str, callback, code_context: str = ""):
        """
        Run search in a background thread. Calls callback(context_str) when done.
        """
        def _run():
            try:
                ctx = self.build_context_for_ai(query, code_context)
                callback(ctx)
            except Exception as e:
                callback(f"[WebAgent Error] {e}")
        threading.Thread(target=_run, daemon=True, name="JARVIS-WebSearch").start()


# ── Singleton instance ────────────────────────────────────────────────────────
_agent_instance: JarvisWebAgent | None = None

def get_web_agent(log_callback=None) -> JarvisWebAgent:
    """Returns (or creates) the singleton JarvisWebAgent."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = JarvisWebAgent(log_callback=log_callback)
    return _agent_instance


# -- Quick Test ---------------------------------------------------------------
if __name__ == "__main__":
    import sys
    # Force UTF-8 output on Windows
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    agent = JarvisWebAgent()
    print("=== Test 1: Wikipedia ===")
    w = agent.wikipedia_summary("artificial intelligence")
    print("Wikipedia OK:", bool(w), "| Length:", len(w or ''))
    if w:
        print(w[:300])

    print("\n=== Test 2: DDG Instant Answer ===")
    d = agent.ddg_instant("Python programming")
    print("DDG instant OK:", bool(d), "| Keys:", list(d.keys()))

    print("\n=== Test 3: News Headlines ===")
    news = agent.news_headlines("artificial intelligence 2025", max_items=3)
    print("News headlines:", len(news), "items")
    for h in news:
        print("-", h)

    print("\nALL TESTS PASSED")
