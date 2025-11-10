#!/usr/bin/env python
"""
Cover Letter Writer - Main Entry Point

This module provides CLI interface for generating cover letters using CrewAI.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from cover_letter_writer.cover_letter_flow import create_cover_letter_flow


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Generate personalized cover letters using AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate cover letter from local job description file
  cover-letter-writer \\
    --job-description job_desc.txt \\
    --cv my_cv.pdf \\
    --output my_cover_letter.md
  
  # Generate from URL with additional documents
  cover-letter-writer \\
    --job-description https://company.com/careers/job \\
    --cv my_cv.pdf \\
    --documents recommendation.pdf certificate.md \\
    --max-iterations 5 \\
    --output cover_letter.md
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--job-description",
        "-j",
        required=True,
        help="Path to job description file or URL to job posting"
    )
    
    parser.add_argument(
        "--cv",
        "-c",
        required=True,
        help="Path to your CV/resume file (PDF or Markdown)"
    )
    
    # Optional arguments
    parser.add_argument(
        "--documents",
        "-d",
        nargs="+",
        default=[],
        help="Additional documents (recommendations, certificates, etc.)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        default="cover_letter.md",
        help="Output file path for the generated cover letter (default: cover_letter.md)"
    )
    
    parser.add_argument(
        "--max-iterations",
        "-m",
        type=int,
        default=3,
        help="Maximum number of review iterations (default: 3)"
    )
    
    return parser.parse_args()


def validate_inputs(args: argparse.Namespace) -> None:
    """
    Validate input arguments.
    
    Args:
        args: Parsed arguments
        
    Raises:
        SystemExit: If validation fails
    """
    errors = []
    
    # Check if CV file exists (unless it's a URL, which we'll validate later)
    if not args.job_description.startswith(('http://', 'https://')):
        if not Path(args.job_description).exists():
            errors.append(f"Job description file not found: {args.job_description}")
    
    # Check if CV exists
    cv_path = Path(args.cv)
    if not cv_path.exists():
        errors.append(f"CV file not found: {args.cv}")
    elif not cv_path.is_file():
        errors.append(f"CV path is not a file: {args.cv}")
    
    # Check additional documents
    for doc_path in args.documents:
        doc = Path(doc_path)
        if not doc.exists():
            errors.append(f"Document not found: {doc_path}")
        elif not doc.is_file():
            errors.append(f"Document path is not a file: {doc_path}")
    
    # Check max iterations
    if args.max_iterations < 1:
        errors.append("Max iterations must be at least 1")
    elif args.max_iterations > 10:
        errors.append("Max iterations cannot exceed 10 (to prevent excessive API usage)")
    
    if errors:
        print("❌ Validation Errors:", file=sys.stderr)
        for error in errors:
            print(f"   - {error}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the cover letter writer CLI."""
    print("\n" + "="*60)
    print(" "*15 + "COVER LETTER WRITER")
    print(" "*10 + "AI-Powered Cover Letter Generation")
    print("="*60 + "\n")
    
    # Parse arguments
    args = parse_arguments()
    
    # Validate inputs
    print("🔍 Validating inputs...")
    validate_inputs(args)
    print("✓ Inputs validated\n")
    
    # Display configuration
    print("📋 Configuration:")
    print(f"   Job Description: {args.job_description}")
    print(f"   CV: {args.cv}")
    if args.documents:
        print(f"   Additional Documents: {len(args.documents)} file(s)")
        for doc in args.documents:
            print(f"      - {doc}")
    print(f"   Output: {args.output}")
    print(f"   Max Iterations: {args.max_iterations}")
    print()
    
    try:
        # Create and run the flow
        flow = create_cover_letter_flow(
            job_description_source=args.job_description,
            cv_path=args.cv,
            output_path=args.output,
            document_paths=args.documents,
            max_iterations=args.max_iterations,
        )
        
        # Execute the flow
        flow.kickoff()
        
        print("\n✅ Success! Your cover letter has been generated.")
        print(f"📄 Output saved to: {Path(args.output).absolute()}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        return 130
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()
        return 1


def kickoff():
    """Entry point for 'crewai run' command."""
    sys.exit(main())


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
        print("Usage: run_with_trigger '{\"job_description\": \"...\", ...}'", file=sys.stderr)
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
        print("Error: Payload must include 'job_description_source' and 'cv_path'", file=sys.stderr)
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
