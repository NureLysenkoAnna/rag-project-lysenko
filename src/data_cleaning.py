import json
import re
import os
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

KEYWORDS = {'succulent', 'cactus', 'cacti', 'aloe', 'echeveria', 'crassula'}
MIN_LENGTH = 100


def clean_text(raw_html):
    if not raw_html:
        return ""
    text = BeautifulSoup(raw_html, "html.parser").get_text(separator=" ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_and_clean(xml_file, output_json):
    valid_question_ids = set()
    cleaned_docs = []

    questions_found = 0
    answers_found = 0

    for event, elem in ET.iterparse(xml_file, events=('end',)):
        if elem.tag == 'row':
            post_type = elem.attrib.get('PostTypeId')
            post_id = elem.attrib.get('Id')
            raw_body = elem.attrib.get('Body', '')
            score = elem.attrib.get('Score', '0')

            is_relevant = False

            # Якщо це питання (PostTypeId="1")
            if post_type == '1':
                tags = elem.attrib.get('Tags', '').lower()
                if any(kw in tags for kw in KEYWORDS):
                    valid_question_ids.add(post_id)
                    questions_found += 1
                    is_relevant = True

            # Якщо це відповідь (PostTypeId="2")
            elif post_type == '2':
                parent_id = elem.attrib.get('ParentId')
                if parent_id in valid_question_ids:
                    answers_found += 1
                    is_relevant = True

            if is_relevant:
                cleaned_text = clean_text(raw_body)

                # Маркування, питання (Q) чи відповідь (A)
                prefix = "Q: " if post_type == '1' else "A: "

                if len(cleaned_text) >= MIN_LENGTH:
                    cleaned_docs.append({
                        "id": post_id,
                        "type": "question" if post_type == '1' else "answer",
                        "score": int(score),
                        "text": prefix + cleaned_text
                    })

            elem.clear()

    os.makedirs(os.path.dirname(output_json), exist_ok=True)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({
            "questions_found": questions_found,
            "answers_found": answers_found,
            "docs_after_cleaning": len(cleaned_docs),
            "documents": cleaned_docs
        }, f, ensure_ascii=False, indent=2)

    print(f"Знайдено цільових питань: {questions_found}")
    print(f"Знайдено відповідей на них: {answers_found}")
    print(f"Очищено та збережено: {len(cleaned_docs)} текстів у {output_json}")


if __name__ == "__main__":
    extract_and_clean("data/Posts.xml", "data/cleaned_posts.json")