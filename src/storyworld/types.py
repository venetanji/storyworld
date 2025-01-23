from pydantic import BaseModel, Field
import yaml
from pathlib import Path

# import stages.yaml
stages = yaml.safe_load((Path(__file__).parent / "stages.yaml").read_text())


class Character(BaseModel):
    name: str
    age: int
    personality: str
    appearance: str
    backstory: str

    # set description to be all the character's attributes
    @property
    def description(self):
        return f"Name: {self.name}\nAge: {self.age}\nPersonality: {self.personality}\nAppearance: {self.appearance}\nBackstory: {self.backstory}"

class StoryEvent(BaseModel):
    description: str = Field(..., description="A detailed description of the event in narrative form")
    characters: list[str]

class StoryEvents(BaseModel):
    events: list[StoryEvent]

class StageDraft(BaseModel):
    chapter_title: str = Field(..., description="A suggestive title that alludes at the events that occur in this stage")
    stage_name: str = Field(..., description="The name of the stage in the Hero's Journey framework")
    synopsis: str = Field(..., description="A synopsis of all the events that occur in this stage")
    stage_number: int = Field(..., description="The number of the stage in the Hero's Journey framework")

class Stage(BaseModel):
    chapter_title: str = Field(..., description="A suggestive title that alludes at the events that occur in this stage")
    events: list[StoryEvent]
    stage_name: str = Field(..., description="The name of the stage in the Hero's Journey framework")
    synopsis: str = Field(..., description="A synopsis of all the events that occur in this stage")
    stage_number: int = Field(..., description="The number of the stage in the Hero's Journey framework")
    
    
    @property
    def summary(self):
        events = "\n".join([f"  - {event.description}" for event in self.events])
        return f"Chapter: {self.chapter_title}\nStage: {self.stage_name}\nSynopsis: {self.synopsis}\nEvents:\n{events}\n"

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
