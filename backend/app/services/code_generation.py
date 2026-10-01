"""Code generation service: orchestrates template generation and optional LLM refinement."""
import logging

from app.core.config import settings
from app.models.project import ProjectLanguage, ProjectType
from app.templates import generate_skeleton

logger = logging.getLogger(__name__)


class CodeGenerationService:
    """Generates project file skeletons from a natural language description.

    When ``LLM_PROVIDER`` is configured as ``openai`` and an API key is
    present, the service can be extended to ask the LLM to refine generated
    files. By default it runs in ``mock`` mode which deterministically
    builds projects from static templates - this keeps the app fully
    functional and testable without requiring external API access.
    """

    def __init__(self, provider: str | None = None):
        self.provider = provider or settings.LLM_PROVIDER

    def generate_project(
        self,
        name: str,
        description: str,
        language: ProjectLanguage,
        project_type: ProjectType,
    ) -> dict[str, str]:
        files = generate_skeleton(name, description, language, project_type)

        if self.provider == "openai" and settings.OPENAI_API_KEY:
            try:
                files = self._refine_with_openai(files, description)
            except Exception:  # pragma: no cover - network/third-party failure
                logger.exception("OpenAI refinement failed, falling back to template output")

        return files

    def _refine_with_openai(self, files: dict[str, str], description: str) -> dict[str, str]:
        """Optionally enrich the generated README with LLM-produced context.

        Kept intentionally small/isolated so it can be mocked in tests and so
        failures never block project generation.
        """
        from openai import OpenAI

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You write concise, helpful project overviews for generated codebases.",
                },
                {"role": "user", "content": description},
            ],
            max_tokens=300,
        )
        summary = response.choices[0].message.content or ""
        if "README.md" in files and summary:
            files["README.md"] += f"\n## AI-Generated Overview\n\n{summary}\n"
        return files


code_generation_service = CodeGenerationService()
