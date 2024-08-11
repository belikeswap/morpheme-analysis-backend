from flask import Flask, request
from nltk import download
from nltk.tokenize import sent_tokenize, word_tokenize
from morphemes import Morphemes

download("punkt_tab")

path = "./data"

m = Morphemes(path)
print(m.parse("promise"))


app = Flask(__name__)


def application(environ, start_response):
    if environ["REQUEST_METHOD"] == "OPTIONS":
        start_response(
            "200 OK",
            [
                ("Content-Type", "application/json"),
                ("Access-Control-Allow-Origin", "*"),
                ("Access-Control-Allow-Headers", "Authorization, Content-Type"),
                ("Access-Control-Allow-Methods", "POST"),
            ],
        )
        return ""


@app.route("/analyse", methods=["POST"])
def analyze():
    data = request.get_json()
    if data and data["text"]:

        results = []

        text = data["text"]
        sentences = sent_tokenize(text)
        for s in sentences:
            words = word_tokenize(s)
            parts = []
            for index, word in enumerate(words):
                parts.append(m.parse(word))

            results.append({"word": word, "index": index, "parts": parts})

        return results
    else:
        return "Not Found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
