import re
from sentence_transformers import SentenceTransformer, util
from intents import INTENTS, ENTITIES


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
intent_embeddings = {
    intent: model.encode(phrases, normalize_embeddings=True)
    for intent, phrases in INTENTS.items()
}

def classify_intent(text, threshold=0.75):
    emb = model.encode(text, normalize_embeddings=True)
    best_intent, best_score = None, 0
    for intent, emb_list in intent_embeddings.items():
        score = util.cos_sim(emb, emb_list).max().item()
        if score > best_score:
            best_score, best_intent = score, intent
    return (best_intent, best_score) if best_score >= threshold else (None, best_score)

def find_entity(text):
    text = text.lower()
    for entity, keywords in ENTITIES.items():
        if any(re.search(rf"\b{re.escape(k)}\b", text) for k in keywords):
            return entity
    return None

def extract_volume_value(text):
    match = re.search(r"\b(\d{1,3})\b", text)
    return int(match.group(1)) if match and 0 <= int(match.group(1)) <= 100 else None

def extract_track_query(text):
    triggers = ["play", "put on", "start"]
    for t in sorted(triggers, key=len, reverse=True):
        if text.lower().startswith(t):
            return text[len(t):].strip()
    return None

WAKE_WORDS = ["jarvis"]

def parse_command(command_text):
    text = command_text.lower().strip()
    if not any(text.startswith(w) for w in WAKE_WORDS):
        return None, None, None, False

    for w in WAKE_WORDS:
        if text.startswith(w):
            text = text[len(w):].strip()
            break
        
    track_query = extract_track_query(text)
    if track_query:
        return "play_track", None, track_query, True

    intent, score = classify_intent(text)
    entity = find_entity(text)
    value = None
    system_command = True

    if intent is None:
        intent = "ask_llm"
        system_command = False
        value = text
        return intent, None, value, system_command

    if intent == "set_volume":
        value = extract_volume_value(text)

    return intent, entity, value, system_command