from flask import Flask, request
from flask_cors import CORS
from nltk import download
from nltk.tokenize import sent_tokenize, word_tokenize
from morphemes import Morphemes

download("punkt_tab")

path = "./data"

m = Morphemes(path)
print(m.parse("promise"))


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "HEAD", "OPTIONS"])
def home():
    return "OK", 200


@app.route("/keep-alive", methods=["GET"])
def keep_alive():
    return "OK", 200


@app.route("/analyse", methods=["POST"])
def analyze():
    data = request.get_json()
    if data and data["text"]:

        results = []

        text = data["text"]
        sentences = sent_tokenize(text)
        for s in sentences:
            words = word_tokenize(s)
            for index, word in enumerate(words):
                result = m.parse(word)
                result["index"] = index
                results.append(result)

        return results
    else:
        return "Not Found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
