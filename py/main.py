import streamlit as st
from styles import load_styles
from config_utils import cargar_config
from auth_utils import init_authenticator
from ui_login import show_login
from ui_admin import show_admin_panel
from ui_user import show_user_panel

st.set_page_config(page_title="Reemplazos", layout="wide")

message_placeholder = st.empty()

# Estilos
load_styles()

# Configuración y autenticación
config = cargar_config()
authenticator = init_authenticator(config)

# 🔑 SIEMPRE renderizar login
show_login(authenticator, message_placeholder)

# Estado de autenticación (después del login)
auth_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

# -----------------------------
# Flujo post-autenticación
# -----------------------------
if auth_status is True:

    roles = config["credentials"]["usernames"].get(username, {}).get("roles", [])
    is_admin = "admin" in roles
    is_user = "user" in roles

    st.success(f"Bienvenido 👋 {username}")

    if is_admin:
        show_admin_panel(username, authenticator)

    elif is_user:
        show_user_panel(username, authenticator)

    else:
        st.warning("Su usuario no tiene permisos asignados. Contacte al administrador.")
