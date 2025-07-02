import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# Configurazione della pagina
st.set_page_config(
    page_title="Calcolatore Tassa di Soggiorno",
    page_icon="🏨",
    layout="wide"
)

# Titolo principale
st.title("🏨 Calcolatore Tassa di Soggiorno - Roma")
st.markdown("---")

# Sidebar con configurazioni
st.sidebar.header("⚙️ Configurazioni")

# Tariffe tassa di soggiorno Roma (aggiornate 2024)
tariffe_default = {
    "Strutture ricettive alberghiere 5 stelle": 7.00,
    "Strutture ricettive alberghiere 4 stelle": 6.00,
    "Strutture ricettive alberghiere 3 stelle": 4.00,
    "Strutture ricettive alberghiere 2 stelle": 3.00,
    "Strutture ricettive alberghiere 1 stella": 2.00,
    "Casa vacanze/Appartamento": 6.00,
    "Bed & Breakfast": 2.00
}

# Selezione tipo struttura
tipo_struttura = st.sidebar.selectbox(
    "Tipo di struttura:",
    list(tariffe_default.keys()),
    index=5  # Default: Casa vacanze/Appartamento
)

tariffa_per_notte = st.sidebar.number_input(
    "Tariffa per notte per adulto (€):",
    min_value=0.0,
    max_value=20.0,
    value=tariffe_default[tipo_struttura],
    step=0.50
)

# Configurazioni aggiuntive
max_notti_tassa = st.sidebar.number_input(
    "Massimo notti soggette a tassa:",
    min_value=1,
    max_value=30,
    value=10,
    help="A Roma la tassa si applica massimo per 10 notti consecutive"
)

