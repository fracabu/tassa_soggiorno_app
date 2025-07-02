# 🏨 Calcolatore Tassa di Soggiorno - Roma

Un'applicazione web sviluppata con Streamlit per calcolare automaticamente le tasse di soggiorno per strutture ricettive a Roma, basata sui dati delle prenotazioni.

## 🌟 Caratteristiche

- **Calcolo Automatico**: Elabora automaticamente tutte le prenotazioni e calcola le tasse dovute
- **Interfaccia Intuitiva**: Dashboard web facile da usare con visualizzazione dei dati in tempo reale
- **Configurazione Flessibile**: Possibilità di modificare tariffe, tipo di struttura e parametri di calcolo
- **Gestione Completa**: Gestisce adulti, bambini, esenzioni per età e stati delle prenotazioni
- **Report Dettagliati**: Tabelle complete con riepilogo mensile e possibilità di export
- **Conformità Normativa**: Rispetta le regole del Comune di Roma per le tasse di soggiorno

## 🚀 Installazione

### Prerequisiti

- Python 3.7 o superiore
- pip (gestore pacchetti Python)

### Passaggi di installazione

1. **Clona o scarica il progetto**
   ```bash
   git clone <repository-url>
   cd tassa-soggiorno-app
   ```

2. **Installa le dipendenze**
   ```bash
   pip install streamlit pandas
   ```

3. **Avvia l'applicazione**
   ```bash
   streamlit run tassa_soggiorno.py
   ```

4. **Apri il browser**
   - L'app si aprirà automaticamente su `http://localhost:8501`
   - Se non si apre automaticamente, vai manualmente all'indirizzo

## 📖 Come Utilizzare l'App

### 1. **Configurazione Iniziale**
Nella barra laterale sinistra puoi configurare:
- **Tipo di struttura**: Seleziona la categoria della tua struttura ricettiva
- **Tariffa per notte**: Modifica la tariffa (default: €6,00 per appartamenti)
- **Massimo notti tassabili**: Imposta il limite di notti soggette a tassa (default: 10)
- **Età minima**: Imposta l'età minima per l'applicazione della tassa (default: 10 anni)

### 2. **Visualizzazione Dati**
- La tabella principale mostra tutte le prenotazioni elaborate
- Vengono considerati solo i soggiorni con stato "OK" o "Mancata presentazione"
- Le prenotazioni cancellate sono visualizzate ma non calcolate nel totale

### 3. **Riepilogo e Statistiche**
Nel pannello destro trovi:
- **Tassa totale da riscuotere**
- **Numero di prenotazioni confermate**
- **Totale notti**
- **Riepilogo mensile** con dettaglio per periodo

### 4. **Export Dati**
- Clicca su "📥 Scarica report CSV" per esportare tutti i dati in formato CSV
- Il file includerà tutti i dettagli delle prenotazioni e i calcoli delle tasse

## 🔧 Configurazione Avanzata

### Modifica Dati Prenotazioni

Per utilizzare i tuoi dati reali, modifica la funzione `parse_booking_data()` nel file `tassa_soggiorno.py`:

```python
def parse_booking_data():
    """I tuoi dati delle prenotazioni"""
    bookings = [
        {
            "nome": "Nome Ospite",
            "adulti": 2,
            "bambini": 1,
            "eta_bambini": [8],  # Età dei bambini
            "checkin": "2025-03-15",  # Formato: YYYY-MM-DD
            "checkout": "2025-03-16",
            "stato": "OK"  # OK, Cancellata, Mancata presentazione
        },
        # Aggiungi altre prenotazioni...
    ]
    return bookings
```

### Personalizzazione Tariffe

Modifica il dizionario `tariffe_default` per aggiornare le tariffe:

```python
tariffe_default = {
    "Strutture ricettive alberghiere 5 stelle": 7.00,
    "Strutture ricettive alberghiere 4 stelle": 6.00,
    # ... altre tariffe
    "Casa vacanze/Appartamento": 6.00,  # La tua tariffa
}
```

## 📊 Regole di Calcolo

L'applicazione segue le normative del Comune di Roma:

### Chi Paga
- **Adulti**: Tutti gli ospiti adulti
- **Bambini**: Solo quelli di età pari o superiore a 10 anni
- **Esenzioni**: Bambini sotto i 10 anni sono automaticamente esenti

### Calcolo Tassa
```
Tassa = (Adulti + Bambini ≥10 anni) × Notti Tassabili × Tariffa per Notte
```

### Limitazioni
- **Massimo 10 notti consecutive** per persona (configurabile)
- **Solo soggiorni turistici** (non per lavoro, studio, salute)

## 🏷️ Tariffe Ufficiali Roma 2024

- **5 stelle**: €7,00/notte
- **4 stelle**: €6,00/notte
- **3 stelle**: €4,00/notte
- **2 stelle**: €3,00/notte
- **1 stella**: €2,00/notte
- **Case vacanze/Appartamenti**: €6,00/notte ⭐
- **B&B**: €2,00/notte

## 📁 Struttura del Progetto

```
tassa-soggiorno-app/
│
├── tassa_soggiorno.py      # File principale dell'applicazione
├── README.md               # Questo file
└── requirements.txt        # Dipendenze (opzionale)
```

## 🔄 Aggiornamenti e Manutenzione

### Aggiornamento Tariffe
Le tariffe possono cambiare annualmente. Verifica sempre le tariffe ufficiali del Comune di Roma e aggiornale nell'app.

### Backup Dati
Esporta regolarmente i report CSV per mantenere uno storico delle tasse calcolate.

## 🆘 Risoluzione Problemi

### L'app non si avvia
```bash
# Verifica versione Python
python --version

# Reinstalla dipendenze
pip install --upgrade streamlit pandas
```

### Errori nei calcoli
- Verifica il formato delle date (YYYY-MM-DD)
- Controlla che i dati numerici siano corretti
- Assicurati che gli stati delle prenotazioni siano: "OK", "Cancellata", o "Mancata presentazione"

### Problemi di visualizzazione
- Svuota la cache del browser
- Riavvia l'applicazione Streamlit

## 📝 Note Legali

⚠️ **Importante**: 
- Questa applicazione è uno strumento di calcolo ausiliario
- Verifica sempre le tariffe ufficiali aggiornate del Comune di Roma
- Le tasse calcolate potrebbero non riflettere situazioni particolari o esenzioni specifiche
- Consulta sempre le normative ufficiali per casi dubbi

## 🤝 Supporto

Per problemi tecnici o miglioramenti:
1. Verifica la documentazione ufficiale di Streamlit
2. Controlla le normative aggiornate del Comune di Roma
3. Testa sempre i calcoli con casi semplici prima dell'uso in produzione

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file LICENSE per maggiori dettagli.

---

**Versione**: 1.0  
**Ultimo aggiornamento**: Luglio 2025  
**Compatibilità**: Python 3.7+, Streamlit 1.0+