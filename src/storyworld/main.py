#!/usr/bin/env python

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from storyworld.types import Character, PlotDraft
from storyworld.crews.plot_development.plot_development import PlotDevelopment
from storyworld.crews.writers.writers import Writers
import os

import yaml
from pathlib import Path
import random
characters_path = Path(os.getenv("STORYWORLD_PATH"))/ "characters"
stages = yaml.safe_load((Path(__file__).parent / "stages.yaml").read_text())

# load all yaml files in characters folder
characters = []
for file in characters_path.rglob("*.yaml"):
    with open(file) as f:
        print("loading character", file)
        characters.append(Character(**yaml.safe_load(f)))

class StoryWorldState(BaseModel):
    characters: list[Character] = []
    plot_draft: PlotDraft = PlotDraft(chapters=[])


class StoryFlow(Flow[StoryWorldState]):



    @start()
    def start(self):
        
        # shuffle characters and select 10
        self.state.characters = random.sample(characters, 2)
        
        inputs = {
            "characters": "\n".join([character.description for character in self.state.characters]),
            "stages": "\n".join(stages["stages"]),
        }

        plot_draft = PlotDevelopment().crew().kickoff(inputs=inputs)
        self.state.plot_draft = plot_draft.pydantic

    @listen('start')
    def develop_stages(self):
        stages_inputs = [{
            "characters": "\n".join([character.description for character in self.state.characters]),
            "stages": "\n".join(stages["stages"]),
            "stage_events": "\n".join([event.description for event in chapter.events]),
            "plot": self.state.plot_draft.summary,
        } for chapter in self.state.plot_draft.chapters]
        chapters = Writers().crew().kickoff_for_each(inputs=stages_inputs)
        
        for chapter in chapters:
            # save chapter to a file in "stages" folder
            with open(f"stages/{chapter.pydantic.chapter_title}.md", "w", encoding='utf8')  as f:
                f.write(chapter.pydantic.prose_markdown)
        
def kickoff():
    story_flow = StoryFlow()
    story_flow.kickoff()


if __name__ == "__main__":
    kickoff()
