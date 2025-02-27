import streamlit as st
import sqlite3
import datetime

def show():
    st.title("Controle de Faltas")
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    
    df_classes = cursor.execute("SELECT name FROM classes").fetchall()
    class_names = [row[0] for row in df_classes]
    
    selected_course = st.selectbox("Selecione uma aula", class_names if class_names else [])
    
    if selected_course and st.button("Registrar Falta"):
        today = datetime.date.today()
        cursor.execute("INSERT INTO absences (course_name, absence_date) VALUES (?, ?)", (selected_course, str(today)))
        conn.commit()
        st.success(f"Falta registrada para {selected_course} em {today}!")
    
    st.subheader("Faltas Registradas")
    df_absences = cursor.execute("SELECT course_name, COUNT(*) AS total_faltas FROM absences GROUP BY course_name").fetchall()
    for course_name, total_faltas in df_absences:
        remaining_absences = 15 - total_faltas
        st.write(f"**{course_name}**: {total_faltas} faltas ({remaining_absences} restantes)")
    
    with st.expander("Remover Falta"):
        df_absence_details = cursor.execute("SELECT id, course_name, absence_date FROM absences").fetchall()
        if df_absence_details:
            selected_falta = st.selectbox("Selecione a falta para remover", [f"{row[1]} - {row[2]}" for row in df_absence_details])
            if st.button("Remover Falta"):
                falta_id = [row[0] for row in df_absence_details if f"{row[1]} - {row[2]}" == selected_falta][0]
                cursor.execute("DELETE FROM absences WHERE id = ?", (falta_id,))
                conn.commit()
                st.success("Falta removida!")
    
    conn.close()
