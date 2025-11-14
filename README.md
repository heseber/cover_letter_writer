# Cover Letter Writer

An AI-powered CrewAI Flow application that generates personalized, high-quality cover letters by matching candidate qualifications with job requirements through an iterative AI-driven review process.

## Features

- 🤖 **Dual AI Agents**: Writer and Reviewer agents collaborate to create high-quality cover letters
- 🔄 **Iterative Refinement**: Automatic review and improvement cycles ensure quality
- 🌍 **Translation Support**: Automatically translate cover letters to multiple languages
- 🔌 **Multi-LLM Support**: Choose from OpenAI, Anthropic Claude, or Ollama models
- 📄 **Multiple Format Support**: Reads PDF and Markdown documents
- 🌐 **URL Support**: Fetch job descriptions directly from URLs
- ⚙️ **YAML Configuration**: Easy configuration management
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

### Activate Virtual Environment

If you're using a virtual environment (recommended):
```bash
# Activate the virtual environment
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

**Note:** After installation, the `cover-letter-writer` command will be available in your activated virtual environment.

### Configuration

Create a `.env` file in the project root and add your API key(s):

```bash
# OpenAI (default)
OPENAI_API_KEY=your_openai_key_here

# Anthropic Claude (optional)
ANTHROPIC_API_KEY=your_anthropic_key_here

# Ollama (optional, for local models)
# No API key needed, just ensure Ollama is running locally
```

The application supports multiple LLM providers. You can configure them in `src/cover_letter_writer/config/cover_letter_writer.yaml`.

## Usage

### Basic Usage

Generate a cover letter from a local job description file:

```bash
cover-letter-writer \
  --job-description path/to/job_description.txt \
  --cv path/to/your_cv.pdf \
  --output-dir ./output
```

### With URL Job Description

Fetch job description directly from a URL:

```bash
cover-letter-writer \
  --job-description https://company.com/careers/job-posting \
  --cv path/to/your_cv.pdf \
  --output-dir ./output
```

### With Additional Documents

Include recommendations and certificates:

```bash
cover-letter-writer \
  --job-description job_desc.txt \
  --cv my_cv.pdf \
  --additional-docs recommendation1.pdf \
  --additional-docs recommendation2.md \
  --additional-docs certificate.pdf \
  --max-iterations 5 \
  --output-dir ./output
```

### With Translation

Generate a cover letter and translate it to another language:

```bash
cover-letter-writer \
  --job-description job_desc.txt \
  --cv my_cv.pdf \
  --translate-to de \
  --output-dir ./output
```

This will generate both:
- English original cover letter
- German translation with `_de` suffix

### Command-Line Options

```
Required Arguments:
  --job-description, -j    Path to job description file or URL to job posting
  --cv, -c                 Path to your CV/resume file (.pdf, .md, .txt)

Optional Arguments:
  --additional-docs, -a    Additional supporting documents (can be specified multiple times)
  --output-dir, -o         Output directory for results (default: ./output)
  --max-iterations, -i     Maximum review iterations (default: 3, config: cover_letter_writer.yaml)
  --translate-to, -t       Target language code for translation (e.g., 'de', 'fr', 'es')
  
LLM Configuration:
  --llm-provider, -p       LLM provider: openai, anthropic, or ollama
  --llm-model, -m          Specific LLM model name (e.g., 'gpt-4o', 'claude-3-5-sonnet-20241022')
  --config                 Path to custom config file (default: config/cover_letter_writer.yaml)
  
Translation Configuration:
  --translation-llm-provider    LLM provider for translation (if different from main)
  --translation-llm-model       LLM model for translation (if different from main)
  
Other:
  --debug                  Enable debug mode with full stack traces
