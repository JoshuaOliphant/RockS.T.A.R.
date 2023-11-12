# RockS.T.A.R.

RockS.T.A.R. is an interactive AI chat application for S.T.A.R. (Situation, Task, Action, Result) interviews. Tell RockS.T.A.R. what kind role you are interviewing for and it will ask you relevant question and offer feedback on your answers.

This application uses:

- Python and Flask on the backend.
- The [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview)
- [HTMX](https://htmx.org/) and [LangUI](https://www.langui.dev/)/Tailspin on the frontend.

## Installation

I used Python 3.10 when writing this application and Poetry for dependency management.

- `poetry install`
- `flask run`
- Go to 127.0.0.1:500/ask_star

## Future Work

- [ ] Save threads so they can be reloaded
- [ ] Add side-panel with thread history

## License

[MIT License](LICENSE)
