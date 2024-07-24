import mariadb
import sys
import re
import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path

# Connect to MariaDB Platform
def request(login, last_name):
    try:
        conn = mariadb.connect(
            user="moodle",
            password="07QgNFy0rsxN8Gl",
            host="192.168.1.210",
            port=3306,
            database="eios"
        )
    except mariadb.Error as e:
        sys.exit(1)
    # Get Cursor
    cur = conn.cursor()

    s =    """SELECT DISTINCT q.questiontext, q.category, qa.responsesummary
    FROM eios_mdl_question q
    JOIN eios_mdl_question_attempts qa ON qa.questionid = q.id
    JOIN eios_mdl_question_usages qu ON qu.id = qa.questionusageid
    JOIN eios_mdl_quiz_attempts a ON a.uniqueid = qu.id
    WHERE a.quiz = 10399
    AND a.id = (
        SELECT MIN(a2.id)
        FROM eios_mdl_quiz_attempts a2
        WHERE a2.quiz = 10399
        AND a2.userid IN (
        SELECT id FROM eios_mdl_user
        WHERE lastname = ?
        AND username = ?)
    );"""
    cur.execute(s, (last_name, login))


    from_q = cur.fetchall()
    for i in from_q:
        print(i)
    return from_q



def extract_text(input_string):
    # Regex to capture text based on the presence of ">" and "<"
    regex = r'(?:>)([^<]*)|^(.*?)(?=<|$)'

    # Using re.search to find the first match
    match = re.search(regex, input_string)
    if match is not None:
        if match.group(1) is not None:
            print(match.group(1))
            return match.group(1)
        elif match.group(2) is not None:
            print(match.group(2))

            return match.group(2)
        else:
            print('Что-то другое')
    else:
        print('НЕ ПОЯВЛЯЕТСЯ',input_string)

    # If a match is found, return the first non-None group
    return "kjjjkj"


def extract_image(input_string):
    # Regex to capture text based on the presence of ">" and "<"
    regex = r'<img\s+[^>]*?src="[^"]*\/([^\/"]+)"'

    # Using re.search to find the first match
    match = re.search(regex, input_string)

    # If a match is found, return the first non-None group
    if match:
        return match.group(1) if match.group(1) is not None else match.group(2)
    return ""


def extract_path(input_string):
    # Regex to capture text based on the presence of ">" and "<"
    regex = r'<img\s+[^>]*?src="([^"]+)"'
    # Using re.search to find the first match
    match = re.search(regex, input_string)
    # If a match is found, return the first non-None group
    if match:
        return match.group(1) if match.group(1) is not None else match.group(2)
    return ""

def build(p, login, last_name):
    try:
        conn = mariadb.connect(
            user="moodle",
            password="07QgNFy0rsxN8Gl",
            host="192.168.1.210",
            port=3306,
            database="eios"
        )
    except mariadb.Error as e:
        sys.exit(1)
    files_data = []
    questions = {}
    answers = {}
    q = 0

    from_q = request(login, last_name)
    for i in from_q:
        question = extract_text(i[0])
        questions[q] = question

        answer = extract_text(i[2])
        answers[q] = answer

        # Search using the regular expression
        match_image = extract_image(i[0])
        match_path = extract_path(i[0])
        # Check if a match is found and print it
        if match_image:
            touple = (match_image, i[1], match_path, q+1, i[2])
            files_data.append(touple)
        else:
            print("No filename found.")
        q += 1
    print("dict :", questions)
    print("answers", answers)

    file_hash = conn.cursor()

    sql_script = """ SELECT DISTINCT f.id, f.contenthash, f.filepath
                    FROM eios_mdl_files f
                    JOIN eios_mdl_question_categories cs ON cs.contextid = f.contextid
                    WHERE cs.id = ? 
                    AND f.filename = ?"""

    img_numbers = []
    for q in range(len(files_data)):
        file_hash.execute(sql_script, (files_data[q][1], files_data[q][0]))
        results = file_hash.fetchall()
        path = files_data[q][2]
        for f in results:
            if f[2] in path:
                contenthash = f[1]


                def get_file_path(contenthash, base_dir='//192.168.1.215/Share/filedir'):
                    """Construct the file path based on the contenthash."""
                    # Split the hash to form the path
                    first_dir = contenthash[:2]
                    second_dir = contenthash[2:4]
                    # Combine parts to form the full path
                    file_path = os.path.join(base_dir, first_dir, second_dir, contenthash)
                    return file_path


                def copy_file(source_path, destination_path):
                    """Copy the file from source to destination."""
                    try:
                        shutil.copy(source_path, destination_path)
                    except Exception as e:
                        print(f"Error copying file: {str(e)}")


                # Example Usage  # Replace this with your file's contenthash
                source_file_path = get_file_path(contenthash)
                destination_path = p + f"/image_{files_data[q][3]}.jpg"  # Set your destination path
                img_numbers.append(files_data[q][3])
                # Copy the file
                copy_file(source_file_path, destination_path)
    return files_data, questions, answers, img_numbers

# pdfmetrics.registerFont(TTFont('DejaVuSans', 'C:/Users/Andrey-CDO/Downloads/DejaVu Sans/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', 'C:/Users/CDO-Oleg/Downloads/DejaVu Sans123/DejaVuSans.ttf'))


def split_text_by_char_limit(text, char_limit):
    """Split text into lines with an exact character limit."""
    lines = []
    while len(text) > char_limit:
        split_point = text.rfind(' ', 0, char_limit)  # Find the last space within the limit
        if split_point == -1:  # No space found, force split at the limit
            split_point = char_limit
        lines.append(text[:split_point].strip())
        text = text[split_point:].lstrip()  # Remove leading spaces on the next line
    lines.append(text)  # Append the remainder of the text
    return lines


