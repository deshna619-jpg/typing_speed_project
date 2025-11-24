from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from datetime import datetime
import random, os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Paragraphs for each difficulty
PARAGRAPHS = {
    "easy": [
        "Typing is one of the most basic yet important computer skills for beginners learning to type correctly helps improve speed and accuracy making everyday tasks like writing emails chatting online or even coding much smoother with regular practice typing becomes second nature and saves a lot of time when working on a computer",
        "Practice makes perfect when it comes to typing starting slow and steady helps you build confidence over time as your fingers get used to the keyboard your speed will naturally increase making everyday computer tasks easier and faster",
        "Learning to type without looking at the keyboard is a valuable skill it allows you to focus on the screen and your thoughts rather than searching for keys this improves efficiency and reduces mistakes"
    ],
    "medium": [
        "Building good digital habits is essential for anyone who spends time on computers simple actions like organizing files into proper folders keeping backups and using antivirus software can make a huge difference in maintaining a secure and efficient system regularly updating your operating system and applications ensures better performance while avoiding suspicious downloads protects your data alongside this managing your time wisely with digital planners or productivity apps helps you stay focused and prevents distractions such as social media from slowing you down",
        "Time management is one of the most important skills in the digital age using calendars reminders and productivity apps can help you stay on track and avoid wasting time on unnecessary distractions",
        "Cybersecurity is not just for experts even regular users should follow basic safety rules like using strong passwords avoiding suspicious links and keeping software updated these small steps protect your data and privacy"
    ],
    "hard": [
        "Python is a powerful and versatile programming language that has become a cornerstone of modern computing it is widely used in fields such as web development data analysis artificial intelligence machine learning and automation its clean and readable syntax makes it beginner friendly while its vast ecosystem of libraries and frameworks allows professionals to solve complex problems efficiently success in programming however is not achieved overnight it requires patience consistent practice and the ability to learn from mistakes debugging errors experimenting with new tools and adapting to evolving technologies are all part of the journey that shapes a skilled programmer",
        "Algorithms are the backbone of computer science they provide step by step instructions to solve problems efficiently understanding algorithms and data structures is crucial for writing optimized code and tackling complex challenges",
        "Machine learning has transformed industries by enabling computers to learn from data instead of being explicitly programmed it powers applications like recommendation systems voice recognition and autonomous vehicles but mastering it requires strong foundations in mathematics programming and statistics"
    ]
}

# CUSTOM ACCURACY FUNCTION
def calculate_accuracy(typed, original):
    correct = 0
    length = min(len(typed), len(original))

    for i in range(length):
        if typed[i] == original[i]:
            correct += 1

    if len(typed) == 0:
        return 0.0

    return round((correct / len(typed)) * 100, 2)


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
        time_taken = float(request.form.get('time_taken', 0))

        typed_text_clean = ' '.join(typed_text.split())
        paragraph_clean = ' '.join(paragraph.split())

        if typed_text_clean and time_taken > 0:

            typed_text_clean = typed_text.strip()
            paragraph_clean = paragraph.strip()

            paragraph_to_compare = paragraph_clean[:len(typed_text_clean)]

            accuracy = calculate_accuracy(typed_text_clean, paragraph_to_compare)

            typed_words = len(typed_text_clean.split())
            result = round(typed_words / (time_taken / 60), 2)

            # Highlight mismatches
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

@app.route('/try-again')
def try_again():
    session.pop('paragraph', None)
    session.pop('difficulty', None)
    return redirect(url_for('index'))

# Stats page (now simply empty)
@app.route('/stats')
def stats():
    return render_template("stats.html", results=[], avg_speed=0, best_speed=0)

if __name__ == "__main__":
    app.run(debug=True)
    
