# Setup Checklist

Use this checklist to ensure your Cover Letter Writer is properly installed and configured.

## ✅ Pre-Installation

- [ ] Python 3.10, 3.11, 3.12, or 3.13 installed
- [ ] Command line access (Terminal, PowerShell, etc.)
- [ ] OpenAI API key (or other LLM provider)
- [ ] Internet connection

### Check Python Version
```bash
python --version
# or
python3 --version
```

Expected output: `Python 3.10.x` through `Python 3.13.x`

---

## ✅ Installation Steps

### 1. Install UV Package Manager
- [ ] UV installed globally

```bash
pip install uv
```

Verify:
```bash
uv --version
```

### 2. Install Project Dependencies
- [ ] Navigate to project directory
- [ ] Run installation command

```bash
cd /path/to/cover_letter_writer
crewai install
# or
uv pip install -e .
```

Expected: No error messages, all packages installed successfully

### 3. Activate Virtual Environment
- [ ] Activate your virtual environment (if using one)

```bash
# If a .venv directory exists
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

**Important:** The `cover-letter-writer` command is installed in your virtual environment. You must either activate the venv or use the full path `.venv/bin/cover-letter-writer`.

### 4. Verify Installation
- [ ] Check that dependencies are installed

```bash
python -c "import crewai; print('CrewAI:', crewai.__version__)"
python -c "import pypdf; print('pypdf: OK')"
python -c "import requests; print('requests: OK')"
python -c "import bs4; print('BeautifulSoup: OK')"
```

---

## ✅ Configuration

### 1. Create .env File
- [ ] Create `.env` file in project root
- [ ] Add API key

```bash
# From project root
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

⚠️ **IMPORTANT:** Replace `your_actual_api_key_here` with your real API key!

### 2. Verify .env File
- [ ] File exists and contains API key

```bash
cat .env
```

Expected output:
```
OPENAI_API_KEY=sk-...
```

### 3. Test API Key (Optional)
- [ ] Verify API key works

```bash
python -c "import openai; import os; from dotenv import load_dotenv; load_dotenv(); print('API Key configured')"
```

---

## ✅ Verification

### 1. Test CLI Installation
- [ ] Command is available

```bash
cover-letter-writer --help
```

Expected: Help message displays

### 2. Run Example Test
- [ ] Test with sample files

```bash
cover-letter-writer \
  --job-description examples/sample_job_description.txt \
  --cv examples/sample_cv.md \
  --documents examples/sample_recommendation.md \
  --output test_cover_letter.md
```

Expected:
- Process runs without errors
- File `test_cover_letter.md` is created
- Contains generated cover letter

### 3. Verify Output
- [ ] Check generated file

```bash
ls -lh test_cover_letter.md
cat test_cover_letter.md
```

Expected:
- File exists
- Contains metadata header
- Contains cover letter content

---

## ✅ Clean Up Test Files
- [ ] Remove test output

```bash
rm test_cover_letter.md
```

---

## ✅ Post-Installation

### 1. Prepare Your Documents
- [ ] Job description ready (file or URL)
- [ ] CV/Resume ready (PDF or Markdown)
- [ ] Additional documents ready (optional)

### 2. Read Documentation
- [ ] Skim [README.md](README.md)
- [ ] Read [QUICKSTART.md](QUICKSTART.md)
- [ ] Review [examples/README.md](examples/README.md)

### 3. First Real Run
- [ ] Run with your own documents

```bash
cover-letter-writer \
  --job-description path/to/your/job.txt \
  --cv path/to/your/cv.pdf \
  --output my_cover_letter.md
```

---

## 🐛 Troubleshooting

### Issue: Command not found
```bash
# Solution: Reinstall with proper PATH
pip install -e .
# or add to PATH manually
```

### Issue: Import errors
```bash
# Solution: Reinstall dependencies
crewai install
```

### Issue: API key errors
```bash
# Solution: Check .env file
cat .env
# Verify no extra spaces or quotes
```

### Issue: Permission errors
```bash
# Solution: Check file permissions
chmod +x src/cover_letter_writer/main.py
```

### Issue: PDF parsing errors
```bash
# Solution: Ensure pypdf is installed
pip install pypdf --upgrade
```

---

## 📊 Final Verification Checklist

- [ ] ✅ Python 3.10-3.13 installed
- [ ] ✅ UV package manager installed
- [ ] ✅ All dependencies installed
- [ ] ✅ .env file created with API key
- [ ] ✅ CLI command works (`cover-letter-writer --help`)
- [ ] ✅ Example test runs successfully
- [ ] ✅ Output file generated correctly
- [ ] ✅ Documentation reviewed
- [ ] ✅ Ready to use with own documents

---

## 🎉 You're All Set!

If all items are checked, your Cover Letter Writer is ready to use!

### Next Steps
1. Prepare your job application documents
2. Run the generator with your documents
3. Review and customize the output
4. Apply for jobs with confidence!

### Need Help?
- 📖 Check [QUICKSTART.md](QUICKSTART.md)
- 📚 Read full [README.md](README.md)
- 🔍 Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- 💬 Ask in CrewAI Discord

---

**Installation Date:** _______________  
**Verified By:** _______________  
**Status:** ⬜ Not Started | ⬜ In Progress | ⬜ Complete

---

*Happy cover letter writing! 🚀*

