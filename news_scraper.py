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

# قراءة القالب الحالي
with open("index.html", "r", encoding="utf-8") as f:
    html_template = f.read()

# توليد محتوى الأخبار
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

# حقن المحتوى داخل <main>...</main>
new_html = re.sub(
    r"(<main.*?>)(.*?)(</main>)",
    f"\1{articles_html}\3",
    html_template,
    flags=re.DOTALL
)

# حفظ الملف النهائي
with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)