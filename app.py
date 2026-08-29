import streamlit as st
import pandas as pd
import datetime
import base64
from io import BytesIO

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="SINAN AI — Journal vocal quotidien", page_icon="S", layout="wide")

# --- PALETTE DE COULEURS ET CSS ---
# Ces styles reproduisent l'apparence des images fournies.
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
    
    /* Style des cartes de métriques */
    .metric-card {{
        background-color: {card_bg_color};
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #2A313A;
        margin-bottom: 15px;
    }}
    .metric-title {{ color: {text_muted}; font-size: 0.9rem; margin-bottom: 5px; }}
    .metric-value {{ color: {text_color}; font-size: 1.8rem; font-weight: bold; }}
    .metric-delta-recette {{ color: #2ECC71; font-size: 1rem; }} /* Vert */
    .metric-delta-depense {{ color: #E74C3C; font-size: 1rem; }} /* Rouge */

    /* Style des onglets */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
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

    /* Style des champs de saisie */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
        background-color: {card_bg_color};
        color: {text_color};
        border-radius: 8px;
        border: 1px solid #2A313A;
    }}
    
    /* Style du bouton OK */
    .stButton > button {{
        background-color: #FFC107; /* Jaune */
        color: {bg_color};
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 8px 20px;
    }}
    
    /* Style des exemples à essayer */
    .example-tag {{
        background-color: rgba(255,255,255,0.03);
        color: {text_muted};
        border-radius: 15px;
        padding: 6px 12px;
        font-size: 0.85rem;
        margin: 5px;
        display: inline-block;
        border: 1px solid #2A313A;
    }}
    
    /* Style de la zone "Votre journal est vide" */
    .empty-journal {{
        background-color: #FDF6E3; /* Beige très clair */
        color: #5D646E; /* Gris foncé */
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
    st.markdown("<p style='color: #9CA3AE; margin-top: -10px;'>Journal vocal quotidien</p>", unsafe_allow_html=True)

st.write("---")

# --- GESTION DE L'ÉTAT DE LA SESSION (Session State) ---
# Ces variables sauvegardent vos données pendant l'utilisation de l'application.
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'debts' not in st.session_state:
    st.session_state.debts = []

# --- LOGIQUE DE SAISIE DES TRANSACTIONS ---
def process_input(text_input):
    # Analyse très basique (simulant l'IA)
    text_input = text_input.lower()
    type = "Autre"
    montant = 0
    categorie = "Non classé"
    
    # Recherche de mots-clés (simpliste, une vraie IA serait nécessaire pour le langage naturel)
    if "vendu" in text_input or "reçu" in text_input:
        type = "Recette"
        categorie = "Vente"
    elif "acheté" in text_input or "payé" in text_input:
        type = "Dépense"
        categorie = "Achat/Loyer"

    # Extraction de nombres (format "15000", "100 mille")
    mots = text_input.split()
    for i, mot in enumerate(mots):
        # Remplacement des mots français courants par des chiffres
        cleaned_mot = mot.replace(",", "").replace(" ", "")
        if cleaned_mot.isdigit():
            montant = int(cleaned_mot)
        elif cleaned_mot == "mille" and i > 0 and mots[i-1].isdigit():
             montant = int(mots[i-1]) * 1000
        elif cleaned_mot == "millions" and i > 0 and mots[i-1].isdigit():
            montant = int(mots[i-1]) * 1000000

    # Ajout de l'opération si un montant a été détecté
    if montant > 0:
        st.session_state.transactions.insert(0, {
            "Date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Description": text_input.capitalize(),
            "Type": type,
            "Montant": montant,
            "Catégorie": categorie
        })
        st.success(f"✅ Opération enregistrée : {montant} F ({type})")
    else:
        st.error("❌ Impossible de détecter un montant. Veuillez reformuler.")


# --- INTERFACE PRINCIPALE (Onglets) ---
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🎙️ Journal", "📈 Finances", "🤝 Dettes", "📄 Rapports"])

with tab1:
    # --- SECTION "DITES VOTRE OPÉRATION" (Saisie) ---
    st.markdown("<h3 style='text-align: center;'>Dites votre opération du jour</h3>", unsafe_allow_html=True)

    col_mic1, col_mic2, col_mic3 = st.columns([1, 2, 1])
    with col_mic2:
        # Simulation du micro
        st.markdown(f"""
        <div style='display: flex; justify-content: center; align-items: center; flex-direction: column;'>
            <div style='width: 120px; height: 120px; background: radial-gradient(circle, {primary_color} 60%, #FFC107 100%); border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 4em; color: {bg_color}; box-shadow: 0 0 30px rgba(255,159,67,0.5);'>
                🎙️
            </div>
            <p style='color: {text_muted}; margin-top: 10px;'>⚪ ⚪ ⚪ ⚪ ⚪</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    # Saisie textuelle (Alternative au micro)
    st.markdown(f"<p style='text-align: center; color: {text_muted};'>⌨️ Ou tapez votre opération</p>", unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns([5, 1])
    with col_input1:
        user_input = st.text_input("Saisie opération", label_visibility="collapsed", placeholder="Ex : j'ai vendu du riz pour 15000 francs")
    with col_input2:
        ok_button = st.button("OK")

    if ok_button and user_input:
        process_input(user_input)

    # Exemples à essayer
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
                # Si on clique sur un exemple, on met à jour l'état et on simule l'enregistrement
                process_input(ex)

with tab2:
    # --- SECTION "FINANCES" (Tableau de bord) ---
    st.subheader("📊 Tableau de bord financier")
    
    df_trans = pd.DataFrame(st.session_state.transactions)
    
    if df_trans.empty:
         st.markdown('<div class="empty-journal">Votre journal est vide. Enregistrez quelques opérations pour voir vos statistiques.</div>', unsafe_allow_html=True)
    else:
        # Calculs
        total_recettes = df_trans[df_trans['Type'] == 'Recette']['Montant'].sum()
        total_depenses = df_trans[df_trans['Type'] == 'Dépense']['Montant'].sum()
        solde = total_recettes - total_depenses
        
        # Affichage des cartes
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>RECETTES (Aujourd'hui)</div>
                    <div class='metric-value'>{total_recettes:,} F</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>DÉPENSES (Aujourd'hui)</div>
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
        # Affichage du tableau avec style
        st.dataframe(df_trans.style.format({'Montant': '{:,.0f} F'}).applymap(lambda x: 'color: #2ECC71' if x == 'Recette' else ('color: #E74C3C' if x == 'Dépense' else ''), subset=['Type']), use_container_width=True)

with tab3:
    # --- MODULE DE GESTION DES DETTES ---
    st.subheader("🤝 Gestion des Dettes (Crédits & Créances)")

    col_d1, col_d2 = st.columns([2, 1])
    
    with col_d1:
        st.markdown("#### Ajouter une dette / créance")
        with st.form("debt_form", clear_on_submit=True):
            debt_name = st.text_input("Nom de la personne ou entité")
            debt_type = st.selectbox("Type", ["Je dois (Crédit)", "On me doit (Créance)"])
            debt_amount = st.number_input("Montant (F)", min_value=0, step=1000)
            debt_desc = st.text_input("Raison (facultatif)")
            submit_debt = st.form_submit_button("Enregistrer la dette")
            
            if submit_debt and debt_name and debt_amount > 0:
                st.session_state.debts.append({
                    "Date": datetime.datetime.now().strftime("%d/%m/%Y"),
                    "Nom": debt_name,
                    "Type": debt_type,
                    "Montant": debt_amount,
                    "Description": debt_desc,
                    "Statut": "En cours"
                })
                st.success("Dette enregistrée.")

    with col_d2:
        # Calcul des totaux de dettes
        df_debts = pd.DataFrame(st.session_state.debts)
        if not df_debts.empty:
            credit_total = df_debts[df_debts['Type'] == "Je dois (Crédit)"]['Montant'].sum()
            creance_total = df_debts[df_debts['Type'] == "On me doit (Créance)"]['Montant'].sum()
            
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>TOTAL DETTES (Je dois)</div>
                    <div class='metric-value' style='color: #E74C3C;'>{credit_total:,} F</div>
                </div>
                <div class='metric-card'>
                    <div class='metric-title'>TOTAL CRÉANCES (On me doit)</div>
                    <div class='metric-value' style='color: #2ECC71;'>{creance_total:,} F</div>
                </div>
            """, unsafe_allow_html=True)

    if not st.session_state.debts:
        st.info("Aucune dette enregistrée.")
    else:
        st.write("#### Suivi des dettes")
        # Affichage du tableau des dettes avec boutons de remboursement
        
        display_debts = df_debts.copy()
        display_debts['Action'] = "Rembourser"
        
        # Édition de la dette pour remboursement
        edited_df_debts = st.data_editor(
            display_debts.style.format({'Montant': '{:,.0f} F'}).applymap(lambda x: 'color: #E74C3C' if x == "Je dois (Crédit)" else ('color: #2ECC71' if x == "On me doit (Créance)" else ''), subset=['Type']),
            use_container_width=True,
            hide_index=True,
            column_config={
                 "Action": st.column_config.Column(
                    "Action",
                    help="Cliquez pour rembourser (supprimer) la dette",
                    width="small",
                 )
            }
