import csv
import html
import json
import re
import time
import urllib.parse
import urllib.request


LABEL_QUERIES = {
    "analysis": [
        "because",
        "defense",
        "efficiency",
        "spacing",
        "usage",
        "pick and roll",
        "true shooting",
        "lineup",
        "rotation",
        "matchup",
    ],
    "hot_take": [
        "overrated",
        "cooked",
        "washed",
        "trash",
        "fraud",
        "not that guy",
        "blow it up",
        "worst",
        "choker",
        "empty stats",
    ],
    "reaction": [
        "no way",
        "insane",
        "crazy",
        "unbelievable",
        "lmao",
        "lol",
        "i can't believe",
        "what a game",
        "bruh",
        "wild",
    ],
    "question": [
        "why",
        "who would you rather",
        "what do you think",
        "which player",
        "how good",
        "is he",
        "should the",
        "can someone explain",
        "would you",
        "who is",
    ],
}

ANALYSIS_MARKERS = re.compile(
    r"\b(because|defense|offense|efficiency|spacing|usage|lineup|rotation|matchup|screen|pick[- ]and[- ]roll|"
    r"true shooting|ts%|assist|turnover|rebound|possession|scheme|coverage|percent|percentage|per 100|on/off)\b",
    re.IGNORECASE,
)
HOT_TAKE_MARKERS = re.compile(
    r"\b(overrated|underrated|cooked|washed|trash|fraud|choker|pathetic|garbage|awful|terrible|"
    r"not that guy|empty stats|blow it up|never winning|worst|best player in the league|fake)\b",
    re.IGNORECASE,
)
REACTION_MARKERS = re.compile(
    r"\b(lmao|lol|bruh|no way|insane|crazy|unbelievable|wild|what a game|i can't believe|"
    r"sick|pain|wow|holy|clutch|choked|cooked him)\b|[!]{2,}",
    re.IGNORECASE,
)
QUESTION_MARKERS = re.compile(r"\?|^(why|who|what|which|how|should|would|can someone|is he|are the)\b", re.IGNORECASE)


def fetch_comments(query, size=100):
    params = urllib.parse.urlencode({"subreddit": "nba", "size": size, "q": query})
    url = f"https://api.pullpush.io/reddit/search/comment/?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "ai201-takemeter-course-project/0.1"})
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response).get("data", [])


def clean_text(text):
    text = html.unescape(text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def source_url(item):
    permalink = item.get("permalink", "")
    if permalink.startswith("/"):
        return f"https://www.reddit.com{permalink}"
    return permalink


def acceptable(text):
    lowered = text.lower()
    if lowered in {"[deleted]", "[removed]"}:
        return False
    if "http://" in lowered or "https://" in lowered:
        return False
    words = text.split()
    return 5 <= len(words) <= 90


def score_label(text, desired):
    scores = {
        "analysis": 0,
        "hot_take": 0,
        "reaction": 0,
        "question": 0,
    }
    word_count = len(text.split())
    has_question = bool(QUESTION_MARKERS.search(text))
    has_analysis = bool(ANALYSIS_MARKERS.search(text))
    has_hot_take = bool(HOT_TAKE_MARKERS.search(text))
    has_reaction = bool(REACTION_MARKERS.search(text))

    if has_analysis:
        scores["analysis"] += 2
    if has_hot_take:
        scores["hot_take"] += 2
    if has_reaction:
        scores["reaction"] += 2
    if has_question:
        scores["question"] += 3
    if word_count >= 28 and has_analysis:
        scores["analysis"] += 1
    if word_count <= 18 and has_reaction:
        scores["reaction"] += 1
    scores[desired] += 1
    return max(scores, key=scores.get), scores


def strong_match(text, label):
    word_count = len(text.split())
    has_question = bool(QUESTION_MARKERS.search(text))
    has_analysis = bool(ANALYSIS_MARKERS.search(text))
    has_hot_take = bool(HOT_TAKE_MARKERS.search(text))
    has_reaction = bool(REACTION_MARKERS.search(text))

    if label == "question":
        return has_question and not (has_reaction and word_count <= 12)
    if label == "reaction":
        return has_reaction and not has_question and (word_count <= 35 or "!" in text)
    if label == "hot_take":
        return has_hot_take and not has_question
    if label == "analysis":
        return has_analysis and word_count >= 20 and not (has_question and text.strip().endswith("?"))
    return False


def note_for(label, query, item, scores):
    created = item.get("created_utc", "")
    return (
        f"source=r/nba PullPush archive; query={query}; created_utc={created}; "
        f"score={item.get('score', '')}; label_scores={scores}"
    )


def main():
    selected = {label: [] for label in LABEL_QUERIES}
    seen = set()

    for label, queries in LABEL_QUERIES.items():
        for query in queries:
            if len(selected[label]) >= 58:
                break
            try:
                comments = fetch_comments(query)
            except Exception as exc:
                print(f"FETCH_ERROR label={label} query={query!r}: {exc}")
                continue
            for item in comments:
                text = clean_text(item.get("body"))
                if not acceptable(text):
                    continue
                key = re.sub(r"\W+", "", text.lower())[:160]
                if key in seen:
                    continue
                predicted, scores = score_label(text, label)
                if predicted != label or not strong_match(text, label):
                    continue
                seen.add(key)
                selected[label].append(
                    {
                        "text": text,
                        "label": label,
                        "notes": note_for(label, query, item, scores),
                        "source_url": source_url(item),
                    }
                )
                if len(selected[label]) >= 58:
                    break
            time.sleep(1)

    rows = []
    for label in ["analysis", "hot_take", "reaction", "question"]:
        rows.extend(selected[label][:50])
        print(label, len(selected[label]))

    with open("work/takemeter_rnba_labeled.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label", "notes", "source_url"])
        writer.writeheader()
        writer.writerows(rows)

    print("total", len(rows))


if __name__ == "__main__":
    main()
