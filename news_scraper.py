import feedparser

feeds = {
    "BBC Politics": "http://feeds.bbci.co.uk/news/politics/rss.xml",
    "Al Jazeera English": "https://www.aljazeera.com/xml/rss/all.xml",
    "Reuters World News": "http://feeds.reuters.com/Reuters/worldNews"
}

html_start = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Your News</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #111; color: #fff; margin: 0; padding: 20px; }
        header { background: #222; padding: 20px; text-align: center; }
        h1 { color: #f00; }
        article { border-bottom: 1px solid #444; padding: 10px 0; }
        a { color: #0af; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .source { font-size: 0.8em; color: #aaa; }
    </style>
</head>
<body>
    <header>
        <img src="logo.png" alt="Your News" height="60"/>
        <h1>Latest Politics & Breaking News</h1>
    </header>
    <main>
'''

html_end = '</main></body></html>'
articles_html = ""

for source, url in feeds.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        summary = entry.get("summary", "")[:300]
        published = entry.get("published", "")
        articles_html += f'''
        <article>
            <h2><a href="{link}" target="_blank">{title}</a></h2>
            <p>{summary}</p>
            <div class="source">{source} - {published}</div>
        </article>
        '''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_start + articles_html + html_end)