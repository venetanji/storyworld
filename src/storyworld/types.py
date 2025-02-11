from pydantic import BaseModel, Field
import yaml
from pathlib import Path

# import stages.yaml
stages = yaml.safe_load((Path(__file__).parent / "stages.yaml").read_text())

class Location(BaseModel):
    name: str
    description: str

class Character(BaseModel):
    name: str
    age: int
    personality: str
    appearance: str
    backstory: str

    # set description to be all the character's attributes
    @property
    def description(self):
        return f"Name: {self.name}\nAge: {self.age}\nPersonality: {self.personality.strip()}\nAppearance: {self.appearance.strip()}\nBackstory: {self.backstory.strip()}\n"

class StoryEvent(BaseModel):
    description: str = Field(..., description="A detailed description of the event in narrative form")
    characters: list[str]

class Chapter(BaseModel):
    title: str = Field(..., description="A title that alludes at the events that occur in this stage")
    events: list[StoryEvent]
    synopsis: str = Field(..., description="A synopsis of all the events that occur in this stage. 500 words minimum")

    @property
    def summary(self):
        return f"Chapter: {self.chapter_title}\nSynopsis: {self.synopsis}\nEvents:\n{self.event_list}\n"
    
    @property
    def event_list(self):      
        return "\n".join([f"  - {event.description}" for event in self.events])

class PlotDraft(BaseModel):
    chapters: list[Chapter]
    
    @property
    def summary(self):
        return "\n".join([chapter.event_list for chapter in self.chapters])

class PlotCharacter(BaseModel):
    name: str
    role: str
    description: str

class Prose(BaseModel):
    characters: list[PlotCharacter] = Field(..., description="A list of characters in the scene")
    chapter_title: str = Field(..., description="The title of the chapter")
    prose_markdown: str = Field(..., description="The prose in markdown format. Minimum 1000 words.")
