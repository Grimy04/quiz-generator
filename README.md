# 🚀 AI Quiz Generator v2.0

Benvenuto! Questo strumento trasforma magicamente le tue dispense universitarie, slide e appunti (PDF, Word, PowerPoint) in **Quiz Interattivi** (Vero/Falso, Risposta Multipla e Aperta) generando un vero e proprio sito web pronto da usare per il tuo studio attivo.

Non preoccuparti se non hai mai programmato: questo tutorial ti guiderà passo dopo passo, che tu usi Windows, Mac o Linux!

---

## 🛠️ Fase 1: I Preparativi (Fallo solo la prima volta)

Prima di iniziare, il tuo computer ha bisogno di due strumenti base.

### 1. Installa Python
Python è il "motore" che fa girare questo script.
* **Windows & Mac:** Vai sul sito ufficiale [python.org/downloads](https://www.python.org/downloads/) e scarica l'ultima versione. 
  * ⚠️ **ATTENZIONE UTENTI WINDOWS:** Durante l'installazione, nella primissima schermata, assicurati di mettere la spunta su **"Add Python to PATH"** (o "Aggiungi Python a PATH"). È fondamentale!
* **Linux:** Apri il terminale e digita: `sudo apt update && sudo apt install python3 python3-pip python3-venv`

### 2. Scarica questo progetto
* **Il metodo facile:** Clicca sul pulsante verde **"Code"** in alto in questa pagina e seleziona **"Download ZIP"**. Estrai la cartella sul tuo desktop.
* **Il metodo per smanettoni:** Apri il terminale e digita `git clone https://github.com/Grimy04/quiz-generator.git`

---

## 💻 Fase 2: Configurazione del progetto

Ora dobbiamo dire al tuo computer di scaricare gli "ingranaggi" necessari per leggere i PDF e generare il sito web.

### 1. Apri il terminale nella cartella del progetto
* **Windows:** Apri la cartella del progetto estratta, fai clic in un punto vuoto con il tasto destro e scegli **"Apri nel Terminale"** (oppure scrivi `cmd` nella barra degli indirizzi in alto e premi Invio).
* **Mac:** Vai in Preferenze di Sistema > Tastiera > Abbreviazioni > Servizi e attiva "Nuovo terminale nella cartella". Ora ti basterà fare clic destro sulla cartella del progetto e scegliere quell'opzione! (In alternativa, apri il Terminale, scrivi cd  seguito da uno spazio, e trascina fisicamente la cartella del progetto dentro la finestra del terminale, poi premi Invio).

cd percorso/della/cartella/progetto**.
* **Linux:** Fai clic col tasto destro nella cartella e seleziona **"Apri nel Terminale"**.

### 2. Crea un "Ambiente Virtuale" (Consigliato per non sporcare il PC)
Nel terminale appena aperto, copia e incolla questo comando e premi Invio:
* **Windows:** `python -m venv venv`
* **Mac/Linux:** `python3 -m venv venv`

Ora **attivalo**:
* **Windows:** `venv\Scripts\activate`
* **Mac/Linux:** `source venv/bin/activate`
*(Vedrai comparire la scritta `(venv)` all'inizio della riga del terminale. Ottimo!)*

### 3. Installa le librerie
Sempre nel terminale, digita:
* **Windows:** `pip install -r requirements.txt`
* **Mac/Linux:** `pip3 install -r requirements.txt`
Attendi che finisca di scaricare tutto.

---

## 🔑 Fase 3: Le Chiavi Magiche (API Keys)

Il programma supporta Gemini, Groq e OpenRouter. Alcuni modelli sono gratuiti, mentre altri potrebbero avere limiti o costi in base al provider scelto.

1. **Gemini:** Vai su [Google AI Studio](https://aistudio.google.com/app/apikey) e crea la tua API Key.
2. **Groq:** Vai su [Groq Console](https://console.groq.com/keys) e crea la tua API Key.
3. **OpenRouter:** Vai su [OpenRouter](https://openrouter.ai/keys) e crea la tua API Key.

**Come inserirle nel programma:**
1. Apri la cartella del progetto.
2. Crea un nuovo file di testo e chiamalo **esattamente** `.env` (con il punto davanti, e senza `.txt` alla fine).
3. Apri il file con il Blocco Note (o TextEdit) e incolla le tue chiavi in questo modo esatto:

```env
GEMINI_API_KEY=incolla_qui_la_chiave_gemini
GROQ_API_KEY=incolla_qui_la_chiave_groq
OPENROUTER_API_KEY=incolla_qui_la_chiave_openrouter
```

## 🚀 Fase 4: Avviare la Magia!

È arrivato il momento di creare i tuoi quiz.
1.  Inserisci i file che vuoi studiare (.pdf, .docx, .pptx) dentro la cartella input_docs.
2.  Ritorna al terminale (assicurati che ci sia scritto (venv) all'inizio, altrimenti riattivalo come al
    passaggio 2.2).
3.  Avvia lo script digitando:
    -   **Windows**: python main.py
    -   **Mac/Linux**: python3 main.py

Guarda la dashboard in tempo reale fare il suo lavoro! Il sistema analizzerà i testi, estrarrà le domande intelligenti e salterà i file che ha già letto in passato.

## 🎯 Fase 5: Gioca e Studia

Quando il terminale ti dice che l'elaborazione è completata:
1.  Apri la cartella output.
2.  Fai doppio clic sul file index.html.
3.  Si aprirà il tuo browser con un fantastico sito web interattivo contenente tutti i quiz generati dai tuoi documenti,
    suddivisi per capitolo!

## 🆘 Risoluzione dei Problemi Frequenti

-   "Il terminale dice che Python non è riconosciuto" (Windows): Non hai spuntato "Add Python to PATH" durante      
    l'installazione. Disinstalla Python, reinstallalo e ricordati di mettere quella spunta!

-   "Errore: GEMINI_API_KEY mancante": Il file .env non è stato creato correttamente. Assicurati che si chiami .env e
    non .env.txt. Su Windows, assicurati di avere abilitato la visualizzazione delle estensioni dei file per controllare.

-   "Blocco SALTATO (Tutte le API esaurite)": Le tue intelligenze artificiali hanno finito il credito gratuito 
    giornaliero. Il programma salverà i file non elaborati e, se lo riavvii domani, ti chiederà se vuoi recuperare i blocchi falliti!