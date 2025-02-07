from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from storyworld.types import PlotDraft, Stage
from crewai.knowledge.knowledge import Knowledge
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from typing import List
import os

embedder = {
	"provider": OpenAIEmbeddingFunction(
		model_name=os.getenv("EMBEDDER_MODEL", "mxbai-embed-large"),
		api_base=os.getenv("EMBEDDER_API_BASE", "http://localhost:11434/v1"),
		api_key=os.getenv("EMBEDDER_API_KEY", "secret"),
	)
}

llm  = LLM(
	model=os.getenv("MODEL"),
	temperature=0.5,
	presence_penalty=0.3,
)

function_calling_llm  = LLM(
	model=os.getenv("MODEL"),
	temperature=0.1,
)


storytelling_knowledge_source = CrewDoclingSource(
    file_paths=[
        "https://en.wikipedia.org/wiki/Hero%27s_journey",
		"https://mythcreants.com/blog/the-eight-character-archetypes-of-the-heros-journey/",
		"https://tvtropes.org/pmwiki/pmwiki.php/Main/TheHerosJourney",
		"https://en.wikipedia.org/wiki/Worldbuilding",
    ],
)

knowledge = Knowledge(
    sources=[storytelling_knowledge_source],
	embedder=embedder,
	collection_name="storytelling"
)

@CrewBase
class PlotDevelopment():
	"""PlotDevelopment crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	
	def story_director(self) -> Agent:
		return Agent(
			config=self.agents_config['story_director'],
			verbose=True,
			knowledge=knowledge,
			llm=llm,
			function_calling_llm=function_calling_llm,
			allow_delegation=True,
		)

	@agent
	def creative_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['creative_writer'],
			verbose=True,
			llm=llm,
			function_calling_llm=function_calling_llm,
			knowledge=knowledge,

		)

	@agent
	def consistency_checker(self) -> Agent:
		return Agent(
			config=self.agents_config['consistency_checker'],
			verbose=True,
			llm=llm,
			function_calling_llm=function_calling_llm,
			knowledge=knowledge,
		)
	
	@task
	def draft_plot(self) -> Task:
		return Task(
			config=self.tasks_config['draft_plot'],
			output_pydantic=PlotDraft,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PlotDevelopment crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			verbose=True,
			memory=False,
			embedder=embedder,
			knowledge=knowledge,
			#planning=True,
			#planning_llm=llm,
			manager_agent=self.story_director(),
			function_calling_llm=function_calling_llm,
			llm=llm
		)
