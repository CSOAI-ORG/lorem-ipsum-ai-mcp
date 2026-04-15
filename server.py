#!/usr/bin/env python3
"""Generate placeholder text in various styles and structures. — MEOK AI Labs."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json, random
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now - t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT:
        return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day. Upgrade: meok.ai"})
    _usage[c].append(now)
    return None

mcp = FastMCP("lorem-ipsum-ai", instructions="Generate placeholder text in various styles and structures. By MEOK AI Labs.")

LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum", "sapien", "faucibus",
    "scelerisque", "felis", "imperdiet", "proin", "fermentum", "leo", "vel",
    "orci", "porta", "arcu", "cursus", "vitae", "congue", "mauris", "rhoncus",
    "aenean", "lacus", "viverra", "nibh", "cras", "pulvinar", "mattis", "nunc",
    "blandit", "turpis", "massa", "tincidunt", "dui", "eget", "semper", "risus",
    "pretium", "quam", "vulputate", "dignissim", "suspendisse", "morbi", "tristique",
    "senectus", "netus", "malesuada", "fames", "ac", "ante", "primis"
]

THEMED_WORDS = {
    "tech": ["algorithm", "data", "server", "cloud", "API", "deployment", "container",
             "microservice", "database", "cache", "latency", "throughput", "scalable",
             "distributed", "kubernetes", "pipeline", "binary", "compiler", "runtime",
             "framework", "protocol", "encryption", "authentication", "endpoint",
             "repository", "integration", "middleware", "payload", "bandwidth", "schema"],
    "business": ["strategy", "revenue", "stakeholder", "synergy", "optimize", "leverage",
                  "pipeline", "quarterly", "deliverable", "benchmark", "scalable",
                  "disruption", "innovation", "ecosystem", "monetize", "acquisition",
                  "portfolio", "ROI", "metrics", "engagement", "conversion", "retention",
                  "alignment", "roadmap", "milestone", "objective", "KPI", "market"],
    "nature": ["forest", "mountain", "river", "ocean", "meadow", "sunset", "breeze",
               "horizon", "valley", "waterfall", "canopy", "wildflower", "glacier",
               "canyon", "prairie", "rainfall", "moonlight", "aurora", "tide",
               "blossom", "pebble", "driftwood", "serenity", "wilderness", "foliage"],
    "food": ["artisan", "savory", "aromatic", "crispy", "seasoned", "simmered",
             "marinated", "roasted", "garnished", "infused", "drizzled", "caramelized",
             "reduction", "umami", "truffle", "saffron", "brioche", "confit",
             "emulsion", "julienne", "blanched", "braised", "zested", "whipped"],
}

CONNECTORS = ["however", "furthermore", "consequently", "meanwhile", "therefore",
              "additionally", "moreover", "nevertheless", "accordingly", "thus"]


def _generate_sentence(word_pool: list, min_words: int = 6, max_words: int = 15) -> str:
    count = random.randint(min_words, max_words)
    words = [random.choice(word_pool) for _ in range(count)]
    words[0] = words[0].capitalize()
    if random.random() < 0.15:
        mid = len(words) // 2
        words.insert(mid, random.choice(CONNECTORS))
    return " ".join(words) + "."


def _generate_paragraph(word_pool: list, min_sentences: int = 3, max_sentences: int = 7) -> str:
    count = random.randint(min_sentences, max_sentences)
    return " ".join(_generate_sentence(word_pool) for _ in range(count))


@mcp.tool()
def generate_paragraphs(count: int = 3, style: str = "lorem", start_with_lorem: bool = True, api_key: str = "") -> str:
    """Generate placeholder paragraphs. Styles: lorem (classic), tech, business, nature, food."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    count = max(1, min(count, 50))
    style = style.lower().strip()
    word_pool = THEMED_WORDS.get(style, LOREM_WORDS)

    paragraphs = []
    for i in range(count):
        para = _generate_paragraph(word_pool)
        if i == 0 and start_with_lorem and style == "lorem":
            para = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " + para
        paragraphs.append(para)

    text = "\n\n".join(paragraphs)
    word_count = len(text.split())
    char_count = len(text)

    return json.dumps({
        "paragraphs": paragraphs,
        "text": text,
        "paragraph_count": count,
        "word_count": word_count,
        "character_count": char_count,
        "style": style,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.tool()
def generate_sentences(count: int = 5, style: str = "lorem", min_words: int = 6, max_words: int = 15, api_key: str = "") -> str:
    """Generate individual placeholder sentences with configurable length."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    count = max(1, min(count, 100))
    min_words = max(3, min(min_words, 30))
    max_words = max(min_words, min(max_words, 50))
    style = style.lower().strip()
    word_pool = THEMED_WORDS.get(style, LOREM_WORDS)

    sentences = [_generate_sentence(word_pool, min_words, max_words) for _ in range(count)]
    text = " ".join(sentences)

    return json.dumps({
        "sentences": sentences,
        "text": text,
        "sentence_count": count,
        "word_count": len(text.split()),
        "character_count": len(text),
        "style": style,
        "word_range": [min_words, max_words],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.tool()
def generate_words(count: int = 50, style: str = "lorem", capitalize: bool = False, api_key: str = "") -> str:
    """Generate a specific number of placeholder words."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    count = max(1, min(count, 1000))
    style = style.lower().strip()
    word_pool = THEMED_WORDS.get(style, LOREM_WORDS)

    words = [random.choice(word_pool) for _ in range(count)]
    if capitalize:
        words = [w.capitalize() for w in words]

    text = " ".join(words)

    return json.dumps({
        "words": words,
        "text": text,
        "word_count": count,
        "character_count": len(text),
        "style": style,
        "unique_words": len(set(w.lower() for w in words)),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.tool()
def generate_structured(template: str = "article", style: str = "lorem", api_key: str = "") -> str:
    """Generate structured placeholder content. Templates: article, email, list, table, form, card."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    style = style.lower().strip()
    template = template.lower().strip()
    word_pool = THEMED_WORDS.get(style, LOREM_WORDS)

    def _title():
        words = [random.choice(word_pool) for _ in range(random.randint(3, 8))]
        return " ".join(words).title()

    def _short():
        return _generate_sentence(word_pool, 4, 10).rstrip(".")

    if template == "article":
        content = {
            "title": _title(),
            "subtitle": _short(),
            "author": f"{random.choice(['Alex', 'Jordan', 'Morgan', 'Casey', 'Taylor'])} {random.choice(['Smith', 'Lee', 'Chen', 'Kumar', 'Garcia'])}",
            "date": datetime.now(timezone.utc).strftime("%B %d, %Y"),
            "sections": [{"heading": _title(), "body": _generate_paragraph(word_pool)} for _ in range(random.randint(2, 4))],
            "tags": [random.choice(word_pool) for _ in range(3)],
        }
    elif template == "email":
        content = {
            "from": f"{random.choice(word_pool)}@example.com",
            "to": f"{random.choice(word_pool)}@example.com",
            "subject": _title(),
            "greeting": f"Dear {random.choice(['colleague', 'team', 'partner'])}",
            "body": [_generate_paragraph(word_pool, 2, 4) for _ in range(2)],
            "closing": random.choice(["Best regards", "Kind regards", "Sincerely", "Thank you"]),
            "signature": f"{random.choice(['Alex', 'Jordan', 'Morgan'])} {random.choice(['Smith', 'Lee'])}",
        }
    elif template == "list":
        content = {
            "title": _title(),
            "items": [{"label": _title(), "description": _generate_sentence(word_pool)} for _ in range(random.randint(5, 10))],
        }
    elif template == "table":
        headers = [random.choice(word_pool).capitalize() for _ in range(4)]
        rows = []
        for _ in range(random.randint(3, 8)):
            rows.append([random.choice(word_pool) for _ in range(4)])
        content = {"headers": headers, "rows": rows, "row_count": len(rows)}
    elif template == "form":
        field_types = ["text", "email", "number", "textarea", "select", "checkbox"]
        content = {
            "title": _title(),
            "description": _generate_sentence(word_pool),
            "fields": [{"label": random.choice(word_pool).capitalize(), "type": random.choice(field_types), "placeholder": _short(), "required": random.random() > 0.4} for _ in range(random.randint(4, 8))],
            "submit_text": random.choice(["Submit", "Send", "Register", "Continue"]),
        }
    elif template == "card":
        content = {
            "title": _title(),
            "description": _generate_sentence(word_pool),
            "image_alt": _short(),
            "tags": [random.choice(word_pool) for _ in range(random.randint(2, 4))],
            "cta_text": random.choice(["Learn More", "Read More", "View Details", "Get Started"]),
            "meta": {"date": datetime.now(timezone.utc).strftime("%b %d"), "read_time": f"{random.randint(2, 15)} min"},
        }
    else:
        return json.dumps({"error": f"Unknown template '{template}'. Use: article, email, list, table, form, card"})

    return json.dumps({
        "template": template,
        "style": style,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


if __name__ == "__main__":
    mcp.run()
