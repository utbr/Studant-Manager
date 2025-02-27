import streamlit as st
import sqlite3
import pandas as pd

def show():
    st.title("Materias da semana")
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    
    with st.expander("Adicionar Matéria"):
        course_name = st.text_input("Nome da Matéria")
        professor = st.text_input("Nome do Professor")
        schedule = st.time_input("Horário")
        day_of_week = st.selectbox("Dia da Semana", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"])
        classroom = st.text_input("Sala de Aula")
        
        if st.button("Salvar Aula"):
            cursor.execute("INSERT INTO classes (name, professor, schedule, day_of_week, classroom) VALUES (?, ?, ?, ?, ?)", 
                           (course_name, professor, str(schedule), day_of_week, classroom))
            conn.commit()
            st.success("Aula adicionada!")
    
    st.subheader("Lista de Matérias")
    df_classes = cursor.execute("SELECT * FROM classes").fetchall()
    
    if df_classes:
        df = pd.DataFrame(df_classes, columns=["ID", "Matéria", "Professor", "Horário", "Dia da Semana", "Sala de Aula"])
        st.dataframe(df, hide_index=True)
    else:
        st.write("Nenhuma matéria cadastrada.")
    
    conn.close()

