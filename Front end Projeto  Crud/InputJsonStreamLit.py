import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

API_URL = "http://localhost:8080/usuarios"

# Sessão
if "auth" not in st.session_state:
    st.session_state.auth = None
if "logado" not in st.session_state:
    st.session_state.logado = False
if "editar_id" not in st.session_state:
    st.session_state.editar_id = None

st.title("Painel de Usuários")

# --- LOGIN ---
if not st.session_state.logado:
    st.subheader("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        auth = HTTPBasicAuth(username, password)
        try:
            response = requests.get(API_URL, auth=auth)
            if response.status_code == 200:
                st.session_state.auth = auth
                st.session_state.logado = True
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
    st.stop()

# --- LOGADO ---
st.success("Você está logado!")

if st.button("Sair"):
    st.session_state.logado = False
    st.session_state.auth = None
    st.session_state.editar_id = None
    st.rerun()

st.divider()

# --- CADASTRO ---
with st.form("form_usuario"):
    st.subheader("Cadastrar novo usuário")
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0, max_value=120)
    cadastrar = st.form_submit_button("Cadastrar")

    if cadastrar:
        if nome:
            payload = {"nome": nome, "idade": idade}
            response = requests.post(API_URL, json=payload, auth=st.session_state.auth)
            if response.status_code == 201:
                st.success("Usuário cadastrado com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao cadastrar.")
        else:
            st.warning("Preencha o nome.")

st.divider()

# --- LISTAGEM COM AÇÕES ---
st.subheader("Usuários cadastrados")

response = requests.get(API_URL, auth=st.session_state.auth)
if response.status_code == 200:
    usuarios = response.json()
    if usuarios:
        for usuario in usuarios:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"👤 **{usuario['nome']}** — {usuario['idade']} anos")

            with col2:
                if st.button("✏️ Editar", key=f"editar_{usuario['id']}"):
                    st.session_state.editar_id = usuario["id"]
                    st.rerun()

            with col3:
                if st.button("🗑️ Excluir", key=f"excluir_{usuario['id']}"):
                    del_resp = requests.delete(f"{API_URL}/{usuario['id']}", auth=st.session_state.auth)
                    if del_resp.status_code == 204:
                        st.success("Usuário removido com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao remover usuário.")
    else:
        st.info("Nenhum usuário cadastrado.")
else:
    st.error("Erro ao buscar usuários.")

# --- FORMULÁRIO DE EDIÇÃO ---
if st.session_state.editar_id:
    st.sidebar.subheader("✏️ Editar usuário")

    usuario_resp = requests.get(f"{API_URL}/{st.session_state.editar_id}", auth=st.session_state.auth)
    
    if usuario_resp.status_code == 200:
        usuario = usuario_resp.json()
        novo_nome = st.sidebar.text_input("Novo nome", value=usuario["nome"])
        nova_idade = st.sidebar.number_input("Nova idade", min_value=0, max_value=120, value=usuario["idade"])
        
        if st.sidebar.button("Salvar"):
            payload = {
                "id": usuario["id"],
                "nome": novo_nome,
                "idade": nova_idade
            }
            put_resp = requests.put(f"{API_URL}/{usuario['id']}", json=payload, auth=st.session_state.auth)
            if put_resp.status_code == 200:
                st.success("Usuário atualizado com sucesso!")
                st.session_state.editar_id = None
                st.rerun()
            else:
                st.error("Erro ao atualizar usuário.")
        
        if st.sidebar.button("Cancelar"):
            st.session_state.editar_id = None
            st.rerun()
    else:
        st.sidebar.error("Erro ao buscar dados do usuário.")
