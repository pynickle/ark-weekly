import os
import hashlib

from flask import Flask, render_template, request, redirect, session

from instance.convert import convert

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")

@app.route("/")
def index():
    numbers = len(os.listdir("./templates/articles"))
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
            return redirect("/post")
        else:
            return redirect("/post/recognize")

@app.route("/post")
def post():
    if session.get("recognize"):
        session["recognize"] = False
        return render_template("post.html")
    else:
        return redirect("/post/recognize")

@app.route("/post/article", methods=["POST"])
def post_article():
    article = request.form.get("article")
    numbers = len(os.listdir("./instance/articles")) + 1
    with open("./instance/articles/" + str(numbers) + ".md", "w", encoding="utf-8") as f:
        f.write(article)
    convert()
    return redirect("/")

if __name__ == "__main__":
    app.run(port = 7070)