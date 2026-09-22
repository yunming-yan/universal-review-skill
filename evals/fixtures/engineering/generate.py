from pathlib import Path

def render():
    return Path(__file__).with_name('template.txt').read_text(encoding='utf-8')
