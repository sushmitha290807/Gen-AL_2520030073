# Week 3 — LLM Monitoring with MongoDB

Configured for:
- Local Ollama model: `qwen3.5:4b`
- Gemini model: `gemini-3.5-flash`
- MongoDB Atlas database: `llm_monitoring`
- Collection: `api_usage`

## 1. Open this folder in VS Code

Open the `Week3_LLM_Monitoring` folder, then open Terminal in VS Code.

## 2. Create and activate a virtual environment (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in that terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Install Python packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Prepare Ollama

Make sure the Ollama application is running. In a terminal:

```powershell
ollama pull qwen3.5:4b
ollama list
```

You should see `qwen3.5:4b` in the model list.

## 5. Set up Gemini API key

1. Open https://aistudio.google.com/apikey
2. Create an API key.
3. Open this project's `.env` file.
4. Replace `PASTE_YOUR_GEMINI_API_KEY_HERE` with your key.

The configured Gemini model is `gemini-3.5-flash`. Google may route older model IDs to a newer compatible Flash model; check Google's current model documentation if you receive a model availability error.

## 6. Set up MongoDB Atlas

1. Open https://cloud.mongodb.com and create/sign in to an account.
2. Create a free M0 cluster (the Week 3 handout suggests AWS Mumbai / `ap-south-1`).
3. Create a database user and password.
4. Add your current public IP under Network Access / IP Access List.
5. Open the cluster's Connect → Drivers page, select Python / PyMongo, and copy the connection string.
6. In `.env`, replace the sample `MONGODB_URI` with the complete connection string. Replace its username/password placeholders. URL-encode special characters in the password.

Do not use `0.0.0.0/0` for this exercise unless you understand the security implications.

## 7. Run the unit test

```powershell
python -m unittest -v test_client
```

Expected: `Ran 1 test` and `OK`.

## 8. Run the application

```powershell
python main.py
```

Type `ollama` or `gemini`, then enter a prompt. A successful call or final failed call is logged to MongoDB.

## 9. Verify MongoDB records

In MongoDB Atlas → Clusters → Browse Collections, open:
- Database: `llm_monitoring`
- Collection: `api_usage`

Each record includes provider, model, input/output/total tokens, latency, estimated cost, status, attempts, and UTC timestamp. Failed requests also include an error message.

## Important security notes

- Never share your `.env` file, Gemini API key, or MongoDB password.
- `.env` is excluded by `.gitignore`.
- The `.env` included in this starter folder contains placeholders only. It does not contain a working API key or database credential.
- Gemini cost rates are set to zero until you enter the correct current USD-per-million-token rates. Ollama is local and its API token charge is recorded as zero; electricity and hardware costs are not included.
