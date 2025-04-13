
import feedparser
import re
import os
from datetime import datetime

feeds = {
    "BBC Politics": "http://feeds.bbci.co.uk/news/politics/rss.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "CNN Top Stories": "http://rss.cnn.com/rss/cnn_allpolitics.rss",
    "Fox News": "https://feeds.foxnews.com/foxnews/politics",
    "Sky News": "https://feeds.skynews.com/feeds/rss/world.xml",
    "The Guardian Politics": "https://www.theguardian.com/politics/rss",
    "ABC News US": "https://feeds.abcnews.com/abcnews/usheadlines",
    "Reuters World": "http://feeds.reuters.com/Reuters/worldNews"
}

def extract_image(entry):
    summary = entry.get("summary", "")
    match = re.search(r'<img[^>]+src="([^"]+)"', summary)
    if match:
        return match.group(1)

    media_content = entry.get("media_content", [])
    if media_content and "url" in media_content[0]:
        return media_content[0]["url"]

    media_thumbnail = entry.get("media_thumbnail", [])
    if media_thumbnail and "url" in media_thumbnail[0]:
        return media_thumbnail[0]["url"]

    return None

today_str = datetime.utcnow().strftime("%Y-%m-%d")

with open("index.html", "r", encoding="utf-8") as f:
    html_template = f.read()

html_template = re.sub(
    r"(<main.*?>)(.*?)(</main>)",
    r"\1\3",
    html_template,
    flags=re.DOTALL
)

articles_html = ""
for source, url in feeds.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:7]:
        title = entry.title
        link = entry.link
        published = entry.get("published", "")
        summary = entry.get("summary", "")
        image_url = extract_image(entry)

        if not image_url:
            continue

        short_summary = re.sub('<[^<]+?>', '', summary)[:300]
        image_tag = f'<img src="{image_url}" alt="News image">'

        articles_html += f'''
        <article>
            {image_tag}
            <h2><a href="{link}" target="_blank">{title}</a></h2>
            <p>{short_summary}...</p>
            <div class="source">{source} - {published}</div>
        </article>
        '''

html_template = re.sub(
    r"(<header>.*?</header>)",
    r'\1\n<nav style="text-align:center; padding:10px;"><a href="archive.html">View Archive</a></nav>',
    html_template,
    flags=re.DOTALL
)

new_html = re.sub(
    r"(<main.*?>)(</main>)",
    f"\1{articles_html}\2",
    html_template,
    flags=re.DOTALL
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

os.makedirs("archive", exist_ok=True)
archive_path = f"archive/news_{today_str}.html"
with open(archive_path, "w", encoding="utf-8") as f:
    f.write(new_html)

dates = sorted(os.listdir("archive"), reverse=True)
archive_links = "".join([f'<li><a href="archive/{f}">{f}</a></li>' for f in dates if f.endswith(".html")])

archive_html = f'''
<html>
<head><title>News Archive</title></head>
<body>
    <h1>News Archive</h1>
    <ul>
        {archive_links}
    </ul>
</body>
</html>
'''

with open("archive.html", "w", encoding="utf-8") as f:
    f.write(archive_html)
