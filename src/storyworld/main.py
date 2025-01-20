#!/usr/bin/env python

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from storyworld.types import Character, Stage
from storyworld.crews.plot_development.plot_development import PlotDevelopment

import yaml
from pathlib import Path
characters_path = Path(__file__).parent / "characters"
stages = yaml.safe_load((Path(__file__).parent / "stages.yaml").read_text())

# load all yaml files in characters folder
characters = []
for file in characters_path.rglob("*.yaml"):
    with open(file) as f:
        characters.append(Character(**yaml.safe_load(f)))

class StoryWorldState(BaseModel):
    characters: list[Character] = characters
    stages: list[Stage] = []


class StoryFlow(Flow[StoryWorldState]):
    initial_state = StoryWorldState()

    @start()
    def start(self):
        for index, stage_name in enumerate(stages["stages"]):
            inputs = {
                "characters": "\n".join([character.description for character in self.state.characters]),
                "stage": f"{stage_name} - {index + 1} of {len(stages['stages'])}",
                "synopsis": "\n".join([stage.summary for stage in self.state.stages])
            }

            new_stage = PlotDevelopment().crew().kickoff(inputs=inputs)
            self.state.stages.append(new_stage.pydantic)

        print("Story complete!")
        print("State of the world:", self.state)
        print("\n\nStory events:")
        print("\n".join([stage.summary for stage in self.state.stages]))
        return self.state

def kickoff():
    story_flow = StoryFlow()
    story_flow.kickoff()


if __name__ == "__main__":
    kickoff()
