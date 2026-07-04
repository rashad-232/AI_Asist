import os
import sys
import webbrowser
import datetime
import random

import speech_recognition as sr
import pyttsx3
import wikipedia
from dotenv import load_dotenv

load_dotenv()

ASSISTANT_NAME = "Джарвис"

engine = pyttsx3.init()
voices = engine.getProperty("voices")
for v in voices:
    if "russian" in v.name.lower() or "ru" in v.id.lower():
        engine.setProperty("voice", v.id)
        break
engine.setProperty("rate", 175)

recognizer = sr.Recognizer()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = None
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
    except ImportError:
        print("openai не установлен, ИИ-ответы отключены")


def speak(text: str):
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Слушаю...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                return ""
    except OSError:
        speak("Не вижу микрофон. Проверь подключение и разрешения.")
        return ""

    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Вы: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Нет соединения с сервисом распознавания речи")
        return ""


def ask_ai(question: str) -> str:
    if not client:
        return "Добавь OPENAI_API_KEY в .env, чтобы я мог отвечать на такие вопросы"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты голосовой ассистент. Отвечай кратко и по-русски, 1-3 предложения."},
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Не получилось обратиться к ИИ: {e}"


def handle_command(command: str) -> bool:
    if not command:
        return True

    if any(word in command for word in ["стоп", "выход", "выключись", "пока"]):
        speak("До встречи!")
        return False

    if "который час" in command or "сколько времени" in command:
        speak(f"Сейчас {datetime.datetime.now().strftime('%H:%M')}")

    elif "открой youtube" in command or "открой ютуб" in command:
        speak("Открываю YouTube")
        webbrowser.open("https://youtube.com")

    elif "открой google" in command or "открой гугл" in command:
        speak("Открываю Google")
        webbrowser.open("https://google.com")

    elif "найди в википедии" in command or "расскажи про" in command:
        query = command.split("про")[-1].strip() if "про" in command else command.replace("найди в википедии", "").strip()
        try:
            wikipedia.set_lang("ru")
            speak(wikipedia.summary(query, sentences=2))
        except Exception:
            speak("Не удалось найти информацию в Википедии")

    elif "какое сегодня число" in command or "какая сегодня дата" in command:
        speak(f"Сегодня {datetime.datetime.now().strftime('%d.%m.%Y')}")

    elif "погугли" in command or "найди в интернете" in command:
        query = command.replace("погугли", "").replace("найди в интернете", "").strip()
        speak(f"Ищу: {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "шутку" in command or "анекдот" in command:
        jokes = [
            "Программист — это устройство для превращения кофе в код.",
            "Есть только 10 типов людей: те, кто понимает двоичный код, и те, кто нет.",
            "Работает — не трогай. Не работает — тоже не трогай, сначала сделай коммит.",
        ]
        speak(random.choice(jokes))

    else:
        speak(ask_ai(command))

    return True


def main():
    speak(f"Привет! Я {ASSISTANT_NAME}, голосовой помощник. Слушаю тебя.")
    running = True
    while running:
        running = handle_command(listen())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nЗавершение работы.")
        sys.exit(0)
