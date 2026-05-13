# Dove Mettere Cosa? Lo Standard dei Notebook

## La Tua Domanda
> Dovrei caricare tutte le librerie? Generare requirements.txt? Caricare anche la rete neurale? Oppure farlo nel secondo notebook?

---

## La Risposta: Dipende dall'Approccio

### Approccio 1: UN Notebook (Semplice)

Se fai **TUTTO in UN notebook**:

```
Notebook Unico
├── Sezione 1: Setup
│   ├── Importazioni tutte qui
│   ├── requirements.txt generato all'inizio
│   └── Setup GPU/seed/configurazione
├── Sezione 2: Dataset
├── Sezione 3: Fine-tuning
├── Sezione 4: Attacchi
└── Sezione 5: Risultati
```

**Quando usare**: Progetti piccoli, < 1000 righe.

---

### Approccio 2: MULTIPLI Notebook (Modulare) - CONSIGLIATO

Se dividi in **notebook tematici**:

**Notebook 1 (Dataset)**
```python
import os, glob, json, numpy, pandas
from sklearn.model_selection import train_test_split

# No PyTorch qui! No rete neurale qui!
# SOLO operazioni su file e dataset
```

**Notebook 2 (Fine-tuning)**
```python
# Ricarica le imports da Notebook 1 (il kernel è separato)
import torch
from torchvision import models, transforms

# Carica il dataset dal notebook 1
# Carica la rete neurale
# Training
```

**Notebook 3 (Attacchi)**
```python
# Carica il modello salvato dal notebook 2
# Esegui attacchi
```

---

## Lo Standard che uso (RACCOMANDATO per te)

### 📋 requirements.txt: UNO SOLO per l'intero progetto

```
# /home/imane/Thesis_AML/requirements.txt (creato UNA VOLTA)

numpy
pandas
matplotlib
scikit-learn
Pillow

torch
torchvision
torchaudio

kaggle
```

✅ **Fatto UNA volta all'inizio**: `pip install -r requirements.txt`

❌ **NON rigenerare in ogni notebook**

---

### 📔 Notebook 1: SOLO Dataset

**`01_dataset_loading.ipynb`** (quello che ho creato)

```python
# Importazioni NECESSARIE per il dataset
import os, glob, json
import numpy, pandas
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from PIL import Image

# ❌ NON importare torch qui!
# ❌ NON importare torchvision qui!
# ❌ NON caricare la rete neurale qui!

# OUTPUT: Salva i percorsi in data/train_split.json, etc.
```

**Perché separare**:
- ✅ Puoi rifare il dataset senza ricaricando PyTorch
- ✅ Il notebook rimane piccolo e veloce
- ✅ Se il training fallisce, il dataset rimane intact

---

### 📔 Notebook 2: Fine-tuning (Prossimo)

**`02_fine_tuning.ipynb`** (da fare)

```python
# Importazioni PER PYTORCH/TRAINING
import torch
import torch.nn as nn
from torch.optim import Adam
from torchvision import models, transforms
from torch.utils.data import DataLoader, Dataset

# ✅ Carichi i dataset dal Notebook 1
with open('../data/train_split.json') as f:
    train_split = json.load(f)

# ✅ Carichi la rete neurale
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(512, 5)  # Per 5 classi

# Training
```

---

### 📔 Notebook 3: Attacchi

**`03_adversarial_attacks.ipynb`** (da fare dopo)

```python
# Import PyTorch minimal
import torch

# ✅ Carichi il modello salvato dal Notebook 2
model = ResNet18()
model.load_state_dict(torch.load('../models/resnet18_finetuned.pth'))

# ✅ Implementi attacchi
# Eseguiture test
```

---

## Cosa Ho Creato per Te (Notebook 1)

### **`01_dataset_loading.ipynb`**

| Sezione | Cosa Fa |
|---------|---------|
| **1. Setup** | Importazioni, seed, path |
| **2. Download Kaggle** | Scarica il dataset automaticamente |
| **3. Esplorazione** | Verifica cartelle, classiche |
| **4. Stratificazione** | Divide in Train/Val/Test 80/10/10 |
| **5. Salvataggio** | Salva i percorsi in `data/*.json` |
| **6. Visualizzazione** | Mostra campioni |
| **7. Statistiche** | Analizza dimensioni, formato |

**Input**: Niente (scarica da Kaggle)
**Output**: 
- `data/train_split.json` ← Percorsi per notebook 2
- `data/val_split.json`
- `data/test_split.json`

