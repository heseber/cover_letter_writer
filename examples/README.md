# Example Files for Cover Letter Writer

This directory contains sample files to help you get started with the Cover Letter Writer application.

## Files Included

1. **sample_job_description.txt** - A sample job posting for a Senior Software Engineer position
2. **sample_cv.md** - A sample CV/resume in Markdown format
3. **sample_recommendation.md** - A sample letter of recommendation

## Quick Test

To test the application with these sample files, run:

```bash
cover-letter-writer \
  --job-description examples/sample_job_description.txt \
  --cv examples/sample_cv.md \
  --documents examples/sample_recommendation.md \
  --output examples/output_cover_letter.md \
  --max-iterations 3
```

Or using relative paths from the project root:

```bash
cd /path/to/cover_letter_writer
cover-letter-writer \
  -j examples/sample_job_description.txt \
  -c examples/sample_cv.md \
  -d examples/sample_recommendation.md \
  -o examples/output_cover_letter.md
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

## Tips for Best Results

1. **Job Description**: Ensure it contains clear requirements and responsibilities
2. **CV Format**: Well-structured CVs with clear sections work best
3. **Recommendations**: Include specific examples of achievements
4. **Iterations**: Start with 3 iterations; increase if needed for better quality
5. **API Key**: Make sure your `.env` file contains a valid API key

## Troubleshooting

**Issue: Documents not loading**
- Check file paths are correct
- Ensure files are readable
- Try using absolute paths

**Issue: Poor quality output**
- Increase max iterations (e.g., `--max-iterations 5`)
- Ensure input documents have sufficient detail
- Check that your LLM API is working correctly

**Issue: Process takes too long**
- Reduce max iterations
- Consider using a faster LLM model
- Check your internet connection

## Next Steps

After testing with these samples:
1. Replace with your own CV and job descriptions
2. Adjust the max iterations based on quality needs
3. Review and edit the generated cover letters
4. Customize agent configurations in `config/` if needed

For more information, see the main [README.md](../README.md) in the project root.

