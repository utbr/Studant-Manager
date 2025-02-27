import sqlite3

def init_db():
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()

    # Tabela para matérias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        professor TEXT NOT NULL,
        schedule TEXT NOT NULL,
        day_of_week TEXT NOT NULL,
        classroom TEXT NOT NULL
    )
    """)

    # Tabela para tarefas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        related_class TEXT NOT NULL,
        due_date TEXT NOT NULL,
        description TEXT
    )
    """)

    # Tabela para provas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        related_class TEXT NOT NULL,
        exam_date TEXT NOT NULL,
        description TEXT
    )
    """)

    # Tabela para faltas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS absences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        absence_date TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def get_classes():
    """Retorna uma lista de matérias cadastradas no sistema."""
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM classes")
    classes = cursor.fetchall()
    conn.close()
    return classes

def add_task(name, related_class, due_date, description):
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO tasks (name, related_class, due_date, description)
    VALUES (?, ?, ?, ?)
    """, (name, related_class, due_date, description))
    conn.commit()
    conn.close()

def delete_task(task_name):
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE name = ?", (task_name,))
    conn.commit()
    conn.close()

def update_task(old_name, new_name, due_date, description):
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE tasks SET name = ?, due_date = ?, description = ? WHERE name = ?
    """, (new_name, due_date, description, old_name))
    conn.commit()
    conn.close()

def add_exam(name, related_class, exam_date, description):
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO exams (name, related_class, exam_date, description)
    VALUES (?, ?, ?, ?)
    """, (name, related_class, exam_date, description))
    conn.commit()
    conn.close()

def delete_exam(exam_name):
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exams WHERE name = ?", (exam_name,))
    conn.commit()
    conn.close()

def update_exam(old_name, new_name, exam_date, description):
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE exams SET name = ?, exam_date = ?, description = ? WHERE name = ?
    """, (new_name, exam_date, description, old_name))
    conn.commit()
    conn.close()

def add_absence(course_name, absence_date):
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO absences (course_name, absence_date)
    VALUES (?, ?)
    """, (course_name, absence_date))
    conn.commit()
    conn.close()

def delete_absence(course_name, absence_date):
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM absences WHERE course_name = ? AND absence_date = ?", (course_name, absence_date))
    conn.commit()
    conn.close()

def update_absence(course_name, old_date, new_date):
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE absences SET absence_date = ? WHERE course_name = ? AND absence_date = ?
    """, (new_date, course_name, old_date))
    conn.commit()
    conn.close()

# Inicializa o banco de dados ao importar este módulo
init_db()
