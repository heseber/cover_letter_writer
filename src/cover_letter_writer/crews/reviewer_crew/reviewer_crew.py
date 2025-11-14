"""Reviewer crew for cover letter review."""

from typing import Any

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class ReviewerCrew:
    """Crew for reviewing cover letters and providing feedback."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, llm: Any):
        """
        Initialize Reviewer crew.

        Args:
            llm: Language model instance
        """
        self.llm = llm

    @agent
    def cover_letter_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["cover_letter_reviewer"],
            llm=self.llm,
        )

    @task
    def review_cover_letter(self) -> Task:
        return Task(
            config=self.tasks_config["review_cover_letter"],
            agent=self.cover_letter_reviewer(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Reviewer Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )
