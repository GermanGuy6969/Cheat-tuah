import json
import tkinter as tk
from tkinter import messagebox
import os
import string
from difflib import SequenceMatcher

def load_words():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    words_file = os.path.join(script_dir, "words.json")
    
    if not os.path.exists(words_file):
        default_words = {
            "entry1": {
                "Word": "hello",
                "Definition": "a greeting or expression used to welcome someone"
            },
            "entry2": {
                "Word": "world",
                "Definition": "the earth and all the people, places, and things on it"
            }
        }
        try:
            with open(words_file, 'w') as file:
                json.dump(default_words, file, indent=4)
            messagebox.showinfo("Info", "Created new words.json file with default words")
            return default_words
        except Exception as e:
            messagebox.showerror("Error", f"Could not create words.json: {str(e)}")
            return {}

    try:
        with open(words_file, 'r') as file:
            data = json.load(file)
            if not isinstance(data, dict):
                messagebox.showerror("Error", "Invalid format in words.json!")
                return {}
            return data
    except Exception as e:
        messagebox.showerror("Error", f"Error loading words.json: {str(e)}")
        return {}

def find_exact_word(words_dict, definition):
    if not isinstance(words_dict, dict) or not definition:
        return None
    try:
        def clean_text(text):
            text = text.lower()
            text = text.translate(str.maketrans("", "", string.punctuation))
            return " ".join(text.split())

        input_def = clean_text(definition)
        input_words = set(input_def.split())
        best_match = None
        highest_ratio = 0

        for entry_id, entry_data in words_dict.items():
            if not isinstance(entry_data, dict) or 'Definition' not in entry_data:
                continue
                
            word = entry_data['Word']
            word_def = entry_data['Definition']
            clean_word_def = clean_text(word_def)
            
            if clean_word_def == input_def:
                return word
            
            if input_def in clean_word_def:
                return word
            
            if clean_word_def in input_def:
                return word

            ratio = SequenceMatcher(None, clean_word_def, input_def).ratio()
            
            word_def_words = set(clean_word_def.split())
            common_words = input_words.intersection(word_def_words)
            keyword_ratio = len(common_words) / len(input_words) if input_words else 0
            
            combined_ratio = (ratio + keyword_ratio) / 2
            
            if combined_ratio > 0.6 and combined_ratio > highest_ratio:
                highest_ratio = combined_ratio
                best_match = word

        return best_match

    except Exception as e:
        messagebox.showerror("Error", f"Search error: {str(e)}")
        return None

class WordFinderApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Word Finder")
        self.window.geometry("400x300")
        self.words_dict = load_words()

        tk.Label(self.window, text="Enter the definition:").pack(pady=10)
        self.definition_entry = tk.Text(self.window, height=5, width=40)
        self.definition_entry.pack(pady=10)

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        search_button = tk.Button(button_frame, text="Find Word", command=self.find_word)
        search_button.pack(side=tk.LEFT, padx=5)

        view_button = tk.Button(button_frame, text="View Dictionary", command=self.view_dictionary)
        view_button.pack(side=tk.LEFT, padx=5)

        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack(pady=10)

        self.status_bar = tk.Label(self.window, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.update_status()

    def find_word(self):
        definition = self.definition_entry.get("1.0", "end-1c").strip()
        if not definition:
            messagebox.showwarning("Warning", "Please enter a definition")
            return

        if not self.words_dict:
            messagebox.showwarning("Warning", "Dictionary is empty")
            return

        word = find_exact_word(self.words_dict, definition)
        if word:
            self.result_label.config(text=f"The word is: {word}")
        else:
            self.result_label.config(text="No matching word found")

    def update_status(self):
        total_entries = len(self.words_dict)
        valid_entries = sum(1 for entry in self.words_dict.values() 
                          if isinstance(entry, dict) and 'Word' in entry and 'Definition' in entry)
        self.status_bar.config(text=f"Dictionary loaded: {valid_entries} valid words out of {total_entries} entries")

    def view_dictionary(self):
        if not self.words_dict:
            messagebox.showinfo("Dictionary", "Dictionary is empty!")
            return
        
        top = tk.Toplevel(self.window)
        top.title("Dictionary")
        top.geometry("500x400")

        frame = tk.Frame(top)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        y_scrollbar = tk.Scrollbar(frame)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=y_scrollbar.set)
        text.pack(fill=tk.BOTH, expand=True)

        y_scrollbar.config(command=text.yview)

        for index, (entry_id, entry_data) in enumerate(sorted(self.words_dict.items()), 1):
            text.insert(tk.END, f"{index}. Word: {entry_data['Word']}\n")
            text.insert(tk.END, f"   Definition: {entry_data['Definition']}\n")
            text.insert(tk.END, "-" * 50 + "\n")
        
        text.config(state='disabled')

    def run(self):
        self.window.mainloop()

def main():
    if not load_words():
        messagebox.showerror("Error", "Could not load words.json file!")
        return
    
    app = WordFinderApp()
    app.run()

if __name__ == "__main__":
    main()
