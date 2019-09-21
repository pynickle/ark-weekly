import os
import pypandoc

def convert():
    for i in range(1, len(os.listdir("instance/articles")) + 1):
        output = pypandoc.convert_file("instance/articles/" + str(i) + ".md", "html")
        with open("templates/articles/" + str(i) + ".html", "w", encoding="utf-8") as f:
            f.write(output)