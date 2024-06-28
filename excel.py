import sys
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path

def load_excel():
    """Загрузка Excel файла через диалоговое окно."""
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if filepath:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, filepath)


def create_excel():
    last_name = entry_lastname.get()
    file_path = entry_file_path.get()

    if not file_path or not last_name:
        print("Please fill in all fields")
        return

    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        print(f"Failed to load Excel file: {e}")
        return

    target_student = data[(data['Фамилия'] == last_name)]
    if target_student.empty:
        print("Студент не найден.")
        return

    questions_and_answers = []
    for i in range(1, (len(data.columns) - 2) // 2 + 1):
        question_col = f'Вопрос {i}'
        answer_col = f'Ответ {i}'
        if question_col in data.columns and answer_col in data.columns:
            questions_and_answers.append((target_student[question_col].values[0], target_student[answer_col].values[0]))

    final_df = pd.DataFrame(questions_and_answers, columns=['Вопрос', 'Ответ'])

    # Определение директории для сохранения Excel файла
    if getattr(sys, 'frozen', False):
        # Путь к директории исполняемого файла
        directory = os.path.dirname(sys.executable)
    else:
        # Путь к директории скрипта
        directory = os.path.dirname(__file__)

    output_file = Path(directory) / f"{last_name}_данные.xlsx"
    try:
        final_df.to_excel(output_file, index=False)
        print(f"Файл '{output_file}' успешно сохранен.")
    except Exception as e:
        print(f"Failed to save Excel file: {e}")



# Основное окно приложения
window = tk.Tk()
window.geometry("600x400+800+400")
window.title("Обработка данных студента")

# Элементы интерфейса
tk.Label(window, text='Путь к файлу:', font=('Arial', 12)).grid(row=0, column=0, sticky='w')
entry_file_path = tk.Entry(window, font=('Arial', 12), width=50)
entry_file_path.grid(row=0, column=1)
btn_load = tk.Button(window, text='Загрузить файл', command=load_excel)
btn_load.grid(row=0, column=2)

tk.Label(window, text='Фамилия:', font=('Arial', 12)).grid(row=1, column=0, sticky='w')
entry_lastname = tk.Entry(window, font=('Arial', 12), width=50)
entry_lastname.grid(row=1, column=1)

tk.Label(window, text='Имя:', font=('Arial', 12)).grid(row=2, column=0, sticky='w')
entry_firstname = tk.Entry(window, font=('Arial', 12), width=50)
entry_firstname.grid(row=2, column=1)

btn_create_excel = tk.Button(window, text='Создать Excel', command=create_excel)
btn_create_excel.grid(row=3, column=1)

window.mainloop()
