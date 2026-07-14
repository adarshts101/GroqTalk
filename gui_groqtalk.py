import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
import requests
from dotenv import load_dotenv

# Load .env file to get GROQ_API_KEY
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "whisper-large-v3"

# === Transcription Logic ===
def send_to_groq(audio_path):
    if not GROQ_API_KEY:
        messagebox.showerror("API Key Missing", "Please set your Groq API Key in the .env file.")
        return None

    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }
    files = {
        "file": (os.path.basename(audio_path), open(audio_path, "rb")),
        "model": (None, MODEL),
    }

    try:
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            return response.json()["text"]
        else:
            messagebox.showerror("Error", f"API Error: {response.text}")
            return None
    except Exception as e:
        messagebox.showerror("Exception", str(e))
        return None

# === File Chooser ===
def choose_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.ogg")]
    )
    if file_path:
        file_label.config(text=os.path.basename(file_path))
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, "🔁 Transcribing... Please wait...\n")
        root.update()

        transcription = send_to_groq(file_path)

        result_box.delete(1.0, tk.END)
        if transcription:
            result_box.insert(tk.END, transcription)
        else:
            result_box.insert(tk.END, "❌ Failed to transcribe.")

# === Save Transcription ===
def save_transcription():
    text = result_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showinfo("Empty", "There is no transcription to save.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if save_path:
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Saved", f"Transcription saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Couldn't save file.\n{str(e)}")

# === GUI Setup ===
root = tk.Tk()
root.title("🎙️ GroqTalk – Whisper AI Transcriber")
root.geometry("720x580")
root.resizable(False, False)
root.configure(bg="#1e1e2f")

# === Fonts & Styles ===
title_font = ("Segoe UI", 18, "bold")
label_font = ("Segoe UI", 11)
text_font = ("Consolas", 10)
button_bg = "#00ADB5"
button_fg = "#ffffff"

# === Title ===
tk.Label(root,
         text="GroqTalk – Upload Audio & Get Transcription",
         font=title_font,
         fg="#eeeeee",
         bg="#1e1e2f").pack(pady=(25, 10))

# === Select File Button ===
tk.Button(root,
          text="📁 Select Audio File",
          command=choose_file,
          font=("Segoe UI", 12, "bold"),
          bg=button_bg,
          fg=button_fg,
          relief="flat",
          padx=12,
          pady=6).pack()

# === Save Button ===
tk.Button(root,
          text="💾 Save Transcription",
          command=save_transcription,
          font=("Segoe UI", 11, "bold"),
          bg="#393E46",
          fg="white",
          relief="flat",
          padx=10,
          pady=5).pack(pady=(5, 10))

# === File Label ===
file_label = tk.Label(root,
                      text="No file selected",
                      fg="#cccccc",
                      bg="#1e1e2f",
                      font=label_font)
file_label.pack(pady=(0, 5))

# === Result Box Frame ===
result_frame = tk.Frame(root, bg="#eeeeee", bd=2, relief="ridge")
result_frame.pack(padx=25, pady=15, fill=tk.BOTH, expand=True)

result_box = scrolledtext.ScrolledText(result_frame,
                                       wrap=tk.WORD,
                                       width=80,
                                       height=20,
                                       font=text_font,
                                       bg="#f9f9f9",
                                       fg="#222222",
                                       insertbackground="black",
                                       borderwidth=0)
result_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# === Footer ===
tk.Label(root,
         text="⚡ Powered by Groq + Whisper",
         font=("Segoe UI", 9),
         bg="#1e1e2f",
         fg="#888888").pack(pady=5)

# === Launch App ===
root.mainloop()
