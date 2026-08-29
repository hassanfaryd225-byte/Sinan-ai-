import streamlit as st

st.set_page_config(page_title="SINAN AI", page_icon="S", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #14171F; color: #EDE7D3; }
    </style>
""", unsafe_allow_html=True)

st.title("SINAN AI — Assistant Financier Vocal")
st.write("Assistant financier intelligent (Version Streamlit Cloud)")

user_input = st.text_input("Saisissez votre opération financière :", placeholder="Ex : Vente de riz 15000 F")

if st.button("Enregistrer"):
    if user_input:
        st.success(f"Opération enregistrée : {user_input}")
    else:
        st.warning("Veuillez entrer une description.")
