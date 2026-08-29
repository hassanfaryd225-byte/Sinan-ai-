import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="SINAN AI — Journal vocal quotidien", page_icon="📖", layout="wide")

# --- DESIGN ET STYLE VISUEL (PROTOTYPE MOBILE CONFORME AUX CAPTURES) ---
bg_color = "#12151B"      
card_bg_color = "#1E222A" 
text_color = "#EDE7D3"    
text_muted = "#9CA3AE"    
primary_orange = "#FF9F43"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    h1, h2, h3, h4, h5, h6 {{ color: {text_color}; }}
    p, label, div {{ color: {text_color}; }}
    
    .stButton > button {{
        background-color: {primary_orange};
        color: #12151B;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 8px 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION DE L'ÉTAT DE SESSION ---
if 'langue' not in st.session_state:
    st.session_state.langue = "Français"
if 'onglet_actif' not in st.session_state:
    st.session_state.onglet_actif = "Journal"
if 'journal' not in st.session_state:
    st.session_state.journal = []
if 'dettes' not in st.session_state:
    st.session_state.dettes = [
        {"tiers": "Konate service", "type": "Dette", "montant": 1000000, "regle": 0, "echeance": "2026-08-29", "statut": "en_retard"}
    ]
if 'tontines' not in st.session_state:
    st.session_state.tontines = []
if 'comptes_360' not in st.session_state:
    st.session_state.comptes_360 = {
        "Orange Money": 125000,
        "Wave": 45000,
        "MTN MoMo": 15000,
        "Djamo": 20000,
        "Compte Bancaire": 850000,
        "Cash / Caisse": 35000
    }

# --- EN-TÊTE DU PROTOTYPE ---
st.markdown("### 📖 SINAN AI")
st.markdown("<p style='color: #9CA3AE; margin-top: -10px;'>Journal vocal quotidien & Consolidation 360°</p>", unsafe_allow_html=True)

# Sélecteur de langue (Français, English, Nouchi, Dioula)
langues = ["Français", "English", "Nouchi", "Dioula"]
cols_lang = st.columns(4)
for i, l in enumerate(langues):
    with cols_lang[i]:
        if st.button(l, key=f"lang_{l}", use_container_width=True):
            st.session_state.langue = l

st.write("")

# Navigation principale sous forme de boutons (style visuel des captures)
menu_items = ["Journal", "Projets", "Finances perso", "Dettes & Créances", "Trésorerie 360°", "Tontine & Cotisations", "Coach IA"]
selected_tab = st.radio("Navigation", menu_items, horizontal=True, label_visibility="collapsed")
st.session_state.onglet_actif = selected_tab

st.write("---")

# ==========================================
# 1. MODULE JOURNAL & ENREGISTREMENT VOCAL
# ==========================================
if st.session_state.onglet_actif == "Journal":
    st.markdown("#### 🎙️ Enregistrement en temps réel")
    
    # Bouton micro central simulé avec support vocal
    col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
    with col_m2:
        if st.button("🎤 Micro prêt — Appuyez pour parler", use_container_width=True):
            st.info("🎙️ Enregistrement vocal actif... (Transcription en cours selon la langue : " + st.session_state.langue + ")")

    # Saisie texte alternative avec bouton micro intégré
    with st.form("form_journal", clear_on_submit=True):
        saisie_texte = st.text_input("Ou tapez votre opération", placeholder="Ex: j'ai vendu du riz pour 15000 francs")
        col_sub1, col_sub2 = st.columns([3, 1])
        with col_sub2:
            valider_saisie = st.form_submit_button("OK", use_container_width=True)
            
        if valider_saisie and saisie_texte:
            st.session_state.journal.insert(0, {
                "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "libelle": saisie_texte,
                "type": "Recette" if "vendu" in saisie_texte.lower() or "reçu" in saisie_texte.lower() else "Dépense",
                "montant": 15000 if "15000" in saisie_texte else 5000
            })
            st.success("Opération ajoutée au journal en temps réel !")

    st.markdown("**Exemples à essayer :**")
    exs = ["J'ai vendu du riz pour quinze mille francs", "J'ai acheté du carburant pour 5000 francs", "J'ai payé le loyer de la boutique, cent mille francs"]
    for ex in exs:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state.journal.insert(0, {"date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "libelle": ex, "type": "Dépense", "montant": 5000})
            st.rerun()

    st.write("---")
    
    # Indicateurs du jour
    df_j = pd.DataFrame(st.session_state.journal)
    recettes_tot = df_j[df_j['type'] == 'Recette']['montant'].sum() if not df_j.empty else 0
    depenses_tot = df_j[df_j['type'] == 'Dépense']['montant'].sum() if not df_j.empty else 0
    solde_jour = recettes_tot - depenses_tot

    c_r1, c_r2 = st.columns(2)
    with c_r1:
        st.metric("📈 Recettes", f"{recettes_tot:,.0f} F")
    with c_r2:
        st.metric("📉 Dépenses", f"{depenses_tot:,.0f} F")
    st.metric("💰 Solde du jour", f"{solde_jour:,.0f} F")

    st.write("#### Historique du Journal")
    if not df_j.empty:
        st.dataframe(df_j.style.format({'montant': '{:,.0f} F'}), use_container_width=True)
        if st.button("📥 Exporter en CSV"):
            st.download_button("Télécharger CSV", data=df_j.to_csv(index=False).encode('utf-8'), file_name="journal.csv", mime="text/csv")
    else:
        st.info("Votre journal est vide. Dites votre première opération pour commencer.")

# ==========================================
# 2. MODULE PROJETS
# ==========================================
elif st.session_state.onglet_actif == "Projets":
    st.subheader("📁 Gestion Multi-Projets")
    st.text_input("🎙️ Ajouter un nouveau projet vocalement ou par texte", placeholder="Ex: Chantier R+4 Angré")
    st.markdown("""
    * **Projet 1 :** Neema Ferme (Actif) — *Solde analytique : +450 000 F*
    * **Projet 2 :** Chantier R+4 Angré (Actif) — *Solde analytique : -1 200 000 F*
    """)

# ==========================================
# 3. MODULE FINANCES PERSO
# ==========================================
elif st.session_state.onglet_actif == "Finances perso":
    st.subheader("🏠 Finances Personnelles & Budget Familial")
    st.metric("Budget Perso Disponible", "320 000 F CFA")
    st.write("Suivi séparé des dépenses familiales et personnelles hors SYSCOHADA strict.")

# ==========================================
# 4. MODULE DETTES & CRÉANCES
# ==========================================
elif st.session_state.onglet_actif == "Dettes & Créances":
    st.subheader("🤝 Gestion des Dettes & Créances")
    
    tot_dettes = sum([d['montant'] - d['regle'] for d in st.session_state.dettes if d['type'] == 'Dette'])
    tot_creances = sum([d['montant'] - d['regle'] for d in st.session_state.dettes if d['type'] == 'Créance'])
    
    c_d1, c_d2 = st.columns(2)
    with c_d1:
        st.metric("Total dettes", f"{tot_dettes:,.0f} F")
    with c_d2:
        st.metric("Total créances", f"{tot_creances:,.0f} F")
    st.metric("Position nette", f"{tot_creances - tot_dettes:,.0f} F")

    st.write("#### Enregistrer un engagement")
    with st.form("form_dette"):
        type_d = st.selectbox("Type", ["Je dois (dette)", "On me doit (créance)"])
         tiers_nom = st.text_input("Nom du fournisseur / client")
         montant_d = st.number_input("Montant total", min_value=0, step=1000)
         echeance_d = st.date_input("Date d'échéance")
         if st.form_submit_button("Enregistrer"):
             st.session_state.dettes.append({"tiers": tiers_nom, "type": "Dette" if "dois" in type_d else "Créance", "montant": montant_d, "regle": 0, "echeance": str(echeance_d), "statut": "en_cours"})
             st.success("Enregistré avec succès !")

    st.write("#### Suivi des tiers")
    for d in st.session_state.dettes:
        st.markdown(f"""
        <div style="background:#1E222A; padding:15px; border-radius:10px; margin-bottom:10px;">
            <b>{d['tiers']}</b> — Échéance : {d['echeance']}<br>
            <span style="color:#FF9F43;">Statut : {d['statut']}</span><br>
            Reste dû : <b>{d['montant'] - d['regle']:,.0f} F</b>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 5. MODULE TRÉSORERIE 360° & PASSERELLE FINANCIÈRE
# ==========================================
elif st.session_state.onglet_actif == "Trésorerie 360°":
    st.subheader("💳 Passerelle Financière & Trésorerie 360°")
    st.write("Agrégation en temps réel : Wave, Orange Money, Moov Money, MTN MoMo, Djamo, Cartes bancaires et Cash.")
    
    total_360 = sum(st.session_state.comptes_360.values())
    st.metric("Trésorerie Globale Consolidée", f"{total_360:,.0f} F CFA")
    
    cols_t = st.columns(2)
    idx = 0
    for k, v in st.session_state.comptes_360.items():
        with cols_t[idx % 2]:
            st.markdown(f"""
            <div style="background:#1E222A; padding:15px; border-radius:10px; margin-bottom:10px;">
                <b>{k}</b><br>
                <span style="font-size:1.4rem; color:#FF9F43;">{v:,.0f} F</span>
            </div>
            """, unsafe_allow_html=True)
        idx += 1

# ==========================================
# 6. MODULE TONTINE ET COTISATIONS
# ==========================================
elif st.session_state.onglet_actif == "Tontine & Cotisations":
    st.subheader("👥 Module Tontine & Cotisations de Groupe")
    st.write("Gérez vos tontines tournantes, épargnes collectives et cotisations professionnelles.")
    
    with st.form("form_tontine"):
        nom_tontine = st.text_input("Nom du cercle de tontine / cotisation")
        montant_part = st.number_input("Montant de la part / cotisation (F)", min_value=0, step=5000)
        frequence = st.selectbox("Fréquence", ["Journalière", "Hebdomadaire", "Mensuelle"])
        beneficiaire = st.text_input("Bénéficiaire du tour actuel")
        if st.form_submit_button("Créer / Rejoindre le groupe de tontine"):
            st.session_state.tontines.append({"nom": nom_tontine, "montant": montant_part, "frequence": frequence, "beneficiaire": beneficiaire})
            st.success("Cercle de tontine enregistré avec succès !")

    if st.session_state.tontines:
        st.write("#### Cercles actifs")
        for t in st.session_state.tontines:
            st.markdown(f"""
            <div style="background:#1E222A; padding:15px; border-radius:10px; margin-bottom:10px;">
                👥 <b>{t['nom']}</b> ({t['frequence']})<br>
                Montant : {t['montant']:,.0f} F | Prochain bénéficiaire : {t['beneficiaire']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aucun cercle de tontine enregistré.")

# ==========================================
# 7. MODULE COACH IA & STRATÉGIE GLOBALE
# ==========================================
elif st.session_state.onglet_actif == "Coach IA":
    st.subheader("🤖 Coach Financier & Analyse Stratégique")
    st.write("Analyse consolidée à 360° de vos performances et propositions de stratégies sur une durée.")
    
    if st.button("Lancer l'analyse globale par le Coach IA"):
        st.markdown("""
        ### 📊 Diagnostic Stratégique Consolidé
        - **Liquidités 360° :** Saines, mais forte concentration sur les comptes Mobile Money.
        - **Alerte Tiers :** Un encours en retard (Konate service - 1 000 000 F) nécessite une relance immédiate pour préserver le fonds de roulement.
        - **Recommandation :** Automatiser les transferts de trésorerie excédentaire vers le compte bancaire principal et structurer les apports de tontines dans le journal pro.
        """)
    
    st.text_input("💬 Posez une question libre au coach financier", placeholder="Ex: Est-ce que je peux financer cet achat de stock ?")
