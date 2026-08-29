import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="SINAN AI — Journal vocal quotidien", page_icon="📖", layout="wide")

# --- DESIGN ET STYLE VISUEL (PROTOTYPE MOBILE) ---
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
    st.session_state.journal = [
        {"date": "29/08/2026 07:10", "libelle": "Vente de marchandises au marché", "type": "Recette", "montant": 45000}
    ]
if 'dettes' not in st.session_state:
    st.session_state.dettes = [
        {"tiers": "Konate service", "type": "Dette", "montant": 1000000, "regle": 0, "echeance": "2026-08-29", "statut": "en_retard"}
    ]
if 'tontines' not in st.session_state:
    st.session_state.tontines = [
        {"nom": "Tontine Entreprise Abidjan", "montant": 50000, "frequence": "Mensuelle", "beneficiaire": "Mamadou"}
    ]
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

# Sélecteur de langue interactif
langues = ["Français", "English", "Nouchi", "Dioula"]
cols_lang = st.columns(4)
for i, l in enumerate(langues):
    with cols_lang[i]:
        if st.button(l, key=f"lang_{l}", use_container_width=True):
            st.session_state.langue = l
            st.toast(f"Langue : {l}")

st.write("")

# Navigation principale interactive (onglets cliquables)
menu_items = ["Journal", "Projets", "Finances perso", "Dettes & Créances", "Trésorerie 360°", "Tontine & Cotisations", "Coach IA"]
selected_tab = st.radio("Navigation", menu_items, horizontal=True, label_visibility="collapsed")
st.session_state.onglet_actif = selected_tab

st.write("---")

# ==========================================
# 1. MODULE JOURNAL & ENREGISTREMENT VOCAL
# ==========================================
if st.session_state.onglet_actif == "Journal":
    st.markdown("#### 🎙️ Enregistrement en temps réel")
    
    col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
    with col_m2:
        if st.button("🎤 Micro prêt — Appuyez pour parler", use_container_width=True):
            st.session_state.journal.insert(0, {
                "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "libelle": "Dictée vocale : Vente reçue par Wave",
                "type": "Recette",
                "montant": 25000
            })
            st.success("🎤 Vocal transcrit et enregistré avec succès !")
            st.rerun()

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
            st.rerun()

    st.markdown("**Exemples à essayer :**")
    exs = ["J'ai vendu du riz pour quinze mille francs", "J'ai acheté du carburant pour 5000 francs", "J'ai payé le loyer de la boutique, cent mille francs"]
    for ex in exs:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state.journal.insert(0, {"date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "libelle": ex, "type": "Dépense", "montant": 5000})
            st.rerun()

    st.write("---")
    
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
        csv_data = df_j.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Exporter en CSV", data=csv_data, file_name="journal.csv", mime="text/csv")
    else:
        st.info("Votre journal est vide.")

# ==========================================
# 2. MODULE PROJETS
# ==========================================
elif st.session_state.onglet_actif == "Projets":
    st.subheader("📁 Gestion Multi-Projets")
    nouveau_projet = st.text_input("🎙️ Ajouter un nouveau projet", placeholder="Ex: Chantier R+4 Angré")
    if st.button("Enregistrer le projet"):
        if nouveau_projet:
            st.success(f"Projet '{nouveau_projet}' créé et activé avec succès !")
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
    if st.button("Ajouter une dépense perso"):
        st.success("Dépense personnelle enregistrée dans le budget familial.")

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
    with st.form("form_dette", clear_on_submit=True):
        type_d = st.selectbox("Type", ["Je dois (dette)", "On me doit (créance)"])
        tiers_nom = st.text_input("Nom du fournisseur / client")
        montant_d = st.number_input("Montant total", min_value=0, step=1000)
        echeance_d = st.date_input("Date d'échéance")
        if st.form_submit_button("Enregistrer l'engagement"):
            st.session_state.dettes.append({
                "tiers": tiers_nom, 
                "type": "Dette" if "dois" in type_d else "Créance", 
                "montant": montant_d, 
                "regle": 0, 
                "echeance": str(echeance_d), 
                "statut": "en_cours"
            })
            st.success("Engagement enregistré avec succès !")
            st.rerun()

    st.write("#### Suivi des tiers")
    for idx, d in enumerate(st.session_state.dettes):
        st.markdown(f"""
        <div style="background:#1E222A; padding:15px; border-radius:10px; margin-bottom:10px;">
            <b>{d['tiers']}</b> — Échéance : {d['echeance']}<br>
            <span style="color:#FF9F43;">Statut : {d['statut']}</span><br>
            Reste dû : <b>{d['montant'] - d['regle']:,.0f} F</b>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Régler une partie ({d['tiers']})", key=f"regler_{idx}"):
            st.session_state.dettes[idx]['regle'] += 50000
            st.success("Règlement pris en compte !")
            st.rerun()

# ==========================================
# 5. MODULE TRÉSORERIE 360°
# ==========================================
elif st.session_state.onglet_actif == "Trésorerie 360°":
    st.subheader("💳 Passerelle Financière & Trésorerie 360°")
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
    
    if st.button("Simuler un transfert Wave -> Banque"):
        st.session_state.comptes_360["Wave"] -= 20000
        st.session_state.comptes_360["Compte Bancaire"] += 20000
        st.success("Transfert de trésorerie effectué avec succès !")
        st.rerun()

# ==========================================
# 6. MODULE TONTINE ET COTISATIONS
# ==========================================
elif st.session_state.onglet_actif == "Tontine & Cotisations":
    st.subheader("👥 Module Tontine & Cotisations de Groupe")
    with st.form("form_tontine", clear_on_submit=True):
        nom_tontine = st.text_input("Nom du cercle de tontine / cotisation")
        montant_part = st.number_input("Montant de la part / cotisation (F)", min_value=0, step=5000)
        frequence = st.selectbox("Fréquence", ["Journalière", "Hebdomadaire", "Mensuelle"])
        beneficiaire = st.text_input("Bénéficiaire du tour actuel")
        if st.form_submit_button("Créer / Rejoindre le groupe de tontine"):
            st.session_state.tontines.append({
                "nom": nom_tontine, 
                "montant": montant_part, 
                "frequence": frequence, 
                "beneficiaire": beneficiaire
            })
            st.success("Cercle de tontine enregistré avec succès !")
            st.rerun()

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
# 7. MODULE COACH IA
# ==========================================
elif st.session_state.onglet_actif == "Coach IA":
    st.subheader("🤖 Coach Financier & Analyse Stratégique")
    if st.button("Lancer l'analyse globale par le Coach IA"):
        st.markdown("""
        ### 📊 Diagnostic Stratégique Consolidé
        - **Liquidités 360° :** Saines, forte présence Mobile Money.
        - **Alerte Tiers :** Encours en retard sur Konate service (1 000 000 F).
        - **Recommandation :** Relancer les créances et automatiser l'épargne tontine.
        """)
    question_coach = st.text_input("💬 Posez une question libre au coach financier", placeholder="Ex: Puis-je acheter ce stock ?")
    if st.button("Envoyer au Coach"):
        if question_coach:
            st.info(f"Analyse IA en cours pour : '{question_coach}' -> Vos liquidités actuelles permettent cet investissement à hauteur de 15% max.")
