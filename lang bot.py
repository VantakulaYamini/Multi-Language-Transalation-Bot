from tkinter import *
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import speech_recognition as sr
from langdetect import detect
from gtts import gTTS
from playsound import playsound
import uuid, os

LANGUAGES = {
    "en": "English", "hi": "Hindi", "te": "Telugu", "ta": "Tamil", "kn": "Kannada",
    "ml": "Malayalam", "bn": "Bengali", "mr": "Marathi", "gu": "Gujarati", "ur": "Urdu"
}

class TranslatorBot:
    def __init__(self, root):  
        self.r = sr.Recognizer()
        root.title("Language Translation Bot")
        root.geometry("700x500")
        Label(root, text="🌐 Language Translation Bot", font=("Arial", 18, "bold")).pack(pady=10)

        f = Frame(root); f.pack(pady=5)
        Label(f, text="Input Language:").grid(row=0, column=0, padx=5)
        self.in_lang = ttk.Combobox(f, values=list(LANGUAGES.values()), state="readonly", width=15)
        self.in_lang.grid(row=0, column=1, padx=5); self.in_lang.set("English")
        Label(f, text="Output Language:").grid(row=0, column=2, padx=5)
        self.out_lang = ttk.Combobox(f, values=list(LANGUAGES.values()), state="readonly", width=15)
        self.out_lang.grid(row=0, column=3, padx=5); self.out_lang.set("Hindi")

        Label(root, text="Enter text to translate:").pack(pady=5)
        self.t_in = Text(root, height=6, width=80, font=("Arial", 12)); self.t_in.pack(pady=5)

        b_f = Frame(root); b_f.pack(pady=10)
        Button(b_f, text="Translate Text", command=self.translate_text, width=18, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)
        Button(b_f, text="Speak and Translate", command=self.speak_translate, width=18, bg="#2196F3", fg="white").grid(row=0, column=1, padx=10)
        Button(b_f, text="Clear", command=self.clear, width=18, bg="#f44336", fg="white").grid(row=0, column=2, padx=10)

        Label(root, text="Translated Text:").pack()
        self.t_out = Text(root, height=6, width=80, font=("Arial", 12), state="disabled"); self.t_out.pack(pady=5)

    def get_code(self, name):
        return next((c for c, n in LANGUAGES.items() if n == name), "en")

    def translate_text(self):
        txt = self.t_in.get("1.0", END).strip()
        if not txt:
            return messagebox.showwarning("Input Required", "Please enter text.")
        src, tgt = self.get_code(self.in_lang.get()), self.get_code(self.out_lang.get())
        try:
            tr = GoogleTranslator(source=src, target=tgt).translate(txt)
            self.show_output(tr)
            self.speak(tr, tgt)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def speak_translate(self):
        src, tgt = self.get_code(self.in_lang.get()), self.get_code(self.out_lang.get())
        with sr.Microphone() as s:
            try:
                messagebox.showinfo("Listening", "Please speak now...")
                audio = self.r.listen(s, timeout=5)
                txt = self.r.recognize_google(audio, language=src)
                self.t_in.delete("1.0", END); self.t_in.insert(END, txt)
                tr = GoogleTranslator(source=detect(txt), target=tgt).translate(txt)
                self.show_output(tr)
                self.speak(tr, tgt)
            except sr.WaitTimeoutError:
                messagebox.showerror("Error", "Listening timed out.")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def speak(self, text, lang):
        try:
            f = f"v_{uuid.uuid4()}.mp3"
            gTTS(text=text, lang=lang).save(f)
            playsound(f)
            os.remove(f)
        except Exception as e:
            print("Speech error:", e)

    def show_output(self, text):
        self.t_out.config(state="normal")
        self.t_out.delete("1.0", END)
        self.t_out.insert(END, text)
        self.t_out.config(state="disabled")

    def clear(self):
        self.t_in.delete("1.0", END)
        self.t_out.config(state="normal")
        self.t_out.delete("1.0", END)
        self.t_out.config(state="disabled")



if __name__ == "__main__":
   root = Tk()
   TranslatorBot(root)
   root.mainloop()