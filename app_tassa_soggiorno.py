import streamlit as st
import pandas as pd
import pdfplumber
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="Tassa di soggiorno - Roma", page_icon="💶", layout="wide")
st.title("💶 Calcolo Tassa di Soggiorno - Comune di Roma")

uploaded_file = st.file_uploader("📂 Carica il file di prenotazioni (.xls, .xlsx, .csv, .pdf)", type=["xls", "xlsx", "csv", "pdf"])

def calcola_tassa(df):
    df = df[df["Stato"].str.strip().str.lower() == "ok"]
    df = df[df["Nome ospite(i)"].notna()].copy()

    def tassa(row):
        nome = str(row["Nome ospite(i)"]).lower()
        if "nardiello" in nome:
            return 0.0
        notti = min(int(row["Durata (notti)"]), 10)
        persone = int(row["Persone"])
        return 6 * notti * persone

    df["Tassa di soggiorno (€)"] = df.apply(tassa, axis=1)
    df["Trimestre"] = pd.to_datetime(df["Arrivo"], errors="coerce").dt.month.map({
        1: "Q1", 2: "Q1", 3: "Q1",
        4: "Q2", 5: "Q2", 6: "Q2",
        7: "Q3", 8: "Q3", 9: "Q3",
        10: "Q4", 11: "Q4", 12: "Q4"
    })
    return df

def mappa_colonne_pdf(df):
    col = [str(c).strip().lower() for c in df.columns if c]
    df.columns = col
    mapping = {
        "nome dell'ospite": "Nome ospite(i)",
        "ospite": "Nome ospite(i)",
        "guest name": "Nome ospite(i)",
        "check in": "Arrivo",
        "check-in": "Arrivo",
        "check out": "Partenza",
        "check-out": "Partenza",
        "notti": "Durata (notti)",
        "persone": "Persone",
        "numero ospiti": "Persone",
        "stato": "Stato"
    }
    rename = {k: v for k, v in mapping.items() if k in df.columns}
    df.rename(columns=rename, inplace=True)
    return df

def genera_csv(df):
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

def genera_pdf(risultato_df, totale, tabella_trimestri):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 40, "Riepilogo Tassa di Soggiorno - Comune di Roma")

    y = height - 80
    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"Totale da versare: {totale:.2f} €")
    y -= 30

    for trimestre, importo in tabella_trimestri.items():
        c.drawString(40, y, f"{trimestre}: {importo:.2f} €")
        y -= 20

    y -= 30
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, "Dettaglio prenotazioni")
    y -= 20
    c.setFont("Helvetica", 9)

    cols = ["Nome ospite(i)", "Arrivo", "Partenza", "Durata (notti)", "Persone", "Tassa di soggiorno (€)", "Trimestre"]

    for _, row in risultato_df[cols].iterrows():
        riga = f"{row['Nome ospite(i)']} | {row['Arrivo']} | {row['Partenza']} | {row['Durata (notti)']} notti | {row['Persone']} ospiti | €{row['Tassa di soggiorno (€)']:.2f} | {row['Trimestre']}"
        c.drawString(40, y, riga)
        y -= 12
        if y < 60:
            c.showPage()
            y = height - 40

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, sep=";", encoding="latin1")
        elif uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                all_text = []
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        all_text.extend(table)
            if not all_text or len(all_text) < 2:
                raise ValueError("⚠️ Nessuna tabella trovata nel PDF.")
            headers = all_text[0]
            n_colonne = len(headers)
            righe_valide = [r for r in all_text[1:] if len(r) == n_colonne]
            df = pd.DataFrame(righe_valide, columns=headers)
            df = mappa_colonne_pdf(df)
        else:
            st.error("❌ Formato file non supportato.")
            st.stop()

        richieste = ["Nome ospite(i)", "Arrivo", "Partenza", "Durata (notti)", "Persone", "Stato"]
        mancanti = [col for col in richieste if col not in df.columns]
        if mancanti:
            st.error(f"⚠️ Colonne mancanti nel file: {', '.join(mancanti)}")
        else:
            risultato = calcola_tassa(df)

            st.success("✅ File caricato e analizzato con successo!")

            st.subheader("📊 Riepilogo prenotazioni valide")
            st.dataframe(risultato[[
                "Nome ospite(i)", "Arrivo", "Partenza",
                "Durata (notti)", "Persone", "Tassa di soggiorno (€)", "Trimestre"
            ]])

            st.subheader("📆 Totale per trimestre:")
            tabella_trimestri = risultato.groupby("Trimestre")["Tassa di soggiorno (€)"].sum()
            st.table(tabella_trimestri)

            st.subheader("💰 Totale complessivo:")
            totale = risultato["Tassa di soggiorno (€)"].sum()
            st.markdown(f"### **Totale da versare: {totale:.2f} €**")

            st.download_button(
                label="⬇️ Scarica riepilogo CSV",
                data=genera_csv(risultato),
                file_name="riepilogo_tassa_soggiorno.csv",
                mime="text/csv"
            )

            st.download_button(
                label="⬇️ Scarica riepilogo PDF",
                data=genera_pdf(risultato, totale, tabella_trimestri.to_dict()),
                file_name="riepilogo_tassa_soggiorno.pdf",
                mime="application/pdf"
            )

            st.divider()
            st.markdown("""
### 📌 Come pagare la tassa di soggiorno a Roma

1. Vai sul sito ufficiale del Comune di Roma: [https://www.comune.roma.it](https://www.comune.roma.it)
2. Cerca "Portale Tassa di Soggiorno"
3. Accedi con SPID o credenziali
4. Vai alla sezione **"Dichiarazione trimestrale"**
5. Inserisci i dati e **effettua il pagamento tramite PagoPA**

---

### 🗓️ Scadenze trimestrali da ricordare:

- **Q1** → Versamento entro **16 aprile**
- **Q2** → Versamento entro **16 luglio**
- **Q3** → Versamento entro **16 ottobre**
- **Q4** → Versamento entro **16 gennaio**

Consigliato: salva questo PDF o CSV per archiviazione.
""")

    except Exception as e:
        st.error(f"❌ Errore durante l'elaborazione: {e}")
