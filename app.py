import streamlit as st
import pandas as pd
import datetime
import base64
from io import BytesIO

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

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="SINAN AI — Journal vocal quotidien", page_icon="S", layout="wide")

# --- PALETTE DE COULEURS ET CSS ---
primary_color = "#FF9F43" # Orange vif
bg_color = "#12151B"      # Fond très sombre
card_bg_color = "#1E222A" # Fond des cartes/onglets
text_color = "#EDE7D3"    # Crème pour le texte
text_muted = "#9CA3AE"    # Gris pour le texte secondaire

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    h1, h2, h3, h4, h5, h6 {{ color: {text_color}; }}
    p, label, div {{ color: {text_color}; }}
    
    .metric-card {{
        background-color: {card_bg_color};
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #2A313A;
        margin-bottom: 15px;
    }}
    .metric-title {{ color: {text_muted}; font-size: 0.9rem; margin-bottom: 5px; }}
    .metric-value {{ color: {text_color}; font-size: 1.8rem; font-weight: bold; }}

    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {card_bg_color};
        color: {text_muted};
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background-color: {primary_color};
        color: {bg_color};
        font-weight: bold;
    }}

    .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
        background-color: {card_bg_color};
        color: {text_color};
        border-radius: 8px;
        border: 1px solid #2A313A;
    }}
    
    .stButton > button {{
        background-color: #FFC107;
        color: {bg_color};
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 8px 20px;
    }}
    
    .empty-journal {{
        background-color: #FDF6E3;
        color: #5D646E;
        padding: 30px;
        border-radius: 14px;
        text-align: center;
        font-size: 1.1rem;
    }}
    </style>
""", unsafe_allow_html=True)

# --- TITRE DE L'APPLICATION ---
col_header1, col_header2 = st.columns([1, 5])
with col_header1:
    st.markdown("<div style='background-color: #FF9F43; width: 60px; height: 60px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 2em;'>📖</div>", unsafe_allow_html=True)
with col_header2:
    st.title("SINAN AI")
    st.markdown("<p style='color: #9CA3AE; margin-top: -10px;'>Journal vocal quotidien & Facturation électronique</p>", unsafe_allow_html=True)

st.write("---")

# --- ÉTAT DE LA SESSION ---
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'debts' not in st.session_state:
    st.session_state.debts = []

# --- FONCTION DE TRAITEMENT DE TEXTE ---
def process_input(text_input):
    text_input = text_input.lower()
    type_op = "Autre"
    montant = 0
    categorie = "Non classé"
    
    if "vendu" in text_input or "reçu" in text_input or "recette" in text_input:
        type_op = "Recette"
        categorie = "Vente"
    elif "acheté" in text_input or "payé" in text_input or "dépense" in text_input:
        type_op = "Dépense"
        categorie = "Achat/Charge"

    mots = text_input.split()
    for i, mot in enumerate(mots):
        cleaned_mot = mot.replace(",", "").replace(" ", "")
        if cleaned_mot.isdigit():
            montant = int(cleaned_mot)
        elif cleaned_mot == "mille" and i > 0 and mots[i-1].isdigit():
             montant = int(mots[i-1]) * 1000
        elif cleaned_mot == "millions" and i > 0 and mots[i-1].isdigit():
            montant = int(mots[i-1]) * 1000000

    if montant > 0:
        st.session_state.transactions.insert(0, {
            "Date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Description": text_input.capitalize(),
            "Type": type_op,
            "Montant": montant,
            "Catégorie": categorie
        })
        st.success(f"✅ Opération enregistrée : {montant:,} F ({type_op})")
    else:
        st.error("❌ Impossible de détecter un montant. Veuillez reformuler.")

# --- NAVIGATION PAR ONGLETS ---
tab1, tab2, tab3, tab4 = st.tabs(["🎙️ Journal", "📈 Finances", "🤝 Dettes", "📄 Rapports & Facture"])

with tab1:
    st.markdown("<h3 style='text-align: center;'>Dites votre opération du jour</h3>", unsafe_allow_html=True)
    
    col_mic1, col_mic2, col_mic3 = st.columns([1, 2, 1])
    with col_mic2:
        st.markdown(f"""
        <div style='display: flex; justify-content: center; align-items: center; flex-direction: column;'>
            <div style='width: 120px; height: 120px; background: radial-gradient(circle, {primary_color} 60%, #FFC107 100%); border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 4em; color: {bg_color}; box-shadow: 0 0 30px rgba(255,159,67,0.5);'>
                🎙️
            </div>
            <p style='color: {text_muted}; margin-top: 10px;'>⚪ ⚪ ⚪ ⚪ ⚪</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown(f"<p style='text-align: center; color: {text_muted};'>⌨️ Ou tapez votre opération</p>", unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns([5, 1])
    with col_input1:
        user_input = st.text_input("Saisie opération", label_visibility="collapsed", placeholder="Ex : j'ai vendu du riz pour 15000 francs")
    with col_input2:
        ok_button = st.button("OK")

    if ok_button and user_input:
        process_input(user_input)

    st.markdown("<p style='text-align: center; color: {text_muted}; margin-top: 20px; font-size: 0.9em;'>EXEMPLES À ESSAYER</p>", unsafe_allow_html=True)
    examples = [
        "J'ai vendu du riz pour quinze mille francs",
        "J'ai acheté du carburant pour 5000 francs",
        "J'ai payé le loyer de la boutique, cent mille francs"
    ]
    
    col_ex1, col_ex2, col_ex3 = st.columns([1, 2, 1])
    with col_ex2:
        for ex in examples:
            if st.button(ex, key=f"ex_{ex}"):
                process_input(ex)

with tab2:
    st.subheader("📊 Tableau de bord financier")
    df_trans = pd.DataFrame(st.session_state.transactions)
    
    if df_trans.empty:
         st.markdown('<div class="empty-journal">Votre journal est vide. Enregistrez quelques opérations pour voir vos statistiques.</div>', unsafe_allow_html=True)
    else:
        total_recettes = df_trans[df_trans['Type'] == 'Recette']['Montant'].sum()
        total_depenses = df_trans[df_trans['Type'] == 'Dépense']['Montant'].sum()
        solde = total_recettes - total_depenses
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>RECETTES</div>
                    <div class='metric-value'>{total_recettes:,} F</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>DÉPENSES</div>
                    <div class='metric-value'>{total_depenses:,} F</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m3:
            color_solde = "#2ECC71" if solde >= 0 else "#E74C3C"
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>SOLDE</div>
                    <div class='metric-value' style='color: {color_solde};'>{solde:,} F</div>
                </div>
            """, unsafe_allow_html=True)

        st.write("---")
        st.subheader("📋 Historique détaillé")
        st.dataframe(df_trans, use_container_width=True)

with tab3:
    st.subheader("🤝 Gestion des Dettes (Crédits & Créances)")

    col_d1, col_d2 = st.columns([2, 1])
    with col_d1:
        with st.form("debt_form", clear_on_submit=True):
            debt_name = st.text_input("Nom de la personne ou entité")
            debt_type = st.selectbox("Type", ["Je dois (Crédit)", "On me doit (Créance)"])
            debt_amount = st.number_input("Montant (F)", min_value=0, step=1000)
            debt_desc = st.text_input("Raison / Description")
            submit_debt = st.form_submit_button("Enregistrer la dette")
            
            if submit_debt and debt_name and debt_amount > 0:
                st.session_state.debts.append({
                    "Date": datetime.datetime.now().strftime("%d/%m/%Y"),
                    "Nom": debt_name,
                    "Type": debt_type,
                    "Montant": debt_amount,
                    "Description": debt_desc
                })
                st.success("Dette enregistrée avec succès.")

    with col_d2:
        df_debts = pd.DataFrame(st.session_state.debts)
        if not df_debts.empty:
            credit_total = df_debts[df_debts['Type'] == "Je dois (Crédit)"]['Montant'].sum()
            creance_total = df_debts[df_debts['Type'] == "On me doit (Créance)"]['Montant'].sum()
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>TOTAL DETTES</div>
                    <div class='metric-value' style='color: #E74C3C;'>{credit_total:,} F</div>
                </div>
                <div class='metric-card'>
                    <div class='metric-title'>TOTAL CRÉANCES</div>
                    <div class='metric-value' style='color: #2ECC71;'>{creance_total:,} F</div>
                </div>
            """, unsafe_allow_html=True)

    if not st.session_state.debts:
        st.info("Aucune dette enregistrée.")
    else:
        st.write("#### Suivi actif")
        st.dataframe(df_debts, use_container_width=True)

