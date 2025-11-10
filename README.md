# Cover Letter Writer

An AI-powered CrewAI Flow application that generates personalized, high-quality cover letters by matching candidate qualifications with job requirements through an iterative AI-driven review process.

## Features

- 🤖 **Dual AI Agents**: Writer and Reviewer agents collaborate to create high-quality cover letters
- 🔄 **Iterative Refinement**: Automatic review and improvement cycles ensure quality
- 📄 **Multiple Format Support**: Reads PDF and Markdown documents
- 🌐 **URL Support**: Fetch job descriptions directly from URLs
- 📝 **Markdown Output**: Easy-to-edit output format
- 🎯 **Smart Matching**: Automatically maps candidate qualifications to job requirements

## Installation

### Prerequisites

- Python >=3.10 <3.14
- [UV](https://docs.astral.sh/uv/) (recommended) or pip

### Install UV (if not already installed)

```bash
pip install uv
```

### Install Dependencies

Using CrewAI CLI:
```bash
crewai install
```

Or manually:
```bash
uv pip install -e .
```

### Configuration

Create a `.env` file in the project root and add your API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

Alternatively, you can use other LLM providers supported by CrewAI (Anthropic Claude, local models, etc.).

## Usage

### Basic Usage

Generate a cover letter from a local job description file:

```bash
cover-letter-writer \
  --job-description path/to/job_description.txt \
  --cv path/to/your_cv.pdf \
  --output my_cover_letter.md
```

### With URL Job Description

Fetch job description directly from a URL:

```bash
cover-letter-writer \
  --job-description https://company.com/careers/job-posting \
  --cv path/to/your_cv.pdf \
  --output cover_letter.md
```

### With Additional Documents

Include recommendations and certificates:

```bash
cover-letter-writer \
  --job-description job_desc.txt \
  --cv my_cv.pdf \
  --documents recommendation1.pdf recommendation2.md certificate.pdf \
  --max-iterations 5 \
  --output cover_letter.md
```

### Command-Line Options

```
Required Arguments:
  --job-description, -j    Path to job description file or URL to job posting
  --cv, -c                 Path to your CV/resume file (PDF or Markdown)

Optional Arguments:
  --documents, -d          Additional documents (recommendations, certificates, etc.)
  --output, -o             Output file path (default: cover_letter.md)
  --max-iterations, -m     Maximum review iterations (default: 3, max: 10)
```

### Help

```bash
cover-letter-writer --help
```

## Supported File Formats

### Input Documents
- **Job Description**: `.txt`, `.md`, `.markdown`, or URL (HTML)
- **CV/Resume**: `.pdf`, `.md`, `.markdown`, `.txt`
- **Additional Documents**: `.pdf`, `.md`, `.markdown`, `.txt`

### Output
- **Cover Letter**: `.md` (Markdown)

## How It Works

1. **Document Loading**: Reads and parses job description and all candidate documents
2. **Initial Draft**: Writer agent analyzes requirements and creates initial cover letter
3. **Review Cycle**: Reviewer agent evaluates the draft and provides feedback
4. **Iteration**: Based on feedback, writer improves the draft
5. **Approval**: Process continues until reviewer approves or max iterations reached
6. **Output**: Final cover letter saved as Markdown with metadata

### The Iterative Process

```
┌─────────────────┐
│ Load Documents  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Writer Agent   │◄─────┐
│  Creates Draft  │      │
└────────┬────────┘      │
         │               │
         ▼               │
┌─────────────────┐      │
│ Reviewer Agent  │      │
│ Evaluates Draft │      │
└────────┬────────┘      │
         │               │
         ▼               │
    ┌────────┐           │
    │Approved?│──NO──────┘
    └───┬────┘       (if not max iterations)
        │
       YES
        │
        ▼
┌─────────────────┐
│  Save Final     │
│  Cover Letter   │
└─────────────────┘
```

## Architecture

### CrewAI Flow
The application uses CrewAI's Flow architecture to manage the multi-step process:

- **State Management**: Tracks documents, drafts, feedback, and iteration count
- **Event-Driven**: Each step triggers the next automatically
- **Error Handling**: Graceful error handling at each stage

### AI Agents

#### Cover Letter Writer Agent
- **Role**: Professional cover letter writer
- **Goal**: Create compelling letters that map qualifications to job requirements
- **Backstory**: Experienced career consultant with expertise in application materials

#### Cover Letter Reviewer Agent
- **Role**: Senior hiring manager and writing critic
- **Goal**: Ensure professional quality and effective matching
- **Backstory**: Seasoned hiring manager with extensive review experience

## Examples

### Example 1: Software Engineer Position

```bash
cover-letter-writer \
  --job-description https://jobs.company.com/software-engineer \
  --cv my_cv.pdf \
  --documents github_contributions.md recommendation_prof_smith.pdf \
  --output software_engineer_cover_letter.md
```

### Example 2: From Local Files

```bash
cover-letter-writer \
  -j job_descriptions/data_scientist.txt \
  -c documents/my_cv.pdf \
  -d documents/recommendation.pdf documents/certificates.md \
  -o applications/data_scientist_cover.md \
  -m 4
```

## Output Format

The generated cover letter includes:

```markdown
---
Generated: 2025-11-10 14:30:00
Iterations: 3
Status: Approved
---

[Your cover letter content here]
```

## Troubleshooting

### Common Issues

**API Key Not Found**
```bash
# Set your API key in .env file
echo "OPENAI_API_KEY=your_key" > .env
```

**File Not Found**
- Verify all file paths are correct
- Use absolute paths if relative paths don't work
- Check file permissions

**PDF Parsing Errors**
- Ensure pypdf is installed: `pip install pypdf`
- Some encrypted PDFs may not be readable
- Try converting to plain text or Markdown

**URL Fetching Fails**
- Check internet connection
- Verify URL is accessible
- Some websites may block automated requests

## Development

### Running Tests
```bash
pytest tests/
```

### Visualize Flow
```bash
plot
```

### Run with CrewAI CLI
```bash
crewai run
```

## Configuration

### Customizing Agents

Edit agent configurations in:
```
src/cover_letter_writer/crews/cover_letter_crew/config/agents.yaml
```

### Customizing Tasks

Edit task configurations in:
```
src/cover_letter_writer/crews/cover_letter_crew/config/tasks.yaml
```

### Using Different LLM Models

You can configure different models via environment variables or directly in the agent configuration. CrewAI supports:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Local models via Ollama
- Other providers

## Future Enhancements

- 🌐 Web interface
- 🔌 REST API
- 🎨 Template customization
- 🌍 Multi-language support
- 📊 Analytics and tracking
- 💾 Application history

## Support

For issues, questions, or contributions:

- **CrewAI Documentation**: [docs.crewai.com](https://docs.crewai.com)
- **GitHub Issues**: Report bugs and request features
- **CrewAI Discord**: [Join the community](https://discord.com/invite/X4JWnZnxPb)

## License

This project uses CrewAI and follows its licensing terms.

---

**Built with [CrewAI](https://crewai.com)** - Multi-Agent AI Framework
