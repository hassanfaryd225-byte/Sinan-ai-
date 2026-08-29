import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="SINAN AI — Assistant Financier & Journal Intelligent", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- DESIGN SYSTEM "SILICON VALLEY X AFRIQUE" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-color: #0B0F17;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Masquer les éléments superflus de Streamlit pour un rendu clean type App Native */
    #MainMenu, header, footer {visibility: hidden;}
    
    /* Cartes au design épuré et moderne */
    .app-card {
        background: #161B22;
        border: 1px solid #21262D;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    
    /* Boutons stylisés */
    .stButton > button {
        background: linear-gradient(135deg, #FF9F43 0%, #FF7600 100%);
        color: #0B0F17;
        font-weight: 700;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255,159,67,0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(255,159,67,0.5);
    }

    /* Champs de saisie */
    .stTextInput > div > div > input, .stSelectbox > div > div {
        background-color: #161B22;
        color: #F0F6FC;
        border-radius: 12px;
        border: 1px solid #30363D;
        padding: 10px;
    }
    
    /* Métriques */
    .metric-container {
        background: #161B22;
        border: 1px solid #21262D;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION DE L'ÉTAT GLOBAL ---
if 'langue' not in st.session_state: st.session_state.langue = "Français"
if 'onglet' not in st.session_state: st.session_state.onglet = "Journal"
if 'journal' not in st.session_state: st.session_state.journal = []
if 'dettes' not in st.session_state: st.session_state.dettes = []
if 'tontines' not in st.session_state: st.session_state.tontines = []
if 'comptes_360' not in st.session_state:
    st.session_state.comptes_360 = {
        "Wave": 125000,
        "Orange Money": 85000,
        "MTN MoMo": 30000,
        "Compte Bancaire": 450000,
        "Cash / Caisse": 45000
    }

# --- EN-TÊTE DE L'APPLICATION ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("<div style='background: linear-gradient(135deg, #FF9F43, #FF7600); width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;'>⚡</div>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h2 style='margin:0; color: #F0F6FC; font-size: 1.5rem;'>SINAN AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; color: #8B949E; font-size: 0.85rem;'>Intelligence financière & Comptabilité intuitive</p>", unsafe_allow_html=True)

st.write("")

# --- SÉLECTEUR DE LANGUE ---
langues = ["Français", "English", "Nouchi", "Dioula"]
cols_lang = st.columns(4)
for i, l in enumerate(langues):
    with cols_lang[i]:
        if st.button(l, key=f"lang_{l}"):
            st.session_state.langue = l
            st.toast(f"Langue activée : {l}")

st.write("---")

# --- NAVIGATION PRINCIPALE ---
onglets = ["Journal", "Trésorerie", "Dettes", "Tontines", "Coach IA"]
selected_tab = st.selectbox("Navigation rapide", onglets, label_visibility="collapsed")
st.session_state.onglet = selected_tab

st.write("")

# ==========================================
# 1. MODULE JOURNAL & VOCAL
# ==========================================
if st.session_state.onglet == "Journal":
    st.markdown("### 🎙️ Saisie en Temps Réel")
    
    if st.button("🎤 Appuyer pour dicter (Ex: 'Vente 15000 Wave')"):
        st.session_state.journal.insert(0, {
            "date": datetime.datetime.now().strftime("%d/%m %H:%M"),
            "libelle": "Vente de marchandises (Vocal)",
            "type": "Recette",
            "montant": 15000
        })
        st.success("Transaction vocale enregistrée instantanément !")
        st.rerun()

    with st.form("form_saisie", clear_on_submit=True):
        texte_op = st.text_input("Ou décrivez votre opération", placeholder="Ex: Achat de carburant 5000 F")
        if st.form_submit_button("Valider l'opération"):
            if texte_op:
                st.session_state.journal.insert(0, {
                    "date": datetime.datetime.now().strftime("%d/%m %H:%M"),
                    "libelle": texte_op,
                    "type": "Dépense" if "achat" in texte_op.lower() or "payé" in texte_op.lower() else "Recette",
                    "montant": 10000
                })
                st.success("Opération enregistrée avec succès !")
                st.rerun()

    st.write("#### Historique & Flux du Jour")
    df_j = pd.DataFrame(st.session_state.journal)
    if not df_j.empty:
        st.dataframe(df_j.style.format({'montant': '{:,.0f} F'}), use_container_width=True)
    else:
        st.info("Aucune opération enregistrée pour le moment. Utilisez le micro ou le formulaire.")

# ==========================================
# 2. MODULE TRÉSORERIE 360°
# ==========================================
elif st.session_state.onglet == "Trésorerie":
    st.markdown("### 💳 Trésorerie 360° (Mobile Money & Banques)")
    total_360 = sum(st.session_state.comptes_360.values())
    
    st.markdown(f"""
    <div class="metric-container">
        <p style="color: #8B949E; margin:0; font-size:0.9rem;">Trésorerie Consolidée Globale</p>
        <h1 style="color: #FF9F43; margin:5px 0 0 0; font-size:2rem;">{total_360:,.0f} F CFA</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    for k, v in st.session_state.comptes_360.items():
        st.markdown(f"""
        <div style="background: #161B22; padding: 14px 18px; border-radius: 12px; border: 1px solid #21262D; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-weight: 600; color: #F0F6FC;">{k}</span>
            <span style="color: #FF9F43; font-weight: 700; font-size: 1.1rem;">{v:,.0f} F</span>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 3. MODULE DETTES & CRÉANCES
# ==========================================
elif st.session_state.onglet == "Dettes":
    st.markdown("### 🤝 Gestion des Dettes & Crédits Tiers")
    
    with st.form("form_dette", clear_on_submit=True):
        tiers = st.text_input("Nom du partenaire (Client / Fournisseur)")
        montant = st.number_input("Montant (F CFA)", min_value=0, step=5000)
        type_dette = st.selectbox("Nature", ["Dette (Je dois)", "Créance (On me doit)"])
        echeance = st.date_input("Date limite d'échéance")
        
        if st.form_submit_button("Enregistrer l'engagement"):
            if tiers and montant > 0:
                st.session_state.dettes.append({"tiers": tiers, "montant": montant, "type": type_dette, "echeance": str(echeance)})
                st.success("Engagement enregistré avec succès !")
                st.rerun()

    df_d = pd.DataFrame(st.session_state.dettes)
    if not df_d.empty:
        st.dataframe(df_d.style.format({'montant': '{:,.0f} F'}), use_container_width=True)
    else:
        st.info("Aucun crédit ou dette en cours.")

# ==========================================
# 4. MODULE TONTINE & COTISATIONS
# ==========================================
elif st.session_state.onglet == "Tontines":
    st.markdown("### 👥 Cercles de Tontine & Épargne Solidaire")
    
    with st.form("form_tontine", clear_on_submit=True):
        nom_cercle = st.text_input("Nom du groupe ou de la tontine")
        cotisation = st.number_input("Montant de la part (F CFA)", min_value=0, step=10000)
        frequence = st.selectbox("Fréquence", ["Journalière", "Hebdomadaire", "Mensuelle"])
        
        if st.form_submit_button("Créer le cercle solidaire"):
            if nom_cercle and cotisation > 0:
                st.session_state.tontines.append({"nom": nom_cercle, "montant": cotisation, "frequence": frequence})
                st.success("Cercle de tontine initialisé avec succès !")
                st.rerun()

    df_t = pd.DataFrame(st.session_state.tontines)
    if not df_t.empty:
        st.dataframe(df_t.style.format({'montant': '{:,.0f} F'}), use_container_width=True)
    else:
        st.info("Aucun cercle de tontine actif.")

# ==========================================
# 5. MODULE COACH IA & STRATÉGIE
# ==========================================
elif st.session_state.onglet == "Coach IA":
    st.markdown("### 🤖 Intelligence Stratégique SINAN")
    
    if st.button("Lancer l'analyse globale de santé financière"):
        st.markdown("""
        <div class="app-card">
            <h4 style="color: #FF9F43; margin-top:0;">📊 Rapport Analytique SINAN AI</h4>
            <p style="color: #F0F6FC; line-height: 1.5;">
            <b>Liquidités :</b> Vos flux Wave et Orange Money couvrent sainement vos charges à court terme.<br><br>
            <b>Recommandation :</b> Pensez à sécuriser vos excédents de caisse vers votre compte bancaire principal pour optimiser votre rentabilité globale.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    question = st.text_input("💬 Posez une question financière à votre assistant IA")
    if st.button("Envoyer au Coach"):
        if question:
            st.info("Analyse IA : Votre position de trésorerie actuelle permet cet investissement sous réserve de maintenir une réserve de sécurité de 20%.")
