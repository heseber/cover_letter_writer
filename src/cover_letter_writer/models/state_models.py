"""Pydantic models for Cover Letter Writer state management."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewFeedback(BaseModel):
    """Model for reviewer feedback."""

    iteration: int = Field(..., description="Iteration number")
    decision: str = Field(..., description="APPROVED or NEEDS_IMPROVEMENT")
    comments: str = Field(..., description="Detailed feedback comments")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Timestamp of feedback"
    )


class CoverLetterState(BaseModel):
    """State model for cover letter generation flow."""

    # Inputs
    job_description: str = Field("", description="Job description text")
    cv_content: str = Field("", description="CV/resume content")
    supporting_docs: list[str] = Field(
        default_factory=list, description="Additional supporting documents"
    )

    # Processing
    current_draft: str = Field(
        "", description="Current version of cover letter being processed"
    )
    iteration_count: int = Field(0, description="Current iteration number")
    max_iterations: int = Field(3, description="Maximum number of iterations")

    # Feedback tracking
    feedback_history: list[ReviewFeedback] = Field(
        default_factory=list, description="History of all reviewer feedback"
    )

    # Status
    status: str = Field("INITIALIZED", description="Current flow status")
    final_decision: str | None = Field(
        None, description="Final decision from reviewer"
    )

    # Translation
    translate_to: str | None = Field(
        None, description="Target language code (e.g., 'de', 'fr')"
    )
    translated_cover_letter: str | None = Field(
        None, description="Translated cover letter content"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