```

### Help

```bash
cover-letter-writer --help
```

## Supported File Formats

### Input Documents
All input documents support the following formats:
- **Text Files**: `.txt` (plain text)
- **Markdown**: `.md`, `.markdown`
- **PDF**: `.pdf` (text extraction via pypdf)
- **URLs**: HTTP/HTTPS URLs for job descriptions (HTML parsing)

Supported for:
- Job descriptions (files or URLs)
- CV/Resume (all file formats)
- Additional documents (recommendations, certificates, portfolios)

### Output
- **Cover Letter**: `.md` (Markdown with metadata header)
- **Translated Cover Letter**: `.md` (when translation is enabled)
- **Feedback History**: `.md` (review iteration logs)

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

### AI Agents (Three Specialized Crews)

#### Writer Crew
- **Agent**: Cover Letter Writer
- **Role**: Professional cover letter writer
- **Goal**: Create compelling letters that map qualifications to job requirements
- **Backstory**: Experienced career consultant with expertise in application materials

#### Reviewer Crew
- **Agent**: Cover Letter Reviewer
- **Role**: Senior hiring manager and writing critic
- **Goal**: Ensure professional quality and effective matching
- **Backstory**: Seasoned hiring manager with extensive review experience

#### Translator Crew (Optional)
- **Agent**: Cover Letter Translator
- **Role**: Professional document translator
- **Goal**: Accurately translate cover letters while preserving tone and formatting
- **Backstory**: Experienced translator specializing in career documents

## Examples

### Example 1: Software Engineer Position

```bash
cover-letter-writer \
  --job-description https://jobs.company.com/software-engineer \
  --cv my_cv.pdf \
  --additional-docs github_contributions.md \
  --additional-docs recommendation_prof_smith.pdf \
  --output-dir ./output/software_engineer
```

### Example 2: From Local Files with Custom Iterations

```bash
cover-letter-writer \
  -j job_descriptions/data_scientist.txt \
  -c documents/my_cv.pdf \
  -a documents/recommendation.pdf \
  -a documents/certificates.md \
  -o applications/data_scientist \
  -i 4
```

### Example 3: Using Different LLM Provider

```bash
cover-letter-writer \
  -j job_desc.txt \
  -c my_cv.pdf \
  -p anthropic \
  -m claude-3-5-sonnet-20241022 \
  -o ./output
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

### Application Configuration

Edit the main configuration file:
```
src/cover_letter_writer/config/cover_letter_writer.yaml
```

This allows you to configure:
- LLM provider and model
- Temperature settings
- Max iterations
- Output directory and file patterns
- Translation settings

Example configuration:
```yaml
llm:
  provider: openai  # or anthropic, ollama
  model: gpt-4o
  temperature: 0.7

translation:
  enabled: false
  target_language: null
  llm_provider: null  # Uses main LLM if not specified
```

### Customizing Agents

Edit agent configurations in each crew's config directory:
```
src/cover_letter_writer/crews/writer_crew/config/agents.yaml
src/cover_letter_writer/crews/reviewer_crew/config/agents.yaml
src/cover_letter_writer/crews/translator_crew/config/agents.yaml
```

### Customizing Tasks

Edit task configurations in each crew's config directory:
```
src/cover_letter_writer/crews/writer_crew/config/tasks.yaml
src/cover_letter_writer/crews/reviewer_crew/config/tasks.yaml
src/cover_letter_writer/crews/translator_crew/config/tasks.yaml
```

### Using Different LLM Models

The application supports multiple LLM providers:

**OpenAI (Default)**
```yaml
llm:
  provider: openai
  model: gpt-4o  # or gpt-4o-mini, gpt-3.5-turbo
  temperature: 0.7
```

**Anthropic Claude**
```yaml
llm:
  provider: anthropic
  model: claude-3-5-sonnet-20241022  # or other Claude models
  temperature: 0.7
```

**Ollama (Local Models)**
```yaml
llm:
  provider: ollama
  model: llama3.1  # or other locally installed models
  temperature: 0.7
```

## Future Enhancements

- 🌐 Web interface
- 🔌 REST API
- 🎨 Template customization
- 📊 Analytics and tracking
- 💾 Application history
- 📧 Email integration
- 🔗 Job board integrations

## Support

For issues, questions, or contributions:

- **CrewAI Documentation**: [docs.crewai.com](https://docs.crewai.com)
- **GitHub Issues**: Report bugs and request features
- **CrewAI Discord**: [Join the community](https://discord.com/invite/X4JWnZnxPb)

## License

This project uses CrewAI and follows its licensing terms.

---

**Built with [CrewAI](https://crewai.com)** - Multi-Agent AI Framework
