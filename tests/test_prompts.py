"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROJECT_ROOT = Path(__file__).resolve().parent.parent
caminho_completo = PROJECT_ROOT / "prompts" / "bug_to_user_story_v2.yml"

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        data = load_prompts(caminho_completo)["bug_to_user_story_v2"]
        assert "system_prompt" in data, "O YAML deve conter a chave 'system_prompt'"
        system_prompt = data["system_prompt"]
        assert isinstance(system_prompt, str), "'system_prompt' deve ser uma string"
        assert system_prompt.strip() != "", "'system_prompt' não pode estar vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        data = load_prompts(caminho_completo)["bug_to_user_story_v2"]
        system_prompt = data["system_prompt"]
        role_markers = ["Você é um", "Você é uma", "You are a", "You are an"]
        assert any(marker in system_prompt for marker in role_markers), (
            "O prompt deve definir explicitamente uma persona/papel "
            "(ex: 'Você é um Product Owner')"
        )

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        data = load_prompts(caminho_completo)["bug_to_user_story_v2"]
        system_prompt = data["system_prompt"]
        format_markers = [
            "Como um",
            "para que",
            "Critérios de Aceitação",
            "User Story",
            "Markdown",
        ]
        assert any(marker in system_prompt for marker in format_markers), (
            "O prompt deve exigir um formato de saída definido "
            "(ex: estrutura de User Story ou Critérios de Aceitação)"
        )

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        data = load_prompts(caminho_completo)["bug_to_user_story_v2"]
        system_prompt = data["system_prompt"]

        # Conta quantos exemplos completos (Relato -> saída) existem
        num_relatos = system_prompt.count("Relato:")
        assert num_relatos >= 2, (
            f"Esperado pelo menos 2 exemplos few-shot (encontrados: {num_relatos}). "
            "Cada exemplo deve conter um 'Relato:' seguido da saída esperada."
        )

        # Confere se existe algum marcador explícito de seção de exemplos
        example_section_markers = ["EXEMPLO", "EX SIMPLES", "EX MÉDIO", "EX COMPLEXO"]
        assert any(marker in system_prompt for marker in example_section_markers), (
            "O prompt deve sinalizar claramente a seção de exemplos (few-shot)"
        )

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        data = load_prompts(caminho_completo)["bug_to_user_story_v2"]
        full_text = yaml.dump(data, allow_unicode=True)

        todo_markers = ["[TODO]", "TODO:", "<TODO>", "TBD", "FIXME"]
        for marker in todo_markers:
            assert marker not in full_text, (
                f"Encontrado placeholder não resolvido '{marker}' no prompt"
            )

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        data = load_prompts(caminho_completo)["bug_to_user_story_v2"]

        # O arquivo usa 'tags' como metadado de técnicas/categorias
        techniques = data.get("techniques") or data.get("tags") or []

        assert isinstance(techniques, list), (
            "As técnicas/tags devem estar listadas como uma lista no YAML"
        )
        assert len(techniques) >= 2, (
            f"Esperado pelo menos 2 técnicas/tags listadas nos metadados "
            f"(encontradas: {len(techniques)})"
        )

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])