import os
import tkinter as tk
from tkinter import ttk
#import openpyxl
import csv
from pathlib import Path
courses = {
    "Профессиональная подготовка по профессии рабочего  'Животновод'": "ПО Животновод",

}

def get_entry4():
    fields = ['username', 'lastname', 'firstname', 'fathername', 'email', 'password', 'course1']
    value1 = entry1.get()
    value2 = entry2.get()
    value3 = entry3.get()
    value4 = combo4.get()
    personal_data = value1.split()
    personal_name = value2.split()
    personal_father_name = value3.split()
    words = {
        "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Е": "E", "Ё": "E",
        "Ж": "Zh", "З": "Z", "И": "I", "Й": "Y", "К": "K", "Л": "L", "М": "M",
        "Н": "N", "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T", "У": "U", "Ф": "F",
        "Х": "Kh", "Ц": "Ts", "Ч": "Ch", "Ш": "Sh", "Щ": "Shch", "Ы": "Y", "Э": "E",
        "Ю": "Yu", "Я": "Ya", "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
        "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k",
        "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
        "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya"
    }
    tb1 = personal_data[0].maketrans(words)
    last_name = personal_data[0].translate(tb1)
    tb2 = personal_name[0].maketrans(words)
    name = personal_name[0].translate(tb2)
    tb3 = personal_father_name[0].maketrans(words)
    father_name = personal_father_name[0].translate(tb3)
    entry5.delete(0, tk.END)
    entry5.insert(0, (last_name + '-' + name + '-' + father_name).lower())
    entry6.delete(0, tk.END)
    entry6.insert(0, ("Zz-12345"))
    value5 = entry5.get()
    value6 = entry6.get()
    value8 = (last_name + "-PK-2022@mail.ru").lower()
    a = courses[f'{value4}']
    entry7.delete(0, tk.END)
    entry7.insert(0, a)
    value7 = entry7.get()
    file_path = Path('users.csv')
    with file_path.open(mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=';', dialect='excel')
        if os.path.getsize(file_path) == 0:
            writer.writeheader()
        writer.writerow({
            'username': value5,
            'lastname': value1,
            'firstname': value2,
            'email': value8,
            'password': value6,
            'course1': value7,
            'fathername': value3
        })



window = tk.Tk()
window.geometry(f"600x300+800+400")
window.title("Добавление слушателя на курсы ПК")
tk.Label(window, text='Фамилия',
         font=('Arial', 14, 'bold'),
         width=22, height=1,
         anchor='w',
         relief=tk.RAISED) \
    .grid(row=0, column=0)
tk.Label(window, text='Имя',
         font=('Arial', 14, 'bold'),
         width=22, height=1,
         anchor='w',
         relief=tk.RAISED) \
    .grid(row=1, column=0)
tk.Label(window, text='Отчество',
         font=('Arial', 14, 'bold'),
         width=22, height=1,
         anchor='w',
         relief=tk.RAISED) \
    .grid(row=2, column=0)
tk.Label(window, text='полное_название_курса',
         font=('Arial', 14, 'bold'),
         width=22, height=1,
         anchor='w',
         relief=tk.RAISED) \
    .grid(row=3, column=0)
tk.Label(window, text='логин',
         font=('Arial', 14, 'bold'),
         width=22, height=1,
         anchor='w',
         relief=tk.RAISED) \
    .place(x=0, y=230)
tk.Label(window, text='пароль',
         font=('Arial', 14, 'bold'),
         width=22, height=1,
         anchor='w',
         relief=tk.RAISED) \
    .place(x=0, y=260)
tk.Label(window, text='краткое_название_курса',
         font=('Arial', 14, 'bold'),
         width=22, height=1,
         anchor='w',
         relief=tk.RAISED) \
    .place(x=0, y=290)
combo_up = tuple(sorted(courses.keys()))
combo_down = courses.values()
entry1 = tk.Entry(window, font=('Arial', 14), width=122)
entry1.grid(row=0, column=1)
entry2 = tk.Entry(window, font=('Arial', 14), width=122)
entry2.grid(row=1, column=1)
entry3 = tk.Entry(window, font=('Arial', 14), width=122)
entry3.grid(row=2, column=1)
combo4 = ttk.Combobox(window, font=('Arial', 14), width=120, value=combo_up)
combo4.grid(row=3, column=1)
entry5 = tk.Entry(window, font=('Arial', 14), width=122)
entry5.place(x=270, y=230)
entry6 = tk.Entry(window, font=('Arial', 14), width=122)
entry6.place(x=270, y=260)
entry7 = tk.Entry(window, font=('Arial', 14), width=122)
entry7.place(x=270, y=290)
btn1 = tk.Button(window, text='добавить пользователя', font=('Arial', 14, 'bold'), command=get_entry4) \
    .place(x=150, y=150)


def change_courses_list(event):
    def filter_keys(key: str):
        try:
            # return key.upper().index(event.widget.get().upper()) >= 0 № ищет под строки в любом месте строки
            return key.upper().startswith(event.widget.get().upper())  # ищет подстроки в начале строки
        except ValueError:
            return False

    event.widget['values'] = tuple(sorted(filter(filter_keys, courses.keys())))


combo4.bind('<Key>', change_courses_list)
window.mainloop()
