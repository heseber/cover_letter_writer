# Example Files for Cover Letter Writer

This directory contains sample files to help you get started with the Cover Letter Writer application.

## Files Included

1. **sample_job_description.txt** - A sample job posting for a Senior Software Engineer position
2. **sample_cv.md** - A sample CV/resume in Markdown format
3. **sample_recommendation.md** - A sample letter of recommendation

## Quick Test

### Basic Test (English Only)

To test the application with these sample files, run:

```bash
cover-letter-writer \
  --job-description examples/sample_job_description.txt \
  --cv examples/sample_cv.md \
  --additional-docs examples/sample_recommendation.md \
  --output-dir ./output \
  --max-iterations 3
```

Or using relative paths from the project root:

```bash
cd /path/to/cover_letter_writer
cover-letter-writer \
  -j examples/sample_job_description.txt \
  -c examples/sample_cv.md \
  -a examples/sample_recommendation.md \
  -o ./output
```

### Test with Translation

To test the application with translation to German:

```bash
cover-letter-writer \
  -j examples/sample_job_description.txt \
  -c examples/sample_cv.md \
  -a examples/sample_recommendation.md \
  -o ./output \
  --translate-to de
```

This will generate two files:
- English original cover letter
- German translation with `_de` suffix

### Test with Different LLM Provider

To use Anthropic Claude instead of OpenAI:

1. First, set your Anthropic API key in `.env`:
```bash
ANTHROPIC_API_KEY=your_anthropic_key_here
```

2. Edit `src/cover_letter_writer/config/cover_letter_writer.yaml`:
```yaml
llm:
  provider: anthropic
  model: claude-3-5-sonnet-20241022
  temperature: 0.7
```

3. Run the same command as before:
```bash
cover-letter-writer \
  -j examples/sample_job_description.txt \
  -c examples/sample_cv.md \
  -a examples/sample_recommendation.md \
  -o ./output
```

## Expected Output

The application will:
1. Load all the sample documents
2. Generate an initial cover letter draft
3. Have the reviewer agent evaluate it
4. Iterate up to 3 times (or until approved)
5. Save the final cover letter to `examples/output_cover_letter.md`

The entire process typically takes 3-10 minutes depending on your LLM provider and iteration count.

## Using Your Own Files

### Job Description
Replace `sample_job_description.txt` with your own job posting. Supported formats:
- `.txt` - Plain text file
- `.md` - Markdown file
- URL - Direct link to online job posting

### CV/Resume
Replace `sample_cv.md` with your own CV. Supported formats:
- `.md` - Markdown (recommended for easy editing)
- `.pdf` - PDF file
- `.txt` - Plain text

### Additional Documents
Add your own:
- Letters of recommendation
- Certificates
- Awards
- Publications
- Portfolio links

**Tip:** Name files with "recommend" or "reference" in the filename to help the system 
categorize them correctly.

## Translation Examples

### Supported Languages

The translation feature supports any language. Common examples:

| Language | Code | Full Name |
|----------|------|-----------|
| German | `de` | German |
| French | `fr` | French |
| Spanish | `es` | Spanish |
| Italian | `it` | Italian |
| Portuguese | `pt` | Portuguese |
| Dutch | `nl` | Dutch |
| Polish | `pl` | Polish |
| Japanese | `ja` | Japanese |
| Chinese | `zh` | Chinese |
| Korean | `ko` | Korean |

### Example: Translate to German

```bash
cover-letter-writer \
  -j examples/sample_job_description.txt \
  -c examples/sample_cv.md \
  --translate-to de \
  -o output/
```

Output files:
- English original cover letter
- German translation with `_de` suffix

### Example: Translate to Multiple Languages

Generate and translate to French and Spanish:

```bash
# Generate English and French
cover-letter-writer \
  -j examples/sample_job_description.txt \
  -c examples/sample_cv.md \
  --translate-to fr \
  -o output/

# Generate English and Spanish
cover-letter-writer \
  -j examples/sample_job_description.txt \
  -c examples/sample_cv.md \
  --translate-to es \
  -o output/
```

### Translation Configuration

You can configure a different LLM for translation in `cover_letter_writer.yaml`:

```yaml
translation:
  enabled: true
  target_language: de
  llm_provider: anthropic  # Use Claude for translation
  llm_model: claude-3-5-sonnet-20241022
```

## Tips for Best Results

1. **Job Description**: Ensure it contains clear requirements and responsibilities
2. **CV Format**: Well-structured CVs with clear sections work best
3. **Recommendations**: Include specific examples of achievements
4. **Iterations**: Start with 3 iterations; increase if needed for better quality
5. **API Key**: Make sure your `.env` file contains a valid API key
6. **Translation**: For best translation quality, use GPT-4 or Claude models
7. **Multi-LLM**: Mix providers (e.g., OpenAI for writing, Claude for translation)

## Troubleshooting

**Issue: Documents not loading**
- Check file paths are correct
- Ensure files are readable
- Try using absolute paths

**Issue: Poor quality output**
- Increase max iterations (e.g., `--max-iterations 5`)
- Ensure input documents have sufficient detail
- Check that your LLM API is working correctly
- Try a more powerful model (e.g., GPT-4o instead of GPT-3.5-turbo)

**Issue: Translation quality issues**
- Use a more powerful model for translation
- Check that the target language is correctly specified
- Verify the translation preserves markdown formatting

**Issue: Process takes too long**
- Reduce max iterations
- Consider using a faster LLM model
- Check your internet connection
- Use Ollama with local models for faster processing (no API calls)

**Issue: LLM provider errors**
- Verify API key is set correctly in `.env` file
- Check provider configuration in `cover_letter_writer.yaml`
- Ensure the model name is correct for the provider
- For Ollama, ensure the service is running locally

## Next Steps

After testing with these samples:
1. Replace with your own CV and job descriptions
2. Adjust the max iterations based on quality needs
3. Experiment with different LLM providers
4. Try translating to your target languages
5. Review and edit the generated cover letters
6. Customize agent configurations in `config/` if needed
7. Configure application settings in `cover_letter_writer.yaml`

## Additional Resources

For more information:
- **Main Documentation**: [README.md](../README.md)
- **Quick Start Guide**: [QUICKSTART.md](../QUICKSTART.md)
- **Setup Checklist**: [SETUP_CHECKLIST.md](../SETUP_CHECKLIST.md)
- **Configuration**: [cover_letter_writer.yaml](../src/cover_letter_writer/config/cover_letter_writer.yaml)

## Advanced Usage

### Combine Multiple Features

Generate a cover letter with all features:

```bash
cover-letter-writer \
  -j examples/sample_job_description.txt \
  -c examples/sample_cv.md \
  -a examples/sample_recommendation.md \
  -o output/senior_swe \
  -i 5 \
  --translate-to de
```

This will:
1. Load all documents
2. Generate initial draft
3. Iteratively improve (up to 5 times)
4. Save English version
5. Translate to German
6. Save German version

### Using Job Description URLs

Instead of a file, use a direct URL:

```bash
cover-letter-writer \
  -j https://company.com/careers/senior-engineer \
  -c examples/sample_cv.md \
  -o output/
```

For more information, see the main [README.md](../README.md) in the project root.

