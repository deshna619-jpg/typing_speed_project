import time
import webbrowser
import os

# Get the absolute path of your HTML file
html_path = os.path.abspath("index.html")

# Open the HTML page in your default browser
webbrowser.open(f"file://{html_path}")

# Sentence to type
sentence = "The quick brown fox jumps over the lazy dog."

input("Press Enter when you are ready to start typing...")

start = time.time()
typed = input("\nType the sentence here:\n")
end = time.time()

time_taken = end - start
words = len(typed.split())
speed = words / (time_taken / 60)

# Accuracy check
correct = 0
for i, c in enumerate(typed):
    if i < len(sentence) and c == sentence[i]:
        correct += 1
accuracy = correct / len(sentence) * 100

print(f"\nTime Taken: {round(time_taken, 2)} seconds")
print(f"Typing Speed: {round(speed, 2)} words per minute")
print(f"Accuracy: {round(accuracy, 2)}%")
