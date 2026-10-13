from enum import Enum

# enum defined for registration available keyboards
class KeyboardsVariant(Enum):
    START_KEYBOARD = "start_menu"
    PHONE_KB = "phone_kb"
    NAVI_KB = "navi_kb_copy"
    NAVI_KB_FAVOURITES = "navi_kb_copy_in_favorites"
    ADD_PHOTOS_KB = "add_photos_kb"
    SKIP_CONTINUE_KB = "skip_continue_kb"
    WAS_IN_ACCIDENT_KB = "was_in_accident_kb"
    ENGINE_CUSTOM_OR_NOT = "engine_custom_or_not"
    YES_OR_NO_KB = "yes_or_no_kb"
    PENTA_GENIUS_KB = "penta_genius_kb"
