import math

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
                # todo change logic for phone num request kb
                if btn == "Поділитись контактом📞":
                    button.request_contact = True
                keyboards_row.append(button)
            keyboard.append(keyboards_row)

        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


    @staticmethod
    def __parse_inline_kb(buttons):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        rows = []
        for row in buttons:
            keyboard_row = []
            for btn in row:
                if isinstance(btn, dict):
                    text = btn.get("text")
                    callback_data = btn.get("callback", text)
                    print(callback_data)
                    keyboard_row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
                else:
                    keyboard_row.append(InlineKeyboardButton(text=btn, callback_data=btn))
            rows.append(keyboard_row)

        keyboard.inline_keyboard = rows
        return keyboard

    @staticmethod
    def generate_inline_keyboards_by_list(data_list, callback_data_body, columns):
        keyword = []
        rows = len(data_list) / columns
        if isinstance(rows, float):
            rows = int(math.floor(rows)) + 1
        index = 0
        for row in range(rows):
            rows_list = []
            current_column = columns
            while current_column % columns != 0 or current_column == columns:
                if index < len(data_list):
                    btn = InlineKeyboardButton(text = data_list[index], callback_data=f"{callback_data_body}_{index}")
                    rows_list.append(btn)
                    index +=1
                current_column -= 1
            keyword.append(rows_list)
        return InlineKeyboardMarkup(inline_keyboard=keyword)

    #it works only with the objects that have a name argument
    @staticmethod
    def generate_inline_keyboards_by_list_objects(list_objects, columns, callback_data_body):
        keyword = []
        rows = len(list_objects) / columns
        if isinstance(rows, float):
            rows = int(math.floor(rows)) + 1
        index = 0
        for row in range(rows):
            rows_list = []
            current_column = columns
            while current_column % columns != 0 or current_column == columns:
                if index < len(list_objects):
                    btn = InlineKeyboardButton(text = list_objects[index].name, callback_data=f"{callback_data_body}_{list_objects[index].id}")
                    rows_list.append(btn)
                    index += 1
                current_column -= 1
            keyword.append(rows_list)
        return InlineKeyboardMarkup(inline_keyboard=keyword)


def get_keyboard(kb_type: KeyboardsVariant):
    return KeyboardService._create_aiogram_keyboard__(kb_type.value)

def get_kb_inline_by_list(data_list, callback_data_body, columns):
    return KeyboardService.generate_inline_keyboards_by_list(data_list, callback_data_body, columns)

def get_kb_inline_by_list_objects(list_objects, columns, callback_data_body):
    return KeyboardService.generate_inline_keyboards_by_list_objects(list_objects, columns, callback_data_body)

