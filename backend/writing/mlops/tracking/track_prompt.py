import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
import mlflow
from typing import Dict
from writing.config.prompts import (
    grammar_check_prompt,
    level_analysis_prompt,
    feedback_prompt,
    writing_tool_selector_prompt,
    generate_vocabulary_prompt,
    english_vietnamese_dictionary_prompt,
    grammar_explanation_prompt,
    sentence_parsing_prompt,
    example_generator_prompt,
    conversation_simulator_prompt,
    error_correction_prompt,
    faq_knowledge_base_prompt,
    quick_tip_prompt,
    fall_to_gemini_prompt
)
from datetime import datetime
from writing.mlops.mlflow_setup import setup_mlflow



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
    with mlflow.start_run(run_name=f"prompt-{name}", nested=True):
        # Log prompt content directly as parameter
        mlflow.log_param("prompt_name", name)
        mlflow.log_param("prompt_template", template)

        # Log version metadata
        for key, value in version_metadata.items():
            mlflow.set_tag(f"meta.{key}", value)

        # Log tags
        for key, value in tags.items():
            mlflow.set_tag(key, value)

        # # Save template as artifact for clarity
        # path = f"{name}_prompt.txt"
        # with open(path, "w", encoding="utf-8") as f:
        #     f.write(template)
        # mlflow.log_artifact(path)

        return {"name": name, "status": "logged"}

def tracking_all_prompts():
    """
    Track all predefined prompts using MLflow prompt registry.
    """
    # Setup MLflow connection before tracking prompts
    setup_mlflow()
    # Dictionary mapping prompt names to templates
    prompts = {
        "grammar_check": grammar_check_prompt,
        "level_analysis": level_analysis_prompt,
        "feedback": feedback_prompt,
        "writing_tool_selector": writing_tool_selector_prompt,
        # "generate_vocabulary": generate_vocabulary_prompt,
        "english_vietnamese_dictionary": english_vietnamese_dictionary_prompt,
        "grammar_explanation": grammar_explanation_prompt,
        "sentence_parsing": sentence_parsing_prompt,
        "example_generator": example_generator_prompt,
        "conversation_simulator": conversation_simulator_prompt,
        "error_correction": error_correction_prompt,
        "faq_knowledge_base": faq_knowledge_base_prompt,
        "quick_tip": quick_tip_prompt,
        "fall_to_gemini": fall_to_gemini_prompt
    }

    # Track each prompt
    tracked_prompts = {}
    for name, template in prompts.items():
        # print(name,111111111111111111111)
        tracked_prompts[name] = tracking_prompt(
            name=name,
            template=template,
            version_metadata={
                "author": "LHH",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "source": "ai-tutor/backend/writing/config/prompts.py"
            },
            tags={
                "task": "writing_assistant",
                "language": "en"
            }
        )
    
    return tracked_prompts


if __name__ == "__main__":
    tracking_all_prompts()