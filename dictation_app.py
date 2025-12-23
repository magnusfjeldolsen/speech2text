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
is_transcribing = False
text_was_modified = False

LANG_MAP = {
    "English (US)": "en",
    "Norsk": "no"
}


def audio_callback(indata, frames, time, status):
    if recording:
        audio_buffer.append(indata.copy())


def start_recording():
    global recording, audio_buffer
    if recording or is_transcribing:
        return
    audio_buffer = []
    recording = True
    status_label.config(text="Recording...")
    start_btn.config(state="disabled")
    stop_btn.config(state="normal")
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
    if not recording:
        return
    recording = False
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")
    status_label.config(text="Transcribing...")
    threading.Thread(target=transcribe_audio, daemon=True).start()


def transcribe_audio():
    global is_transcribing, text_was_modified
    is_transcribing = True

    if not audio_buffer:
        status_label.config(text="No audio detected")
        is_transcribing = False
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

    status_label.config(text="Copied to clipboard")

    # Append to existing text if there's content, otherwise just insert
    if output_text.get("1.0", tk.END).strip():
        output_text.insert(tk.END, "\n" + text)
    else:
        output_text.insert(tk.END, text)

    # Auto-scroll to the end
    output_text.see(tk.END)
    text_was_modified = False
    is_transcribing = False


def clear_text():
    global text_was_modified
    output_text.delete("1.0", tk.END)
    status_label.config(text="Ready")
    text_was_modified = False


def on_text_modified(event=None):
    """Called when user manually edits the text field"""
    global text_was_modified
    current_status = status_label.cget("text")
    if current_status == "Copied to clipboard":
        status_label.config(text="Text modified")
        text_was_modified = True


def copy_selected_text(event=None):
    """Copy selected text to clipboard with Ctrl+C"""
    try:
        selected_text = output_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        if selected_text:
            pyperclip.copy(selected_text)
            if text_was_modified:
                status_label.config(text="Selection copied (modified)")
            else:
                status_label.config(text="Selection copied")
    except tk.TclError:
        # No selection, copy all text
        all_text = output_text.get("1.0", tk.END).strip()
        if all_text:
            pyperclip.copy(all_text)
            if text_was_modified:
                status_label.config(text="All text copied (modified)")
            else:
                status_label.config(text="All text copied")
    return "break"


def copy_all_text():
    """Copy all text from the text field"""
    all_text = output_text.get("1.0", tk.END).strip()
    if all_text:
        pyperclip.copy(all_text)
        if text_was_modified:
            status_label.config(text="All text copied (modified)")
        else:
            status_label.config(text="All text copied")
    else:
        status_label.config(text="No text to copy")


def toggle_recording(event=None):
    if recording:
        stop_recording()
    elif not is_transcribing:
        start_recording()


def handle_delete(event=None):
    clear_text()
    return "break"


# ---------------- UI ----------------
root = tk.Tk()
root.title("Speech to Text")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

language_var = tk.StringVar(value="English (US)")

ttk.Label(frame, text="Language:").pack(anchor="w")
language_menu = ttk.Combobox(
    frame,
    textvariable=language_var,
    values=list(LANG_MAP.keys()),
    state="readonly"
)
language_menu.pack(fill="x", pady=5)

btn_frame = ttk.Frame(frame)
btn_frame.pack(pady=10)

start_btn = ttk.Button(btn_frame, text="Start (Space)", command=start_recording)
start_btn.pack(side="left", padx=5)

stop_btn = ttk.Button(btn_frame, text="Stop (Space)", command=stop_recording, state="disabled")
stop_btn.pack(side="left", padx=5)

clear_btn = ttk.Button(btn_frame, text="Clear (Del)", command=clear_text)
clear_btn.pack(side="left", padx=5)

copy_btn = ttk.Button(btn_frame, text="Copy All", command=copy_all_text)
copy_btn.pack(side="left", padx=5)

status_label = ttk.Label(frame, text="Ready")
status_label.pack(pady=5)

# Scrollable text area
text_frame = ttk.Frame(frame)
text_frame.pack(fill="both", expand=True)

scrollbar = ttk.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

output_text = tk.Text(text_frame, height=8, wrap="word", yscrollcommand=scrollbar.set)
output_text.pack(side="left", fill="both", expand=True)

scrollbar.config(command=output_text.yview)

# Detect text modifications
output_text.bind("<<Modified>>", on_text_modified)
output_text.bind("<KeyRelease>", on_text_modified)

# Keyboard shortcuts
root.bind("<space>", toggle_recording)
root.bind("<Delete>", handle_delete)
output_text.bind("<Control-c>", copy_selected_text)
output_text.bind("<Control-C>", copy_selected_text)

root.mainloop()
