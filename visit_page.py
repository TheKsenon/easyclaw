import httpx
import re
import html

SCHEMA = {
    "name": "visit_page",
    "description": "Fetch and extract readable text from a webpage URL. Automatically cleans HTML and truncates long content.",
    "parameters": "The URL of the webpage to visit"
}

async def execute(arg: str, context: dict) -> str:
    url = arg.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            text = response.text
            
            # Remove invisible elements (scripts, styles, svgs, etc.)
            text = re.sub(r'<(script|style|noscript|svg|canvas|video|audio)[^>]*>.*?</\1>', ' ', text, flags=re.IGNORECASE | re.DOTALL)
            
            # Replace block elements with newlines for readable formatting
            text = re.sub(r'</?(div|p|br|h[1-6]|li|tr|article|section)[^>]*>', '\n', text, flags=re.IGNORECASE)
            
            # Remove all remaining HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            
            # Unescape HTML entities (&amp;, &quot;, etc.)
            text = html.unescape(text)
            
            # Clean up whitespace (collapse multiple spaces, preserve intentional newlines)
            text = re.sub(r'[ \t]+', ' ', text)
            text = re.sub(r'\n\s*\n', '\n\n', text).strip()
            
            # Token overloading protection (truncate to ~10000 chars / ~2500 tokens)
            max_chars = 10000
            if len(text) > max_chars:
                text = text[:max_chars] + "\n\n... [Content truncated due to length limits]"
                
            return f"Content from {url}:\n\n{text}" if text else "Page fetched but no readable text found."
            
    except Exception as e:
        return f"Failed to visit page {url}: {str(e)}"
