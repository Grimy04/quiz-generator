import os
import json
import random
import time
import uuid
import warnings
import requests
import re
import sys
from datetime import datetime

from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="pypdf")

from pypdf import PdfReader
from docx import Document
from pptx import Presentation
from google import genai
from google.genai import types
from groq import Groq
from dotenv import load_dotenv

# =========================
# SETUP API
# =========================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERRORE: GEMINI_API_KEY mancante nel file .env")
    exit()

client = genai.Client(api_key=api_key)

groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key) if groq_api_key else None

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

PALETTE_OPZIONI = [
    {"nome": "Amber Warm", "ground": "#100E0A", "ground-2": "#1A1712", "cream": "#ECE5D6", "cream-2": "#A69C87", "cream-3": "#766C59", "signal": "#E0913A", "signal-2": "#F4B662", "signal-ink": "#B16C26", "cap_tones": ["#DDBE73", "#CBA158", "#B9853F", "#A56A33", "#8C552B", "#9A6A2F"]},
    {"nome": "Ocean Blue", "ground": "#0A0D10", "ground-2": "#12161A", "cream": "#E0E7F3", "cream-2": "#8797A6", "cream-3": "#596876", "signal": "#3A82E0", "signal-2": "#62A4F4", "signal-ink": "#265CB1", "cap_tones": ["#739DDD", "#5887CB", "#3F6FB9", "#335AA5", "#2B4C8C", "#2F509A"]},
    {"nome": "Sage Green", "ground": "#0A100B", "ground-2": "#121A13", "cream": "#E0F3E3", "cream-2": "#87A68D", "cream-3": "#59765F", "signal": "#42704C", "signal-2": "#6BA877", "signal-ink": "#2B5234", "cap_tones": ["#73DD84", "#58CB6C", "#3FB955", "#33A548", "#2B8C3E", "#2F9A43"]}
]

# =========================
# RATE LIMIT E TEMPI
# =========================

MAX_RPM = 10
INTERVALLO = 60 / MAX_RPM
ultima_richiesta = 0
gemini_resume_time = 0

def rate_limit():
    global ultima_richiesta
    delta = time.time() - ultima_richiesta
    if delta < INTERVALLO: time.sleep(INTERVALLO - delta)
    ultima_richiesta = time.time()

# =========================
# UI: DASHBOARD RENDERER
# =========================

def print_banner():
    print(f"\033[96m╔════════════════════════════════════════════════════╗\033[0m")
    print(f"\033[96m║              AI QUIZ GENERATOR v2.0                ║\033[0m")
    print(f"\033[96m║      PDF • DOCX • PPTX → Quiz Interattivi          ║\033[0m")
    print(f"\033[96m╚════════════════════════════════════════════════════╝\033[0m\n")

def print_final_box(mins, files, blocks, qs, tot_db):
    def rpad(s, w=27): return str(s).ljust(w)
    tot_db_str = f"{tot_db:,}".replace(',', '.')
    
    print(f"\n\033[92m╔══════════════════════════════════════════════╗\033[0m")
    print(f"\033[92m║                ELABORAZIONE TERMINATA        ║\033[0m")
    print(f"\033[92m╠══════════════════════════════════════════════╣\033[0m")
    print(f"\033[92m║ Tempo Totale      {rpad(f'{mins} min')}║\033[0m")
    print(f"\033[92m║ File Elaborati    {rpad(files)}║\033[0m")
    print(f"\033[92m║ Blocchi           {rpad(blocks)}║\033[0m")
    print(f"\033[92m║ Domande Generate  {rpad(qs)}║\033[0m")
    print(f"\033[92m║ Database Totale   {rpad(tot_db_str)}║\033[0m")
    print(f"\033[92m╚══════════════════════════════════════════════╝\033[0m\n")

