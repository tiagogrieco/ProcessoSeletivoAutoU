import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import openai
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class NLPEngine:
    def __init__(self):
        self._ensure_nltk_resources()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('portuguese'))

    def _ensure_nltk_resources(self):
        try:
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK resources...")
            nltk.download('stopwords')
            nltk.download('wordnet')
            nltk.download('punkt')
            nltk.download('omw-1.4')

    def preprocess_text(self, text):
        """
        Cleans and tokenizes text.
        """
        # Simple tokenization and lowercasing
        words = nltk.word_tokenize(text.lower(), language='portuguese')
        # Remove stop words and non-alphabetic tokens
        cleaned = [
            self.lemmatizer.lemmatize(word) 
            for word in words 
            if word.isalpha() and word not in self.stop_words
        ]
        return " ".join(cleaned)

    def classify_and_respond(self, raw_text):
        """
        Uses OpenAI (or fallback) to classify and generate response.
        """
        if not openai.api_key:
            return self._mock_classification(raw_text)

        try:
            # Classification Prompt
            classification_response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that classifies emails into 'Produtivo' or 'Improdutivo'. Produtivo: requires action (support, request, question). Improdutivo: no action needed (thanks, greeting). Just return the category name."},
                    {"role": "user", "content": raw_text}
                ],
                max_tokens=10,
                temperature=0
            )
            category = classification_response.choices[0].message.content.strip()

            # Response Generation Prompt
            generation_response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant. The email was classified as '{category}'. specific_instructions: If Produtivo, draft a polite, professional, and concise reply acknowledging the request and promising action. If Improdutivo, draft a polite, brief thank you note. Language: Portuguese."},
                    {"role": "user", "content": raw_text}
                ],
                max_tokens=150,
                temperature=0.7
            )
            reply = generation_response.choices[0].message.content.strip()

            return {
                "category": category,
                "reply": reply,
                "raw_text_preview": raw_text if len(raw_text) <= 1000 else raw_text[:1000] + "..."
            }

        except Exception as e:
            print(f"Error invoking AI: {e}")
            return self._mock_classification(raw_text, error=str(e))

    def _mock_classification(self, text, error=None):
        """
        Fallback logic if API fails or key is missing.
        """
        try:
            processed = self.preprocess_text(text)
            productive_keywords = ['problema', 'ajuda', 'suporte', 'erro', 'falha', 'solicito', 'duvida', 'urgente', 'pagamento', 'reunião', 'entregar']
            is_productive = any(kw in processed for kw in productive_keywords)
        except Exception as e:
            # Fallback if NLTK fails
            print(f"NLP Preprocess failed: {e}")
            is_productive = 'problema' in text.lower() or 'ajuda' in text.lower()

        category = "Produtivo" if is_productive else "Improdutivo"
        
        notification = ""
        if error:
            notification = f"\n[System Note: AI API failed ({error}). Using offline heuristic.]"
        elif not openai.api_key:
            notification = "\n[System Note: No OpenAI API Key found. Using offline heuristic.]"

        if category == "Produtivo":
            reply = f"Prezado Cliente,\n\nRecebemos sua solicitação e nossa equipe técnica já está analisando. Entraremos em contato em breve.\n\nAtenciosamente,\nEquipe AutoU{notification}"
        else:
            reply = f"Olá,\n\nAgradecemos seu contato e suas palavras. Ficamos à disposição!\n\nAtenciosamente,\nEquipe AutoU{notification}"

        return {
            "category": category,
            "reply": reply,
            "raw_text_preview": text if len(text) <= 1000 else text[:1000] + "..."
        }
