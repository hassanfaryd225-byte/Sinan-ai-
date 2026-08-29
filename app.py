%%writefile app.py
import streamlit as st

st.set_page_config(page_title="SINAN AI", page_icon="🎙️", layout="centered")

# Design CSS global inspiré du modèle sombre et épuré
st.markdown("""
    <style>
    .stApp { background-color: #0b0f17; color: #f8fafc; font-family: sans-serif; }
    
    /* En-tête */
    .title-container { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
    .logo-box { background: #d97706; padding: 10px 14px; border-radius: 12px; font-size: 20px; }
    
    /* Cartes de statistiques */
    .stat-card { background: #131b2e; border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px; margin-bottom: 12px; }
    
    /* Bouton d'exemple */
    .example-btn { background: #131b2e; border: 1px solid rgba(255,255,255,0.1); padding: 12px 16px; border-radius: 30px; text-align: center; color: #94a3b8; font-size: 14px; margin-bottom: 8px; cursor: pointer; }
    
    /* Coach financier */
    .coach-card { background: #1a1612; border: 1px solid #78350f; padding: 16px; border-radius: 16px; margin-bottom: 16px; }
    </style>
""", unsafe_allow_html=True)

# 1. En-tête
st.markdown("""
    <div class="title-container">
        <div class="logo-box">📖</div>
        <div>
            <h2 style="margin:0; font-size:22px; color:#ffffff;">SINAN AI</h2>
            <p style="margin:0; font-size:13px; color:#94a3b8;">Journal vocal quotidien</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. Sélecteur de langue (boutons côte à côte)
lang_cols = st.columns(4)
with lang_cols[0]:
    st.button("🇫🇷 Français", use_container_width=True, type="primary")
with lang_cols[1]:
    st.button("English", use_container_width=True)
with lang_cols[2]:
    st.button("Nouchi", use_container_width=True)
with lang_cols[3]:
    st.button("Dioula", use_container_width=True)

st.write("")

# 3. Menu de navigation par onglets
nav_cols = st.columns(3)
with nav_cols[0]:
    st.button("📖 Journal", use_container_width=True)
with nav_cols[1]:
    st.button("📁 Projets", use_container_width=True)
with nav_cols[2]:
    st.button("🏠 Finances perso", use_container_width=True, type="primary")

st.markdown("---")

# 4. Zone d'enregistrement vocal principale
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:14px; margin-bottom:5px;'>🏠 Personnel</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:16px; font-weight:bold;'>Dites votre opération du jour</p>", unsafe_allow_html=True)

# Bouton audio natif Streamlit customisé en grand rond orange central
audio_value = st.audio_input("")

st.markdown("<p style='text-align:center; color:#64748b; font-size:13px;'>⌨️ Ou tapez votre opération</p>", unsafe_allow_html=True)

# Saisie manuelle textuelle
user_input = st.text_input("", placeholder="Ex : j'ai vendu du riz pour 15000 francs", label_visibility="collapsed")
if st.button("OK", use_container_width=True):
    if user_input:
        st.success(f"Opération enregistrée : {user_input}")

# 5. Exemples à essayer
st.markdown("<p style='text-align:center; color:#64748b; font-size:12px; letter-spacing:1px; margin-top:15px;'>EXEMPLES À ESSAYER</p>", unsafe_allow_html=True)

examples = [
    "J'ai vendu du riz pour quinze mille francs",
    "J'ai acheté du carburant pour 5000 francs",
    "J'ai payé le loyer de la boutique, cent mille francs",
    "Reçu de vingt-cinq mille francs pour une prestation"
]

for ex in examples:
    if st.button(ex, use_container_width=True):
        st.info(f"Simulation de l'opération : {ex}")

st.markdown("---")

# 6. Statistiques & Coach Financier (Image 9)
stat_col1, stat_col2 = st.columns(2)
with stat_col1:
    st.markdown('<div class="stat-card"><span style="color:#34d399; font-size:13px;">📈 Recettes</span><h3 style="margin:5px 0 0 0; color:#34d399;">0 F</h3></div>', unsafe_allow_html=True)
with stat_col2:
    st.markdown('<div class="stat-card"><span style="color:#f87171; font-size:13px;">📉 Dépenses</span><h3 style="margin:5px 0 0 0; color:#f87171;">0 F</h3></div>', unsafe_allow_html=True)

st.markdown('<div class="stat-card"><span style="color:#fbbf24; font-size:13px;">💼 Solde du jour</span><h3 style="margin:5px 0 0 0; color:#fbbf24;">0 F</h3></div>', unsafe_allow_html=True)

# Coach financier aperçu
st.markdown("""
    <div class="coach-card">
        <span style="color:#fbbf24; font-size:14px; font-weight:bold;">✨ Coach financier (aperçu)</span>
        <p style="color:#94a3b8; font-size:13px; margin:8px 0 0 0;">Enregistrez quelques opérations pour recevoir vos premiers conseils.</p>
    </div>
""", unsafe_allow_html=True)

# Journal vide
st.markdown("""
    <div style="background:#131b2e; border:1px solid rgba(255,255,255,0.06); padding:24px; border-radius:16px; text-align:center; color:#94a3b8; font-size:14px;">
        Votre journal est vide. Dites votre première opération pour commencer.
    </div>
""", unsafe_allow_html=True)
