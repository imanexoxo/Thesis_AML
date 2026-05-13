# Guida Completa: Jupyter Notebook e Organizzazione Progetto

## Parte 1: Che Cos'è Jupyter Notebook?

### Idea Base
**Jupyter Notebook** è un'applicazione web che ti permette di scrivere codice e testo insieme, eseguendo il codice passo-passo e vedendo i risultati immediati.

Non è un file `.py` tradizionale dove scrivi tutto e poi esegui da terminale. È **interattivo**.

### Come Funziona (Semplicemente)

```
1. Apri un browser
2. Vedi un documento diviso in "celle"
3. In ogni cella puoi:
   - Scrivere testo formattato (Markdown)
   - Scrivere codice Python
4. Esegui cella per cella con Shift+Enter
5. Vedi il risultato sotto ogni cella
6. Le variabili rimangono in memoria (il "Kernel")
```

### Differenza con Python Tradizionale

**File Python normale** (`script.py`):
```
script.py → python script.py → Output terminale → Fine
```

**Jupyter Notebook** (`.ipynb`):
```
Cella 1 → Esegui → Output visualizzato
        ↓ (variabili rimangono)
Cella 2 → Esegui → Output visualizzato
        ↓ (riuso variabili da Cella 1)
Cella 3 → Esegui → Output visualizzato
```

---

## Parte 2: Concetti Chiave di Jupyter

### 1️⃣ Le Celle

Un notebook è diviso in **celle**. Ci sono 2 tipi principali:

#### **Markdown Cell** (per testo)
```
Scrivi testo formattato, titoli, liste, formule...
# Titolo
## Sottotitolo
- Lista
**Grassetto**
```

Non si esegue, è solo documentazione.

#### **Code Cell** (per Python)
```python
x = 5
y = 10
print(x + y)
```

Si esegue quando premi Shift+Enter. Il codice gira e mostra il risultato.

---

### 2️⃣ Il Kernel (Memoria Persistente)

Il **Kernel** è il "cervello" di Python che rimane in vita durante tutta la sessione di notebook.

**Esempio pratico**:

**Cella 1:**
```python
numero = 42
```

**Cella 2:**
```python
print(numero)  # Funziona! Jupyter ricorda che numero = 42
```

**Cella 3:**
```python
numero = numero * 2
print(numero)  # 84
```

⚠️ **Importante**: Se esegui le celle in ordine casuale, le variabili potrebbero non esistere.

**Soluzione**: Se qualcosa non funziona:
```
Kernel → Restart and Clear Output
Poi: Run → Run All Cells (dall'inizio)
```

---

### 3️⃣ Esecuzione delle Celle

**3 modi per eseguire**:

| Scorciatoia | Azione |
|------------|--------|
| **Shift + Enter** | Esegui cella attuale e vai a quella dopo |
| **Ctrl + Enter** | Esegui cella attuale e resta qui |
| **Alt + Enter** | Esegui cella e crea una nuova sotto |

