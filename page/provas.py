import streamlit as st
import sqlite3

def show():
    st.title("Provas e Avaliações")
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()
    
    with st.expander("Adicionar Prova"):
        exam_name = st.text_input("Nome da Prova")
        df_classes = cursor.execute("SELECT name FROM classes").fetchall()
        class_names = [row[0] for row in df_classes]
        related_class = st.selectbox("Aula Relacionada", class_names if class_names else [])
        exam_date = st.date_input("Data da Prova")
        exam_description = st.text_area("Descrição da Prova")
        
        if st.button("Salvar Prova"):
            cursor.execute("INSERT INTO exams (name, related_class, exam_date, description) VALUES (?, ?, ?, ?)",
                           (exam_name, related_class, str(exam_date), exam_description))
            conn.commit()
            st.success("Prova adicionada!")
    
    st.subheader("Lista de Provas")
    df_exams = cursor.execute("SELECT * FROM exams").fetchall()
    if df_exams:
        for exam in df_exams:
            with st.expander(f"{exam[1]} - {exam[2]} - Data: {exam[3]}"):
                st.write(f"**Nome:** {exam[1]}")
                st.write(f"**Aula Relacionada:** {exam[2]}")
                st.write(f"**Data da Prova:** {exam[3]}")
                st.write(f"**Descrição:** {exam[4]}")
                
                # Botão para apagar a prova
                if st.button(f"Apagar {exam[1]}", key=f"delete_{exam[0]}"):
                    cursor.execute("DELETE FROM exams WHERE id = ?", (exam[0],))
                    conn.commit()
                    st.success("Prova apagada!")
                    st.rerun()

    else:
        st.write("Nenhuma prova cadastrada.")
    
    conn.close()
