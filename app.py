from flask import Flask, render_template, request
from transformers import pipeline
from newspaper import Article
import re

app = Flask(__name__)

# Use lighter model (recommended)
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

def is_url(text):
    url_pattern = re.compile(
        r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$'
    )
    return re.match(url_pattern, text.strip()) is not None

def extract_article_from_url(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    user_input = request.form.get('article').strip()

    try:
        # Auto-detect URL or Text
        if is_url(user_input):
            article_text = extract_article_from_url(user_input)
        else:
            article_text = user_input

        if len(article_text.split()) < 50:
            summary = "Content is too short to generate a meaningful summary."
        else:
            result = summarizer(
                article_text,
                max_length=150,
                min_length=50,
                do_sample=False
            )
            summary = result[0]['summary_text']

    except Exception:
        summary = "Unable to process the article. Please try another input."

    return render_template(
        'index.html',
        summary=summary,
        article=user_input
    )

if __name__ == '__main__':
    app.run(debug=True)
