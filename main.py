from flask import Flask, render_template, request
import os
from pdf_reader import read_pdf
from qa_engine import answer_question

app = Flask(__name__, template_folder='templates')

document_text = ""

@app.route("/", methods=["GET", "POST"])
def home():
    global document_text
    response = ""
    if request.method == "POST":
        if "pdf" in request.files:
            file = request.files["pdf"]
            if file.filename != "":
                os.makedirs("uploads", exist_ok=True)
                path = os.path.join("uploads", file.filename)
                file.save(path)
                document_text = read_pdf(path)
        question = request.form.get("question", "")
        if question:
            if document_text:
                response = answer_question(question, document_text)
            else:
                response = "Pehle PDF upload karo"
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
