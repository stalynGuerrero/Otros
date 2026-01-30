import streamlit as st
from pathlib import Path


def show_login(authenticator, message_placeholder):
    with st.sidebar:

        # === Logo ===
        logo_path = Path(__file__).resolve().parent / "assets" / "IDT_logo.png"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)

        # === Títulos ===
        st.markdown("# Ingreso al Sistemas")
        st.markdown("## Solo usuarios autorizados")

        authenticator.login(
            location="sidebar",
            fields={
                "Form name": "Acceso",
                "Username": "Usuario",
                "Password": "Contraseña",
                "Login": "Ingresar"
            },
            captcha=False
        )

    # === Mensajes ===
    auth_status = st.session_state.get("authentication_status")

    if auth_status is False:
        message_placeholder.error("Usuario o contraseña incorrectos")
    elif auth_status is None:
        message_placeholder.info("Ingrese sus credenciales para acceder al sistema")
