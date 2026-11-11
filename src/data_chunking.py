import json

# Налаштування чанкування
CHUNK_SIZE = 300    # максимальна кількість слів у чанку
OVERLAP = 45        # кількість слів перекриття (15%)


def chunk_text(doc):
    text = doc["text"]
    doc_id = doc["id"]

    score = doc.get("score", 0)
    doc_type = doc.get("type", "unknown")

    words = text.split()
    chunks = []

    if len(words) == 0:
        return chunks

    step = CHUNK_SIZE - OVERLAP
    for i in range(0, len(words), step):
        chunk_words = words[i:i + CHUNK_SIZE]
        chunk_text_str = " ".join(chunk_words)

        chunk_metadata = {
            "chunk_id": f"{doc_id}_{len(chunks) + 1}",  # стабільний глобальний ідентифікатор
            "doc_id": doc_id,                           # ідентифікатор документа-джерела
            "chunk_index": len(chunks) + 1,             # порядковий номер чанка у документі
            "score": score,                             # рейтинг
            "type": doc_type,                           # тип (питання чи відповідь)
            "text": chunk_text_str
        }
        chunks.append(chunk_metadata)

        if i + CHUNK_SIZE >= len(words):
            break

    return chunks


def build_corpus(input_json, output_jsonl):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        cleaned_docs = data["documents"]

    total_chunks = 0

    with open(output_jsonl, "w", encoding="utf-8") as f_out:
        for doc in cleaned_docs:
            chunks = chunk_text(doc)
            total_chunks += len(chunks)

            # Збереження у форматі JSONL (один об'єкт на рядок)
            for chunk in chunks:
                f_out.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"Згенеровано {total_chunks} чанків. Результат збережено у {output_jsonl}")


if __name__ == "__main__":
    build_corpus("data/cleaned_posts.json", "data/data_corpus.jsonl")