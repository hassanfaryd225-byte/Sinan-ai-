import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="SINAN AI — Assistant Comptable & Financier", page_icon="S", layout="wide")

# --- PALETTE DE COULEURS ET DESIGN (SYSCOHADA & PRO) ---
primary_color = "#FF9F43" 
bg_color = "#12151B"      
card_bg_color = "#1E222A" 
text_color = "#EDE7D3"    
text_muted = "#9CA3AE"    

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

    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div {{
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
    </style>
""", unsafe_allow_html=True)

# --- ÉTAT DE SESSION & AUTHENTIFICATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_phone' not in st.session_state:
    st.session_state.user_phone = ""
if 'role_utilisateur' not in st.session_state:
    st.session_state.role_utilisateur = "Propriétaire"
if 'projets' not in st.session_state:
    st.session_state.projets = ["Neema Ferme", "Chantier R+4 Angré", "Général"]
if 'ecritures_pro' not in st.session_state:
    st.session_state.ecritures_pro = []
if 'operations_perso' not in st.session_state:
    st.session_state.operations_perso = []
if 'dettes_creances' not in st.session_state:
    st.session_state.dettes_creances = []
if 'comptes_360' not in st.session_state:
    st.session_state.comptes_360 = {
        "Orange Money": 125000,
        "Wave": 45000,
        "MTN MoMo": 15000,
        "Compte Bancaire (Ecobank)": 850000,
        "Cash / Caisse": 35000,
        "Djamo / Cartes": 20000
    }

# --- EN-TÊTE PRINCIPAL ---
col1, col2 = st.columns([1, 6])
with col1:
    st.markdown("<div style='background-color: #FF9F43; width: 60px; height: 60px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 2em;'>📖</div>", unsafe_allow_html=True)
with col2:
    st.title("SINAN AI")
    st.markdown("<p style='color: #9CA3AE; margin-top: -10px;'>Journal vocal comptable, multi-projets, comptes de groupe & Consolidation 360°[span_0](start_span)[span_0](end_span)</p>", unsafe_allow_html=True)

st.write("---")

# --- MODULE D'AUTHENTIFICATION DIRECT (CENTRAL) ---
if not st.session_state.logged_in:
    st.subheader("🔐 Identifiez-vous pour commencer")
    with st.form("auth_form"):
        phone_input = st.text_input("Votre numéro de téléphone", placeholder="+225 0700000000")
        role_input = st.selectbox("Votre rôle dans le compte de groupe", ["Propriétaire", "Caissier / Gestionnaire", "Associé / Validateur"])
        submit_auth = st.form_submit_button("Se connecter / Accéder à l'application")
        
        if submit_auth:
            if phone_input:
                st.session_state.logged_in = True
                st.session_state.user_phone = phone_input
                st.session_state.role_utilisateur = role_input
                st.rerun()
            else:
                st.error("Veuillez entrer un numéro de téléphone valide.")
else:
    # Barre de statut connectée + Option de déconnexion
    c_info1, c_info2 = st.columns([4, 1])
    with c_info1:
        st.success(f"Connecté : {st.session_state.user_phone} ({st.session_state.role_utilisateur})")
    with c_info2:
        if st.button("Déconnexion"):
            st.session_state.logged_in = False
            st.rerun()

    st.write("")
    espace_type = st.radio("Sélectionner l'espace d'activité", ["Espace Professionnel (SYSCOHADA strict)", "Espace Personnel (Budget simplifié)"], horizontal=True)

    st.write("")
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🎙️ Saisie & Micro Global", 
        "🏦 Consolidation 360°", 
        "📊 Comptabilité & Projets", 
        "🤝 Dettes & Tiers", 
        "📄 Facturation FNE", 
        "🤖 Coach Stratégique IA",
        "📤 Exports"
    ])

    with tab1:
        st.subheader("🎙️ Saisie Vocale et Manuelle Multi-modules")
        st.info("💡 Astuce mobile : Utilisez le micro de votre clavier virtuel pour dicter vos textes dans les champs ci-dessous.")
        
        with st.form("entry_form", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                desc_input = st.text_input("🎙️ Description / Libellé de l'opération", placeholder="Ex: Achat marchandises")
                type_mouvement = st.selectbox("Sens de l'opération", ["Recette / Produit (Classe 7)", "Dépense / Charge (Classe 6)"])
                projet_choisi = st.selectbox("Nomination & Séparation du projet", st.session_state.projets)
            with col_f2:
                montant_input = st.number_input("Montant en Francs CFA (XOF)", min_value=0, step=500)
                passerelle_source = st.selectbox("Passerelle de Paiement / Source", [
                    "Espèces / Cash", "Orange Money", "Wave", "MTN MoMo", 
                    "Moov Money", "Djamo", "Compte Bancaire", "Carte Bancaire / App Pay"
                ])
                
            submitted = st.form_submit_button("Enregistrer l'opération")
            
            if submitted and desc_input and montant_input > 0:
                date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                sens_val = "Recette" if "Recette" in type_mouvement else "Dépense"
                compte = "707 - Ventes de marchandises" if sens_val == "Recette" else "6051 - Fournitures & Services"
                
                if passerelle_source in st.session_state.comptes_360:
                    if sens_val == "Recette":
                        st.session_state.comptes_360[passerelle_source] += montant_input
                    else:
                        st.session_state.comptes_360[passerelle_source] -= montant_input

                if "Professionnel" in espace_type:
                    st.session_state.ecritures_pro.insert(0, {
                        "Date": date_str,
                        "Auteur": st.session_state.user_phone,
                        "Libellé": desc_input,
                        "Projet": projet_choisi,
                        "Sens": sens_val,
                        "Source": passerelle_source,
                        "Compte SYSCOHADA": compte,
                        "Montant": montant_input
                    })
                else:
                    st.session_state.operations_perso.insert(0, {
                        "Date": date_str,
                        "Auteur": st.session_state.user_phone,
                        "Libellé": desc_input,
                        "Source": passerelle_source,
                        "Montant": montant_input
                    })
                st.success("Opération enregistrée avec succès !")

    with tab2:
        st.subheader("🏦 Consolidation 360° (Mobile Money, Banques & Cash)")
        total_360 = sum(st.session_state.comptes_360.values())
        st.metric("Trésorerie Globale Consolidée", f"{total_360:,.0f} F CFA")
        
        cols_c = st.columns(3)
        idx = 0
        for k, v in st.session_state.comptes_360.items():
            with cols_c[idx % 3]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">{k}</div>
                    <div class="metric-value" style="font-size: 1.4rem;">{v:,.0f} F</div>
                </div>
                """, unsafe_allow_html=True)
            idx += 1

    with tab3:
        st.subheader("📊 Comptabilité par Projet & Grand Livre")
        if "Professionnel" in espace_type:
            df = pd.DataFrame(st.session_state.ecritures_pro)
            if df.empty:
                st.info("Aucune écriture enregistrée.")
            else:
                projet_filtre = st.selectbox("Filtrer par projet analytique", ["Tous les projets"] + st.session_state.projets)
                df_affiche = df[df['Projet'] == projet_filtre] if projet_filtre != "Tous les projets" else df
                st.dataframe(df_affiche.style.format({'Montant': '{:,.0f} F'}), use_container_width=True)
        else:
            df_perso = pd.DataFrame(st.session_state.operations_perso)
            if df_perso.empty:
                st.info("Aucune opération personnelle.")
            else:
                st.dataframe(df_perso.style.format({'Montant': '{:,.0f} F'}), use_container_width=True)

    with tab4:
        st.subheader("🤝 Gestion des Tiers, Dettes & Créances")
        with st.form("debt_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                tiers_nom = st.text_input("Nom du Tiers (Client / Fournisseur)")
            with c2:
                dette_type = st.selectbox("Nature", ["Dette (Je dois / Fournisseur 401)", "Créance (On me doit / Client 411)"])
            with c3:
                dette_montant = st.number_input("Montant initial (F)", min_value=0, step=1000)
                
            echeance_date = st.date_input("Date d'échéance")
            submit_debt = st.form_submit_button("Enregistrer l'engagement")
            
            if submit_debt and tiers_nom and dette_montant > 0:
                st.session_state.dettes_creances.append({
                    "Tiers": tiers_nom, "Type": dette_type, "Montant": dette_montant,
                    "Échéance": str(echeance_date), "Statut": "En cours"
                })
                st.success("Engagement tiers enregistré.")

        df_dettes = pd.DataFrame(st.session_state.dettes_creances)
        if not df_dettes.empty:
            st.dataframe(df_dettes.style.format({'Montant': '{:,.0f} F'}), use_container_width=True)
        else:
            st.info("Aucune dette ou créance active.")

    with tab5:
        st.subheader("📄 Facturation FNE (Conforme DGI Côte d'Ivoire)")
        with st.form("fne_form"):
            f_client = st.text_input("Nom du Client", "Client Partenaire")
            f_ifu = st.text_input("Numéro de Compte Contribuable (NCC)", "CI-0000000X")
            f_item = st.text_input("Désignation de la prestation", "Prestation commerciale")
            f_ht = st.number_input("Montant Hors TVA (F)", min_value=0, step=1000, value=50000)
            gen_fne = st.form_submit_button("Générer le spécimen FNE")
            
        if gen_fne:
            tva = f_ht * 0.18
            ttc = f_ht + tva
            spec_id = datetime.datetime.now().strftime("FNE-%Y%m%d-%H%M")
            st.markdown(f"""
            <div style="background: #FFFFFF; color: #000000; padding: 25px; border-radius: 8px;">
                <h3 style="text-align: center; color: #111;">FACTURE NORMALISÉE ÉLECTRONIQUE (Brouillon FNE)</h3>
                <hr>
                <p><b>N° Spécimen :</b> {spec_id}</p>
                <p><b>Client :</b> {f_client} | <b>NCC :</b> {f_ifu}</p>
                <p><b>Total HT :</b> {f_ht:,.0f} F | <b>TVA (18%) :</b> {tva:,.0f} F</p>
                <h3 style="text-align: right; color: #D35400;">TOTAL TTC : {ttc:,.0f} F CFA</h3>
            </div>
            """, unsafe_allow_html=True)

    with tab6:
        st.subheader("🤖 Coach Financier & Analyse Stratégique Globale")
        if st.button("Lancer l'analyse globale"):
            tot_rec = sum([x['Montant'] for x in st.session_state.ecritures_pro if x['Sens'] == 'Recette'])
            tot_dep = sum([x['Montant'] for x in st.session_state.ecritures_pro if x['Sens'] == 'Dépense'])
            st.markdown(f"""
            ### 📋 Rapport d'Analyse Globale
            - **Trésorerie 360° :** `{sum(st.session_state.comptes_360.values()):,.0f} F CFA`
            - **Résultat net :** `{tot_rec - tot_dep:,.0f} F CFA`
            - **Recommandation :** Consolidez vos flux Wave et Orange Money vers votre compte bancaire principal et maintenez le suivi analytique par projet.
            """)

    with tab7:
        st.subheader("📤 Export Tabulaire")
        df_export = pd.DataFrame(st.session_state.ecritures_pro) if "Professionnel" in espace_type else pd.DataFrame(st.session_state.operations_perso)
        if not df_export.empty:
            csv_data = df_export.to_csv(index=False, sep=';').encode('utf-8-sig')
            st.download_button("📥 Télécharger le Grand Livre (CSV)", data=csv_data, file_name="export_sinan.csv", mime="text/csv")
        else:
            st.info("Rien à exporter pour l'instant.")