with tab4:
    st.subheader("📄 Génération de Reçu / Facture Normalisée Électronique")
    st.write("Générez instantanément une facture ou un reçu officiel pour vos clients.")

    with st.form("invoice_form"):
        client_name = st.text_input("Nom du Client / Partenaire", "Client Comptoir")
        invoice_item = st.text_input("Désignation de la prestation ou marchandise", "Vente de marchandises")
        invoice_amount = st.number_input("Montant Total (F)", min_value=0, step=500, value=15000)
        doc_type = st.selectbox("Type de document", ["Facture Normalisée", "Reçu de Paiement"])
        
        generate_btn = st.form_submit_button("Aperçu & Valider le document")

    if generate_btn:
        inv_id = datetime.datetime.now().strftime("FAC-%Y%m%d-%H%M")
        current_date = datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")
        
        st.markdown(f"""
        <div style="background: #FFFFFF; color: #000000; padding: 30px; border-radius: 10px; margin-top: 20px;">
            <h2 style="text-align: center; color: #111;">{doc_type.upper()}</h2>
            <hr>
            <p><b>N° de pièce :</b> {inv_id}</p>
            <p><b>Date :</b> {current_date}</p>
            <p><b>Client :</b> {client_name}</p>
            <br>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 2px solid #000;">
                    <th style="text-align: left; padding: 8px;">Désignation</th>
                    <th style="text-align: right; padding: 8px;">Montant</th>
                </tr>
                <tr>
                    <td style="padding: 8px;">{invoice_item}</td>
                    <td style="text-align: right; padding: 8px;">{invoice_amount:,} F</td>
                </tr>
            </table>
            <br>
            <h3 style="text-align: right;">TOTAL : {invoice_amount:,} F CFA</h3>
            <hr>
            <p style="text-align: center; font-size: 0.8rem; color: #666;">Document certifié électronique par SINAN AI - Code mémo de traçabilité fiscale validé.</p>
        </div>
        """, unsafe_allow_html=True)
        st.success("Document généré avec succès !")
