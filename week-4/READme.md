# Week 4 - Tokenizer Lab
## BPE, WordPiece and SentencePiece comparison

This project follows the supplied Week 4 practical document. It compares:
- BPE - GPT-2 (`gpt2`)
- WordPiece - Multilingual BERT (`bert-base-multilingual-cased`)
- SentencePiece - XLM-R (`xlm-roberta-base`)

The same English, Telugu and Hindi sentences are passed to all three pretrained tokenizers. The program prints token pieces, token IDs and token counts.

## Requirements
- Python 3.10 or later
- VS Code (recommended)
- Internet connection on the first run (the pretrained tokenizer files are downloaded then)

## Setup in Windows PowerShell (VS Code terminal)

If you already have a virtual environment named `.MyEnv` in the parent `LAB` folder, open this `Week4_Tokenizer_Lab` folder and run:

```powershell
..\.MyEnv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python tokenizer_comparison.py
```

If PowerShell blocks activation, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
..\.MyEnv\Scripts\Activate.ps1
```

### If you do not have an existing `.MyEnv`
Create and activate a virtual environment inside this folder:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python tokenizer_comparison.py
```

## Run again later
Activate the same environment, then run:

```powershell
python tokenizer_comparison.py
```

## Expected output
For each language, the program displays the input sentence and, for each tokenizer:
- Tokens
- Token IDs
- Token count

Exact token pieces, IDs and counts come from the downloaded pretrained tokenizer files and should not be hard-coded.

## Important interpretation note
This practical compares real pretrained tokenizers, not three algorithms trained on the same dataset with the same vocabulary size. GPT-2 is primarily English-trained, while multilingual BERT and XLM-R are multilingual. Therefore, token-count differences reflect both tokenizer method and each model's vocabulary/training data. XLM-R uses SentencePiece with a BPE model; SentencePiece is a framework, not one single algorithm.

## Common issue
If downloading fails, check internet connectivity and rerun the program. The first run may take time because tokenizer files need to be downloaded. Do not close the terminal while downloads are in progress.
