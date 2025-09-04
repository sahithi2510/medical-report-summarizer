from transformers import pipeline
import os

MODEL_NAME = os.getenv("SUMMARIZER_MODEL", "sshleifer/distilbart-cnn-12-6")
summarizer = pipeline("summarization", model=MODEL_NAME)

def _chunk_text(text, max_chars=1200):
    text = (text or "").strip()
    if len(text) <= max_chars:
        return [text]
    paragraphs = text.split("\n\n")
    chunks, cur = [], ""
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if len(cur) + len(p) + 2 <= max_chars:
            cur = f"{cur}\n\n{p}" if cur else p
        else:
            if cur:
                chunks.append(cur)
            if len(p) > max_chars:
                sentences = p.split(". ")
                cur2 = ""
                for s in sentences:
                    s = s.strip()
                    if not s:
                        continue
                    if len(cur2) + len(s) + 2 <= max_chars:
                        cur2 = f"{cur2}. {s}" if cur2 else s
                    else:
                        if cur2:
                            chunks.append(cur2.strip() + ".")
                        cur2 = s
                if cur2:
                    chunks.append(cur2.strip() + ".")
                cur = ""
            else:
                cur = p
    if cur:
        chunks.append(cur)
    return chunks

def generate_summary(text):
    if not text:
        return "No text found to summarize."

    preface = (
        "Summarize the following medical report in simple language that anyone can understand. "
        "Avoid medical jargon, or if you must use a term, explain it in plain words. "
        "Organize with short headings or bullet points when useful.\n\n"
    )
    chunks = _chunk_text(text, max_chars=1200)
    summaries = []
    for chunk in chunks:
        inp = preface + chunk
        result = summarizer(inp, max_length=220, min_length=40, do_sample=False)
        summaries.append(result[0]["summary_text"].strip())

    if len(summaries) == 1:
        return summaries[0]
    else:
        aggregate = " ".join(summaries)
        final = summarizer(preface + aggregate, max_length=220, min_length=50, do_sample=False)
        return final[0]["summary_text"].strip()
