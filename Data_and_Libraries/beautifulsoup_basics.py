"""
BeautifulSoup Basics
=====================
BeautifulSoup4 parses HTML and XML and provides a Pythonic interface
to navigate, search, and modify the parse tree.

Install: pip install beautifulsoup4 requests
"""

try:
    from bs4 import BeautifulSoup
    import requests
    print("BeautifulSoup4 available.")
except ImportError:
    print("Install with: pip install beautifulsoup4 requests")
    exit(1)

# Sample HTML we'll parse throughout this file
SAMPLE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Python Articles</title>
    <meta name="description" content="A collection of Python learning resources">
</head>
<body>
    <nav>
        <a href="/home">Home</a>
        <a href="/articles">Articles</a>
    </nav>

    <header>
        <h1 id="main-title" class="title highlight">Python for All</h1>
        <p class="subtitle">Learn Python from beginner to advanced</p>
    </header>

    <main>
        <section class="articles">
            <article class="post featured" data-id="1">
                <h2 class="post-title"><a href="/post/1">Getting Started with Python</a></h2>
                <p class="meta">By <span class="author">SilasChalwe</span> | <time>2024-01-15</time></p>
                <p class="summary">Learn the basics of Python programming...</p>
                <ul class="tags">
                    <li class="tag">python</li>
                    <li class="tag">beginner</li>
                </ul>
            </article>

            <article class="post" data-id="2">
                <h2 class="post-title"><a href="/post/2">Advanced Python Decorators</a></h2>
                <p class="meta">By <span class="author">Alice</span> | <time>2024-02-20</time></p>
                <p class="summary">Explore decorators and their uses...</p>
                <ul class="tags">
                    <li class="tag">python</li>
                    <li class="tag">advanced</li>
                    <li class="tag">decorators</li>
                </ul>
            </article>

            <article class="post" data-id="3">
                <h2 class="post-title"><a href="/post/3">Pandas for Data Analysis</a></h2>
                <p class="meta">By <span class="author">Bob</span> | <time>2024-03-10</time></p>
                <p class="summary">A complete guide to Pandas DataFrames...</p>
                <ul class="tags">
                    <li class="tag">pandas</li>
                    <li class="tag">data</li>
                </ul>
            </article>
        </section>
    </main>

    <footer>
        <p>&copy; 2024 Python for All | <a href="/about">About</a></p>
    </footer>
</body>
</html>
"""


# ==============================================================================
# 1. PARSING HTML
# ==============================================================================

print("=" * 45)
print("PARSING HTML")
print("=" * 45)

# Create a BeautifulSoup object
# 'html.parser' is the built-in Python parser (no extra install)
# 'lxml' is faster but requires: pip install lxml
soup = BeautifulSoup(SAMPLE_HTML, "html.parser")

# Pretty-printed HTML
print("Title tag:", soup.title)
print("Title text:", soup.title.string)

# Access nested tags with dot notation
print("h1:", soup.h1)
print("h1 text:", soup.h1.text)

# Tag attributes
h1_tag = soup.find("h1")
print("h1 id:", h1_tag.get("id"))
print("h1 classes:", h1_tag.get("class"))


# ==============================================================================
# 2. find() AND find_all()
# ==============================================================================

print("\n--- find() and find_all() ---")

# find() — returns first matching tag
first_article = soup.find("article")
print("First article data-id:", first_article.get("data-id"))

# find_all() — returns a list of ALL matching tags
all_articles = soup.find_all("article")
print(f"Number of articles: {len(all_articles)}")

# find by class
featured = soup.find("article", class_="featured")
print("Featured article:", featured.get("data-id"))

# find by id
title = soup.find(id="main-title")
print("Element with id='main-title':", title.text)

# find_all with limit
first_two = soup.find_all("article", limit=2)
print(f"First 2 articles: {[a.get('data-id') for a in first_two]}")

# find_all with string matching
import re
h2_tags = soup.find_all("h2", string=re.compile("Python", re.IGNORECASE))
print(f"h2 tags containing 'Python': {len(h2_tags)}")


# ==============================================================================
# 3. CSS SELECTORS WITH select()
# ==============================================================================

print("\n--- CSS Selectors ---")

# select() — like CSS selectors, returns a list
# select_one() — like find(), returns first match

# Select all tags with a class
summaries = soup.select("p.summary")
for s in summaries:
    print(f"  Summary: {s.text[:40]}...")

# Select nested elements
post_titles = soup.select("article h2 a")
for t in post_titles:
    print(f"  Post: {t.text}  href={t.get('href')}")

# Select by attribute
all_tags_li = soup.select("li.tag")
tag_texts = [li.text for li in all_tags_li]
print(f"\nAll tags: {tag_texts}")
print(f"Unique tags: {list(set(tag_texts))}")


# ==============================================================================
# 4. EXTRACTING TEXT AND ATTRIBUTES
# ==============================================================================

print("\n--- Extracting Text & Attributes ---")

# Extract all authors
authors = [span.text for span in soup.find_all("span", class_="author")]
print("Authors:", authors)

# Extract all links
links = [(a.text.strip(), a.get("href")) for a in soup.find_all("a", href=True)]
print("\nLinks:")
for text, href in links:
    print(f"  '{text}' → {href}")

# Extract all article metadata
print("\nArticle metadata:")
for article in soup.find_all("article"):
    article_id = article.get("data-id")
    title_text = article.select_one("h2 a").text
    author     = article.find("span", class_="author").text
    date       = article.find("time").text
    tags       = [li.text for li in article.find_all("li", class_="tag")]
    print(f"  [{article_id}] {title_text}")
    print(f"       Author: {author} | Date: {date} | Tags: {tags}")


# ==============================================================================
# 5. NAVIGATING THE PARSE TREE
# ==============================================================================

print("\n--- Tree Navigation ---")

main_section = soup.find("section", class_="articles")

# Parent, children, siblings
print("Section parent:", main_section.parent.name)  # main

# .children generator (direct children)
children = [c for c in main_section.children if c.name]
print(f"Direct children of section: {len(children)} articles")

# Next/previous sibling
first = soup.find("article")
second = first.find_next_sibling("article")
print(f"First:  {first.get('data-id')}")
print(f"Second: {second.get('data-id')}")


# ==============================================================================
# 6. GETTING TEXT CONTENT
# ==============================================================================

print("\n--- Getting Text ---")

# .get_text() — all text, stripping tags
page_text = soup.get_text(separator=" ", strip=True)
print("Page text (first 150 chars):")
print(page_text[:150] + "...")

# .stripped_strings — generator of non-empty text strings
header = soup.find("header")
header_texts = list(header.stripped_strings)
print(f"\nHeader texts: {header_texts}")
