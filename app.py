import streamlit as st
from database import init_db
from page import materias, tarefas, provas, faltas, notas  

st.set_page_config(page_title="Gestão Acadêmica", layout="wide")
init_db()

st.sidebar.title("Menu")
page = st.sidebar.radio("Escolha uma página", [
    "Matérias", 
    "Tarefas", 
    "Provas", 
    "Controle de Faltas", 
    "Notas e Desempenho"  
])

if page == "Matérias":
    materias.show()
elif page == "Tarefas":
    tarefas.show()
elif page == "Provas":
    provas.show()
elif page == "Controle de Faltas":
    faltas.show()
elif page == "Notas e Desempenho":
    notas.show()
