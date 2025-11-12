from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from datetime import datetime
import random, json, os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Paragraphs for each difficulty
PARAGRAPHS = {
    "easy": [
        "Typing is one of the most basic yet important computer skills for beginners. Learning to type correctly helps improve speed and accuracy, making everyday tasks like writing emails, chatting online, or even coding much smoother. With regular practice, typing becomes second nature and saves a lot of time when working on a computer."
    ],
    "medium": [
        "Building good digital habits is essential for anyone who spends time on computers. Simple actions like organizing files into proper folders, keeping backups, and using antivirus software can make a huge difference in maintaining a secure and efficient system. Regularly updating your operating system and applications ensures better performance, while avoiding suspicious downloads protects your data. Alongside this, managing your time wisely with digital planners or productivity apps helps you stay focused and prevents distractions such as social media from slowing you down."
    ],
    "hard": [
        "Python is a powerful and versatile programming language that has become a cornerstone of modern computing. It is widely used in fields such as web development, data analysis, artificial intelligence, machine learning, and automation. Its clean and readable syntax makes it beginner-friendly, while its vast ecosystem of libraries and frameworks allows professionals to solve complex problems efficiently. Success in programming, however, is not achieved overnight—it requires patience, consistent practice, and the ability to learn from mistakes. Debugging errors, experimenting with new tools, and adapting to evolving technologies are all part of the journey that shapes a skilled programmer."
    ]
}

RESULTS_FILE = "results.json"


def save_result(speed, accuracy):
    """Save a single test result to a JSON file."""
    record = {
        "speed": speed,
        "accuracy": accuracy,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    results = []
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r") as f:
                results = json.load(f)
        except json.JSONDecodeError:
            results = []
    results.append(record)
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=4)


@app.route('/', methods=['GET', 'POST'])
def index():
    typed_text = ""
    result = None
    accuracy = None

    # Get difficulty from form (POST) or query param (GET)
    difficulty = request.values.get('difficulty', 'medium')
    if difficulty not in PARAGRAPHS:
        difficulty = 'medium'

    # Reset paragraph if new difficulty selected
    if 'paragraph' not in session or session.get('difficulty') != difficulty:
        session['paragraph'] = random.choice(PARAGRAPHS[difficulty])
        session['difficulty'] = difficulty

    paragraph = session['paragraph']

    if request.method == 'POST':
        typed_text = request.form.get('typed_text', '').strip()
        time_taken = float(request.form.get('time_taken', 0))  # seconds

        if typed_text and time_taken > 0:
            typed_words = typed_text.split()
            original_words = paragraph.split()

            correct_words = sum(
                1 for i in range(min(len(typed_words), len(original_words)))
                if typed_words[i] == original_words[i]
            )

            total_typed_words = len(typed_words)
            accuracy = round((correct_words / total_typed_words) * 100, 2) if total_typed_words else 0
            result = round(correct_words / (time_taken / 60), 2)  # WPM
            save_result(result, accuracy)
        else:
            result = 0
            accuracy = 0.0

    # For AJAX updates (difficulty switch)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        new_paragraph = random.choice(PARAGRAPHS[difficulty])
        session['paragraph'] = new_paragraph
        session['difficulty'] = difficulty
        return jsonify({'paragraph': new_paragraph, 'difficulty': difficulty})

    return render_template(
        'index.html',
        paragraph=paragraph,
        typed_text=typed_text,
        result=result,
        accuracy=accuracy,
        difficulty=difficulty
    )


@app.route('/try-again')
def try_again():
    session.pop('paragraph', None)
    session.pop('difficulty', None)
    return redirect(url_for('index'))


@app.route('/stats')
def stats():
    """Show all previous results and average/best speeds."""
    results = []
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r") as f:
                results = json.load(f)
        except json.JSONDecodeError:
            results = []

    speeds = [r["speed"] for r in results]
    avg_speed = round(sum(speeds) / len(speeds), 2) if speeds else 0
    best_speed = max(speeds) if speeds else 0
    return render_template("stats.html", results=results, avg_speed=avg_speed, best_speed=best_speed)

if __name__ == "__main__":
    app.run(debug=True)
