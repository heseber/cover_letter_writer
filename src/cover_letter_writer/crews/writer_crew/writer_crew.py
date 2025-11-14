"""Writer crew for cover letter generation."""

from typing import Any

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class WriterCrew:
    """Crew for writing cover letters."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, llm: Any):
        """
        Initialize Writer crew.

        Args:
            llm: Language model instance
        """
        self.llm = llm

    @agent
    def cover_letter_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["cover_letter_writer"],
            llm=self.llm,
        )

    @task
    def write_cover_letter(self) -> Task:
        return Task(
            config=self.tasks_config["write_cover_letter"],
            agent=self.cover_letter_writer(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Writer Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )


