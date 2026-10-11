import os
import json
import pickle
import re
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

app = Flask(__name__)

# Initialize Gemini Client (using google-genai package as specified)
try:
    client = genai.Client()
except Exception as e:
    print(f"Warning: Gemini Client initialization error: {e}")
    client = None

# Global state trackers for metrics (Part E)
analytics_data = {
    "categories": {"requirements": 0, "schedule": 0, "payment": 0, "scholarship": 0, "registrar services": 0},
    "ratings": {"thumbs_up": 0, "thumbs_down": 0}
}

# Load FAQ knowledge base (Part B)
with open("faq.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# Load ML components (Part D)
try:
    with open("model.pkl", "rb") as f:
        clf_model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        tfidf_vectorizer = pickle.load(f)
except Exception as e:
    print(f"ML artifacts not found. Run python train.py first. Error: {e}")
    clf_model, tfidf_vectorizer = None, None

def extract_meaningful_words(text):
    """Lowercase text and exclude common filler words (Part C)"""
    tokens = re.findall(r'\b\w+\b', text.lower())
    stop_words = {'the', 'ang', 'is', 'ng', 'sa', 'at', 'a', 'to', 'in', 'of', 'for', 'and', 'mga', 'na', 'ba'}
    return [t for t in tokens if t not in stop_words]

def keyword_bm25_retrieval(user_query, documents, top_n=3):
    """Finds top N documents based on overlapping vocabulary terms (Part C)"""
    query_words = set(extract_meaningful_words(user_query))
    if not query_words:
        return documents[:top_n]
    
    scored_docs = []
    for doc in documents:
        doc_words = set(extract_meaningful_words(doc["question"] + " " + doc["answer"]))
        matches = len(query_words.intersection(doc_words))
        scored_docs.append((matches, doc))
        
    # Sort descending strictly by match count integer (index 0) to avoid dict comparison crashes
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    
    # Extract only the clean document dictionary element (index 1) from the top matches
    return [item[1] for item in scored_docs[:top_n]]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    
    # Validation constraints (Part C.1)
    if not message:
        return jsonify({"error": "Message body cannot be blank."}), 400
    if len(message) > 500:
        return jsonify({"error": "Message exceeds maximum length constraint of 500 characters."}), 400
        
    # ML Predictive Classification inference tracking (Part D)
    predicted_cat = "requirements"
    if clf_model and tfidf_vectorizer:
        feats = tfidf_vectorizer.transform([message])
        preds = clf_model.predict(feats)
        if len(preds) > 0:
            predicted_cat = str(preds[0])
        
    # Bump metrics counter
    if predicted_cat in analytics_data["categories"]:
        analytics_data["categories"][predicted_cat] += 1
        
    # RAG Retrieval System matching (Part C.2)
    relevant_contexts = keyword_bm25_retrieval(message, faq_data, top_n=3)
    context_ids = [doc["id"] for doc in relevant_contexts]
    
    # Structured Prompt Construction (Part C.3)
    context_text = "\n".join([f"ID: {d['id']} | Q: {d['question']} | A: {d['answer']}" for d in relevant_contexts])
    
    system_instruction = (
        "You are an AI assistant for Bayanihan College. You must answer the user's questions based strictly "
        "on the verified context snippets provided below. Do not use external facts, do not invent policies.\n"
        "If the context does not explicitly provide the answer, you must reply precisely with: 'Pasensya na, "
        "hindi ko alam ang sagot sa tanong na iyon batay sa opisyal na impormasyon.' or 'I am sorry, but I do "
        "not know the answer based on the official guidelines.'\n"
        "Crucial: Answer in the same language style used by the user (English, Filipino, or Taglish)."
    )
    
    user_prompt = f"Context files:\n{context_text}\n\nUser Question: {message}\nAnswer:"
    
    ai_response = "Error: LLM Engine service unavailable."
    if client:
        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1
                )
            )
            ai_response = response.text.strip()
        except Exception as err:
            ai_response = f"An API connection failure occurred. Details: {str(err)}"

    return jsonify({
        "answer": ai_response,
        "ids": context_ids,
        "category": predicted_cat
    })

@app.route("/api/rating", methods=["POST"])
def submit_rating():
    data = request.get_json() or {}
    feedback_type = data.get("type") # "up" or "down"
    if feedback_type == "up":
        analytics_data["ratings"]["thumbs_up"] += 1
    elif feedback_type == "down":
        analytics_data["ratings"]["thumbs_down"] += 1
    return jsonify({"status": "success"})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    # Part E analytics compilation calculation
    total_up = analytics_data["ratings"]["thumbs_up"]
    total_down = analytics_data["ratings"]["thumbs_down"]
    grand_total = total_up + total_down
    
    positive_percentage = 100.0 if grand_total == 0 else round((total_up / grand_total) * 100, 1)
    
    return jsonify({
        "questions_per_category": analytics_data["categories"],
        "thumbs_up_percentage": positive_percentage,
        "raw_counts": analytics_data["ratings"]
    })

# Render dynamic port binding configuration (Part G Deployment requirement)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
