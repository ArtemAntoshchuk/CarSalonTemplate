import yaml
from app.keyboards.keyboards_enum import KeyboardsVariant
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# todo check location and modificator for method
def load_menu(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

class KeyboardService:
    @staticmethod
    def _create_aiogram_keyboard__(keyboard_type:str):
        menu_data = load_menu("resources/keyboard_pressets/keyboard.yaml")[keyboard_type.lower()]
        menu_type = menu_data.get("type", "REPLY")
        buttons = menu_data.get("buttons", [])

        if menu_type == "REPLY":
            return KeyboardService.__parse_reply_kb(buttons)
        elif menu_type == "INLINE":
            return KeyboardService.__parse_inline_kb(buttons)
        else:
            raise ValueError("Unknown menu type in YAML")

    @staticmethod
    def __parse_reply_kb(buttons):
        keyboard = []
        for row in buttons:
            keyboards_row = []
            for btn in row:
                button = KeyboardButton(text=btn)
                keyboards_row.append(button)
            keyboard.append(keyboards_row)

        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


    @staticmethod
    def __parse_inline_kb(buttons):
        keyboard = InlineKeyboardMarkup()
        for row in buttons:
            keyboard_row = []
            for btn in row:
                if isinstance(btn, dict):
                    text = btn.get("text")
                    callback_data = btn.get("callback", text)
                    keyboard_row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
                else:
                    keyboard_row.append(InlineKeyboardButton(text=btn, callback_data=btn))
            keyboard.row(*keyboard_row)
        return keyboard


def get_keyboard(kb_type: KeyboardsVariant):
    return KeyboardService._create_aiogram_keyboard__(kb_type.value)
