import tkinter as tk
from tkinter import ttk
import threading
import sounddevice as sd
import numpy as np
import whisper
import pyperclip

# ---------------- CONFIG ----------------
SAMPLE_RATE = 16000
MODEL_NAME = "base"  # tiny / base / small
# ----------------------------------------

model = whisper.load_model(MODEL_NAME)

recording = False
audio_buffer = []

LANG_MAP = {
    "Norsk": "no",
    "English (US)": "en"
}


def audio_callback(indata, frames, time, status):
    if recording:
        audio_buffer.append(indata.copy())


def start_recording():
    global recording, audio_buffer
    audio_buffer = []
    recording = True
    status_label.config(text="🎤 Lytter...")
    threading.Thread(target=record_audio, daemon=True).start()


def record_audio():
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        callback=audio_callback,
    ):
        while recording:
            sd.sleep(100)


def stop_recording():
    global recording
    recording = False
    status_label.config(text="⏳ Transkriberer...")
    threading.Thread(target=transcribe_audio, daemon=True).start()


def transcribe_audio():
    if not audio_buffer:
        status_label.config(text="❌ Ingen lyd")
        return

    audio = np.concatenate(audio_buffer, axis=0).flatten()
    language = LANG_MAP[language_var.get()]

    # Pass audio array directly to avoid ffmpeg dependency
    result = model.transcribe(
        audio,
        language=language,
        fp16=False
    )

    text = result["text"].strip()
    pyperclip.copy(text)

    status_label.config(text="✅ Kopiert til clipboard")

    # Append to existing text if there's content, otherwise just insert
    if output_text.get("1.0", tk.END).strip():
        output_text.insert(tk.END, "\n" + text)
    else:
        output_text.insert(tk.END, text)

    # Auto-scroll to the end
    output_text.see(tk.END)


def clear_text():
    output_text.delete("1.0", tk.END)
    status_label.config(text="Klar")


# ---------------- UI ----------------
root = tk.Tk()
root.title("Tale til tekst")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

language_var = tk.StringVar(value="Norsk")

ttk.Label(frame, text="Språk:").pack(anchor="w")
language_menu = ttk.Combobox(
    frame,
    textvariable=language_var,
    values=list(LANG_MAP.keys()),
    state="readonly"
)
language_menu.pack(fill="x", pady=5)

btn_frame = ttk.Frame(frame)
btn_frame.pack(pady=10)

start_btn = ttk.Button(btn_frame, text="▶ Start", command=start_recording)
start_btn.pack(side="left", padx=5)

stop_btn = ttk.Button(btn_frame, text="■ Stopp", command=stop_recording)
stop_btn.pack(side="left", padx=5)

clear_btn = ttk.Button(btn_frame, text="🗑 Tøm", command=clear_text)
clear_btn.pack(side="left", padx=5)

status_label = ttk.Label(frame, text="Klar")
status_label.pack(pady=5)

# Scrollable text area
text_frame = ttk.Frame(frame)
text_frame.pack(fill="both", expand=True)

scrollbar = ttk.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

output_text = tk.Text(text_frame, height=8, wrap="word", yscrollcommand=scrollbar.set)
output_text.pack(side="left", fill="both", expand=True)

scrollbar.config(command=output_text.yview)

root.mainloop()
