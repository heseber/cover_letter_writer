#!/usr/bin/env python
"""
Cover Letter Writer - Main Entry Point

This module provides CLI interface for generating cover letters using CrewAI.
"""

import sys
from pathlib import Path

import click

from cover_letter_writer.cover_letter_flow import create_cover_letter_flow


def validate_inputs(
    job_description: str,
    cv: str,
    documents: tuple[str, ...],
    max_iterations: int,
) -> None:
    """
    Validate input arguments.

    Args:
        job_description: Path to job description file or URL
        cv: Path to CV file
        documents: Tuple of additional document paths
        max_iterations: Maximum number of review iterations

    Raises:
        click.ClickException: If validation fails
    """
    errors = []

    # Check if job description file exists (unless it's a URL)
    if not job_description.startswith(("http://", "https://")):
        if not Path(job_description).exists():
            errors.append(f"Job description file not found: {job_description}")

    # Check if CV exists
    cv_path = Path(cv)
    if not cv_path.exists():
        errors.append(f"CV file not found: {cv}")
    elif not cv_path.is_file():
        errors.append(f"CV path is not a file: {cv}")

    # Check additional documents
    for doc_path in documents:
        doc = Path(doc_path)
        if not doc.exists():
            errors.append(f"Document not found: {doc_path}")
        elif not doc.is_file():
            errors.append(f"Document path is not a file: {doc_path}")

    # Check max iterations
    if max_iterations < 1:
        errors.append("Max iterations must be at least 1")
    elif max_iterations > 10:
        errors.append(
            "Max iterations cannot exceed 10 (to prevent excessive API usage)"
        )

    if errors:
        error_message = "❌ Validation Errors:\n" + "\n".join(
            f"   - {error}" for error in errors
        )
        raise click.ClickException(error_message)


@click.command(
    context_settings={"max_content_width": 200},
    help="Generate personalized cover letters using AI agents",
    epilog="""
\b
Examples:
  cover-letter-writer -j job.txt -c cv.pdf -o letter.md

  cover-letter-writer -j https://company.com/job -c cv.pdf \\
                      -d rec.pdf -m 5 -o letter.md
""",
)
@click.option(
    "--job-description",
    "-j",
    required=True,
    help="Path to job description file or URL to job posting",
)
@click.option(
    "--cv",
    "-c",
    required=True,
    help="Path to your CV/resume file (PDF or Markdown)",
)
@click.option(
    "--documents",
    "-d",
    multiple=True,
    default=[],
    help="Additional documents (recommendations, certificates, etc.). Can be specified multiple times.",
)
@click.option(
    "--output",
    "-o",
    default="cover_letter.md",
    help="Output file path for the generated cover letter",
    show_default=True,
)
@click.option(
    "--max-iterations",
    "-m",
    type=int,
    default=3,
    help="Maximum number of review iterations",
    show_default=True,
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode with full stack traces",
)
def main(
    job_description: str,
    cv: str,
    documents: tuple[str, ...],
    output: str,
    max_iterations: int,
    debug: bool,
) -> int:
    """Main entry point for the cover letter writer CLI."""
    print("\n" + "=" * 60)
    print(" " * 15 + "COVER LETTER WRITER")
    print(" " * 10 + "AI-Powered Cover Letter Generation")
    print("=" * 60 + "\n")

    # Validate inputs
    print("🔍 Validating inputs...")
    validate_inputs(job_description, cv, documents, max_iterations)
    print("✓ Inputs validated\n")

    # Display configuration
    print("📋 Configuration:")
    print(f"   Job Description: {job_description}")
    print(f"   CV: {cv}")
    if documents:
        print(f"   Additional Documents: {len(documents)} file(s)")
        for doc in documents:
            print(f"      - {doc}")
    print(f"   Output: {output}")
    print(f"   Max Iterations: {max_iterations}")
    print()

    try:
        # Create and run the flow
        flow = create_cover_letter_flow(
            job_description_source=job_description,
            cv_path=cv,
            output_path=output,
            document_paths=list(documents),
            max_iterations=max_iterations,
        )

        # Execute the flow
        flow.kickoff()

        print("\n✅ Success! Your cover letter has been generated.")
        print(f"📄 Output saved to: {Path(output).absolute()}")

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        return 130

    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        if debug:
            import traceback

            traceback.print_exc()
        return 1


def kickoff():
    """Entry point for 'crewai run' command."""
    sys.exit(main(standalone_mode=False))


def plot():
    """Generate a plot of the flow structure."""
    from cover_letter_writer.cover_letter_flow import CoverLetterFlow

    print("Generating flow plot...")
    flow = CoverLetterFlow()
    flow.plot()
    print("✓ Flow plot generated")


def run_with_trigger():
    """
    Run the flow with trigger payload (for future web/API integration).
    """
    import json

    if len(sys.argv) < 2:
        print("Error: No trigger payload provided.", file=sys.stderr)
        print(
            'Usage: run_with_trigger \'{"job_description": "...", ...}\'',
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("Error: Invalid JSON payload", file=sys.stderr)
        sys.exit(1)

    # Extract parameters from payload
    job_desc = payload.get("job_description_source")
    cv_path = payload.get("cv_path")

    if not job_desc or not cv_path:
        print(
            "Error: Payload must include 'job_description_source' and 'cv_path'",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        flow = create_cover_letter_flow(
            job_description_source=job_desc,
            cv_path=cv_path,
            output_path=payload.get("output_path", "cover_letter.md"),
            document_paths=payload.get("document_paths", []),
            max_iterations=payload.get("max_iterations", 3),
        )

        flow.kickoff()
        return 0

    except Exception as e:
        print(f"Error running flow: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
