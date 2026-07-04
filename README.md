# 🎙️ Voice AI Assistant (Голосовой помощник с ИИ)

Голосовой помощник для ПК на Python: распознаёт речь, отвечает голосом, выполняет команды и (опционально) отвечает на любые вопросы через OpenAI GPT.

## Возможности
- 🎤 Распознавание речи с микрофона (Google Speech Recognition)
- 🔊 Озвучка ответов (pyttsx3, работает офлайн)
- ⏰ Время и дата
- 🌐 Открытие сайтов (YouTube, Google)
- 📚 Поиск в Wikipedia
- 🔍 Поиск в интернете
- 😄 Шутки
- 🤖 Ответы на произвольные вопросы через OpenAI GPT (если указан API-ключ)

## Установка

```bash
git clone https://github.com/yourusername/voice-ai-assistant.git
cd voice-ai-assistant
pip install -r requirements.txt
```

> На Windows PyAudio иногда не ставится через pip напрямую — используйте:
> `pip install pipwin && pipwin install pyaudio`

## Настройка ИИ-режима (необязательно)

1. Скопируйте `.env.example` в `.env`
2. Впишите свой ключ:
```
OPENAI_API_KEY=sk-...
```
Без ключа ассистент всё равно работает: доступны все базовые команды.

## Запуск

```bash
python main.py
```

Скажите, например:
- «Который час?»
- «Открой ютуб»
- «Расскажи про Пушкина»
- «Расскажи шутку»
- Любой другой вопрос — если подключён ИИ

## Технологии
Python · SpeechRecognition · pyttsx3 · OpenAI API · Wikipedia API

## Лицензия
MIT
