from flask import Flask, request, jsonify
from ai_summarizer import process_notes

app = Flask(__name__)


@app.route("/api/summarize", methods=["POST"])
def generate_summary():
    data = request.get_json(silent=True) or {}
    notes = data.get("notes", "")

    if not isinstance(notes, str) or not notes.strip():
        return jsonify({
            "error": "Please enter meeting notes."
        }), 400

    if len(notes) > 50000:
        return jsonify({
            "error": "Notes must be under 50,000 characters."
        }), 400

    result = process_notes(notes)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
