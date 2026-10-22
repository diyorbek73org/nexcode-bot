import asyncio
import datetime
import html
import logging
import random
import sqlite3
import sys
import time

from aiogram import Bot, Dispatcher, F, BaseMiddleware
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    TelegramObject,
)
from typing import Callable, Dict, Any, Awaitable

# ============================================================
# ⚙️ SOZLAMALAR
# ============================================================

TOKEN = "8638814634:AAFAPqHNUq_2vbGpU3n6cVmLvcG7vWYTmRw"

OWNER_USERNAME = "@D778s"

ADMIN_IDS = {
    8703647047,
    8256060918,
}

PRIMARY_ADMIN_ID = 8703647047

DB_FILE = "nexcode_menedjer.db"

DAILY_REWARD = 100
WORK_COOLDOWN = 60
DAILY_COOLDOWN = 86400

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s 🌟 %(levelname)s 🌟 %(name)s 🌟 %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger("NexcodeMenedjerBot")
dp = Dispatcher(storage=MemoryStorage())


# ============================================================
# 🎮 FSM (HOLATLAR)
# ============================================================

class GameState(StatesGroup):
    waiting_for_currency = State()
    waiting_for_amount = State()
    waiting_for_choice = State()


# ============================================================
# ⌨️ ASOSIY MENYU TUGMALARI
# ============================================================

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 𝑃𝑅𝑂𝐹𝐼𝐿"), KeyboardButton(text="🏢 𝐵𝐼𝑍𝑁𝐸𝑆")],
        [KeyboardButton(text="🛒 𝐷𝑂'𝐾𝑂𝑁"), KeyboardButton(text="🎁 𝐾𝑈𝑁𝐿𝐼𝐾 𝐵𝑂𝑁𝑈𝑆")],
        [KeyboardButton(text="🎮 𝑂'𝑌𝐼𝑁𝐿𝐴𝑅 𝑀𝐸𝑁𝑌𝑈𝑆𝐼"), KeyboardButton(text="🏆 𝑇𝑂𝑃 𝑅𝐸𝑌𝑇𝐼𝑁𝐺")],
    ],
    resize_keyboard=True,
)


# ============================================================
# 🗄 MA’LUMOTLAR BAZASI
# ============================================================

class Database:
    def __init__(self, db_file=DB_FILE):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL DEFAULT '',
                messages INTEGER DEFAULT 0,
                karma INTEGER DEFAULT 0,
                balance INTEGER DEFAULT 250,
                almaz INTEGER DEFAULT 0,
                gender TEXT DEFAULT 'Aniqlanmagan ❓',
                points INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                last_bonus REAL DEFAULT 0,
                last_work REAL DEFAULT 0,
                last_daily REAL DEFAULT 0,
                warnings INTEGER DEFAULT 0,
                inventory TEXT DEFAULT 'Yo''q',
