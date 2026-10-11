import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

print("Loading dataset intents.csv...")
df = pd.read_csv("intents.csv")

X = df["text"]
y = df["category"]

# Split data 80/20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Feature extraction using TF-IDF
vectorizer = TfidfVectorizer(lowercase=True)
X_train_tfidf = vectorizer.fit_transform(X_train)

# Train Classifier
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Save artifacts
print("\nSaving model.pkl and vectorizer.pkl...")
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Training pipeline finished successfully!")