**Il modo consigliato**: Shift + Enter (dall'alto verso il basso)

---

### 4️⃣ Output e Visualizzazione

**Output automatico**:
```python
# Jupyter mostra automaticamente l'ultimo valore
5 + 5  # Mostra: 10
```

**Output con print**:
```python
print("Ciao")  # Mostra: Ciao
```

**Output di grafici** (con Matplotlib):
```python
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.show()  # Mostra il grafico dentro il notebook
```

---

## Parte 3: Come Usare Jupyter (Passo-Passo)

### Step 1: Avviare Jupyter
```bash
cd /home/imane/Thesis_AML
jupyter notebook
```

Si apre automaticamente nel browser (di solito localhost:8888).

### Step 2: Creare un Notebook
1. Clicca "New" → "Python 3"
2. Si crea un nuovo `.ipynb` vuoto

### Step 3: Scrivere la Prima Cella
Digita nella prima cella (Markdown):
```
# Il Mio Progetto di Tesi

Questo notebook analizza gli attacchi adversarial.
```

Poi **Shift + Enter** per eseguire.

### Step 4: Scrivere Codice
Cella di codice:
```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.show()
```

**Shift + Enter** → Vedi il grafico!

### Step 5: Aggiungere Spiegazioni
Tra il codice aggiungi celle Markdown che spiegano cosa stai facendo:

```
## Fase 1: Caricamento Dati
Qui carico il dataset CIFAR-10...

[CELLA DI CODICE per caricare dati]

## Fase 2: Fine-tuning
Ora addestro il modello...

[CELLA DI CODICE per training]
```

### Step 6: Salvare
**Ctrl + S** (come in ogni editor)

Il file si salva come `.ipynb` (formato JSON).

---

## Parte 4: Comandi Utili ("Magic Commands")

Jupyter ha comandi speciali che iniziano con `%`:

```python
# Misurare il tempo di una riga
%time sum(range(100))

# Misurare il tempo medio (ripete 7 volte)
%timeit sum(range(100))

# Installare librerie direttamente dal notebook
!pip install foolbox

# Visualizzare grafici dentro il notebook
%matplotlib inline

# Elencare tutte le variabili
%whos
```

---

## Parte 5: Scorciatoie Tastiera Essenziali

Quando selezioni una cella (bordo blu):

| Tasto | Azione |
|-------|--------|
| **Y** | Converti in Code cell |
| **M** | Converti in Markdown cell |
| **A** | Inserisci cella SOPRA |
| **B** | Inserisci cella SOTTO |
| **D, D** | Elimina cella |
| **Z** | Annulla eliminazione |
| **Shift + M** | Mergia celle |

**Durante l'editing di una cella**:
- **Escape** → Esci dalla cella, selezionala
- **Enter** → Entra in modalità edit

---

## Parte 6: Organizzazione del Progetto - Lo Standard

### 🎯 La Domanda Giusta: UN Notebook o MULTIPLI?

**Risposta**: **Dipende dalla complessità**.

---

### Scenario A: Progetto Semplice → 1 Notebook

Se il tuo progetto è:
- Carico dati
- Faccio fine-tuning
- Faccio attacchi
- Mostro risultati

**Allora**: 1 notebook organizzato in sezioni.

**Struttura**:
```
Thesis_AML/
├── notebooks/
│   └── adversarial_attacks.ipynb  ← Un solo notebook
├── data/
├── models/
└── results/
```

**Inside il notebook**:
```
# Sezione 1: Setup
# [code cells per setup]

# Sezione 2: Caricamento Dati
# [code cells per dati]

# Sezione 3: Fine-tuning
# [code cells per training]

# Sezione 4: Attacchi
# [code cells per attacchi]

# Sezione 5: Risultati
# [code cells per grafici]
```

---

### Scenario B: Progetto Complesso → MULTIPLI Notebook

Se il tuo progetto ha:
- **Fase 1**: Preparazione dati (esplorativo)
- **Fase 2**: Training (lungo)
- **Fase 3**: Attacchi (esperimenti diversi)
- **Fase 4**: Analisi (statistiche)

**Allora**: Multipli notebook, uno per fase.

**Struttura**:
```
Thesis_AML/
├── notebooks/
│   ├── 1_caricamento_dati.ipynb      ← Esploro il dataset
│   ├── 2_fine_tuning.ipynb           ← Addestro il modello
│   ├── 3_attacchi.ipynb              ← Genero attacchi
│   └── 4_analisi_risultati.ipynb     ← Grafici e statistiche
├── data/
├── models/
└── results/
```

**Vantaggi multipli notebook**:
- Ogni notebook ha uno scopo specifico
- Riavviare il kernel della fase 1 non cancella i modelli della fase 2
- Più organizzato per progetti complessi

---

### Lo Standard Internazionale

Nel machine learning, gli **standard** sono:

#### ✅ Se lavori da solo o è una tesi:
- **1 notebook** se < 500 righe
- **2-3 notebook** se 500-1500 righe
- **4+ notebook** se progetto molto complesso

#### ✅ Se lavori in team (GitHub):
- Ogni notebook ha **un proposito chiaro** nel nome
- I notebook vengono **versionati** (git)
- Ogni team member ha il suo notebook per esperimenti

#### ✅ In ricerca scientifica:
- **Notebook di ricerca**: 1 notebook = 1 esperimento
- **Notebook di produzione**: Codice diviso in moduli `.py` + notebook che li usa

---

## Parte 7: Struttura delle Cartelle - Perché?

```
Thesis_AML/
├── notebooks/          ← I TUOI NOTEBOOK (.ipynb)
├── src/               ← CODICE RIUTILIZZABILE (.py)
├── data/              ← DATASET
├── models/            ← MODELLI SALVATI
└── results/           ← RISULTATI (CSV, grafici)
```

### Perché questa struttura?

**`notebooks/`**
- Contiene solo `.ipynb` (i tuoi esperimenti)
- È il "diario" della ricerca
- Facile da leggere e condividere

**`src/`**
- Codice Python in file `.py` separati
- Funzioni che riusi in più notebook
- Più organizzato e manutenibile

**Esempio**: Se scrivi una funzione di attacco:

❌ **Male**: La scrivi in ogni notebook
```
notebook1.ipynb: def fgsm_attack(...): ...
notebook2.ipynb: def fgsm_attack(...): ...  # Copia!
```

✅ **Bene**: La scrivi una volta in `src/attacks.py`
```python
# src/attacks.py
def fgsm_attack(...):
    ...

# Poi in notebook:
from src.attacks import fgsm_attack
```

**`data/`**
- Dataset grandi non li metti su GitHub
- Ma la cartella rimane documentata

**`models/`**
- Salvi i modelli addestrati
- Così non devi riaddestrare ogni volta

**`results/`**
- CSV, PNG, JSON dei risultati
- Facili da leggere e analizzare

---

## Parte 8: Flusso di Lavoro Tipico

### Approccio 1: UN Notebook

```
Apri adversarial_attacks.ipynb
    ↓
Esegui Sezione 1 (setup)
    ↓
Esegui Sezione 2 (dati)
    ↓
Esegui Sezione 3 (training) ← Questo impiega 10 minuti...
    ↓
Esegui Sezione 4 (attacchi)
    ↓
Salva risultati
    ↓
Ctrl+S (salva notebook)
```

**Quando usare**: Progetti lineari e semplici.

---

### Approccio 2: MULTIPLI Notebook

```
1_caricamento_dati.ipynb
    ↓ (salvo dati processati in data/)
    
2_fine_tuning.ipynb
    ↓ (carico dati salvati, addestro, salvo modello)
    
3_attacchi.ipynb
    ↓ (carico modello, faccio attacchi)
    
4_analisi_risultati.ipynb
    ↓ (carico risultati, faccio grafici)
```

**Vantaggi**:
- Se il training fallisce, riavvio solo il notebook 2
- I dati elaborati rimangono in `data/`
- Più modulare

**Quando usare**: Progetti che dividono chiaramente il lavoro.

---

## Parte 9: Organizzazione Logica di UN Notebook

Se usi UN notebook per tutta la tesi:

```markdown
# TITLE: Adversarial Machine Learning - Attacchi su Reti Neurali

## Sezione 1: Setup Iniziale
   - Importazioni
   - GPU/CPU
   - Seed per riproducibilità

## Sezione 2: Caricamento e Esplorazione Dati
   - Caricare dataset
   - Visualizzare campioni
   - Statistiche

## Sezione 3: Preparazione del Modello
   - Caricare modello pre-addestrato
   - Fine-tuning strategy
   - Training setup

## Sezione 4: Training del Modello
   - Loop di training
   - Monitoraggio loss
   - Salvataggio modello

## Sezione 5: Generazione Attacchi Adversarial
   - Implementare FGSM
   - Implementare PGD
   - Generare immagini perturbate

## Sezione 6: Valutazione e Metriche
   - Accuracy su clean images
   - Accuracy su adversarial images
   - Tabella dei risultati

## Sezione 7: Visualizzazione Risultati
   - Grafici accuracy vs epsilon
   - Confronto immagini clean vs adversarial
   - Analisi perturbazioni

## Conclusioni
   - Riassunto risultati
   - Possibili estensioni
```

Ogni **Sezione** = 1-2 **Markdown cell** + 3-5 **Code cells**.

---

## Parte 10: Organizzazione Logica di MULTIPLI Notebook

Se dividi in notebook:

### **1_caricamento_dati.ipynb**
```
# Caricamento e Esplorazione Dataset CIFAR-10

## Cosa farò
[Markdown cell spiegando obiettivo]

## Caricamento
[Code cell: dataset download]

## Visualizzazione
[Code cell: immagini di esempio]

## Analisi
[Code cell: statistiche, distribuzioni]

## Salvataggio
[Code cell: salvo dati elaborati in data/]
```

Output: Dati salvati in `data/`, pronto per il notebook successivo.

---

### **2_fine_tuning.ipynb**
```
# Fine-tuning di ResNet-18

## Caricamento dati (dal notebook 1)
[Code cell: load da data/]

## Setup modello
[Code cell: carica ResNet pre-addestrato]

## Training
[Code cell: training loop (+ tempo!)]

## Salvataggio
[Code cell: salvo modello in models/]
```

Output: Modello salvato in `models/`, pronto per notebook 3.

---

### **3_attacchi.ipynb**
```
# Generazione Attacchi Adversarial

## Caricamento modello (dal notebook 2)
[Code cell: load da models/]

## Implementazione attacchi
[Code cell: FGSM, PGD]

## Applicazione su test set
[Code cell: genero immagini perturbate]

## Valutazione
[Code cell: accuracy su adversarial]

## Salvataggio risultati
[Code cell: CSV in results/]
```

Output: Risultati in `results/`, analizzati dal notebook 4.

---

### **4_analisi_risultati.ipynb**
```
# Analisi e Visualizzazione Risultati

## Caricamento risultati (dal notebook 3)
[Code cell: load CSV da results/]

## Grafici
[Code cell: accuracy vs epsilon]
[Code cell: clean vs adversarial]

## Statistiche
[Code cell: tabelle riassuntive]

## Conclusioni
[Markdown + codice analitiche]
```

Output: Grafici per la tesi.

---

## Parte 11: Cosa Salvo Dove?

### Durante il Notebook

```python
# Dati elaborati → data/
torch.save(processed_dataset, 'data/cifar10_processed.pt')

# Modelli addestrati → models/
torch.save(model.state_dict(), 'models/resnet18_finetuned.pth')

# Risultati → results/
results_df.to_csv('results/accuracy_results.csv')
plt.savefig('results/accuracy_plot.png')
```

Questo permette di **ricaricare** tutto senza rieseguire.

### Come Ricaricare

**Notebook successivo**:
```python
# Caricare dati dal notebook precedente
dataset = torch.load('data/cifar10_processed.pt')

# Caricare modello dal training
model = ResNet18(...)
model.load_state_dict(torch.load('models/resnet18_finetuned.pth'))

# Caricare risultati
results_df = pd.read_csv('results/accuracy_results.csv')
```

Non devi rieseguire tutto da capo! ⚡

---

## Parte 12: Riassunto - Lo Standard per la Tua Tesi

### Scelta 1: UN Notebook (Consigliato per tesi semplice)

**Quando**:
- Progetto lineare
- Tutte le fasi son dipendenti
- < 2000 righe di codice

**Cartelle necessarie**:
```
Thesis_AML/
├── notebooks/
│   └── adversarial_attacks.ipynb
├── data/              (scaricate auto)
├── models/            (salvati dal notebook)
└── results/           (salvati dal notebook)
```

**Workflow**:
1. Apri il notebook
2. Esegui tutto dall'alto al basso (Shift+Enter)
3. Vedi tutti i risultati in una sessione

---

### Scelta 2: MULTIPLI Notebook (Consigliato per tesi complessa)

**Quando**:
- Fasi indipendenti
- Ogni fase è lunga
- > 2000 righe di codice

**Cartelle necessarie**:
```
Thesis_AML/
├── notebooks/
│   ├── 1_caricamento_dati.ipynb
│   ├── 2_fine_tuning.ipynb
│   ├── 3_attacchi.ipynb
│   └── 4_analisi_risultati.ipynb
├── src/
│   ├── attacks.py      (funzioni riutilizzabili)
│   └── utils.py        (funzioni generali)
├── data/
├── models/
└── results/
```

**Workflow**:
1. Esegui notebook 1 → salva dati
2. Esegui notebook 2 → carica dati, salva modello
3. Esegui notebook 3 → carica modello, salva risultati
4. Esegui notebook 4 → carica risultati, visualizza

---

### Perché `src/`?

Se scrivi funzioni che usi in **multipli notebook**:

```python
# src/attacks.py
def fgsm_attack(model, images, labels, epsilon):
    ...

def pgd_attack(model, images, labels, epsilon, alpha):
    ...
```

Poi in ogni notebook:
```python
from src.attacks import fgsm_attack, pgd_attack
```

Non devi copiare il codice! ✅

---

## Conclusione

### Per la Tua Tesi, Sceglierei:

**MULTIPLI Notebook** se:
- Il training è lungo (riavviare il kernel = perdere il modello)
- Vuoi esperimenti indipendenti
- Vuoi che sia facilmente leggibile

**UN Notebook** se:
- Vuoi semplicità
- Tutto è una sequenza logica
- Preferisci una vista d'insieme

---

Non c'è scelta "giusta" o "sbagliata". 

Dipende da **come ragioni** e **come preferisci lavorare**.

Lo standard internazionale è: **Usa quello che ha senso per il TUO progetto**.

