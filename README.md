# enrollment-assistant
# Bayanihan College - Enrollment Helpdesk Chat Assistant

An educational retrieval-augmented generation (RAG) platform incorporating an ML-based intent classifier and a strict contextual guardrail verification layout.

## Local Installation Guide
1. Open the repository inside your development workstation container environment.
2. Initialize environment library requirements via shell:
   ```bash
   pip install flask scikit-learn google-genai pandas
   ```
3. Generate the required machine learning artifacts:
   ```bash
   python train.py
   ```
4. Define your active platform security credentials:
   ```bash
   export GEMINI_API_KEY="your-actual-api-key-here"
   ```
5. Run the local Flask server framework:
   ```bash
   python app.py
   ```
6. Access the interfaces via browser at `http://127.0.0` (Chat Interface) and `http://127.0.0admin` (Dashboard Metrics Panel).

## Core RAG System Prompt Instruction Design
```text
You are an AI assistant for Bayanihan College. You must answer the user's questions based strictly on the verified context snippets provided below. Do not use external facts, do not invent policies.
If the context does not explicitly provide the answer, you must reply precisely with: 'Pasensya na, hindi ko alam ang sagot sa tanong na iyon batay sa opisyal na impormasyon.' or 'I am sorry, but I do not know the answer based on the official guidelines.'
Crucial: Answer in the same language style used by the user (English, Filipino, or Taglish).
```

## Intention Model Error Analysis Documentation
* **Confused Intent Matrix Categories:** The trained Multinomial Naive Bayes classifier exhibits potential confusion structural collisions between the `requirements` category and the `registrar services` category.
* **Underlying Failure Reason:** This happens because words like *documents*, *records*, *certificates*, and *submission* frequently overlap in both categories (e.g., submitting enrollment requirements vs. requesting certified records). Because the TF-IDF feature space maps identical word components across these categories, questions containing these shared terms may occasionally be misclassified without deeper contextual analysis.
