from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os
from storyworld.types import Prose
# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


embedder_config = {
	"provider": OpenAIEmbeddingFunction(
		model_name=os.getenv("EMBEDDER_MODEL", "mxbai-embed-large"),
		api_base=os.getenv("EMBEDDER_API_BASE", "http://localhost:11434/v1"),
		api_key="secret",
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


@CrewBase
class Writers():
	"""Writers crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def creative_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['creative_writer'],
			verbose=True
		)
	
	@task
	def expand_events(self) -> Task:
		return Task(
			config=self.tasks_config['expand_events'],
		)
  
	@task
	def stage_writeup(self) -> Task:
		return Task(
			config=self.tasks_config['stage_writeup'],
			output_pydantic=Prose,
			context=[self.expand_events()]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Writers crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
