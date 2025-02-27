import streamlit as st
import sqlite3
from datetime import datetime

def show():
    st.title("Tarefas e Trabalhos")
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    
    with st.expander("Adicionar Tarefa"):
        task_name = st.text_input("Nome da Tarefa")
        df_classes = cursor.execute("SELECT name FROM classes").fetchall()
        class_names = [row[0] for row in df_classes]
        related_class = st.selectbox("Aula Relacionada", class_names if class_names else [], key="add_task_related_class")
        due_date = st.date_input("Data de Entrega")
        due_time = st.time_input("Hora de Entrega")
        task_description = st.text_area("Descrição da Tarefa")
        
        if st.button("Salvar Tarefa"):
            full_due_datetime = datetime.combine(due_date, due_time)
            formatted_due_date = full_due_datetime.strftime("%d/%m %H:%M")
            cursor.execute("INSERT INTO tasks (name, related_class, due_date, description) VALUES (?, ?, ?, ?)",
                           (task_name, related_class, formatted_due_date, task_description))
            conn.commit()
            st.success("Tarefa adicionada!")
    
    st.subheader("Lista de Tarefas")
    df_tasks = cursor.execute("SELECT * FROM tasks").fetchall()
    if df_tasks:
        for task in df_tasks:
            with st.expander(f"{task[1]} - {task[2]} - Prazo: {task[3]}"):
                st.write(f"**Nome:** {task[1]}")
                st.write(f"**Aula Relacionada:** {task[2]}")
                st.write(f"**Data de Entrega:** {task[3]}")
                st.write(f"**Descrição:** {task[4]}")
                
                # Botão para apagar a tarefa
                if st.button(f"Apagar {task[1]}", key=f"delete_{task[0]}"):
                    cursor.execute("DELETE FROM tasks WHERE id = ?", (task[0],))
                    conn.commit()
                    st.success("Tarefa apagada!")
                    st.rerun()

    else:
        st.write("Nenhuma tarefa cadastrada.")
    
    conn.close()
