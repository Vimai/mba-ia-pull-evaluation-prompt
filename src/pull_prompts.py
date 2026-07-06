"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    prompt_template = hub.pull("leonanluppi/bug_to_user_story_v1")
    system_prompt = prompt_template.messages[0]
    human_promt = prompt_template.messages[1]
    return {
        "bug_to_user_story_v1": {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt.prompt.template,
            "user_prompt": human_promt.prompt.template,
            "version": "v1",
            "created_at": "2025-01-15",
            "tags": ["bug-analysis", "user-story", "product-management"]
        }
    }


def main():
    """Função principal"""
    data = pull_prompts_from_langsmith()
    save_yaml(data, "prompts/bug_to_user_story_v1.yml")


if __name__ == "__main__":
    sys.exit(main())
