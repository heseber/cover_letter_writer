"""Translator crew for cover letter translation."""

from typing import Any

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class TranslatorCrew:
    """Crew for translating cover letters to different languages."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, llm: Any):
        """
        Initialize Translator crew.

        Args:
            llm: Language model instance
        """
        self.llm = llm

    @agent
    def cover_letter_translator(self) -> Agent:
        return Agent(
            config=self.agents_config["cover_letter_translator"],
            llm=self.llm,
        )

    @task
    def translate_cover_letter(self) -> Task:
        return Task(
            config=self.tasks_config["translate_cover_letter"],
            agent=self.cover_letter_translator(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Translator Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )

