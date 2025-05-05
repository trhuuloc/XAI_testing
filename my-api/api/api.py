from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Sample premises and reasoning logic (replace with your model)
premises_db = {
    "0": "Every course contains knowledge.",
    "1": "Does Natural Language Processing Semester 242 contain knowledge?"
}

def reason(premises, question):
    if question in premises_db.values():
        return {"answer": "Yes", "idx": [list(premises_db.keys())[list(premises_db.values()).index(question)]]}
    elif any("contains knowledge" in p for p in premises_db.values()):
        return {"answer": "Yes", "idx": [str(i) for i, p in premises_db.items() if "contains knowledge" in p]}
    return {"answer": "Uncertain", "idx": []}

def generate_explanation(idx, answer):
    if answer == "Yes" and idx:
        return ["Premise " + i + " states that the course contains knowledge, supporting the answer." for i in idx]
    return ["No relevant premises found to determine the answer."]

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        premises = data.get("premises", [])
        questions = data.get("questions", [])

        if not questions:
            return jsonify({"error": "No questions provided"}), 400

        results = []
        for question in questions:
            result = reason(premises, question)
            result["explanation"] = generate_explanation(result["idx"], result["answer"])
            results.append(result)

        return jsonify({"answers": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)