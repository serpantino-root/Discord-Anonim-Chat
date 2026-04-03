import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import asyncio
import io
import aiohttp
from datetime import datetime, timezone
from typing import Optional
import logging

load_dotenv()

TOKEN     = os.getenv("DISCORD_TOKEN")
GUILD_ID  = int(os.getenv("GUILD_ID", 0))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN не найден в .env файле!")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("AnonChat")

class Color:
    MAIN    = 0x5865F2
    SUCCESS = 0x57F287
    ERROR   = 0xED4245
    WARN    = 0xFEE75C
    GHOST   = 0x2B2D31
    INFO    = 0x4FACC8
    PURPLE  = 0x9C59B6

ANON_AVATAR   = "https://cdn.discordapp.com/embed/avatars/1.png"
ANON_NAME     = "👤 Анонимный собеседник"
BOT_ICON      = "https://cdn.discordapp.com/embed/avatars/0.png"

intents = discord.Intents.default()
intents.message_content = True
intents.members         = True
intents.dm_messages     = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

sessions: dict[int, int] = {}
pending: dict[int, int] = {}
user_lang: dict[int, str] = {}

STRINGS: dict[str, dict[str, str]] = {
    "no_session_title":   {"ru": "👤 AnonChat",              "en": "👤 AnonChat"},
    "no_session_desc":    {"ru": "У вас нет активного анонимного чата.\n\nПерейдите на сервер и используйте `/anon @пользователь` чтобы начать анонимную переписку.",
                           "en": "You have no active anonymous chat.\n\nGo to the server and use `/anon @user` to start an anonymous conversation."},
    "no_session_footer":  {"ru": "AnonChat • Нет сессии",    "en": "AnonChat • No session"},
    "anon_name":          {"ru": "👤 Анонимный собеседник",  "en": "👤 Anonymous user"},
    "msg_footer":         {"ru": "AnonChat • Анонимное сообщение", "en": "AnonChat • Anonymous message"},
    "sticker_footer":     {"ru": "AnonChat • Стикер",        "en": "AnonChat • Sticker"},
    "photo_caption":      {"ru": "🖼️ *Фотография*",          "en": "🖼️ *Photo*"},
    "video_caption":      {"ru": "🎬 *Видеозапись*",          "en": "🎬 *Video*"},
    "file_field":         {"ru": "📎 Файл",                  "en": "📎 File"},
    "file_caption":       {"ru": "📎 *Файл*",                "en": "📎 *File*"},
    "chat_started_title": {"ru": "🔒 Анонимный чат начат",   "en": "🔒 Anonymous chat started"},
    "chat_started_desc":  {"ru": "Соединение установлено! Теперь вы можете общаться **анонимно**.\n\n> 📝 Текст\n> 🖼️ Фото\n> 🎬 Видео\n> 🎭 Стикеры\n\nИспользуйте `/stop` для завершения чата.",
                           "en": "Connection established! You can now chat **anonymously**.\n\n> 📝 Text\n> 🖼️ Photo\n> 🎬 Video\n> 🎭 Stickers\n\nUse `/stop` to end the chat."},
    "chat_started_footer":{"ru": "AnonChat • Чат начат",     "en": "AnonChat • Chat started"},
    "decline_you_title":  {"ru": "❌ Запрос отклонён",       "en": "❌ Request declined"},
    "decline_you_desc":   {"ru": "Вы отклонили приглашение в анонимный чат.", "en": "You declined the anonymous chat invitation."},
    "decline_them_desc":  {"ru": "Пользователь отклонил ваше приглашение в анонимный чат.", "en": "The user declined your anonymous chat invitation."},
    "timeout_title":      {"ru": "⏰ Запрос истёк",          "en": "⏰ Request expired"},
    "timeout_desc":       {"ru": "Пользователь не ответил на ваш запрос в течение 5 минут.", "en": "The user did not respond to your request within 5 minutes."},
    "invite_title":       {"ru": "📨 Анонимное приглашение", "en": "📨 Anonymous invitation"},
    "invite_desc":        {"ru": "**Кто-то хочет начать с вами анонимный чат.**\n\nВы не узнаете личность собеседника до завершения чата.\n\n⏰ Приглашение действует **5 минут**.",
                           "en": "**Someone wants to start an anonymous chat with you.**\n\nYou won't know their identity until the chat ends.\n\n⏰ Invitation valid for **5 minutes**."},
    "invite_footer":      {"ru": "AnonChat • Новое приглашение", "en": "AnonChat • New invitation"},
    "invite_field":       {"ru": "Принять или отклонить?",   "en": "Accept or decline?"},
    "invite_field_val":   {"ru": "Нажмите кнопку ниже:",     "en": "Press a button below:"},
    "btn_accept":         {"ru": "Принять",                  "en": "Accept"},
    "btn_decline":        {"ru": "Отклонить",                "en": "Decline"},
    "err_not_for_you":    {"ru": "Это приглашение не для вас.", "en": "This invitation is not for you."},
    "err_outdated":       {"ru": "Этот запрос уже недействителен или был отозван.", "en": "This request is no longer valid or was revoked."},
    "outdated_title":     {"ru": "⚠️ Устаревший запрос",     "en": "⚠️ Outdated request"},
    "sent_title":         {"ru": "📨 Запрос отправлен",      "en": "📨 Request sent"},
    "sent_desc":          {"ru": "Приглашение отправлено.\nОжидайте — вы получите уведомление, когда он примет запрос.\n\n⏰ Запрос действует 5 минут.",
                           "en": "Invitation sent.\nYou'll be notified when they accept.\n\n⏰ Request valid for 5 minutes."},
    "sent_footer":        {"ru": "AnonChat • Запрос в ожидании", "en": "AnonChat • Request pending"},
    "send_fail_title":    {"ru": "❌ Ошибка отправки",       "en": "❌ Send error"},
    "send_fail_desc":     {"ru": "Не удалось отправить приглашение пользователю.\nВозможно, у него закрыты личные сообщения от участников сервера.",
                           "en": "Failed to send invitation.\nThe user may have DMs disabled for server members."},
    "err_self":           {"ru": "Вы не можете начать анонимный чат сами с собой.", "en": "You cannot start an anonymous chat with yourself."},
    "err_bot":            {"ru": "Нельзя начать анонимный чат с ботом.", "en": "Cannot start an anonymous chat with a bot."},
    "err_active":         {"ru": "У вас уже есть активный анонимный чат.\nЗавершите его командой `/stop` перед началом нового.", "en": "You already have an active anonymous chat.\nUse `/stop` to end it before starting a new one."},
    "err_pending":        {"ru": "Этот пользователь уже получил запрос на анонимный чат и ещё не ответил.", "en": "This user already has a pending anonymous chat request."},
    "stop_title":         {"ru": "🔒 Чат завершён",          "en": "🔒 Chat ended"},
    "stop_desc":          {"ru": "Анонимный чат был завершён. Личности участников так и остались скрытыми.", "en": "The anonymous chat has ended. Identities remain hidden."},
    "stop_footer":        {"ru": "AnonChat • Завершено",      "en": "AnonChat • Ended"},
    "stop_partner_desc":  {"ru": "Ваш собеседник завершил анонимный чат.", "en": "Your chat partner ended the anonymous chat."},
    "stop_partner_footer":{"ru": "AnonChat • Завершено партнёром", "en": "AnonChat • Ended by partner"},
    "no_chat_title":      {"ru": "❌ Нет активного чата",    "en": "❌ No active chat"},
    "no_chat_desc":       {"ru": "У вас нет активного анонимного чата.\nНачните новый с помощью `/anon @пользователь`.", "en": "You have no active anonymous chat.\nStart one with `/anon @user`."},
    "status_active_title":{"ru": "🟢 Чат активен",           "en": "🟢 Chat active"},
    "status_active_desc": {"ru": "У вас есть **активный анонимный чат**.\n\nПишите боту в личные сообщения — они анонимно доставляются собеседнику.\n\nДля завершения используйте `/stop`.",
                           "en": "You have an **active anonymous chat**.\n\nWrite to the bot in DMs — messages are delivered anonymously.\n\nUse `/stop` to end it."},
    "status_pending_title":{"ru": "⏳ Запрос в ожидании",    "en": "⏳ Request pending"},
    "status_pending_desc": {"ru": "Вы отправили запрос на анонимный чат. Ожидайте ответа...", "en": "You sent an anonymous chat request. Waiting for a response..."},
    "status_none_title":  {"ru": "🔴 Нет активного чата",    "en": "🔴 No active chat"},
    "status_none_desc":   {"ru": "У вас нет активного анонимного чата.\n\nНачните новый командой `/anon @пользователь` на сервере.", "en": "You have no active anonymous chat.\n\nStart one with `/anon @user` on the server."},
    "unavail_title":      {"ru": "⚠️ Собеседник недоступен", "en": "⚠️ Partner unavailable"},
    "unavail_desc":       {"ru": "Не удалось доставить сообщение. Возможно, собеседник заблокировал бота или закрыл ЛС.\n**Сессия завершена.**",
                           "en": "Failed to deliver message. The partner may have blocked the bot or closed DMs.\n**Session ended.**"},
    "fwd_label":          {"ru": "*📨 Пересланное сообщение:*\n\n", "en": "*📨 Forwarded message:*\n\n"},
    "fwd_footer":         {"ru": "AnonChat • Пересланное сообщение", "en": "AnonChat • Forwarded message"},
    "fwd_media_footer":   {"ru": "AnonChat • Медиа (переслано)", "en": "AnonChat • Media (forwarded)"},
    "lang_title":         {"ru": "🌐 Язык изменён",          "en": "🌐 Language changed"},
    "lang_desc_ru":       {"ru": "Язык бота установлен на **Русский**.", "en": "Bot language set to **Russian**."},
    "lang_desc_en":       {"ru": "Язык бота установлен на **English**.", "en": "Bot language set to **English**."},
    "lang_footer":        {"ru": "AnonChat • Настройки",      "en": "AnonChat • Settings"},
    "help_title":         {"ru": "👤 AnonChat — Справка",     "en": "👤 AnonChat — Help"},
    "help_desc":          {"ru": "**Бот для полностью анонимного общения в Discord.**\nВаша личность скрыта на протяжении всего чата.", "en": "**A bot for fully anonymous messaging in Discord.**\nYour identity is hidden throughout the chat."},
    "help_commands":      {"ru": "📋 Команды",                "en": "📋 Commands"},
    "help_commands_val":  {"ru": "`/anon @пользователь` — отправить приглашение в анонимный чат\n`/stop` — завершить текущий чат\n`/status` — посмотреть статус вашего чата\n`/lang` — сменить язык\n`/help` — эта справка",
                           "en": "`/anon @user` — send an anonymous chat invitation\n`/stop` — end the current chat\n`/status` — view chat status\n`/lang` — change language\n`/help` — this help"},
    "help_formats":       {"ru": "📦 Поддерживаемые форматы", "en": "📦 Supported formats"},
    "help_formats_val":   {"ru": "📝 Текст · 🖼️ Фото · 🎬 Видео\n🎭 Стикеры · 📎 Файлы", "en": "📝 Text · 🖼️ Photo · 🎬 Video\n🎭 Stickers · 📎 Files"},
    "help_anon":          {"ru": "🔒 Как работает анонимность?", "en": "🔒 How does anonymity work?"},
    "help_anon_val":      {"ru": "Бот пересылает сообщения без указания отправителя.\nНикто — включая администраторов сервера — не узнает вашу личность.", "en": "The bot forwards messages without revealing the sender.\nNo one — including server admins — will know your identity."},
    "help_start":         {"ru": "⚡ Как начать?",            "en": "⚡ How to start?"},
    "help_start_val":     {"ru": "1. Введите `/anon @пользователь` на сервере\n2. Получатель получит приглашение в ЛС\n3. После принятия — пишите боту в личные сообщения!", "en": "1. Type `/anon @user` on the server\n2. The recipient gets a DM invitation\n3. After accepting — message the bot in DMs!"},
    "help_footer":        {"ru": "AnonChat v2.0 • /help",     "en": "AnonChat v2.0 • /help"},
}

