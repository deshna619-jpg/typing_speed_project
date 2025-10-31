from flask import Flask, render_template, request
import time, random   # ← Added random here

app = Flask(__name__)

# Multiple paragraphs to choose from
paragraphs = [
    "Python is a powerful and easy to learn programming language.",
    "Flask allows developers to create web applications using simple Python code.",
    "Programming helps develop problem solving and logical thinking skills.",
    "Data structures like lists, tuples, and dictionaries make Python very flexible.",
    "Learning to code improves creativity and analytical abilities among students."
]

@app.route("/", methods=["GET", "POST"])
def index():
    paragraph = random.choice(paragraphs)   # ← Randomly pick one each time

    if request.method == "POST":
        user_input = request.form["typed_text"]
        start_time = float(request.form["start_time"])
        end_time = time.time()

        total_time = end_time - start_time
        words = len(user_input.split())
        speed = round(words / (total_time / 60), 2) if total_time > 0 else 0

        # Calculate accuracy
        correct_chars = 0
        for i in range(min(len(paragraph), len(user_input))):
            if paragraph[i] == user_input[i]:
                correct_chars += 1
        accuracy = round((correct_chars / len(paragraph)) * 100, 2)

        return render_template("index.html", paragraph=paragraph, speed=speed, accuracy=accuracy, done=True)

    return render_template("index.html", paragraph=paragraph, done=False)

if __name__ == "__main__":
    app.run(debug=True)

