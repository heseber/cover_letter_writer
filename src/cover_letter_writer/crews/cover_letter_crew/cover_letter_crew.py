from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, task


@CrewBase
class CoverLetterCrew:
    """Cover Letter Writing and Review Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def cover_letter_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["cover_letter_writer"],  # type: ignore[index]
        )

    @agent
    def cover_letter_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["cover_letter_reviewer"],  # type: ignore[index]
        )

    @task
    def write_cover_letter(self) -> Task:
        return Task(
            config=self.tasks_config["write_cover_letter"],  # type: ignore[index]
            agent=self.cover_letter_writer(),
        )

    @task
    def review_cover_letter(self) -> Task:
        return Task(
            config=self.tasks_config["review_cover_letter"],  # type: ignore[index]
            agent=self.cover_letter_reviewer(),
        )

    def writer_crew(self) -> Crew:
        """Creates a crew with just the writer"""
        return Crew(
            agents=[self.cover_letter_writer()],
            tasks=[self.write_cover_letter()],
            process=Process.sequential,
            verbose=True,
        )

    def reviewer_crew(self) -> Crew:
        """Creates a crew with just the reviewer"""
        return Crew(
            agents=[self.cover_letter_reviewer()],
            tasks=[self.review_cover_letter()],
            process=Process.sequential,
            verbose=True,
        )