def t(user_id: int, key: str) -> str:
    lang = user_lang.get(user_id, "ru")
    return STRINGS.get(key, {}).get(lang, STRINGS.get(key, {}).get("ru", key))

def anon_name(user_id: int) -> str:
    return t(user_id, "anon_name")

def now() -> datetime:
    return datetime.now(timezone.utc)

def make_embed(
    title: str = "",
    description: str = "",
    color: int = Color.MAIN,
    footer: str = "AnonChat",
    thumbnail: Optional[str] = None,
    timestamp: bool = True,
) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=now() if timestamp else None,
    )
    embed.set_footer(text=footer, icon_url=BOT_ICON)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    return embed

def is_in_session(user_id: int) -> bool:
    return user_id in sessions

async def end_session(user_id: int) -> Optional[int]:
    partner_id = sessions.pop(user_id, None)
    if partner_id:
        sessions.pop(partner_id, None)
    return partner_id

async def safe_dm(user: discord.User, **kwargs) -> bool:
    try:
        await user.send(**kwargs)
        return True
    except (discord.Forbidden, discord.HTTPException) as e:
        log.warning("Не удалось отправить ЛС пользователю %s: %s", user.id, e)
        return False

async def fetch_as_file(url: str, filename: str) -> Optional[discord.File]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status != 200:
                    return None
                data = await resp.read()
                return discord.File(io.BytesIO(data), filename=filename)
    except Exception as e:
        log.warning("Не удалось скачать файл %s: %s", url, e)
        return None

