import mlflow
from typing import Dict


def tracking_prompt(name: str, template: str, commit_message: str | None = None,
                    version_metadata: Dict | None = None, tags: Dict | None = None):
    """
    Register a prompt with MLflow(update prompt if the name is existed).

    :param name: Name of the prompt.
    :param template: Template for the prompt.
    :param commit_message: Optional commit message for the version.
    :param version_metadata: Optional metadata for the version.(author, time, source)
    :param tags: Optional tags for the prompt.(despribe the task, language)

    """
    # Register a new prompt
    prompt = mlflow.register_prompt(
        name=name,
        template=template,
        commit_message=commit_message,
        version_metadata=version_metadata,
        tags=tags,
    )
    return prompt

