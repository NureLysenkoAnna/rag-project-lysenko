import json
from collections import Counter

IGNORE_WORDS = {
    'the', 'and', 'to', 'a', 'of', 'in', 'is', 'it', 'i', 'that', 'for', 'you', 'your', 'are',
    'with', 'on', 'this', 'have', 'my', 'can', 'but', 'as', 'be', 'not', 'if', 'or',
    'so', 'they', 'at', 'from', "it's", 'just', 'like', 'how', 'about', 'what', 'was',
    'has', 'some', 'one', 'had', 'know', "i'm", 'should', 'been', 'them', 'would',
    'there', 'when', 'any', 'all', 'do', 'does', 'did', 'very', 'were', 'will',
    'more', 'which', 'up', 'out', 'get', 'can', 'we', 'me', 'am', 'then', 'than',
    'its', 'two', "i've", 'it.', 'other', 'new', 'now', 'few', 'could',
    'also', 'got', 'too', 'these', 'look', 'looks'
}


def analyze_corpus(cleaned_json, final_jsonl):
    with open(cleaned_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        questions_found = data.get("questions_found", 0)
        answers_found = data.get("answers_found", 0)
        docs_after_cleaning = data.get("docs_after_cleaning", 0)

    total_chunks = 0
    all_words = []

    with open(final_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            chunk = json.loads(line)
            total_chunks += 1
            words = chunk["text"].lower().split()
            all_words.extend(words)

    docs_found = questions_found + answers_found
    filtered_words = [w for w in all_words if w not in IGNORE_WORDS and len(w) > 2]
    top_20_words = Counter(filtered_words).most_common(20)
    avg_chunk_size = len(all_words) / total_chunks if total_chunks > 0 else 0

    print("\nСтатистика для DATA CARD:")
    print(f"Документів знайдено (до очищення): {docs_found}")
    print(f"Документів після фільтрації (> 100 символів): {docs_after_cleaning}")
    print(f"Загальна кількість чанків: {total_chunks}")
    print(f"Середній розмір чанка: {avg_chunk_size:.1f} слів")
    print(f"Топ-20 слів:\n{top_20_words}")

if __name__ == "__main__":
    analyze_corpus("data/cleaned_posts.json", "data/data_corpus.jsonl")