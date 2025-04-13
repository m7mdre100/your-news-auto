import feedparser
import re

feeds = {
    "BBC Politics": "http://feeds.bbci.co.uk/news/politics/rss.xml",
    "Al Jazeera English": "https://www.aljazeera.com/xml/rss/all.xml",
    "Reuters World News": "http://feeds.reuters.com/Reuters/worldNews"
}

def extract_image(summary):
    match = re.search(r'<img[^>]+src="([^"]+)"', summary)
    return match.group(1) if match else None

html_start = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Your News</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #0f0f0f; color: #fff; margin: 0; padding: 0; }
        header { background: #1c1c1c; padding: 20px; text-align: center; }
        h1 { color: #ff4757; margin: 0; }
        main { padding: 20px; max-width: 900px; margin: auto; }
        article { background: #1e1e1e; border: 1px solid #333; margin-bottom: 20px; padding: 15px; border-radius: 8px; }
        article img { max-width: 100%; border-radius: 5px; margin-bottom: 10px; }
        article h2 { margin-top: 0; }
        article a { color: #1e90ff; text-decoration: none; }
        article a:hover { text-decoration: underline; }
        .source { font-size: 0.85em; color: #aaa; margin-top: 10px; }
    </style>
</head>
<body>
    <header>
        <img src="logo.png" alt="Your News" height="60"/>
        <h1>Latest Politics & Breaking News</h1>
    </header>
    <main>
'''

html_end = '''
    </main>
</body>
</html>
'''

articles_html = ""
for source, url in feeds.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        published = entry.get("published", "")
        summary = entry.get("summary", "")
        image_url = extract_image(summary)

        image_tag = f'<img src="{image_url}" alt="News image">' if image_url else ""
        short_summary = re.sub('<[^<]+?>', '', summary)[:300]

        articles_html += f'''
        <article>
            {image_tag}
            <h2><a href="{link}" target="_blank">{title}</a></h2>
            <p>{short_summary}...</p>
            <div class="source">{source} - {published}</div>
        </article>
        '''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_start + articles_html + html_end)