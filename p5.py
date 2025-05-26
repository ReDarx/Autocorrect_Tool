import re
import nltk
import tkinter as tk
from tkinter import scrolledtext
from nltk.tokenize import sent_tokenize
from spellchecker import SpellChecker
from transformers import pipeline
nltk.download('punkt', quiet=True)
grammar_corrector = pipeline("text2text-generation", model="vennify/t5-base-grammar-correction")
spell = SpellChecker()

def correct_spelling(text):
    corrected_words = []
    for word in text.split():
        # Preserve apostrophes and punctuation
        cleaned = re.sub(r"[^\w']", '', word)
        if cleaned.lower() in spell or not cleaned:
            corrected_words.append(word)
        else:
            correction = spell.correction(cleaned)
            corrected_word = word.replace(cleaned, correction)
            corrected_words.append(corrected_word)
    return " ".join(corrected_words)
# Grammar correction function
def correct_grammar(text):
    sentences = sent_tokenize(text)
    corrected_sentences = []
    for sentence in sentences:
        result = grammar_corrector(sentence, max_length=256, do_sample=False)
        corrected_sentences.append(result[0]['generated_text'])
    return " ".join(corrected_sentences)
#F.Pipeline
def autocorrect_pipeline(text):
    spelling_fixed = correct_spelling(text)
    grammar_fixed = correct_grammar(spelling_fixed)
    return grammar_fixed
# GUI
def run_gui():
    def process_text():
        user_input = input_text.get("1.0", tk.END).strip()
        if user_input:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Processing...\n")
            root.update_idletasks()
            try:
                corrected = autocorrect_pipeline(user_input)
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, corrected)
            except Exception as e:
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, f"Error: {str(e)}")

    root = tk.Tk()
    root.title("Grammar & Spell Checker")

    tk.Label(root, text="Enter your text below:").pack()

    input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
    input_text.pack(padx=10, pady=5)

    tk.Button(root, text="Correct Text", command=process_text).pack(pady=10)

    tk.Label(root, text="Corrected Output:").pack()

    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
    output_text.pack(padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