def draw_dashboard(doc_name, blocco_curr, blocco_tot, dom_gen, motore, eta, file_curr, file_tot, b_curr, b_tot, tot_dom, speed, api_gem, api_groq, api_or, is_first=False):
    if not is_first:
        sys.stdout.write("\033[17A") # Ora 17 righe perché ne abbiamo aggiunta una

    doc_str = f"{doc_name[:28]}"
    prog_str = f"{blocco_curr} / {blocco_tot} blocchi"
    dom_str = f"{dom_gen} generate"
    orario = datetime.now().strftime("%H:%M:%S")

    print(f"┌──────────────────────────────────────────────┐\033[K")
    print(f"│ Documento     {doc_str:<30} │\033[K")
    print(f"│ Progresso     {prog_str:<30} │\033[K")
    print(f"│ Domande       {dom_str:<30} │\033[K")
    print(f"│ Motore        {motore:<30} │\033[K")
    print(f"│ ETA           {eta:<30} │\033[K")
    print(f"│ Aggiornato    {orario:<30} │\033[K")
    print(f"└──────────────────────────────────────────────┘\033[K")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[K")
    print(f"📚 File analizzati      {file_curr} / {file_tot}\033[K")
    print(f"🧩 Blocchi processati   {b_curr} / {b_tot}\033[K")
    print(f"📝 Domande generate     {tot_dom}\033[K")
    print(f"⚡ Velocità media       {speed} blocchi/min\033[K")
    print(f"🤖 Gemini               {api_gem} richieste\033[K")
    print(f"🤖 Groq                 {api_groq} richieste\033[K")
    print(f"🤖 OpenRouter           {api_or} richieste\033[K")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[K")
    sys.stdout.flush()

# =========================
# PROMPT
# =========================

def get_prompt(blocco):
    return f"""
Sei un professore universitario esigente. Genera da 4 a 7 domande FONDAMENTALI basandoti ESCLUSIVAMENTE sul testo fornito.
REGOLE IMPORTANTISSIME:
1. IGNORA TOTALMENTE info organizzative: nomi prof, università, bibliografia, indici.
2. Concentrati sui concetti teorici, tecnici e pratici.
3. Includi domande Vero/Falso (vf), a risposta multipla (mc) e a risposta aperta (open).
4. REGOLA CRITICA: I quesiti di tipo "vf" DEVONO essere AFFERMAZIONI dichiarative (es. "La system call read ha 3 parametri."), ASSOLUTAMENTE NON domande dirette (vietato il punto interrogativo).
5. ASSOLUTAMENTE VIETATO creare domande che facciano riferimento a immagini, grafici, tabelle, foto o figure (es. "Nella foto...", "Come illustrato nel grafico..."). Le domande devono essere comprensibili e risolvibili al 100% usando solo testo.
6. NON ripetere concetti.

Restituisci ESCLUSIVAMENTE un oggetto JSON con UNA SOLA CHIAVE chiamata "domande", che contiene un array di oggetti. NESSUN TESTO FUORI DAL JSON.

Struttura esatta obbligatoria:
- "q": testo della domanda (o affermazione se vf)
- "fmt": "vf", "mc", o "open"
- "correct": per "vf" (true/false), per "mc" l'indice (0-3), per "open" null
- "opts": per "mc" un array di 4 stringhe, altrimenti null
- "explain": spiegazione per "vf" o "mc", altrimenti null
- "points": per "open" un array di stringhe con concetti chiave, altrimenti null

TESTO DEL BLOCCO:
{blocco}
"""

def parse_domande(data, cid):
    items = data.get("domande", data) if isinstance(data, dict) else data
    out = []
    if not isinstance(items, list): return []
    for d in items:
        if isinstance(d, dict) and "q" in d:
            d["ch"] = cid
            d["id"] = f"{cid}-{uuid.uuid4().hex[:8]}"
            out.append(d)
    return out

# =========================
# LETTURA E SPLIT LOGICO
# =========================

def estrai_testo(filepath):
    ext = filepath.lower().split(".")[-1]
    testo = ""
    try:
        if ext == "pdf":
            reader = PdfReader(filepath)
            for p in reader.pages:
                t = p.extract_text()
                if t: testo += t + "\n"
        elif ext == "docx":
            doc = Document(filepath)
            for p in doc.paragraphs: testo += p.text + "\n"
        elif ext == "pptx":
            prs = Presentation(filepath)
            for s in prs.slides:
                for shape in s.shapes:
                    if hasattr(shape, "text"): testo += shape.text + "\n"
    except: pass
    return testo

def split_logico(testo, max_chars=7500):
    paragrafi = testo.replace("\r\n", "\n").split("\n\n")
    blocchi = []
    blocco_corrente = ""
    for p in paragrafi:
        if len(p) > max_chars:
            if blocco_corrente.strip():
                blocchi.append(blocco_corrente.strip())
                blocco_corrente = ""
            blocchi.append(p[:max_chars].strip())
            continue
        if len(blocco_corrente) + len(p) < max_chars:
            blocco_corrente += p + "\n\n"
        else:
            if blocco_corrente.strip():
                blocchi.append(blocco_corrente.strip())
            blocco_corrente = p + "\n\n"
    if blocco_corrente.strip():
        blocchi.append(blocco_corrente.strip())
    return blocchi

# =========================
# MOTORI AI (Silenziati per la UI)
# =========================

def genera_gemini(blocco, cid):
    global gemini_resume_time
    if time.time() < gemini_resume_time: return None
    try:
        rate_limit()
        r = client.models.generate_content(
            model="gemini-2.5-flash", contents=get_prompt(blocco),
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return parse_domande(json.loads(r.text), cid), "Gemini"
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            gemini_resume_time = time.time() + 86400
        return None

def genera_groq(blocco, cid):
    if not groq_client: return None
    try:
        r = groq_client.chat.completions.create(
            messages=[{"role":"user","content":get_prompt(blocco)}],
            model="llama-3.3-70b-versatile", response_format={"type":"json_object"}
        )
        return parse_domande(json.loads(r.choices[0].message.content), cid), "Groq"
    except: return None

def genera_openrouter(blocco, cid):
    if not openrouter_api_key: return None
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {openrouter_api_key}"},
            json={"model":"meta-llama/llama-3.1-8b-instruct", "messages":[{"role":"user","content":get_prompt(blocco)}]},
            timeout=30
        )
        if r.status_code == 200:
            content = r.json()["choices"][0]["message"]["content"]
            match = re.search(r'\{[\s\S]*\}', content)
            content_pulito = match.group(0) if match else content.replace("```json", "").replace("```", "").strip()
            return parse_domande(json.loads(content_pulito), cid), "OpenRouter"
        return None
    except: return None

def genera_domande(blocco, cid):
    res = genera_gemini(blocco, cid)
    if res: return res
    res = genera_groq(blocco, cid)
    if res: return res
    res = genera_openrouter(blocco, cid)
    if res: return res
    return [], "FALLITO"

# =========================
# MAIN
# =========================

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print_banner()
    
    input_dir, output_dir = "input_docs", "output"
    os.makedirs(output_dir, exist_ok=True)
    
    db_path = os.path.join(output_dir, "database.json")
    path_mancati = os.path.join(output_dir, "blocchi_mancati.json")
    
    db = {"questions": [], "chapters": []}
    if os.path.exists(db_path):
        db = json.load(open(db_path, "r", encoding="utf-8"))

    # LOGICA RECUPERO BLOCCHI MANCANTI
    usa_mancati = False
    mancati_data = []
    
    if os.path.exists(path_mancati):
        try:
            mancati_data = json.load(open(path_mancati, "r", encoding="utf-8"))
            if mancati_data and len(mancati_data) > 0:
                print(f"\033[93m⚠️  ATTENZIONE: Trovati {len(mancati_data)} blocchi salvati in 'blocchi_mancati.json' che avevano fallito.\033[0m")
                scelta = input("   Vuoi generare ORA le domande per questi blocchi mancanti? (s/n): ").strip().lower()
                if scelta == 's':
                    usa_mancati = True
                print("") # Spazio vuoto per pulizia
        except: pass

    file_map = []
    total_blocks = 0

    if usa_mancati:
        print("\033[90m⚙️  Preparazione blocchi mancati in corso...\033[0m")
        grouped = {}
        for m in mancati_data:
            k = (m["f"], m["cid"])
            grouped.setdefault(k, []).append(m["testo"])
        
        for (f_nome, cid_val), blocchi_list in grouped.items():
            file_map.append((f_nome, cid_val, blocchi_list))
            total_blocks += len(blocchi_list)
            
    else:
        # LOGICA NORMALE: Cerca in input_docs
        files = [f for f in os.listdir(input_dir) if f.endswith((".pdf",".docx",".pptx"))]
        if not files:
            print("\033[91m❌ Nessun file trovato nella cartella 'input_docs'\033[0m")
            return

        print("\033[90m⚙️  Controllo file e calcolo blocchi logici...\033[0m")
        capitoli_esistenti = {c["id"] for c in db.get("chapters", [])}

        for f in files:
            cid = f.split(".")[0].lower().replace(" ", "_")
            if cid in capitoli_esistenti: continue
            testo = estrai_testo(os.path.join(input_dir, f))
            blocchi = split_logico(testo)
            file_map.append((f, cid, blocchi))
            total_blocks += len(blocchi)

    if not file_map:
        if usa_mancati:
            print("\n\033[92m✅ Nessun blocco mancante da processare.\033[0m\n")
        else:
            print("\n\033[92m✅ Tutti i documenti sono già stati processati. Database aggiornato!\033[0m\n")
        return

    print(f"\033[92m✓ Trovati {len(file_map)} file da elaborare ({total_blocks} blocchi totali).\033[0m\n")
    print("Inizio elaborazione. Non chiudere la finestra...\n")
    
    # Inizializzazione Dashboard
    seen = set(q.get("q","") for q in db["questions"])
    processed = 0
    total_q = 0
    start_time = time.time()
    time_history = []
    api_stats = {"Gemini": 0, "Groq": 0, "OpenRouter": 0, "FALLITO": 0}
    is_first_draw = True
    
    nuovi_mancati = []

    for file_idx, (f, cid, blocchi) in enumerate(file_map):
        if not any(c.get("id") == cid for c in db.get("chapters", [])):
            db["chapters"].append({"id": cid, "nome_originale": f})

        tot_blocchi_file = len(blocchi)
        domande_nel_file = 0

        for i, b in enumerate(blocchi):
            b_start = time.time()
            blocco_idx = i + 1
            
            avg = sum(time_history[-10:]) / len(time_history[-10:]) if time_history else INTERVALLO
            eta_sec = (total_blocks - processed) * avg
            minuti, secondi = divmod(int(eta_sec), 60)
            eta_str = f"{minuti:02d}m {secondi:02d}s"
            
            elapsed_min = (time.time() - start_time) / 60.0
            speed = int(processed / elapsed_min) if elapsed_min > 0 else 0

            draw_dashboard(f, blocco_idx, tot_blocchi_file, domande_nel_file, "Pensiero...", eta_str, file_idx + 1, len(file_map), processed, total_blocks, total_q, speed, api_stats["Gemini"], api_stats["Groq"], api_stats["OpenRouter"], is_first_draw)
            is_first_draw = False

            # Generazione
            qs, engine = genera_domande(b, cid)
            
            time_history.append(time.time() - b_start)
            processed += 1
            num_domande = len(qs)
            
            # GESTIONE FALLIMENTI E MANCATI
            if num_domande == 0:
                nuovi_mancati.append({"f": f, "cid": cid, "testo": b})
            
            domande_nel_file += num_domande
            total_q += num_domande
            
            if engine in api_stats: api_stats[engine] += 1

            # Aggiornamento UI
            elapsed_min = (time.time() - start_time) / 60.0
            speed = int(processed / elapsed_min) if elapsed_min > 0 else 0
            eta_sec = (total_blocks - processed) * avg
            minuti, secondi = divmod(int(eta_sec), 60)
            eta_str = f"{minuti:02d}m {secondi:02d}s"
            
            draw_dashboard(f, blocco_idx, tot_blocchi_file, domande_nel_file, engine, eta_str, file_idx + 1, len(file_map), processed, total_blocks, total_q, speed, api_stats["Gemini"], api_stats["Groq"], api_stats["OpenRouter"], False)

            for q in qs:
                if q["q"] not in seen:
                    db["questions"].append(q)
                    seen.add(q["q"])

    # AGGIORNAMENTO FILE MANCATI
    if usa_mancati:
        # Se abbiamo processato i mancati, salviamo SOLO quelli che hanno fallito di nuovo
        json.dump(nuovi_mancati, open(path_mancati, "w", encoding="utf-8"), indent=2)
    else:
        # Se abbiamo fatto un giro normale, aggiungiamo i nuovi fallimenti a quelli vecchi
        mancati_data.extend(nuovi_mancati)
        json.dump(mancati_data, open(path_mancati, "w", encoding="utf-8"), indent=2)

    # Aggiornamento Sito Web
    json.dump(db, open(db_path,"w",encoding="utf-8"), indent=2)
    palette = random.choice(PALETTE_OPZIONI)
    
    with open(f"{output_dir}/data.js", "w", encoding="utf-8") as f:
        f.write(f"const BANK = {json.dumps(db['questions'], indent=2)};\n")
        meta = "const META = [\n"
        for i, c in enumerate(db["chapters"]):
            col = palette["cap_tones"][i % len(palette["cap_tones"])]
            nome_pulito = c.get("nome_originale", c["id"]).replace(".pdf", "").replace(".docx", "").replace(".pptx", "")
            meta += f'  {{ch:"{c["id"]}", num:"{i+1:02d}", nm:"{nome_pulito}", sb:"", tone:"{col}"}},\n'
        f.write(meta + "];\n")

    try:
        with open("template/index.html", "r", encoding="utf-8") as t:
            html = t.read().replace("/* {{THEME_VARIABLES}} */", f":root {{ --ground: {palette['ground']}; --signal: {palette['signal']}; }}")
        with open(f"{output_dir}/index.html", "w", encoding="utf-8") as o:
            o.write(html)
    except: pass

    # Scatola Finale
    minuti_totali = int((time.time() - start_time) // 60)
    print_final_box(minuti_totali, len(file_map), total_blocks, total_q, len(db['questions']))
    
    if len(nuovi_mancati) > 0:
        print(f"\033[93m⚠️  Nota: {len(nuovi_mancati)} blocchi hanno generato 0 domande e sono stati salvati in 'blocchi_mancati.json'.\033[0m\n")

if __name__ == "__main__":
    main()