<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          👤   A N O N C H A T   B O T                       ║
║                                                              ║
║          Anonymous Messenger for Discord                     ║
║          Анонимный мессенджер для Discord                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-57F287?style=for-the-badge)

</div>

---

# 🇬🇧 English

## What is AnonChat?

**AnonChat** is a Discord bot that allows server members to chat with each other **completely anonymously**. No one — including server administrators — will ever know who is behind the messages. Identities are hidden from start to finish.

## ✨ Features

| Feature | Description |
|---|---|
| 🔒 Full anonymity | Identities are never revealed during the chat |
| 📝 Text messages | Send any text anonymously |
| 🖼️ Photos | Forward images directly |
| 🎬 Video | Send videos with inline playback |
| 🎭 Stickers | Discord stickers forwarded with preview |
| 📎 Files | Any file type forwarded with size info |
| 📨 Forwarded messages | Forward any DM message — text and media are relayed |
| 🌐 Bilingual | Each user chooses their own language (RU / EN) |
| ⏰ Auto-expiry | Chat invitations expire after 5 minutes |
| ✅ Delivery receipts | Reaction confirms message was delivered |

## ⚙️ Commands

| Command | Description |
|---|---|
| `/anon @user` | Send an anonymous chat invitation to a server member |
| `/stop` | End your current anonymous chat session |
| `/status` | Check whether you have an active chat |
| `/lang` | Switch your language (🇷🇺 Russian / 🇬🇧 English) |
| `/help` | Show the help guide |

## 🚀 Installation

### 1. Clone or download the bot file

```
anonchat_bot.py
.env
requirements.txt
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your `.env` file

```env
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
GUILD_ID=0
LOG_LEVEL=INFO
```

> `GUILD_ID=0` — commands are registered globally (may take up to 1 hour to sync).  
> Set it to your server's ID for instant sync during development.

### 4. Set up Discord Developer Portal

Go to [discord.com/developers](https://discord.com/developers/applications) → Your App → **Bot**:

- ✅ Enable **Message Content Intent**
- ✅ Enable **Server Members Intent**

Under **OAuth2 → URL Generator**, select:
- Scopes: `bot`, `applications.commands`
- Permissions: `Send Messages`, `Read Message History`

### 5. Run

```bash
python anonchat_bot.py
```

## 🔄 How It Works

```
Server member A                   Bot                    Server member B
      │                            │                            │
      │──── /anon @B ─────────────>│                            │
      │                            │──── DM: invitation ───────>│
      │<─── "Request sent" ────────│          [Accept] [Decline]│
      │                            │<──── clicks Accept ────────│
      │<─── "Chat started" ────────│──── "Chat started" ───────>│
      │                            │                            │
      │──── DM message ───────────>│──── forwarded anon ───────>│
      │<─────────────────── ✅ ────│                            │
      │                            │                            │
      │──── /stop ────────────────>│──── "Chat ended" ─────────>│
```

---

---

# 🇷🇺 Русский

## Что такое AnonChat?

**AnonChat** — это Discord-бот, позволяющий участникам сервера общаться **полностью анонимно**. Никто — включая администраторов сервера — никогда не узнает, кто стоит за сообщениями. Личности скрыты с начала и до конца чата.

## ✨ Возможности

| Функция | Описание |
|---|---|
| 🔒 Полная анонимность | Личности не раскрываются в течение всего чата |
| 📝 Текстовые сообщения | Отправка любого текста анонимно |
| 🖼️ Фотографии | Пересылка изображений напрямую |
| 🎬 Видео | Отправка видео со встроенным плеером |
| 🎭 Стикеры | Стикеры Discord пересылаются с превью |
| 📎 Файлы | Любые файлы с указанием размера |
| 📨 Пересланные сообщения | Перешлите любое ЛС — текст и медиа будут доставлены |
| 🌐 Двуязычность | Каждый пользователь выбирает свой язык (RU / EN) |
| ⏰ Авто-истечение | Приглашения в чат истекают через 5 минут |
| ✅ Подтверждение доставки | Реакция подтверждает, что сообщение доставлено |

## ⚙️ Команды

| Команда | Описание |
|---|---|
| `/anon @пользователь` | Отправить приглашение в анонимный чат участнику сервера |
| `/stop` | Завершить текущую сессию анонимного чата |
| `/status` | Проверить, есть ли у вас активный чат |
| `/lang` | Сменить язык (🇷🇺 Русский / 🇬🇧 English) |
| `/help` | Показать справку по боту |

## 🚀 Установка

### 1. Скачайте файлы бота

```
anonchat_bot.py
.env
requirements.txt
```

### 2. Установите зависимости

```bash
pip install -r requirements.txt
```

### 3. Настройте файл `.env`

```env
DISCORD_TOKEN=ВАШ_ТОКЕН_ЗДЕСЬ
GUILD_ID=0
LOG_LEVEL=INFO
```

> `GUILD_ID=0` — команды регистрируются глобально (синхронизация до 1 часа).  
> Укажите ID вашего сервера для мгновенной синхронизации во время разработки.

### 4. Настройте Discord Developer Portal

Перейдите на [discord.com/developers](https://discord.com/developers/applications) → Ваше приложение → **Bot**:

- ✅ Включите **Message Content Intent**
- ✅ Включите **Server Members Intent**

В разделе **OAuth2 → URL Generator** выберите:
- Scopes: `bot`, `applications.commands`
- Permissions: `Send Messages`, `Read Message History`

### 5. Запустите

```bash
python anonchat_bot.py
```

## 🔄 Как это работает

```
Участник А                        Бот                        Участник Б
      │                            │                            │
      │──── /anon @Б ─────────────>│                            │
      │                            │──── ЛС: приглашение ──────>│
      │<─── "Запрос отправлен" ────│     [Принять] [Отклонить] │
      │                            │<──── нажимает Принять ─────│
      │<─── "Чат начат" ───────────│──── "Чат начат" ──────────>│
      │                            │                            │
      │──── сообщение в ЛС ───────>│──── анонимно ─────────────>│
      │<─────────────────── ✅ ────│                            │
      │                            │                            │
      │──── /stop ────────────────>│──── "Чат завершён" ───────>│
```

---

## 📁 Структура проекта

```
anonchat_bot.py     — основной файл бота
.env                — токен и конфигурация (не публиковать!)
.env.example        — шаблон конфигурации
requirements.txt    — зависимости Python
README.md           — эта документация
```

## 📦 Зависимости / Dependencies

```
discord.py >= 2.3.0
python-dotenv >= 1.0.0
aiohttp >= 3.9.0
```

---

<div align="center">

Made with ❤️ for anonymous conversations

*AnonChat Bot — your identity, always protected*

</div>