async def resolve_user(user_id: int) -> Optional[discord.User]:
    try:
        return await bot.fetch_user(user_id)
    except Exception:
        return None

@bot.event
async def on_ready():
    log.info("Бот %s запущен и готов к работе!", bot.user)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="👤 анонимные чаты | /help"
        )
    )
    try:
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
        else:
            synced = await bot.tree.sync()
        log.info("Синхронизировано %d команд(ы).", len(synced))
    except Exception as e:
        log.error("Ошибка синхронизации команд: %s", e)

class InviteView(discord.ui.View):
    def __init__(self, sender_id: int, target_id: int):
        super().__init__(timeout=300)
        self.sender_id = sender_id
        self.target_id = target_id

    @discord.ui.button(label="✅ Принять", style=discord.ButtonStyle.success)
    async def accept_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        uid = interaction.user.id
        if uid != self.target_id:
            await interaction.response.send_message(
                embed=make_embed("❌", t(uid, "err_not_for_you"), Color.ERROR),
                ephemeral=True,
            )
            return

        if self.target_id not in pending or pending[self.target_id] != self.sender_id:
            embed = make_embed(t(uid, "outdated_title"), t(uid, "err_outdated"), Color.WARN)
            await interaction.response.edit_message(embed=embed, view=None)
            return

        del pending[self.target_id]
        sessions[self.sender_id] = self.target_id
        sessions[self.target_id] = self.sender_id

        self.stop()

        start_embed = make_embed(
            t(self.target_id, "chat_started_title"),
            t(self.target_id, "chat_started_desc"),
            Color.SUCCESS,
            thumbnail=ANON_AVATAR,
            footer=t(self.target_id, "chat_started_footer"),
        )
        await interaction.response.edit_message(embed=start_embed, view=None)

        sender = await resolve_user(self.sender_id)
        if sender:
            sender_embed = make_embed(
                t(self.sender_id, "chat_started_title"),
                t(self.sender_id, "chat_started_desc"),
                Color.SUCCESS,
                thumbnail=ANON_AVATAR,
                footer=t(self.sender_id, "chat_started_footer"),
            )
            await safe_dm(sender, embed=sender_embed)

        log.info("Сессия создана: %d ↔ %d", self.sender_id, self.target_id)

    @discord.ui.button(label="❌ Отклонить", style=discord.ButtonStyle.danger)
    async def decline_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        uid = interaction.user.id
        if uid != self.target_id:
            await interaction.response.send_message(
                embed=make_embed("❌", t(uid, "err_not_for_you"), Color.ERROR),
                ephemeral=True,
            )
            return

        if self.target_id in pending:
            del pending[self.target_id]

        self.stop()

        decline_embed = make_embed(
            t(self.target_id, "decline_you_title"),
            t(self.target_id, "decline_you_desc"),
            Color.ERROR,
            footer=t(self.target_id, "stop_footer"),
        )
        await interaction.response.edit_message(embed=decline_embed, view=None)

        sender = await resolve_user(self.sender_id)
        if sender:
            notif = make_embed(
                t(self.sender_id, "decline_you_title"),
                t(self.sender_id, "decline_them_desc"),
                Color.ERROR,
                footer=t(self.sender_id, "stop_footer"),
            )
            await safe_dm(sender, embed=notif)

        log.info("Запрос от %d к %d отклонён.", self.sender_id, self.target_id)

    async def on_timeout(self):
        if self.target_id in pending and pending[self.target_id] == self.sender_id:
            del pending[self.target_id]

        sender = await resolve_user(self.sender_id)
        if sender:
            expire = make_embed(
                t(self.sender_id, "timeout_title"),
                t(self.sender_id, "timeout_desc"),
                Color.WARN,
                footer="AnonChat • Таймаут",
            )
            await safe_dm(sender, embed=expire)

        log.info("Приглашение от %d к %d истекло.", self.sender_id, self.target_id)
        log.info("Приглашение от %d к %d истекло.", self.sender_id, self.target_id)

if __name__ == "__main__":
    bot.run(TOKEN, log_handler=None)