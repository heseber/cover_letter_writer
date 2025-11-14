#!/usr/bin/env python
"""
Cover Letter Writer - Main Entry Point

This module provides CLI interface for generating cover letters using CrewAI.
"""

import sys

import click

from cover_letter_writer.config import Config
from cover_letter_writer.cover_letter_flow import CoverLetterFlow
from cover_letter_writer.tools.document_parser import DocumentParser
from cover_letter_writer.utils import FileHandler, LLMFactory


@click.command(
    context_settings={"max_content_width": 200},
    help="Generate personalized cover letters using AI agents",
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
    "--additional-docs",
    "-a",
    multiple=True,
    default=[],
    help="Additional supporting documents (can be specified multiple times)",
)
@click.option(
    "--llm-provider",
    "-p",
    type=click.Choice(["openai", "anthropic", "ollama"], case_sensitive=False),
    help="LLM provider (openai, anthropic, ollama)",
)
@click.option(
    "--llm-model",
    "-m",
    help="Specific LLM model name",
)
@click.option(
    "--max-iterations",
    "-i",
    type=int,
    help="Maximum number of iterations",
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Path to config file",
)
@click.option(
    "--output-dir",
    "-o",
    help="Output directory for results",
)
@click.option(
    "--translate-to",
    "-t",
    help="Target language code for translation (e.g., 'de', 'fr')",
)
@click.option(
    "--translation-llm-provider",
    help="LLM provider for translation (if different from main)",
)
@click.option(
    "--translation-llm-model",
    help="LLM model for translation (if different from main)",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode with full stack traces",
)
def main(
    job_description: str,
    cv: str,
    additional_docs: tuple[str, ...],
    llm_provider: str | None,
    llm_model: str | None,
    max_iterations: int | None,
    config: str | None,
    output_dir: str | None,
    translate_to: str | None,
    translation_llm_provider: str | None,
    translation_llm_model: str | None,
    debug: bool,
) -> int:
    """Main entry point for the cover letter writer CLI."""
    try:
        # Load configuration
        cfg = Config(config_file=config)

        # Override with CLI arguments
        if llm_provider:
            cfg.set("llm.provider", llm_provider)
        if llm_model:
            cfg.set("llm.model", llm_model)
        if max_iterations:
            cfg.set("writer.max_iterations", max_iterations)
        if output_dir:
            cfg.set("output.directory", output_dir)
        if translate_to:
            cfg.set("translation.target_language", translate_to)
            cfg.set("translation.enabled", True)
        if translation_llm_provider:
            cfg.set("translation.llm_provider", translation_llm_provider)
        if translation_llm_model:
            cfg.set("translation.llm_model", translation_llm_model)

        # Display configuration
        print("\n" + "=" * 80)
        print("COVER LETTER WRITER - Configuration")
        print("=" * 80)
        print(f"LLM Provider: {cfg.llm_provider}")
        print(f"LLM Model: {cfg.llm_model}")
        print(f"Max Iterations: {cfg.max_iterations}")
        print(f"Output Directory: {cfg.output_directory}")
        if cfg.translation_target_language:
            print(f"Translation: {cfg.translation_target_language.upper()}")
            if cfg.translation_llm_provider:
                print(
                    f"Translation LLM: {cfg.translation_llm_provider}/{cfg.translation_llm_model or 'default'}"
                )
        print("=" * 80 + "\n")

        # Parse job description
        print("Loading job description...")
        try:
            job_desc_text = DocumentParser.parse_source(job_description)
            print(f"✅ Job description loaded ({len(job_desc_text)} characters)\n")
        except Exception as e:
            raise click.ClickException(
                f"Failed to load job description: {str(e)}"
            ) from e

        # Parse CV
        print("Loading CV...")
        try:
            cv_text = DocumentParser.parse_file(cv)
            print(f"✅ CV loaded ({len(cv_text)} characters)\n")
        except Exception as e:
            raise click.ClickException(f"Failed to load CV: {str(e)}") from e

        # Parse additional documents
        supporting_docs_content = []
        if additional_docs:
            print(f"Loading {len(additional_docs)} additional document(s)...")
            try:
                for doc_path in additional_docs:
                    doc_content = DocumentParser.parse_file(doc_path)
                    supporting_docs_content.append(doc_content)
                print("✅ All documents loaded\n")
            except Exception as e:
                raise click.ClickException(
                    f"Failed to load additional documents: {str(e)}"
                ) from e

        # Create LLM instance
        print("Initializing LLM...")
        try:
            llm = LLMFactory.create_llm(
                provider=cfg.llm_provider,
                model=cfg.llm_model,
                temperature=cfg.llm_temperature,
            )
            print("✅ LLM initialized\n")
        except Exception as e:
            raise click.ClickException(f"Failed to initialize LLM: {str(e)}") from e

        # Create translation LLM if needed
        translation_llm = None
        if cfg.translation_target_language and cfg.translation_llm_provider:
            print("Initializing translation LLM...")
            try:
                translation_llm = LLMFactory.create_llm(
                    provider=cfg.translation_llm_provider,
                    model=cfg.translation_llm_model or cfg.llm_model,
                    temperature=cfg.llm_temperature,
                )
                print("✅ Translation LLM initialized\n")
            except Exception as e:
                print(f"⚠️  Failed to initialize translation LLM: {str(e)}")
                print("   Using main LLM for translation instead\n")
                translation_llm = None

        # Run generation flow
        flow = CoverLetterFlow(llm, translation_llm=translation_llm)

        # Initialize state with inputs
        flow.state.job_description = job_desc_text
        flow.state.cv_content = cv_text
        flow.state.supporting_docs = supporting_docs_content
        flow.state.max_iterations = cfg.max_iterations
        flow.state.translate_to = cfg.translation_target_language

        # Run the flow
        flow.kickoff()

        # Save outputs
        print("\n" + "=" * 80)
        print("SAVING OUTPUTS")
        print("=" * 80 + "\n")

        # Save final cover letter
        cover_letter_path = FileHandler.save_cover_letter(
            cover_letter_content=flow.state.current_draft,
            output_dir=cfg.output_directory,
            filename_pattern=cfg.cover_letter_filename_pattern,
        )
        print(f"✅ Final cover letter saved: {cover_letter_path}")

        # Save translated cover letter if available
        if flow.state.translated_cover_letter:
            # Use the same base filename as the English cover letter (without extension)
            base_filename = (
                cover_letter_path.stem
            )  # e.g., "cover_letter_optimized_20251113_123456"
            translated_cover_letter_path = FileHandler.save_translated_cover_letter(
                cover_letter_content=flow.state.translated_cover_letter,
                output_dir=cfg.output_directory,
                language_code=cfg.translation_target_language,
                base_filename=base_filename,
            )
            print(
                f"✅ Translated cover letter ({cfg.translation_target_language.upper()}) saved: {translated_cover_letter_path}"
            )

        # Save feedback history
        feedback_content = FileHandler.format_feedback_history(
            flow.state.feedback_history
        )
        feedback_path = FileHandler.save_feedback_history(
            feedback_content=feedback_content,
            output_dir=cfg.output_directory,
            filename_pattern=cfg.feedback_filename_pattern,
        )
        print(f"✅ Feedback history saved: {feedback_path}")

        # Display summary
        print("\n" + "=" * 80)
        print("GENERATION SUMMARY")
        print("=" * 80)
        print(f"Status: {flow.state.status}")
        print(f"Iterations Completed: {flow.state.iteration_count}")
        print(f"Final Decision: {flow.state.final_decision or 'N/A'}")
        print(f"Output Directory: {cfg.output_directory}")
        print("=" * 80 + "\n")

        if flow.state.status == "APPROVED":
            print("✅ Cover letter was approved by the reviewer!")
        elif flow.state.status == "MAX_ITERATIONS_REACHED":
            print(
                "⚠️  Maximum iterations reached. Consider running again with more iterations."
            )

        print("\nThank you for using Cover Letter Writer!\n")

        return 0

    except click.ClickException:
        raise
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
    print("Generating flow plot...")
    from cover_letter_writer.utils import LLMFactory

    # Create a dummy LLM for plotting
    llm = LLMFactory.create_llm("openai", "gpt-4o", temperature=0.7)

    flow = CoverLetterFlow(llm)
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
    job_desc = payload.get("job_description")
    cv_path = payload.get("cv")

    if not job_desc or not cv_path:
        print(
            "Error: Payload must include 'job_description' and 'cv'",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build arguments for main
    args = [
        "--job-description",
        job_desc,
        "--cv",
        cv_path,
    ]

    # Add optional parameters
    if payload.get("additional_docs"):
        for doc in payload["additional_docs"]:
            args.extend(["--additional-docs", doc])

    if payload.get("output_dir"):
        args.extend(["--output-dir", payload["output_dir"]])

    if payload.get("max_iterations"):
        args.extend(["--max-iterations", str(payload["max_iterations"])])

    # Run main with arguments
    sys.argv = ["cover-letter-writer"] + args
    sys.exit(main(standalone_mode=False))


if __name__ == "__main__":
    sys.exit(main())
