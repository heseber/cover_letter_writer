# Quick Start Guide

Get your first cover letter generated in 5 minutes!

## Prerequisites

- Python 3.10 - 3.13
- OpenAI API key (or other LLM provider)

## Step 1: Installation

```bash
# Clone or navigate to the project directory
cd cover_letter_writer

# Install UV (if not already installed)
pip install uv

# Install dependencies
crewai install
# or
uv pip install -e .
```

## Step 2: Configure API Key

Create a `.env` file in the project root:

```bash
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

**Important:** Replace `your_actual_api_key_here` with your real API key!

## Step 3: Run with Sample Files

Test the application with the provided examples:

```bash
cover-letter-writer \
  --job-description examples/sample_job_description.txt \
  --cv examples/sample_cv.md \
  --documents examples/sample_recommendation.md \
  --output my_first_cover_letter.md
```

**Expected time:** 3-10 minutes

## Step 4: Check the Output

```bash
cat my_first_cover_letter.md
```

You should see a professionally written cover letter!

## Step 5: Use Your Own Files

### Prepare Your Documents

1. **Job Description:** Save the job posting to a text file or copy its URL
2. **Your CV:** Have your resume in PDF or Markdown format
3. **Optional:** Recommendations, certificates, etc.

### Run the Generator

```bash
cover-letter-writer \
  --job-description path/to/job_posting.txt \
  --cv path/to/your_cv.pdf \
  --documents path/to/recommendation.pdf \
  --output cover_letter_for_company.md \
  --max-iterations 3
```

### From URL

```bash
cover-letter-writer \
  --job-description https://company.com/careers/job-123 \
  --cv my_cv.pdf \
  --output cover_letter.md
```

## Command Options

| Option | Short | Required | Description | Default |
|--------|-------|----------|-------------|---------|
| `--job-description` | `-j` | Yes | Job posting file or URL | - |
| `--cv` | `-c` | Yes | Your CV/resume file | - |
| `--documents` | `-d` | No | Additional documents | - |
| `--output` | `-o` | No | Output file path | cover_letter.md |
| `--max-iterations` | `-m` | No | Max review cycles | 3 |

## What Happens During Generation

1. 📄 **Loading**: Reads all your documents
2. ✍️ **Draft 1**: AI writer creates initial cover letter
3. 🔍 **Review 1**: AI reviewer evaluates and provides feedback
4. ✍️ **Draft 2**: Writer improves based on feedback
5. 🔍 **Review 2**: Reviewer evaluates again
6. ✅ **Finalize**: Saves approved version or best draft after max iterations

## Troubleshooting

### "API key not found"
```bash
# Check .env file exists
ls -la .env
# Verify it contains your key
cat .env
```

### "File not found"
```bash
# Use absolute paths
cover-letter-writer \
  -j /full/path/to/job.txt \
  -c /full/path/to/cv.pdf
```

### "PDF parsing error"
```bash
# Ensure pypdf is installed
pip install pypdf
# Or convert PDF to text/markdown
```

### Process is slow
- Normal: Each iteration takes 1-3 minutes
- Reduce iterations: `--max-iterations 2`
- Check internet connection
- Try during off-peak hours

## Tips for Best Results

✅ **DO:**
- Provide detailed job descriptions
- Use well-formatted CVs
- Include relevant recommendations
- Review and edit the output
- Start with 3 iterations

❌ **DON'T:**
- Use very old job postings
- Provide empty or minimal CVs
- Expect perfect output without review
- Use more than 5-6 iterations (diminishing returns)

## Next Steps

- 📖 Read the full [README.md](README.md)
- 🎨 Customize agents in `src/cover_letter_writer/crews/cover_letter_crew/config/`
- 🔧 Explore advanced options
- 📝 Save time by creating document templates

## Getting Help

- Check [examples/README.md](examples/README.md) for more examples
- Review full [documentation](README.md)
- Report issues on GitHub
- Join CrewAI Discord community

---

**Ready to apply?** Generate your cover letter and land that dream job! 🚀