eta_minima = st.sidebar.number_input(
    "Età minima soggetta a tassa:",
    min_value=0,
    max_value=18,
    value=10,
    help="Bambini sotto questa età sono esenti"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Nota**: Le tariffe mostrate sono quelle ufficiali del Comune di Roma aggiornate al 2024.")

# Funzione per parsare i dati dalle prenotazioni
def parse_booking_data():
    """Simula i dati delle prenotazioni dal PDF"""
    bookings = [
        {"nome": "Fabio Minella", "adulti": 2, "bambini": 0, "checkin": "2025-03-15", "checkout": "2025-03-16", "stato": "OK"},
        {"nome": "Alessandra Nardiello", "adulti": 2, "bambini": 0, "checkin": "2025-04-17", "checkout": "2025-04-18", "stato": "OK"},
        {"nome": "Giulia Cola", "adulti": 2, "bambini": 0, "checkin": "2025-04-18", "checkout": "2025-04-21", "stato": "Cancellata"},
        {"nome": "Victoriia Nahorna", "adulti": 3, "bambini": 0, "checkin": "2025-04-19", "checkout": "2025-04-21", "stato": "OK"},
        {"nome": "Alessia Raffaeli", "adulti": 2, "bambini": 1, "eta_bambini": [3], "checkin": "2025-04-25", "checkout": "2025-04-27", "stato": "Cancellata"},
        {"nome": "Lars Haubner", "adulti": 1, "bambini": 0, "checkin": "2025-04-25", "checkout": "2025-04-27", "stato": "OK"},
        {"nome": "Motlagh Zahra", "adulti": 1, "bambini": 0, "checkin": "2025-04-29", "checkout": "2025-05-05", "stato": "OK"},
        {"nome": "Roberto Trifiletti", "adulti": 1, "bambini": 0, "checkin": "2025-05-07", "checkout": "2025-05-08", "stato": "OK"},
        {"nome": "Mazzariol Claudia", "adulti": 2, "bambini": 0, "checkin": "2025-05-08", "checkout": "2025-05-09", "stato": "OK"},
        {"nome": "Mirko Rossi", "adulti": 2, "bambini": 1, "eta_bambini": [7], "checkin": "2025-05-09", "checkout": "2025-05-11", "stato": "OK"},
        {"nome": "Luca Rapis", "adulti": 2, "bambini": 0, "checkin": "2025-05-11", "checkout": "2025-05-15", "stato": "OK"},
        {"nome": "Giorgio Lo Iacono", "adulti": 2, "bambini": 1, "eta_bambini": [1], "checkin": "2025-05-15", "checkout": "2025-05-18", "stato": "OK"},
        {"nome": "Maya Robnett", "adulti": 1, "bambini": 0, "checkin": "2025-05-21", "checkout": "2025-05-27", "stato": "OK"},
        {"nome": "Mathias Karine", "adulti": 2, "bambini": 0, "checkin": "2025-05-29", "checkout": "2025-06-03", "stato": "OK"},
        {"nome": "Ciari Denise", "adulti": 2, "bambini": 0, "checkin": "2025-06-07", "checkout": "2025-06-08", "stato": "OK"},
        {"nome": "Alexis Zuguem", "adulti": 1, "bambini": 0, "checkin": "2025-06-09", "checkout": "2025-06-12", "stato": "Mancata presentazione"},
        {"nome": "Frigerio Laura", "adulti": 2, "bambini": 1, "eta_bambini": [13], "checkin": "2025-06-14", "checkout": "2025-06-15", "stato": "OK"},
        {"nome": "Cataldo Monteleone", "adulti": 2, "bambini": 0, "checkin": "2025-06-19", "checkout": "2025-06-20", "stato": "OK"},
        {"nome": "Janaka Bellana Vithanage", "adulti": 2, "bambini": 1, "eta_bambini": [2], "checkin": "2025-06-20", "checkout": "2025-06-26", "stato": "OK"},
        {"nome": "Marino Tinelli", "adulti": 2, "bambini": 0, "checkin": "2025-06-26", "checkout": "2025-06-28", "stato": "OK"},
        {"nome": "Federica Gatta", "adulti": 3, "bambini": 0, "checkin": "2025-06-28", "checkout": "2025-06-29", "stato": "OK"},
        {"nome": "Giulia Ciot", "adulti": 2, "bambini": 0, "checkin": "2025-07-21", "checkout": "2025-07-22", "stato": "OK"}
    ]
    return bookings

def calcola_tassa_soggiorno(adulti, bambini, eta_bambini, notti, tariffa, max_notti, eta_min):
    """Calcola la tassa di soggiorno per una prenotazione"""
    # Adulti soggetti a tassa
    adulti_tassabili = adulti
    
    # Bambini soggetti a tassa (solo quelli sopra l'età minima)
    bambini_tassabili = 0
    if bambini > 0 and eta_bambini:
        bambini_tassabili = sum(1 for eta in eta_bambini if eta >= eta_min)
    
    # Totale persone tassabili
    persone_tassabili = adulti_tassabili + bambini_tassabili
    
    # Notti soggette a tassa (massimo stabilito)
    notti_tassabili = min(notti, max_notti)
    
    # Calcolo tassa totale
    tassa_totale = persone_tassabili * notti_tassabili * tariffa
    
    return tassa_totale, persone_tassabili, notti_tassabili

# Layout principale
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Calcolo Tasse di Soggiorno")
    
    # Carica e processa i dati
    bookings = parse_booking_data()
    
    # Calcola le tasse per ogni prenotazione
    risultati = []
    totale_generale = 0
    
    for booking in bookings:
        if booking["stato"] in ["OK", "Mancata presentazione"]:
            checkin = datetime.strptime(booking["checkin"], "%Y-%m-%d")
            checkout = datetime.strptime(booking["checkout"], "%Y-%m-%d")
            notti = (checkout - checkin).days
            
            eta_bambini = booking.get("eta_bambini", [])
            
            tassa, persone_tassabili, notti_tassabili = calcola_tassa_soggiorno(
                booking["adulti"], 
                booking["bambini"], 
                eta_bambini,
                notti, 
                tariffa_per_notte, 
                max_notti_tassa, 
                eta_minima
            )
            
            risultato = {
                "Nome": booking["nome"],
                "Check-in": booking["checkin"],
                "Check-out": booking["checkout"],
                "Adulti": booking["adulti"],
                "Bambini": booking["bambini"],
                "Notti": notti,
                "Persone Tassabili": persone_tassabili,
                "Notti Tassabili": notti_tassabili,
                "Tassa (€)": round(tassa, 2),
                "Stato": booking["stato"]
            }
            risultati.append(risultato)
            
            if booking["stato"] == "OK":
                totale_generale += tassa
    
    # Crea DataFrame
    df = pd.DataFrame(risultati)
    
    # Mostra la tabella
    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Tassa (€)": st.column_config.NumberColumn(
                    "Tassa (€)",
                    format="€%.2f"
                )
            }
        )
        
        # Bottone per scaricare CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Scarica report CSV",
            data=csv,
            file_name=f"tasse_soggiorno_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col2:
    st.header("💰 Riepilogo")
    
    if 'df' in locals() and not df.empty:
        # Statistiche generali
        prenotazioni_confermate = len(df[df["Stato"] == "OK"])
        prenotazioni_totali = len(df)
        notti_totali = df[df["Stato"] == "OK"]["Notti"].sum()
        
        # Metriche principali
        st.metric("Tassa Totale da Riscuotere", f"€{totale_generale:.2f}")
        st.metric("Prenotazioni Confermate", f"{prenotazioni_confermate}")
        st.metric("Notti Totali", f"{notti_totali}")
        
        st.markdown("---")
        
        # Riepilogo per mese
        st.subheader("📅 Riepilogo Mensile")
        
        df_ok = df[df["Stato"] == "OK"].copy()
        if not df_ok.empty:
            df_ok["Mese"] = pd.to_datetime(df_ok["Check-in"]).dt.strftime("%Y-%m")
            riepilogo_mensile = df_ok.groupby("Mese").agg({
                "Tassa (€)": "sum",
                "Nome": "count"
            }).rename(columns={"Nome": "Prenotazioni"})
            
            st.dataframe(
                riepilogo_mensile,
                column_config={
                    "Tassa (€)": st.column_config.NumberColumn(
                        "Tassa (€)",
                        format="€%.2f"
                    )
                }
            )
    
    st.markdown("---")
    st.info(
        f"""
        **Configurazione Attuale:**
        - Tipo: {tipo_struttura}
        - Tariffa: €{tariffa_per_notte}/notte/adulto
        - Max notti tassabili: {max_notti_tassa}
        - Età minima: {eta_minima} anni
        """
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
    📍 Tasse di soggiorno calcolate secondo le tariffe del Comune di Roma<br>
    ⚠️ Verificare sempre le tariffe ufficiali aggiornate
    </div>
    """, 
    unsafe_allow_html=True
)

# Note informative
with st.expander("ℹ️ Informazioni sulla Tassa di Soggiorno"):
    st.markdown("""
    ### Tassa di Soggiorno - Roma
    
    **Chi deve pagare:**
    - Tutti gli ospiti dai 10 anni in su
    - Solo per soggiorni turistici (non per motivi di lavoro/studio/salute)
    
    **Durata:**
    - Massimo 10 notti consecutive per persona
    
    **Tariffe 2024:**
    - Strutture 5 stelle: €7,00/notte
    - Strutture 4 stelle: €6,00/notte  
    - Strutture 3 stelle: €4,00/notte
    - Strutture 2 stelle: €3,00/notte
    - Strutture 1 stella: €2,00/notte
    - **Case vacanze/Appartamenti: €6,00/notte**
    - B&B: €2,00/notte
    
    **Esenzioni:**
    - Bambini sotto i 10 anni
    - Soggiorni per motivi di salute, lavoro, studio
    - Accompagnatori di disabili
    """)