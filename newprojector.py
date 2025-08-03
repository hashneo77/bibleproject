import tkinter as tk
from tkinter import ttk
import csv
import sys
import os
import unicodedata

def normalize_text(text):
    if not text:
        return ''
    text = unicodedata.normalize('NFKC', text)
    text = text.replace('\u200d', '')  # zero width joiner removal
    text = text.replace('\u00A0', ' ') # non-breaking space to normal space
    return text.strip()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def safe_int(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return -1

# Load CSV data
data = []
with open(resource_path('verses.csv'), encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Parse Title field
for row in data:
    title = row['Title'].strip()
    if ':' not in title:
        row['Book'] = row['Chapter'] = row['Verse'] = ''
    else:
        left, verse = title.rsplit(':', 1)
        left_parts = left.strip().rsplit(' ', 1)
        row['Book'] = left_parts[0].strip() if len(left_parts) == 2 else ''
        row['Chapter'] = left_parts[1].strip() if len(left_parts) == 2 else ''
        row['Verse'] = verse.strip()

data.sort(key=lambda r: (r['Book'], safe_int(r['Chapter']), safe_int(r['Verse'])))

def unique_ordered(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]

books = [
    "ഉല്‍‍പത്തി", "പുറപ്പാട്", "ലേവ്യര്‍", "സംഖ്യ", "നിയമാവര്‍ത്തനം",
    "ജോഷ്വാ", "ന്യായാധിപ‌ന്‍മാര്‍", "റൂത്ത്",
    "1 സാമുവല്‍", "2 സാമുവല്‍", "1 രാജാക്ക‌ന്‍മാര്‍", "2 രാജാക്ക‌ന്‍മാര്‍",
    "1 ദിനവൃത്താന്തം", "2 ദിനവൃത്താന്തം", "എസ്രാ", "നെഹമിയ", "തോബിത്",
    "യൂദിത്ത്", "എസ്തേര്‍", "1 മക്കബായര്‍", "2 മക്കബായര്‍", "ജോബ്",
    "സങ്കീര്‍ത്തനങ്ങള്‍", "സുഭാഷിതങ്ങള്‍", "സഭാപ്രസംഗക‌ന്‍", "ഉത്തമഗീതം",
    "ജ്ഞാനം", "പ്രഭാഷക‌ന്‍", "ഏശയ്യാ", "ജെറെമിയ", "വിലാപങ്ങള്‍", "ബാറൂക്ക്",
    "എസെക്കിയേല്‍", "ദാനിയേല്‍", "ഹോസിയാ", "ജോയേല്‍", "ആമോസ്", "ഒബാദിയ",
    "യോനാ", "മിക്കാ", "നാഹും", "ഹബക്കുക്ക്", "സെഫാനിയ", "ഹഗ്ഗായി",
    "സഖറിയാ", "മലാക്കി", "****", "മത്തായി", "മര്‍ക്കോസ്", "ലൂക്കാ", "യോഹന്നാ‌ന്‍",
    "അപ്പ. പ്രവര്‍ത്തനങ്ങള്‍", "റോമാ", "1 കൊറിന്തോസ്", "2 കൊറിന്തോസ്", "ഗലാത്തിയാ",
    "എഫേസോസ്", "ഫിലിപ്പി", "കൊളോസോസ്", "1 തെസലോനിക്കാ", "2 തെസലോനിക്കാ",
    "1 തിമോത്തേയോസ്", "2 തിമോത്തേയോസ്", "തീത്തോസ്", "ഫിലെമോ‌ന്‍",
    "ഹെബ്രായര്‍", "യാക്കോബ്", "1 പത്രോസ്", "2 പത്രോസ്", "1 യോഹന്നാ‌ന്‍",
    "2 യോഹന്നാ‌ന്‍", "3 യോഹന്നാ‌ന്‍", "യുദാസ്", "വെളിപാട്"
]

root = tk.Tk()
root.title("Bible Verse Navigator")
root.geometry('1000x700')
root.minsize(700, 400)
style = ttk.Style()
style.configure("Small.TButton", font=("TkDefaultFont", 8))

book_selected = tk.StringVar()
chapter_selected = tk.StringVar()
verse_selected = tk.StringVar()

verse_window = None
text_box = None
verse_label_widget = None

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill='both', expand=True)

book_frame = ttk.LabelFrame(main_frame, text="Books")
book_frame.grid(row=0, column=0, sticky='NSEW', padx=5, pady=5)

chapter_frame = ttk.LabelFrame(main_frame, text="Chapters")
chapter_frame.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)

verse_frame = ttk.LabelFrame(main_frame, text="Verses")
verse_frame.grid(row=2, column=0, sticky='NSEW', padx=5, pady=5)



