import httpx, re, html, urllib.parse
SCHEMA = {
    "name": "web_search",
    "description": "Search the web using DuckDuckGo",
    "parameters": "Search query string"
}
async def execute(arg: str, context: dict) -> str:
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(arg)}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            matches = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)".*?>([^<]+)</a>', response.text, re.DOTALL)
            results = []
            for link, title in matches[:5]:
                if link.startswith('/'):
                    m = re.search(r'uddg=([^&]+)', link)
                    if m: link = urllib.parse.unquote(m.group(1))
                results.append(f"Title: {html.unescape(title.strip())}\nURL: {link}")
            return "\n\n".join(results) if results else "Nothing found."
        except Exception as e:
            return f"Web search error: {str(e)}"
