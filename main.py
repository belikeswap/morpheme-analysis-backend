from flask import Flask, request
from nltk.tokenize import sent_tokenize, word_tokenize
from morphemes import Morphemes

path = "./data"

m = Morphemes(path)
print(m.parse("promise"))


app = Flask(__name__)


@app.route("/analyse", methods=["POST"])
def analyze():
    if request.json and request.json["text"]:

        results = []

        text = request.json["text"]
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
    app.run(host="localhost", port=3000)
