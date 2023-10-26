__all__ = []
import re
from datetime import datetime


def normalize_text(text: str):
    text = text.lower()
    pattern = {
        'а': 'a',
        'в': 'b',
        'е': 'e',
        'к': 'k',
        'м': 'm',
        'о': 'o',
        'т': 't',
        'с': 'c',
        'р': 'p',
        'х': 'x',
        ' ': '',
    }

    # Замена похожих букв
    for rus_letter, eng_letter in pattern.items():
        text = re.sub(rus_letter, eng_letter, text)

    # Удаление знаков препинания
    text = re.sub(r'[^\w\s]', '', text)
    return text


def get_server_time_context():
    context = {'server_time': str(datetime.now().year)}
    return context
