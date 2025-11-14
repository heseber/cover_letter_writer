# Changelog

All notable changes to the Cover Letter Writer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Multi-crew architecture with specialized crews (Writer, Reviewer, Translator)
- Translation crew for multi-language cover letter support
- Centralized configuration system (`config/config_loader.py`)
- LLM factory for flexible model provider selection (`utils/llm_factory.py`)
- Enhanced file handling utilities (`utils/file_handler.py`)
- Dedicated PDF reading tool (`tools/pdf_reader.py`)
- Dedicated web scraping tool (`tools/web_scraper.py`)
- Document parser module (`tools/document_parser.py`)
- State models module for improved type safety (`models/state_models.py`)
- Support for Anthropic Claude models (`langchain-anthropic`)
- Support for Ollama local models (`langchain-ollama`)
- YAML-based configuration file (`config/cover_letter_writer.yaml`)

### Changed
- Refactored from single-crew to multi-crew architecture
- Split `cover_letter_crew` into specialized `writer_crew`, `reviewer_crew`, and `translator_crew`
- Updated main flow to support new multi-crew architecture
- Improved document tools organization and separation of concerns
- Enhanced error handling and state management
- Updated package dependencies in `pyproject.toml`

### Removed
- Legacy `cover_letter_crew` module (replaced by specialized crews)

## [0.1.0] - 2024-11-10

### Added
- Initial MVP release
- Core CrewAI Flow-based architecture
- Iterative cover letter generation with writer and reviewer agents
- Support for multiple input formats (PDF, Markdown, plain text)
- URL support for job description fetching
- Command-line interface with comprehensive options
- Document parsing utilities (`tools/document_tools.py`)
- Support for additional documents (recommendations, certificates)
- Configurable iteration limits (max 10)
- Markdown output format with metadata
- Professional README and QUICKSTART guides
- Example files for testing
- Unit tests for document tools
- Flow visualization support (`crewai flow plot`)

### Fixed
- Flow visualization displaying with correct proportions
- Method listener configuration for proper flow execution
- Backward edge optimization in flow graph

### Dependencies
- crewai[tools]==1.3.0
- pypdf>=5.1.0
- requests>=2.31.0
- beautifulsoup4>=4.12.0
- pytest>=7.4.0
- langchain-openai>=1.0.2

## [0.0.1] - 2024-11-01

### Added
- Initial project setup
- Basic project structure
- CrewAI Flow scaffolding
- Project configuration files

---

## Release Notes

### Version 0.2.0 (Upcoming)
This release represents a major architectural refactoring to support multiple specialized crews and multi-language support. The single-crew architecture has been replaced with a modular multi-crew system that allows for better separation of concerns and enhanced extensibility.

**Key Highlights:**
- 🌍 Multi-language support via dedicated Translation Crew
- 🎯 Specialized crews for writing, reviewing, and translation
- 🔧 Flexible LLM provider support (OpenAI, Anthropic, Ollama)
- ⚙️ Centralized configuration management
- 🏗️ Improved architecture for future enhancements

**Migration Notes:**
- Configuration files have been reorganized under `config/` directory
- Crew definitions are now in separate modules under `crews/`
- State models have been extracted to `models/` module
- Tool modules have been split for better organization

### Version 0.1.0 (MVP)
Initial production-ready release with core cover letter generation functionality. Implements a complete iterative writing and review process using CrewAI Flows.

**Key Features:**
- Dual-agent collaboration (Writer + Reviewer)
- Automatic iteration and refinement
- Multi-format document support
- URL job description fetching
- Command-line interface
- Professional output formatting

---

## Upgrade Guide

### From 0.1.0 to 0.2.0

1. **Update dependencies:**
   ```bash
   uv pip install -e .
   ```

2. **Configuration changes:**
   - Review new configuration options in `config/cover_letter_writer.yaml`
   - Set up LLM provider preferences if using non-OpenAI models

3. **Environment variables:**
   - Add `ANTHROPIC_API_KEY` if using Claude models
   - Configure Ollama endpoint if using local models

4. **Code changes (if extending):**
   - Import crews from new locations: `crews.writer_crew`, `crews.reviewer_crew`, `crews.translator_crew`
   - Use `models.state_models` for state definitions
   - Use `utils.llm_factory` for LLM initialization

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to this project.

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation in README.md
- Review examples in `examples/` directory

---

**Repository:** https://github.com/yourusername/cover-letter-writer
**Documentation:** See README.md
**License:** See LICENSE file