def insert_centered_text(widget, text,book,chapter,verse):
    if widget is None:
        return
    widget.configure(state='normal')
    widget.delete('1.0', tk.END)
    total_lines = int(widget['height'])
    verse_lines = text.count('\n') + 1
    top_padding = max((total_lines - verse_lines) // 3, 0)
    padding = '\n' * top_padding
    widget.insert('1.0', padding + text)
    widget.insert('1.0', '\n'+ book +" "+ chapter+":"+verse)
    widget.tag_configure('center', justify='center')
    widget.tag_add('center', '1.0', 'end')
    widget.configure(state='disabled')

def display_verse():
    global verse_window, text_box, verse_label_widget
    book = book_selected.get()
    chapter = chapter_selected.get()
    verse = verse_selected.get()
    for row in data:
        b = normalize_text(row['Book'])
        c = normalize_text(row['Chapter'])
        v = normalize_text(row['Verse'])
        if b == normalize_text(book) and c == normalize_text(chapter) and v == normalize_text(verse):
            if verse_window is None or not verse_window.winfo_exists():
                verse_window = tk.Toplevel(root)
                verse_window.title("Verse Display")
                verse_window.geometry("800x500")
                verse_label_widget = ttk.Label(verse_window, text=f"{book} {chapter}:{verse}", font=('Noto Sans Malayalam', 18, 'bold'))
                verse_label_widget.pack(pady=(10, 0))
                text_box = tk.Text(verse_window, wrap=tk.WORD, font=('Noto Sans Malayalam', 49,'bold'), spacing3=10, height=10)
                text_box.pack(fill='both', expand=True, padx=10, pady=10)
                btn_frame = ttk.Frame(verse_window)
                btn_frame.pack(pady=5)
                ttk.Button(btn_frame, text="Previous", command=prev_verse, style="Small.TButton").pack(side='left', padx=5)
                ttk.Button(btn_frame, text="Next", command=next_verse, style="Small.TButton").pack(side='left', padx=5)
            
            else:
                verse_window.deiconify()
                verse_label_widget.config(text=f"{book} {chapter}:{verse}")
                verse_window.title(f"{book} {chapter}:{verse}")
            insert_centered_text(text_box, row['Text'],book,chapter,verse)
            break

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def load_books():
    clear_frame(book_frame)
    max_cols = 17
    font_style = ('Noto Sans Malayalam', 10,'bold')
    style = ttk.Style()
    style.configure('Book.TButton', font=font_style)
    display_index = 0
    for book in books:
        if book == "****":
            display_index = ((display_index // max_cols) + 1) * max_cols
            continue
        row = display_index // max_cols
        col = display_index % max_cols
        btn = ttk.Button(book_frame, text=book, width=16, command=lambda b=book: select_book(b), style='Book.TButton')
        btn.grid(row=row, column=col, padx=2, pady=2)
        display_index += 1

def select_book(book):
    book_selected.set(book)
    clear_frame(chapter_frame)
    clear_frame(verse_frame)
    chapters = unique_ordered(row['Chapter'] for row in data if normalize_text(row['Book']) == normalize_text(book))
    max_cols = 45
    for idx, ch in enumerate(chapters):
        if ch:
            row = idx // max_cols
            col = idx % max_cols
            btn = ttk.Button(chapter_frame, text=ch, width=4, command=lambda c=ch: select_chapter(c))
            btn.grid(row=row, column=col, padx=2, pady=2)

def select_chapter(chapter):
    chapter_selected.set(chapter)
    clear_frame(verse_frame)
    book = book_selected.get()
    verses = unique_ordered(
        row['Verse'] for row in data
        if normalize_text(row['Book']) == normalize_text(book) and normalize_text(row['Chapter']) == normalize_text(chapter)
    )
    max_cols = 45
    for idx,v in enumerate(verses):
        if v:
            row = idx // max_cols
            col = idx % max_cols
            btn = ttk.Button(verse_frame, text=v, width=4, command=lambda vv=v: select_verse(vv))
            btn.grid(row=row, column=col, padx=2, pady=2)

def select_verse(verse):
    verse_selected.set(verse)
    display_verse()

def next_verse():
    idx = find_current_index()
    if idx == -1 or idx >= len(data) - 1:
        return
    next_row = data[idx + 1]
    book_selected.set(next_row['Book'])
    select_book(next_row['Book'])
    chapter_selected.set(next_row['Chapter'])
    select_chapter(next_row['Chapter'])
    verse_selected.set(next_row['Verse'])
    display_verse()

def prev_verse():
    idx = find_current_index()
    if idx <= 0:
        return
    prev_row = data[idx - 1]
    book_selected.set(prev_row['Book'])
    select_book(prev_row['Book'])
    chapter_selected.set(prev_row['Chapter'])
    select_chapter(prev_row['Chapter'])
    verse_selected.set(prev_row['Verse'])
    display_verse()
    

def find_current_index():
    book = normalize_text(book_selected.get())
    chapter = normalize_text(chapter_selected.get())
    verse = normalize_text(verse_selected.get())
    for i, row in enumerate(data):
        if (normalize_text(row['Book']) == book and
            normalize_text(row['Chapter']) == chapter and
            normalize_text(row['Verse']) == verse):
            return i
    return -1



load_books()
root.mainloop()