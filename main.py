from flask import Flask, render_template, request, session
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # required for session

# Long paragraphs
PARAGRAPHS = [
    "python is a powerful programming language that is widely used in web development data analysis artificial intelligence machine learning and automation its simplicity readability and versatility make it a favorite among beginners and professionals learning python can open many opportunities in software development data science and other tech careers practicing python regularly helps improve coding skills and problem solving",
    
    "effective time management is crucial for students and professionals prioritize tasks set realistic goals avoid procrastination and manage deadlines efficiently using calendars reminders and task tracking tools can help stay organized creating daily routines focusing on important tasks and breaking down large projects into smaller parts improves productivity over time disciplined time management reduces stress and helps achieve better results in academic and professional work",
    
    "typing is an essential skill for programmers writers and office workers it improves productivity allows fast communication and reduces errors practicing typing daily helps increase speed and accuracy focusing on each word maintaining correct posture and minimizing distractions enhances performance consistent practice leads to better typing skills and confidence for work or exams using proper typing techniques ensures long term efficiency and reduces fatigue"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    typed_text = ""
    result = None
    accuracy = None

    # Select paragraph if not in session
    if 'paragraph' not in session:
        session['paragraph'] = random.choice(PARAGRAPHS)
    paragraph = session['paragraph']

    if request.method == 'POST':
        typed_text = request.form['typed_text'].strip()
        start_time = float(request.form['start_time'])
        end_time = datetime.now().timestamp()
        time_taken = end_time - start_time

        typed_words = typed_text.split()
        original_words = paragraph.split()

        # Count only correctly typed words
        correct_words = 0
        for i in range(len(typed_words)):
            if i < len(original_words) and typed_words[i] == original_words[i]:
                correct_words += 1

        total_typed_words = len(typed_words) if len(typed_words) > 0 else 1
        accuracy = round((correct_words / total_typed_words) * 100, 2)

        # WPM counts only correct words
        result = round(correct_words / (time_taken / 60), 2)

    return render_template('index.html',
                           paragraph=paragraph,
                           typed_text=typed_text,
                           result=result,
                           accuracy=accuracy,
                           start_time=datetime.now().timestamp())

@app.route('/try-again')
def try_again():
    # Change paragraph randomly on Try Again
    session['paragraph'] = random.choice(PARAGRAPHS)
    return "<script>window.location.href='/'</script>"

if __name__ == "__main__":
    app.run(debug=True)







