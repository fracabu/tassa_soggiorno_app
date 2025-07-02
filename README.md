
### ✅ `README.md`

````markdown
# 💶 Tassa di Soggiorno - Comune di Roma

Questa applicazione Streamlit ti permette di caricare un file di prenotazioni (esportato da Booking.com) e ottenere automaticamente il **calcolo della tassa di soggiorno** da versare al Comune di Roma, suddiviso per trimestre.

---

## 🚀 Funzionalità

- 📥 Caricamento file **.xls**, **.xlsx** e **.pdf**
- 📊 Calcolo della **tassa di soggiorno**:
  - 6 €/notte per persona (fino a 10 notti)
  - Esenzioni automatiche (es. ospiti residenti a Roma, bambini sotto i 10 anni)
- 📆 Riepilogo per **trimestre fiscale**:
  - Q1 (gen-mar), Q2 (apr-giu), Q3 (lug-set), Q4 (ott-dic)
- 💰 Totale complessivo da versare

---

## 📁 File supportati

- **Excel (.xls / .xlsx)** esportato da Booking.com
- **PDF** contenente tabelle leggibili (no scansioni)

---

## 🛠️ Requisiti

- Python 3.8+
- Pacchetti:

```bash
pip install -r requirements.txt
````

---

## 📂 Struttura del progetto

```
tassa_soggiorno_app/
├── app_tassa_soggiorno.py      # Codice principale dell'app
├── requirements.txt            # Librerie da installare
├── README.md                   # Questo file
├── .env.example                # (Facoltativo) Configurazioni future
├── .gitignore                  # File da ignorare in Git
```

---

## 🧪 Avvio rapido

1. Clona o crea la cartella del progetto
2. (Facoltativo) Crea un ambiente virtuale:

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
# oppure
source venv/bin/activate  # Mac/Linux
```

3. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

4. Avvia l'app Streamlit:

```bash
streamlit run app_tassa_soggiorno.py
```

---

## 🧠 Note importanti

* Il file deve contenere almeno queste colonne:
  `"Nome ospite(i)", "Arrivo", "Partenza", "Durata (notti)", "Persone", "Stato"`
* Le righe con **stato diverso da "ok"** (es. cancellate) vengono ignorate
* L’app applica automaticamente la regola delle **10 notti max** e ignora gli ospiti con **nome "Nardiello"** (esempio residente a Roma)

---

## 📌 Prossimi sviluppi

* 📤 Download Excel/PDF con riepilogo
* 🔐 Login e gestione utenti
* 📅 Notifiche per scadenze trimestrali (16/04, 16/07, 16/10, 16/01)
* ☁️ Pubblicazione online (Streamlit Cloud o server dedicato)

---

### 🛟 Supporto

Se hai problemi con il file Booking, o vuoi adattare l'app a un altro comune, contattami!

---

Creato con ❤️ per aiutare i piccoli host romani a gestire la burocrazia più facilmente.

```


