# Storyworld generator

This flow generates a story using crewai.

Flow kickoff can be found here `src/storyworld/main.py`.



## Environment Setup

Refer to `.env_example` for environment variables.
Make a COPY of `.env_example` and rename it to `.env`.
Do not commit `.env` to git.

## Customizing

### Characters

Edit characters in `src/storyworld/characters/` as yaml files.

### Crew

The crew folder is: `src/storyworld/crews/plot_development`

Main crew is defined in `plot_development.py`.

Agents and Tasks are defined in `config/agents.yaml` and `config/tasks.yaml`.


## Running the Project

To start the flow run this from the root folder of your project:

```bash
crewai flow kickoff
```

