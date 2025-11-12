from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI


@CrewBase
class CoverLetterCrew:
    """Cover Letter Writing and Review Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model="gpt-4o")

    @agent
    def cover_letter_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["cover_letter_writer"],
            llm=self.llm,
        )

    @agent
    def cover_letter_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["cover_letter_reviewer"],
            llm=self.llm,
        )

    @task
    def write_cover_letter(self) -> Task:
        return Task(
            config=self.tasks_config["write_cover_letter"],
            agent=self.cover_letter_writer(),
        )

    @task
    def review_cover_letter(self) -> Task:
        return Task(
            config=self.tasks_config["review_cover_letter"],
            agent=self.cover_letter_reviewer(),
        )

    @crew
    def write_crew(self) -> Crew:
        """Creates a crew with only the writer task"""
        return Crew(
            agents=[self.cover_letter_writer()],
            tasks=[self.write_cover_letter()],
            process=Process.sequential,
            verbose=False,
        )

    @crew
    def review_crew(self) -> Crew:
        """Creates a crew with only the reviewer task"""
        return Crew(
            agents=[self.cover_letter_reviewer()],
            tasks=[self.review_cover_letter()],
            process=Process.sequential,
            verbose=False,
        )
