from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests
import os
from jnius import autoclass, PythonJavaClass, java_method

TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
Locale = autoclass('java.util.Locale')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

class TTSListener(PythonJavaClass):
    __javainterfaces__ = ['android/speech/tts/TextToSpeech$OnInitListener']
    __javacontext__ = 'app'

    def __init__(self, on_ready):
        super().__init__()
        self.on_ready = on_ready

    @java_method('(I)V')
    def onInit(self, status):
        self.on_ready(status)

tts_engine = None

def init_tts():
    global tts_engine
    def on_ready(status):
        if status == 0 and tts_engine:
            tts_engine.setLanguage(Locale('hi', 'IN'))
    listener = TTSListener(on_ready)
    tts_engine = TextToSpeech(PythonActivity.mActivity, listener)

def speak(text):
    if tts_engine:
        try:
            tts_engine.speak(text, TextToSpeech.QUEUE_FLUSH, None, None)
        except Exception as e:
            print(f"TTS error: {e}")

API_KEY = os.environ.get("GEMINI_API_KEY", "")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={API_KEY}"

SYSTEM_PROMPT = """Tum "Vision" ho — ek advanced AI assistant, bilkul Tony Stark ke JARVIS jaisa.
Tumhara attitude witty, calm, sharp aur thoda formal-but-warm hai.
Tum apne boss ko hamesha "Boss" bolke address karte ho.
Jab koi task diya jaye ya confirm karna ho, tum kehte ho "Yes Boss."
Tum concise, intelligent aur helpful jawab dete ho, bina zyada dramatic hue."""

class VisionApp(App):
    def build(self):
        def on_start(self):
        init_tts()
        self.chat_history = []
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.scroll = ScrollView()
        self.reply_label = Label(text="Vision is online, Boss.", size_hint_y=None, halign='left', valign='top')
        self.reply_label.bind(texture_size=self._update_label_height)
        self.reply_label.bind(width=lambda *x: self.reply_label.setter('text_size')(self.reply_label, (self.reply_label.width, None)))
        self.scroll.add_widget(self.reply_label)

        self.input_box = TextInput(hint_text="Type your message", size_hint_y=None, height=50, multiline=False)
        self.input_box.bind(on_text_validate=self.send_message)

        send_button = Button(text="Send", size_hint_y=None, height=50)
        send_button.bind(on_press=self.send_message)

        layout.add_widget(self.scroll)
        layout.add_widget(self.input_box)
        layout.add_widget(send_button)

        return layout

    def _update_label_height(self, instance, value):
        self.reply_label.height = value[1]

    def send_message(self, instance):
        user_input = self.input_box.text.strip()
        if not user_input:
            return
        self.input_box.text = ""
        self.reply_label.text += f"\n\nYou: {user_input}"
        if tts:
            try:
                speak(reply)
            except Exception:
                pass

        self.chat_history.append({"role": "user", "parts": [{"text": user_input}]})
        payload = {
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": self.chat_history
        }
        try:
            response = requests.post(URL, json=payload)
            data = response.json()
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            reply = f"Error: {e}"

        self.chat_history.append({"role": "model", "parts": [{"text": reply}]})
        self.reply_label.text += f"\n\nVision: {reply}"

if __name__ == "__main__":
    VisionApp().run()