def create_pdf(pdf_path, login, last_name):
    def change_slashes(path):
        return path.replace("\\", "/")
    p = change_slashes(pdf_path)


    files_data, questions, answers, img_numbers = build(p, login, last_name)
    c = canvas.Canvas(p + f"/{login}.pdf", pagesize=letter)
    width, height = letter
    h = 50  # Initial vertical offset from the top of the page
    intra_line_spacing = 15  # Space between lines within the same paragraph
    inter_paragraph_spacing = 25  # Space between different paragraphs

    for key in list(questions.keys()):
        image_path = p + f"/image_{key}.jpg"
        if key not in img_numbers:
            lines_q = split_text_by_char_limit(questions[key].replace('\n', ' '),
                                               70)  # Normalize newlines and split text
            for i, line in enumerate(lines_q):
                if height - 50 - h < 20:  # Check if there's enough space to write another line
                    c.showPage()  # Add a new page if not enough space
                    h = 50  # Reset vertical offset at the top of the new page
                c.setFont("DejaVuSans", 12)
                line_to_draw = f"{key + 1}. {line}" if i == 0 else line
                c.drawString(50, height - 50 - h, line_to_draw)
                # Increment h based on whether it's the last line of the paragraph or not
                if i < len(lines_q) - 1:
                    h += intra_line_spacing
                else:
                    h += inter_paragraph_spacing
            lines_a = split_text_by_char_limit(answers[key].replace('\n', ' '),
                                               70)  # Normalize newlines and split text
            for i, line in enumerate(lines_a):
                if height - 50 - h < 20:  # Check if there's enough space to write another line
                    c.showPage()  # Add a new page if not enough space
                    h = 50  # Reset vertical offset at the top of the new page
                c.setFont("DejaVuSans", 12)
                c.drawString(50, height - 50 - h, line)
                # Increment h based on whether it's the last line of the paragraph or not
                if i < len(lines_a) - 1:
                    h += intra_line_spacing + 30
                else:
                    h += inter_paragraph_spacing + 30
        else:
            lines_q = split_text_by_char_limit(questions[key].replace('\n', ' '),
                                               70)  # Normalize newlines and split text
            for i, line in enumerate(lines_q):
                if height - 50 - h < 20:  # Check if there's enough space to write another line
                    c.showPage()  # Add a new page if not enough space
                    h = 50  # Reset vertical offset at the top of the new page
                c.setFont("DejaVuSans", 12)

                line_to_draw = f"{key + 1}. {line}" if i == 0 else line
                c.drawString(50, height - 50 - h, line_to_draw)
                # Increment h based on whether it's the last line of the paragraph or not
                if i < len(lines_q) - 1:
                    h += intra_line_spacing
                else:
                    h += inter_paragraph_spacing
            print(h)

            image_height = 100  # Задайте фактическую высоту изображения
            if height - 50 - h - image_height < 20:  # Проверка на переполнение страницы изображением
                c.showPage()
                h = 50
            c.drawImage(image_path, x=40, y=height - 150 - h, width=150, height=image_height+50)
            h += image_height + 50  # Дополнительное пространство после изображения

            # c.drawImage(image_path, x=40, y=height - 150 - h, width=150, height=100)
            #
            # h += 150
            lines_a = split_text_by_char_limit(answers[key].replace('\n', ' '),
                                               70)  # Normalize newlines and split text
            for i, line in enumerate(lines_a):
                if height - 50 - h < 20:  # Check if there's enough space to write another line
                    c.showPage()  # Add a new page if not enough space
                    h = 50  # Reset vertical offset at the top of the new page
                c.setFont("DejaVuSans", 12)
                c.drawString(50, height - 50 - h, line)
                # Increment h based on whether it's the last line of the paragraph or not
                if i < len(lines_a) - 1:
                    h += intra_line_spacing + 30
                else:
                    h += inter_paragraph_spacing + 30
    c.save()


# Paths and text



def run_script():
    last_name = entry_lastname.get()
    login = entry_login.get()

    if getattr(sys, 'frozen', False):
        # Путь к директории исполняемого файла
        directory = os.path.dirname(sys.executable)
    else:
        # Путь к директории скрипта
        directory = os.path.dirname(__file__)
    cur_dir = Path(directory)
    # / f"{last_name}_данные.xlsx"

    student_dir = os.path.join(cur_dir, login)
    if not os.path.exists(student_dir):
        os.makedirs(student_dir)

    pdf_output_path = student_dir

    create_pdf(pdf_output_path, login, last_name)
    return print("afjdfjdjgdjdjgjd")


# Основное окно приложения
window = tk.Tk()
window.geometry("600x400+800+400")
window.title("Обработка данных студента")

# Элементы интерфейса
tk.Label(window, text='Фамилия:', font=('Arial', 12)).grid(row=0, column=0, sticky='w')
entry_lastname = tk.Entry(window, font=('Arial', 12), width=50)
entry_lastname.grid(row=0, column=1)

tk.Label(window, text='Логин:', font=('Arial', 12)).grid(row=1, column=0, sticky='w')
entry_login = tk.Entry(window, font=('Arial', 12), width=50)
entry_login.grid(row=1, column=1)

btn_create_excel = tk.Button(window, text='Создать Excel', command=run_script)
btn_create_excel.grid(row=2, column=1)

window.mainloop()
