from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from datetime import datetime
import random, json, os
import difflib

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

RESULTS_FILE = "results.json"

# Paragraphs for each difficulty
PARAGRAPHS = {
    "easy": [
        "Typing is one of the most basic yet important computer skills for beginners learning to type correctly helps improve speed and accuracy making everyday tasks like writing emails chatting online or even coding much smoother with regular practice typing becomes second nature and saves a lot of time when working on a computer"
    ],
    "medium": [
        "Building good digital habits is essential for anyone who spends time on computers simple actions like organizing files into proper folders keeping backups and using antivirus software can make a huge difference in maintaining a secure and efficient system regularly updating your operating system and applications ensures better performance while avoiding suspicious downloads protects your data alongside this managing your time wisely with digital planners or productivity apps helps you stay focused and prevents distractions such as social media from slowing you down"
    ],
    "hard": [
        "Python is a powerful and versatile programming language that has become a cornerstone of modern computing it is widely used in fields such as web development data analysis artificial intelligence machine learning and automation its clean and readable syntax makes it beginner friendly while its vast ecosystem of libraries and frameworks allows professionals to solve complex problems efficiently success in programming however is not achieved overnight it requires patience consistent practice and the ability to learn from mistakes debugging errors experimenting with new tools and adapting to evolving technologies are all part of the journey that shapes a skilled programmer"
    ]
}

# Save a result
def save_result(speed, accuracy):
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

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    typed_text = ""
    result = None
    accuracy = None
    highlighted_paragraph = ""

    # Get difficulty
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

        # Clean whitespace for accurate comparison
        typed_text_clean = ' '.join(typed_text.split())
        paragraph_clean = ' '.join(paragraph.split())

        if typed_text_clean and time_taken > 0:
            # Clean typed text and paragraph
            typed_text_clean = typed_text.strip()
            paragraph_clean = paragraph.strip()
            # Only compare the portion that the user typed
            paragraph_to_compare = paragraph_clean[:len(typed_text_clean)]
            matcher = difflib.SequenceMatcher(None, typed_text_clean, paragraph_to_compare)
            accuracy = round(matcher.ratio() * 100, 2)


            # WPM = typed words / time in minutes
            typed_words = len(typed_text_clean.split())
            result = round(typed_words / (time_taken / 60), 2)

            save_result(result, accuracy)

            # Highlight mismatched words character-by-character
            original_words = paragraph_clean.split()
            typed_words_list = typed_text_clean.split()
            highlighted_words = []

            for i, word in enumerate(original_words):
                if i < len(typed_words_list):
                    typed_word = typed_words_list[i]
                    highlighted_word = ''
                    for j, c in enumerate(word):
                        if j < len(typed_word) and typed_word[j] == c:
                            highlighted_word += f'<span class="correct">{c}</span>'
                        else:
                            highlighted_word += f'<span class="incorrect">{c}</span>'
                    # If typed_word is longer than the original word, mark extra chars incorrect
                    if len(typed_word) > len(word):
                        for extra_char in typed_word[len(word):]:
                            highlighted_word += f'<span class="incorrect">{extra_char}</span>'
                    highlighted_words.append(highlighted_word)
                else:
                    highlighted_words.append(''.join(f'<span class="incorrect">{c}</span>' for c in word))

            highlighted_paragraph = " ".join(highlighted_words)
        else:
            result = 0
            accuracy = 0.0
            highlighted_paragraph = paragraph_clean

    # AJAX difficulty switch
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
        highlighted_paragraph=highlighted_paragraph,
        difficulty=difficulty
    )

# Try again
@app.route('/try-again')
def try_again():
    session.pop('paragraph', None)
    session.pop('difficulty', None)
    return redirect(url_for('index'))

# Stats page
@app.route('/stats')
def stats():
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
