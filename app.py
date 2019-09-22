import os
import re
import hashlib

from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import pypandoc

from instance.convert import convert

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")

@app.route("/")
def index():
    numbers = len(os.listdir("./templates/articles")) - 1
    return render_template("index.html", numbers = numbers)

@app.route("/article/<int:number>")
def article(number):
    return render_template("articles/" + str(number) + ".html")

@app.route("/post/recognize", methods=["POST", "GET"])
def recognize():
    if request.method == "GET":
        return render_template("recognize.html")
    else:
        password = request.form.get("password")
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        if md5.hexdigest() == '1431d23edb7b88d900a10b68da06e7b1':
            session["recognize"] = True
            if request.form.get("type") == "1":
                return redirect("/post/hand")
            else:
                return redirect("/post/pdf")
        else:
            return redirect("/post/recognize")

@app.route("/post/hand")
def post():
    if session.get("recognize"):
        session["recognize"] = False
        return render_template("post.html")
    else:
        return redirect("/post/recognize")

@app.route("/post/pdf", methods=["GET", "POST"])
def post_pdf():
    if request.method == "GET":
        if session.get("recognize"):
            session["recognize"] = False
            return render_template("post-pdf.html")
        else:
            return redirect('/post/recognize')
    else:
        if "file" not in request.files:
            return redirect("/post/pdf")
        file = request.files["file"]
        if file.filename == "":
            return redirect("/post/pdf")
        filename = secure_filename(file.filename)
        path = "./instance/pdf/" + filename
        file.save(path)
        r = os.popen("pdf2html " + path)
        output = r.read()
        numbers = len(os.listdir("./templates/articles"))
        output = output.replace("<title>None</title>", "<title>方舟周报（第" + str(numbers) + "期）</title>")
        output += "<link rel='stylesheet' href=\"{{ url_for('static', filename='article.css') }}\" type='text/css'>"
        with open("./templates/articles/" + str(numbers) + ".html", "w", encoding="utf-8") as f:
            f.write(output)
        return redirect("/")

@app.route("/post/article", methods=["POST"])
def post_article():
    article = request.form.get("article")
    numbers = len(os.listdir("./instance/articles"))
    with open("./instance/articles/" + str(numbers) + ".md", "w", encoding="utf-8") as f:
        f.write(article)
    convert()
    return redirect("/")

if __name__ == "__main__":
    app.run(port = 7070)