---

## Come Procedere (Workflow Consigliato)

### Step 1: Setup Iniziale (Una volta)

```bash
cd /home/imane/Thesis_AML

# Installa tutte le dipendenze
pip install -r requirements.txt

# Setup Kaggle (vedi README)
mkdir -p ~/.kaggle
# Copia kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

### Step 2: Esegui Notebook 1

```
jupyter notebook
→ Apri notebooks/01_dataset_loading.ipynb
→ Esegui Shift+Enter per ogni cella (dall'alto al basso)
→ Risultato: dati salvati in data/
```

Tempo: ~10 minuti (incluso download da Kaggle)

### Step 3: Esegui Notebook 2 (Prossimo)

```
→ Apri notebooks/02_fine_tuning.ipynb
→ Carica i dati dal notebook 1
→ Addestra il modello
→ Salva il modello in models/
```

Tempo: ~15 minuti (dipende da GPU/CPU)

### Step 4: Esegui Notebook 3 (Prossimo)

```
→ Apri notebooks/03_adversarial_attacks.ipynb
→ Carica il modello dal notebook 2
→ Genera attacchi
→ Salva risultati in results/
```

Tempo: ~10 minuti

---

## Cosa Mettere Dove - Tabella Riassuntiva

| Elemento | Dove | Quando |
|----------|------|--------|
| **requirements.txt** | Root (`/Thesis_AML/`) | UNA VOLTA all'inizio |
| **Importazioni librerie** | Inizio di ogni notebook | IN OGNI NOTEBOOK (è ok importare 2 volte) |
| **Import torch** | Notebook 2+ | Solo dove serve PyTorch |
| **Rete neurale** | Notebook 2 | Non in notebook 1 |
| **DataLoader** | Notebook 2 | Non in notebook 1 |
| **Dataset paths** | Salvati da notebook 1, caricati in 2-3 | Separato |
| **Modello salvato** | `models/` | Salvato da notebook 2, caricato in 3 |
| **Risultati** | `results/` | Salvati da notebook 3 |

---

## FAQ

### D: Devo importare le stesse librerie in ogni notebook?

**R**: **Sì**, è normale! Ogni notebook è un "programma indipendente". Se Notebook 2 ha bisogno di torch, lo importa. Non è una copia, è la best practice.

```python
# Notebook 1
import os, glob, json, numpy, pandas
from sklearn.model_selection import train_test_split

# Notebook 2 (separato, importa di nuovo)
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
```

---

### D: Devo ripetere il setup (seed, path) in ogni notebook?

**R**: **Sì**, meglio duplicare che perdere codice. Ogni notebook dev'essere "self-contained".

```python
# Ogni notebook inizia così
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)

PROJECT_ROOT = Path("..")
DATASET_PATH = PROJECT_ROOT / "dataset"
```

---

### D: Posso mettere il codice comune in `src/`?

**R**: **Sì, ma opzionale** per progetti semplici. Esempio:

```python
# src/config.py
RANDOM_SEED = 42
BATCH_SIZE = 32
NUM_EPOCHS = 5

# In ogni notebook
from src.config import RANDOM_SEED, BATCH_SIZE
```

Per la tua tesi, **non è necessario** all'inizio. Fai i 3 notebook e basta. Se diventa disordinato, refactorizzi.

---

### D: Cosa succede se il notebook 1 ha errori?

**R**: Cancella i file in `data/`, `models/`, `results/` e riesegui il notebook 1 da zero. È facile con i JSON!

---

## Riassunto: La Tua Strategia

| Fase | Cosa Fare |
|------|-----------|
| **Oggi** | Esegui Notebook 1 (dataset) |
| **Domani** | Creo Notebook 2 (fine-tuning) |
| **Giorno 3** | Creo Notebook 3 (attacchi) |
| **Giorno 4** | Raccogli i grafici e scrivi la tesi |

---

## File che Hai Ora

```
Thesis_AML/
├── requirements.txt                        ← Installa UNA VOLTA
├── GUIDA_JUPYTER_E_STRUTTURA.md            ← Leggi questa
├── notebooks/
│   └── 01_dataset_loading.ipynb             ← Esegui ADESSO ← TU SEI QUI
├── data/                                    ← Output del notebook 1
├── models/                                  ← Output del notebook 2 (prossimo)
└── results/                                 ← Output del notebook 3 (prossimo)
```

---

**Prossimo step**: Esegui il notebook 1 dal tuo server!
