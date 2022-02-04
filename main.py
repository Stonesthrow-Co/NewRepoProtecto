import markdown
import json
from flask import Flask
import markdown.extensions.fenced_code

app = Flask(__name__)



@app.route("/")
def index():
    """
    Reads in the README.md file and returns it rendered as HTML.
    :return: [string] HTML rendering of the README.md file
    """
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )
    return md_template_string


if __name__ == "__main__":
    app.run()