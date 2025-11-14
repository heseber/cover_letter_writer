"""Cover Letter Generation Flow using CrewAI Flow."""

import re
from datetime import datetime
from typing import Any, Literal

from crewai.flow import Flow, listen, or_, router, start

from cover_letter_writer.crews.reviewer_crew import ReviewerCrew
from cover_letter_writer.crews.translator_crew import TranslatorCrew
from cover_letter_writer.crews.writer_crew import WriterCrew
from cover_letter_writer.models.state_models import CoverLetterState, ReviewFeedback


class CoverLetterFlow(Flow[CoverLetterState]):
    """Flow for iterative cover letter generation with review and revision."""

    def __init__(self, llm: Any, translation_llm: Any | None = None):
        """
        Initialize Cover Letter Generation Flow.

        Args:
            llm: Language model instance for generation
            translation_llm: Optional separate LLM for translation (uses main LLM if None)
        """
        super().__init__()
        self.llm = llm
        self.translation_llm = translation_llm or llm

    @start()
    def initialize_flow(self):
        """Initialize the flow and load all documents."""
        print(f"\n{'=' * 80}")
        print("COVER LETTER GENERATOR - STARTING")
        print(f"{'=' * 80}\n")
        print(f"Job Description length: {len(self.state.job_description)} characters")
        print(f"CV length: {len(self.state.cv_content)} characters")
        print(f"Supporting Documents: {len(self.state.supporting_docs)}")
        print(f"Max Iterations: {self.state.max_iterations}\n")

        # Initialize status
        self.state.status = "WRITING"

    @listen(initialize_flow)
    def create_first_draft(self):
        """Generate the initial cover letter draft."""
        self.state.iteration_count = 1

        print(f"\n{'=' * 80}")
        print(f"ITERATION {self.state.iteration_count} - WRITING PHASE")
        print(f"{'=' * 80}\n")

        # Prepare supporting docs text
        supporting_docs_text = self._format_supporting_docs()

        # Run writer crew
        result = (
            WriterCrew(self.llm)
            .crew()
            .kickoff(
                inputs={
                    "job_description": self.state.job_description,
                    "cv_content": self.state.cv_content,
                    "supporting_documents": supporting_docs_text,
                    "reviewer_feedback": "This is the initial draft. Please create a compelling cover letter.",
                    "draft_content": "No previous draft.",
                }
            )
        )

        # Extract the writer's output
        if hasattr(result, "tasks_output") and len(result.tasks_output) > 0:
            draft = result.tasks_output[0].raw
        else:
            draft = result.raw

        # Clean up the draft
        draft = self._clean_markdown_wrapper(draft)

        # Update state
        self.state.current_draft = draft

        print(f"\nFirst draft length: {len(draft)} characters")
        print(f"Completed iteration {self.state.iteration_count}\n")

        # Move to review
        self.state.status = "REVIEWING"

    @listen("decision_to_revise")
    def revise_draft(self):
        """Generate an improved draft based on feedback."""
        self.state.iteration_count += 1

        print(f"\n{'=' * 80}")
        print(f"ITERATION {self.state.iteration_count} - WRITING PHASE")
        print(f"{'=' * 80}\n")

        # Get latest feedback
        latest_feedback = self.state.feedback_history[-1].comments

        # Prepare supporting docs text
        supporting_docs_text = self._format_supporting_docs()

        # Run writer crew
        result = (
            WriterCrew(self.llm)
            .crew()
            .kickoff(
                inputs={
                    "job_description": self.state.job_description,
                    "cv_content": self.state.cv_content,
                    "supporting_documents": supporting_docs_text,
                    "reviewer_feedback": latest_feedback,
                    "draft_content": self.state.current_draft,
                }
            )
        )

        # Extract the writer's output
        if hasattr(result, "tasks_output") and len(result.tasks_output) > 0:
            revised_draft = result.tasks_output[0].raw
        else:
            revised_draft = result.raw

        # Clean up the draft
        revised_draft = self._clean_markdown_wrapper(revised_draft)

        # Update state
        self.state.current_draft = revised_draft

        print(f"\nRevised draft length: {len(revised_draft)} characters")
        print(f"Completed iteration {self.state.iteration_count}\n")

        # Move to review
        self.state.status = "REVIEWING"

    @listen(or_(create_first_draft, revise_draft))
    def review_draft(self):
        """Review the current draft."""
        print(f"\n{'=' * 80}")
        print(f"ITERATION {self.state.iteration_count} - REVIEW PHASE")
        print(f"{'=' * 80}\n")

        # Prepare supporting docs text
        supporting_docs_text = self._format_supporting_docs()

        # Run reviewer crew
        result = (
            ReviewerCrew(self.llm)
            .crew()
            .kickoff(
                inputs={
                    "job_description": self.state.job_description,
                    "cv_content": self.state.cv_content,
                    "supporting_documents": supporting_docs_text,
                    "draft_content": self.state.current_draft,
                    "reviewer_feedback": "",
                }
            )
        )

        # Extract reviewer's feedback
        if hasattr(result, "tasks_output") and len(result.tasks_output) > 0:
            review_output = result.tasks_output[0].raw
        else:
            review_output = result.raw

        print("\n✅ Review completed!")

        # Parse the review to check if approved
        review_upper = review_output.upper()
        if "DECISION: APPROVED" in review_upper or "DECISION:APPROVED" in review_upper:
            decision = "APPROVED"
            comments = review_output
            print("✅ Draft APPROVED by reviewer!")
        else:
            decision = "NEEDS_IMPROVEMENT"
            comments = (
                f"Based on the review, please improve the draft:\n\n{review_output}"
            )
            print("⚠️  Draft needs improvement. Feedback provided for next iteration.")

        # Create feedback object
        feedback = ReviewFeedback(
            iteration=self.state.iteration_count,
            decision=decision,
            comments=comments,
            timestamp=datetime.now(),
        )

        # Add to history
        self.state.feedback_history.append(feedback)

        print(f"\nReviewer Decision: {decision}")
        print(f"Feedback length: {len(review_output)} characters\n")

        # Store decision for routing
        self.state.final_decision = decision

    @router(review_draft)
    def route_decision(
        self,
    ) -> Literal["decision_to_finalize", "decision_to_revise"]:
        """
        Route based on reviewer decision.

        Returns:
            Next method to execute
        """
        decision = self.state.final_decision

        # Check if approved
        if decision == "APPROVED":
            print(f"\n{'=' * 80}")
            print("COVER LETTER APPROVED - Flow Complete")
            print(f"{'=' * 80}\n")
            self.state.status = "APPROVED"
            return "decision_to_finalize"

        # Check if max iterations reached
        if self.state.iteration_count >= self.state.max_iterations:
            print(f"\n{'=' * 80}")
            print("MAX ITERATIONS REACHED - Flow Complete")
            print(f"{'=' * 80}\n")
            self.state.status = "MAX_ITERATIONS_REACHED"
            return "decision_to_finalize"

        # Continue to revision
        print("\nContinuing to revision phase...")
        self.state.status = "REVISING"
        return "decision_to_revise"

    @listen("decision_to_finalize")
    def complete_flow(self):
        """Complete the writing phase."""
        print(f"\n{'=' * 80}")
        print("COVER LETTER WRITING COMPLETE")
        print(f"{'=' * 80}\n")
        print(f"Final Status: {self.state.status}")
        print(f"Total Iterations: {self.state.iteration_count}")
        print(f"Total Feedback Entries: {len(self.state.feedback_history)}\n")

    @router(complete_flow)
    def route_translation(
        self,
    ) -> Literal["decision_to_translate", "decision_to_end"]:
        """
        Route based on translation requirement.

        Returns:
            Next method to execute or None to end flow
        """
        if self.state.translate_to:
            print(f"\nTranslation requested to {self.state.translate_to.upper()}...")
            return "decision_to_translate"
        else:
            print("\nNo translation requested. Flow complete.")
            return "decision_to_end"

    @listen("decision_to_translate")
    def translate_cover_letter(self):
        """Translate the final cover letter to the target language."""
        print(f"\n{'=' * 80}")
        print(f"TRANSLATION PHASE - Translating to {self.state.translate_to.upper()}")
        print(f"{'=' * 80}\n")

        # Run translator crew with appropriate LLM
        result = (
            TranslatorCrew(self.translation_llm)
            .crew()
            .kickoff(
                inputs={
                    "cover_letter_content": self.state.current_draft,
                    "target_language": self.state.translate_to,
                }
            )
        )

        translated_draft = result.raw if hasattr(result, "raw") else str(result)

        # Clean up the translated draft
        translated_draft = self._clean_markdown_wrapper(translated_draft)

        # Update state
        self.state.translated_cover_letter = translated_draft

        print(f"\nTranslated cover letter length: {len(translated_draft)} characters")
        print(f"Translation to {self.state.translate_to.upper()} complete\n")

    @listen(or_(translate_cover_letter, "decision_to_end"))
    def finalize_flow(self):
        """Final cleanup and flow termination."""
        print(f"\n{'=' * 80}")
        print("FLOW FINALIZED")
        print(f"{'=' * 80}\n")

    def _format_supporting_docs(self) -> str:
        """
        Format supporting documents for display.

        Returns:
            Formatted supporting documents text
        """
        if self.state.supporting_docs:
            return "\n\n".join(
                f"Document {i + 1}:\n{doc}"
                for i, doc in enumerate(self.state.supporting_docs)
            )
        return "No additional documents provided."

    @staticmethod
    def _clean_markdown_wrapper(content: str) -> str:
        """
        Remove markdown code block wrappers if present.

        Sometimes LLMs wrap their markdown output in code blocks like:
        ```markdown
        content here
        ```
        or
        ```
        content here
        ```

        This method strips those wrappers to get the raw content.

        Args:
            content: Raw content from LLM

        Returns:
            Cleaned content
        """
        content = content.strip()

        # Check if content starts with ``` and ends with ```
        if content.startswith("```") and content.endswith("```"):
            # Remove opening ```
            content = content[3:]

            # Remove language identifier if present (e.g., 'markdown')
            if content.startswith("markdown"):
                content = content[8:]

            # Remove first newline after opening ```
            if content.startswith("\n"):
                content = content[1:]

            # Remove closing ```
            if content.endswith("```"):
                content = content[:-3]

            # Remove trailing newline before closing ```
            content = content.rstrip("\n")

        # Remove any leading/trailing "Here is" type phrases
        content = re.sub(
            r"^(Here is|Here's|Below is|The following is).*?cover letter:?\s*",
            "",
            content,
            flags=re.IGNORECASE | re.MULTILINE,
        )

        return content.strip()
