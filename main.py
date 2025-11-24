from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import random
from difflib import SequenceMatcher  

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # to secure the session

# Sample paragraphs for different difficulty levels
PARAGRAPHS = {
    "easy": [
        "Algorithms are the backbone of computer science they provide step by step instructions to solve problems efficiently understanding algorithms and data structures is crucial for writing optimized code and tackling complex challenges",
        "Time management is one of the most important skills in the digital age using calendars reminders and productivity apps can help you stay on track and avoid wasting time on unnecessary distractions",
        "Cybersecurity is not just for experts even regular users should follow basic safety rules like using strong passwords avoiding suspicious links and keeping software updated these small steps protect your data and privacy"
    ],
    "medium": [
        "Typing is one of the most basic yet important computer skills for beginners learning to type correctly helps improve speed and accuracy making everyday tasks like writing emails chatting online or even coding much smoother with regular practice typing becomes second nature and saves a lot of time when working on a computer",
        "Practice makes perfect when it comes to typing starting slow and steady helps you build confidence over time as your fingers get used to the keyboard your speed will naturally increase making everyday computer tasks easier and faster",
        "Learning to type without looking at the keyboard is a valuable skill it allows you to focus on the screen and your thoughts rather than searching for keys this improves efficiency and reduces mistakes"
    ],
    "hard": [
        "Python is a powerful and versatile programming language that has become a cornerstone of modern computing it is widely used in fields such as web development data analysis artificial intelligence machine learning and automation its clean and readable syntax makes it beginner friendly while its vast ecosystem of libraries and frameworks allows professionals to solve complex problems efficiently success in programming however is not achieved overnight it requires patience consistent practice and the ability to learn from mistakes debugging errors experimenting with new tools and adapting to evolving technologies are all part of the journey that shapes a skilled programmer",
        "Building good digital habits is essential for anyone who spends time on computers simple actions like organizing files into proper folders keeping backups and using antivirus software can make a huge difference in maintaining a secure and efficient system regularly updating your operating system and applications ensures better performance while avoiding suspicious downloads protects your data alongside this managing your time wisely with digital planners or productivity apps helps you stay focused and prevents distractions such as social media from slowing you down",
        "Machine learning has transformed industries by enabling computers to learn from data instead of being explicitly programmed it powers applications like recommendation systems voice recognition and autonomous vehicles but mastering it requires strong foundations in mathematics programming and statistics"
    ]
}

# Function to calculate accuracy
def calculate_accuracy(typed, original):
    if not typed:
        return 0.0
    return round(SequenceMatcher(None, typed, original).ratio() * 100, 2)


@app.route('/', methods=['GET', 'POST'])
def index():
    typed_text = ""
    result = None
    accuracy = None

    # Get difficulty from request or default to medium
    difficulty = request.values.get('difficulty', 'medium')
    if difficulty not in PARAGRAPHS:
        difficulty = 'medium'  # Fallback to medium if invalid

    # Pick a paragraph if new session or difficulty changed
    if 'paragraph' not in session or session.get('difficulty') != difficulty:
        session['paragraph'] = random.choice(PARAGRAPHS[difficulty])
        session['difficulty'] = difficulty

    paragraph = session['paragraph']

    if request.method == 'POST':
        typed_text = request.form.get('typed_text', '').strip()
        time_taken = float(request.form.get('time_taken', 0))

        if typed_text and time_taken > 0:
            paragraph_to_compare = paragraph[:len(typed_text)]
            accuracy = calculate_accuracy(typed_text, paragraph_to_compare)
            typed_words = len(typed_text.split())
            result = round(typed_words / (time_taken / 60), 2)
        else:
            result = 0
            accuracy = 0.0

    # Handle AJAX request for new paragraph
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        new_paragraph = random.choice(PARAGRAPHS[difficulty])
        session['paragraph'] = new_paragraph
        session['difficulty'] = difficulty
        return jsonify({'paragraph': new_paragraph, 'difficulty': difficulty})

    # Send to main typing test page
    return render_template(
        'index.html',
        paragraph=paragraph,
        typed_text=typed_text,
        result=result,
        accuracy=accuracy,
        difficulty=difficulty
    )

@app.route('/try-again') # Route to reset the test
def try_again():
    session.pop('paragraph', None)
    session.pop('difficulty', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
