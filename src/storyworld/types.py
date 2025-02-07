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


class Stage(BaseModel):
    chapter_title: str = Field(..., description="A suggestive title that alludes at the events that occur in this stage")
    events: list[StoryEvent]
    stage_name: str = Field(..., description="The name of the stage in the Hero's Journey framework")
    synopsis: str = Field(..., description="A synopsis of all the events that occur in this stage")
    narrative_prose: str = Field(..., description="The narrative prose for this stage. Minimum 1000 words.")
    stage_number: int = Field(..., description="The number of the stage in the Hero's Journey framework")

    @property
    def summary(self):
        return f"Chapter: {self.chapter_title}\nStage: {self.stage_name}\nNarrative Prose: {self.narrative_prose}\nEvents:\n{self.events}\n"
    
    @property
    def event_list(self):      
        return "\n".join([f"  - {event.description}" for event in self.events])

class PlotDraft(BaseModel):
    stages: list[Stage]
    
    @property
    def summary(self):
        return "\n".join([stage.event_list for stage in self.stages])

class Prose(BaseModel):
    characters: list[str] = Field(..., description="A list of characters in the scene")
    chapter_title: str = Field(..., description="The title of the chapter")
    prose_markdown: str = Field(..., description="The prose in markdown format. Minimum 1000 words.")
    
    
class Inconsistency(BaseModel):
    problem: str
    suggestion: str
    severity: str

class ConsistencyCheck(BaseModel):
    issues: list[Inconsistency]
    events: list[StoryEvent]

class Plot(BaseModel):
    stages: list[Stage]
    characters: list[Character]
