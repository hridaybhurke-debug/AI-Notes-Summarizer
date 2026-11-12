import re
from collections import Counter

STOP_WORDS = {
    "the", "is", "are", "was", "were", "a", "an",
    "and", "or", "but", "to", "of", "in", "on",
    "for", "with", "by", "this", "that", "it",
    "we", "they", "he", "she", "will", "be"
}


def split_sentences(text):
    return [
        s.strip()
        for s in re.split(r'(?<=[.!?])\s+', text.strip())
        if s.strip()
    ]


def summarize(text, max_sentences=3):
    sentences = split_sentences(text)

    if not sentences:
        return ""

    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    keywords = [
        word for word in words
        if word not in STOP_WORDS
    ]

    frequencies = Counter(keywords)

    scores = {}

    for index, sentence in enumerate(sentences):
        sentence_words = re.findall(
            r'\b[a-zA-Z]+\b', sentence.lower()
        )

        score = sum(
            frequencies[word]
            for word in sentence_words
            if word not in STOP_WORDS
        )

        scores[index] = score / max(len(sentence_words), 1)

    selected = sorted(
        scores,
        key=scores.get,
        reverse=True
    )[:max_sentences]

    # Preserve the original sentence order.
    selected.sort()

    return " ".join(sentences[i] for i in selected)


def extract_items(text, keywords):
    return [
        sentence
        for sentence in split_sentences(text)
        if any(
            keyword in sentence.lower()
            for keyword in keywords
        )
    ]


def process_notes(text):
    decisions = extract_items(text, [
        "agreed", "decided", "approved",
        "confirmed", "decision"
    ])

    actions = extract_items(text, [
        "will", "must", "need to",
        "assigned", "responsible for"
    ])

    return {
        "summary": summarize(text),
        "decisions": decisions,
        "action_items": actions
    }
