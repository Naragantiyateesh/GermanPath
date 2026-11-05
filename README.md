# GermanPath AI — VS Code starter project

A Streamlit prototype for exploring German Master's programmes using the **University List** worksheet from your Excel file.

## Important data/privacy note
The original workbook also contains `Student Name` and `Personal Details` sheets. Those sheets are deliberately excluded. They contain personal information, including a credential-like entry. If that password is real, change it immediately and avoid sharing the original workbook publicly. This project imports only `University List`.

## 1. Install prerequisites
- Python 3.10 or newer
- Visual Studio Code
- VS Code Python extension

## 2. Open in VS Code
1. Download and extract `GermanPath_AI.zip`.
2. Open VS Code.
3. Select **File → Open Folder**.
4. Choose the extracted `GermanPath_AI` folder.
5. Open **Terminal → New Terminal**.

## 3. Create a virtual environment

### Windows PowerShell
```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt:
```cmd
.venv\\Scripts\\activate.bat
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 4. Run the app
```bash
python -m streamlit run app.py
```
Streamlit will show a local URL, normally http://localhost:8501. Open it in your browser.

## 5. Project structure
```text
GermanPath_AI/
├── app.py
├── data/
│   └── universities.csv
├── src/
│   ├── __init__.py
│   └── matcher.py
├── requirements.txt
├── .env.example
└── README.md
```

## What works in this first version
- Loads 159 programme records from the uploaded `University List` worksheet.
- Student profile form.
- Course-interest matching and ranked shortlist.
- Displays recorded requirements, special requirements, application route, and deadline.
- Searchable programme table.
- Basic local dataset question retrieval.

## Known limitations — do not use as final admissions advice
- The spreadsheet is not a verified live source. Deadlines, links, fees and requirements may be outdated.
- Some fields mix numeric scores, CEFR levels and shorthand such as `Y`, `N`, `R`, `B2`, and `C1`. Their meanings are not consistently defined.
- CGPA values mix German grades, non-German numbers, `N`, and text. A reliable GPA conversion and per-programme grading-scale validation are required.
- The current match score is a transparent prototype ranking, **not an admission probability**.
- ECTS, module-level prerequisites, accepted exam alternatives, and exact application routes need official-source verification.
- The current assistant is keyword retrieval, not a production RAG system.

## Next development milestones
1. Normalize every admission requirement into structured fields and preserve the raw source value.
2. Add official source URLs, source type, intake year, and `last_verified_at`.
3. Verify each programme's current deadline and application route from its official page.
4. Add document ingestion + embeddings + vector search for a grounded RAG assistant.
5. Add authentication and a database only after the core matching logic is tested.
