from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from storyworld.types import Character, StoryEvent, Stage
from crewai.knowledge.knowledge import Knowledge
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from langchain_ollama import ChatOllama
from typing import List
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# import litellm
# litellm.set_verbose = True

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

embedder_config = {
	"provider": OpenAIEmbeddingFunction(
		model_name="mxbai-embed-large",
		api_base="http://localhost:11434/v1",
		api_key="secret",
	)
}

storytelling_knowledge_source = CrewDoclingSource(
    file_paths=[
        "https://en.wikipedia.org/wiki/Hero%27s_journey",
		"https://mythcreants.com/blog/the-eight-character-archetypes-of-the-heros-journey/",
    ],
)

knowledge = Knowledge(
    sources=[storytelling_knowledge_source],
	embedder_config=embedder_config,
	collection_name="storytelling"
)

llm  = LLM(
	model="ollama/llama3.1-8k",
	base_url="http://thor:11434",
	temperature=0.6,
	presence_penalty=0.2,
	n_ctx=8192,
	max_completion_tokens=8192
)

function_calling_llm = LLM(
	model="ollama/llama3.1-8k",
	base_url="http://thor:11434",
	temperature=0.2,
	num_ctx=8192,
	max_completion_tokens=8192
)
# llm = ChatOllama(
# 	model="llama3.1-16k",
# 	base_url="http://thor:11434",
# 	temperature=0.6,
# 	num_ctx=16384, # 16384 is the maximum context length for the model
# )


@CrewBase
class PlotDevelopment():
	"""PlotDevelopment crew"""

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
			verbose=True,
			knowledge=knowledge,
			allow_delegation=True,

			llm=llm
		)

	@agent
	def consistency_checker(self) -> Agent:
		return Agent(
			config=self.agents_config['consistency_checker'],
			verbose=True,
			knowledge=knowledge,
			llm=llm
		)
	
	# def director(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['director'],
	# 		verbose=True,
	# 		knowledge=knowledge,
	# 		allow_delegation=True,
	# 		llm=llm
	# 	)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	# @task
	# def create_character(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['create_character'],
	# 		output_pydantic=Character,
	# 		knowledge=knowledge
	# 	)

	@task
	def develop_environment(self) -> Task:
		return Task(
			config=self.tasks_config['develop_environment'],
			output_pydantic=StoryEvent,
			knowledge=knowledge,
			agent=self.creative_writer()
		)
	
	@task
	def develop_character(self) -> Task:
		return Task(
			config=self.tasks_config['develop_character'],
			output_pydantic=StoryEvent,		
			agent=self.creative_writer()

		)

	@task
	def consistency_check(self) -> Task:
		return Task(
			config=self.tasks_config['consistency_check'],
			agent=self.consistency_checker(),
			#context=[self.develop_environment(), self.develop_character()]
		)
	
	@task
	def stage_writeup(self) -> Task:
		return Task(
			config=self.tasks_config['stage_writeup'],
			output_pydantic=Stage,
			agent=self.creative_writer(),
			context=[self.develop_environment(), self.develop_character(), self.consistency_check()]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PlotDevelopment crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			#process=Process.sequential,
			verbose=True,
			memory=True,
			embedder=embedder_config,
			knowledge=knowledge,
			function_calling_llm=function_calling_llm,
			#manager_agent=self.director(),
			llm=llm,
			#manager_llm=llm,
			#process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
