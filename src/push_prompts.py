"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from utils import load_yaml, check_env_vars, print_section_header
from pydantic import BaseModel, ConfigDict, ValidationError, Field

load_dotenv()

PROMPT_NAME = f"{os.getenv('USERNAME_LANGSMITH_HUB' )}/bug_to_user_story_v2"

class PromptData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str | None = None
    system_prompt: str = Field(..., min_length=1)
    user_prompt: str = Field(..., min_length=1)
    tags: list[str] | None = None
    created_at: str | None = None
    version: str



def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    system_template = SystemMessagePromptTemplate.from_template(prompt_data["system_prompt"])
    human_template = HumanMessagePromptTemplate.from_template(prompt_data["user_prompt"])

    prompt = ChatPromptTemplate.from_messages([
        system_template,
        human_template
    ])

    url = hub.push(
        prompt_name,
        prompt,
        new_repo_is_public=True,
        tags=prompt_data.get("tags", [])
    )
    print(f"URL: {url}")
    return True


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    try:
        PromptData.model_validate(prompt_data)
        return True, []

    except ValidationError as exc:
        errors = [
            f"{'.'.join(map(str, error['loc']))}: {error['msg']}"
            for error in exc.errors()
        ]
        print(errors)
        return False, errors


def main() -> int:
    """Função principal"""
    prompt_data = load_yaml("prompts/bug_to_user_story_v2.yml")
    data = prompt_data["bug_to_user_story_v2"]
    is_valid, _ = validate_prompt(data)

    if not is_valid:
        return 1
    success = push_prompt_to_langsmith(PROMPT_NAME, data)
    if not success:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
