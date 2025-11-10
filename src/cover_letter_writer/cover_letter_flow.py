"""Main Flow for Cover Letter Generation with Iterative Review."""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field
from crewai.flow import Flow, listen, start, router, or_

from cover_letter_writer.crews.cover_letter_crew.cover_letter_crew import CoverLetterCrew
from cover_letter_writer.tools.document_tools import (
    read_job_description,
    read_document,
)


class CoverLetterState(BaseModel):
    """State management for the cover letter generation flow."""
    
    # Input data
    job_description_source: str = ""
    job_description: str = ""
    cv_path: str = ""
    cv_content: str = ""
    document_paths: List[str] = Field(default_factory=list)
    recommendations_content: str = "No recommendations provided."
    certificates_content: str = "No certificates provided."
    
    # Output configuration
    output_path: str = "cover_letter.md"
    max_iterations: int = 3
    
    # Process state
    current_iteration: int = 0
    current_draft: str = ""
    reviewer_feedback: str = "This is the initial draft. Please create a compelling cover letter."
    is_approved: bool = False
    error_message: str = ""


class CoverLetterFlow(Flow[CoverLetterState]):
    """
    Flow for generating cover letters with iterative review process.
    
    This flow:
    1. Reads job description from file or URL
    2. Reads candidate documents (CV, recommendations, certificates)
    3. Generates initial cover letter draft
    4. Iteratively reviews and improves the draft
    5. Saves the final approved version
    """

    @start()
    def load_documents(self):
        """Load and parse all input documents."""
        print("\n" + "="*60)
        print("COVER LETTER GENERATOR - Starting Document Loading")
        print("="*60 + "\n")
        
        try:
            # Load job description
            print(f"📄 Loading job description from: {self.state.job_description_source}")
            self.state.job_description = read_job_description(
                self.state.job_description_source
            )
            print(f"✓ Job description loaded ({len(self.state.job_description)} characters)")
            
            # Load CV
            print(f"\n📄 Loading CV from: {self.state.cv_path}")
            self.state.cv_content = read_document(self.state.cv_path)
            print(f"✓ CV loaded ({len(self.state.cv_content)} characters)")
            
            # Load additional documents
            if self.state.document_paths:
                print(f"\n📄 Loading {len(self.state.document_paths)} additional document(s)")
                
                recommendations = []
                certificates = []
                
                for doc_path in self.state.document_paths:
                    print(f"  - Loading: {doc_path}")
                    content = read_document(doc_path)
                    
                    # Simple heuristic: if filename contains 'recommend' or 'reference', 
                    # treat as recommendation, otherwise as certificate
                    filename_lower = Path(doc_path).name.lower()
                    if 'recommend' in filename_lower or 'reference' in filename_lower:
                        recommendations.append(content)
                    else:
                        certificates.append(content)
                
                if recommendations:
                    self.state.recommendations_content = "\n\n---\n\n".join(recommendations)
                    print(f"✓ Loaded {len(recommendations)} recommendation(s)")
                
                if certificates:
                    self.state.certificates_content = "\n\n---\n\n".join(certificates)
                    print(f"✓ Loaded {len(certificates)} certificate(s)")
            
            print("\n✓ All documents loaded successfully!")
            
        except Exception as e:
            self.state.error_message = f"Error loading documents: {str(e)}"
            print(f"\n✗ Error: {self.state.error_message}")
            raise

    @listen(load_documents)
    def generate_initial_draft(self):
        """Generate the initial cover letter draft."""
        self.state.current_iteration = 1
        
        print("\n" + "="*60)
        print(f"ITERATION {self.state.current_iteration}/{self.state.max_iterations} - Generating Initial Draft")
        print("="*60 + "\n")
        
        try:
            # Prepare inputs for the crew
            inputs = {
                "job_description": self.state.job_description,
                "cv_content": self.state.cv_content,
                "recommendations_content": self.state.recommendations_content,
                "certificates_content": self.state.certificates_content,
                "reviewer_feedback": self.state.reviewer_feedback,
                "draft_content": "No previous draft.",
            }
            
            print("✍️  Writer agent is creating the cover letter...")
            
            # Create crew instance
            crew = CoverLetterCrew()
            
            # Execute only the writing task
            result = crew.crew().kickoff(inputs=inputs)
            
            # Extract only the writer's output (first task)
            if hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
                self.state.current_draft = result.tasks_output[0].raw
            else:
                self.state.current_draft = result.raw
            
            print("\n✓ Initial draft generated successfully!")
            print(f"   Draft length: {len(self.state.current_draft)} characters")
            
        except Exception as e:
            self.state.error_message = f"Error generating draft: {str(e)}"
            print(f"\n✗ Error: {self.state.error_message}")
            raise

    @listen(or_(generate_initial_draft, "improve_draft"))
    def review_draft(self):
        """Review the current draft."""
        print("\n" + "="*60)
        print(f"ITERATION {self.state.current_iteration}/{self.state.max_iterations} - Reviewing Draft")
        print("="*60 + "\n")
        
        try:
            # Prepare inputs for reviewer
            inputs = {
                "job_description": self.state.job_description,
                "cv_content": self.state.cv_content,
                "recommendations_content": self.state.recommendations_content,
                "certificates_content": self.state.certificates_content,
                "draft_content": self.state.current_draft,
                "reviewer_feedback": "",
            }
            
            print("🔍 Reviewer agent is evaluating the draft...")
            
            # Create a minimal crew with just the reviewer
            crew = CoverLetterCrew()
            result = crew.crew().kickoff(inputs=inputs)
            
            # Extract reviewer's feedback
            if hasattr(result, 'tasks_output') and len(result.tasks_output) > 1:
                review_output = result.tasks_output[1].raw
            else:
                review_output = result.raw
            
            print("\n✓ Review completed!")
            print("\n" + "-"*60)
            print("REVIEW FEEDBACK:")
            print("-"*60)
            print(review_output[:500] + "..." if len(review_output) > 500 else review_output)
            print("-"*60 + "\n")
            
            # Parse the review to check if approved
            review_upper = review_output.upper()
            if "DECISION: APPROVED" in review_upper or "DECISION:APPROVED" in review_upper:
                self.state.is_approved = True
                print("✓ Draft APPROVED by reviewer!")
            else:
                self.state.is_approved = False
                self.state.reviewer_feedback = f"Based on the review, please improve the draft:\n\n{review_output}"
                print("⚠️  Draft needs improvement. Feedback provided for next iteration.")
            
        except Exception as e:
            self.state.error_message = f"Error reviewing draft: {str(e)}"
            print(f"\n✗ Error: {self.state.error_message}")
            raise

    @router(review_draft)
    def check_continuation(self):
        """Decide whether to continue iterating or finalize."""
        print("\n" + "="*60)
        print("DECISION POINT")
        print("="*60 + "\n")
        
        if self.state.is_approved:
            print("✓ Cover letter approved! Moving to finalization.")
            return "finalize"
        elif self.state.current_iteration >= self.state.max_iterations:
            print(f"⚠️  Maximum iterations ({self.state.max_iterations}) reached.")
            print("   Proceeding with current draft as final version.")
            return "finalize"
        else:
            print(f"→ Continuing to iteration {self.state.current_iteration + 1}")
            return "improve"

    @listen("improve")
    def improve_draft(self):
        """Generate an improved draft based on feedback."""
        self.state.current_iteration += 1
        
        print("\n" + "="*60)
        print(f"ITERATION {self.state.current_iteration}/{self.state.max_iterations} - Improving Draft")
        print("="*60 + "\n")
        
        try:
            inputs = {
                "job_description": self.state.job_description,
                "cv_content": self.state.cv_content,
                "recommendations_content": self.state.recommendations_content,
                "certificates_content": self.state.certificates_content,
                "reviewer_feedback": self.state.reviewer_feedback,
                "draft_content": self.state.current_draft,
            }
            
            print("✍️  Writer agent is improving the cover letter...")
            
            crew = CoverLetterCrew()
            result = crew.crew().kickoff(inputs=inputs)
            
            # Extract writer's output
            if hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
                self.state.current_draft = result.tasks_output[0].raw
            else:
                self.state.current_draft = result.raw
            
            print("\n✓ Improved draft generated!")
            print(f"   Draft length: {len(self.state.current_draft)} characters")
            
        except Exception as e:
            self.state.error_message = f"Error improving draft: {str(e)}"
            print(f"\n✗ Error: {self.state.error_message}")
            raise

    @listen("finalize")
    def save_final_document(self):
        """Save the final cover letter to a file."""
        print("\n" + "="*60)
        print("FINALIZING COVER LETTER")
        print("="*60 + "\n")
        
        try:
            # Ensure output path has .md extension
            output_path = Path(self.state.output_path)
            if output_path.suffix.lower() != '.md':
                output_path = output_path.with_suffix('.md')
            
            # Add metadata header
            metadata = f"""---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Iterations: {self.state.current_iteration}
Status: {'Approved' if self.state.is_approved else 'Max iterations reached'}
---

"""
            
            final_content = metadata + self.state.current_draft
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            print(f"✓ Cover letter saved to: {output_path.absolute()}")
            print(f"   Total iterations: {self.state.current_iteration}")
            print(f"   Status: {'Approved by reviewer' if self.state.is_approved else 'Maximum iterations reached'}")
            print(f"   File size: {len(final_content)} characters")
            
            if not self.state.is_approved:
                print("\n⚠️  Note: This draft reached maximum iterations without final approval.")
                print("   You may want to review and edit it manually.")
            
            print("\n" + "="*60)
            print("COVER LETTER GENERATION COMPLETE!")
            print("="*60 + "\n")
            
        except Exception as e:
            self.state.error_message = f"Error saving final document: {str(e)}"
            print(f"\n✗ Error: {self.state.error_message}")
            raise


def create_cover_letter_flow(
    job_description_source: str,
    cv_path: str,
    output_path: str = "cover_letter.md",
    document_paths: Optional[List[str]] = None,
    max_iterations: int = 3,
) -> CoverLetterFlow:
    """
    Create and configure a cover letter generation flow.
    
    Args:
        job_description_source: File path or URL to job description
        cv_path: Path to CV/resume file
        output_path: Path where final cover letter will be saved
        document_paths: Optional list of paths to additional documents
        max_iterations: Maximum number of review iterations
        
    Returns:
        Configured CoverLetterFlow instance
    """
    flow = CoverLetterFlow()
    flow.state.job_description_source = job_description_source
    flow.state.cv_path = cv_path
    flow.state.output_path = output_path
    flow.state.document_paths = document_paths or []
    flow.state.max_iterations = max_iterations
    
    return flow
