import streamlit as st
import sqlite3
from datetime import datetime

def show():
    st.title("Notas e Desempenho")
    conn = sqlite3.connect("student_management.db", check_same_thread=False)
    cursor = conn.cursor()

    # Seção para adicionar uma nova nota/avaliação
    with st.expander("Adicionar Nota"):
        assessment_name = st.text_input("Nome da Avaliação")
        # Recupera as aulas existentes para associar a avaliação
        df_classes = cursor.execute("SELECT name FROM classes").fetchall()
        class_names = [row[0] for row in df_classes]
        related_class = st.selectbox("Aula Relacionada", class_names if class_names else [])
        evaluation_date = st.date_input("Data da Avaliação")
        score = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")
        description = st.text_area("Descrição (opcional)")

        if st.button("Salvar Nota"):
            cursor.execute(
                "INSERT INTO grades (assessment_name, related_class, evaluation_date, score, description) VALUES (?, ?, ?, ?, ?)",
                (assessment_name, related_class, str(evaluation_date), score, description)
            )
            conn.commit()
            st.success("Nota adicionada com sucesso!")

    st.subheader("Notas Registradas")
    df_grades = cursor.execute("SELECT * FROM grades").fetchall()
    if df_grades:
        # Calcula a média das notas por aula
        subject_grades = {}
        for grade in df_grades:
            # Estrutura esperada: (id, assessment_name, related_class, evaluation_date, score, description)
            subject = grade[2]
            score_value = grade[4]
            subject_grades.setdefault(subject, []).append(score_value)

        # Exibe cada avaliação cadastrada com opção de remoção
        for grade in df_grades:
            with st.expander(f"{grade[1]} - {grade[2]} - Data: {grade[3]}"):
                st.write(f"**Nome da Avaliação:** {grade[1]}")
                st.write(f"**Aula Relacionada:** {grade[2]}")
                st.write(f"**Data da Avaliação:** {grade[3]}")
                st.write(f"**Nota:** {grade[4]}")
                if grade[5]:
                    st.write(f"**Descrição:** {grade[5]}")
                if st.button(f"Apagar {grade[1]}", key=f"delete_grade_{grade[0]}"):
                    cursor.execute("DELETE FROM grades WHERE id = ?", (grade[0],))
                    conn.commit()
                    st.success("Nota removida!")
                    st.experimental_rerun()

        st.subheader("Desempenho por Aula")
        # Exibe a média e o total de avaliações para cada aula
        for subject, scores in subject_grades.items():
            average = sum(scores) / len(scores) if scores else 0
            st.write(f"**{subject}**: Média: {average:.1f} (Total de avaliações: {len(scores)})")
    else:
        st.write("Nenhuma nota cadastrada.")

    conn.close()
