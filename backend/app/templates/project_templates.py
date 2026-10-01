"""Static project-skeleton templates for each supported language/project type.

Each template is a mapping of relative file path -> file content. The
generation service combines these skeletons with content tailored to the
user's natural language description (optionally refined by an LLM).
"""
from app.models.project import ProjectLanguage, ProjectType


def _python_fastapi(name: str, description: str) -> dict[str, str]:
    return {
        "README.md": f"# {name}\n\n{description}\n\n## Run\n\n```bash\npip install -r requirements.txt\nuvicorn main:app --reload\n```\n",
        "requirements.txt": "fastapi\nuvicorn[standard]\n",
        "main.py": (
            "from fastapi import FastAPI\n\n"
            f"app = FastAPI(title=\"{name}\")\n\n\n"
            "@app.get(\"/\")\n"
            "def read_root():\n"
            f"    return {{\"message\": \"{description}\"}}\n"
        ),
    }


def _python_django(name: str, description: str) -> dict[str, str]:
    return {
        "README.md": f"# {name}\n\n{description}\n\n## Run\n\n```bash\npip install -r requirements.txt\npython manage.py runserver\n```\n",
        "requirements.txt": "Django\n",
        "manage.py": "#!/usr/bin/env python\nimport os\nimport sys\n\nif __name__ == '__main__':\n    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')\n    from django.core.management import execute_from_command_line\n    execute_from_command_line(sys.argv)\n",
    }


def _javascript_react(name: str, description: str) -> dict[str, str]:
    return {
        "README.md": f"# {name}\n\n{description}\n\n## Run\n\n```bash\nnpm install\nnpm run dev\n```\n",
        "package.json": (
            "{\n"
            f'  "name": "{name.lower().replace(" ", "-")}",\n'
            '  "version": "0.1.0",\n'
            '  "private": true,\n'
            '  "scripts": {\n'
            '    "dev": "vite",\n'
            '    "build": "vite build"\n'
            "  },\n"
            '  "dependencies": {\n'
            '    "react": "^18.3.1",\n'
            '    "react-dom": "^18.3.1"\n'
            "  }\n"
            "}\n"
        ),
        "src/App.jsx": (
            "export default function App() {\n"
            "  return (\n"
            "    <div>\n"
            f"      <h1>{name}</h1>\n"
            f"      <p>{description}</p>\n"
            "    </div>\n"
            "  );\n"
            "}\n"
        ),
    }


def _typescript_node_express(name: str, description: str) -> dict[str, str]:
    return {
        "README.md": f"# {name}\n\n{description}\n\n## Run\n\n```bash\nnpm install\nnpm run dev\n```\n",
        "package.json": (
            "{\n"
            f'  "name": "{name.lower().replace(" ", "-")}",\n'
            '  "version": "0.1.0",\n'
            '  "scripts": {\n'
            '    "dev": "ts-node src/index.ts",\n'
            '    "build": "tsc"\n'
            "  },\n"
            '  "dependencies": {\n'
            '    "express": "^4.21.0"\n'
            "  },\n"
            '  "devDependencies": {\n'
            '    "typescript": "^5.6.0",\n'
            '    "ts-node": "^10.9.0",\n'
            '    "@types/express": "^4.17.0"\n'
            "  }\n"
            "}\n"
        ),
        "src/index.ts": (
            "import express from 'express';\n\n"
            "const app = express();\n"
            "const port = process.env.PORT || 3000;\n\n"
            "app.get('/', (_req, res) => {\n"
            f"  res.json({{ message: '{description}' }});\n"
            "});\n\n"
            "app.listen(port, () => console.log(`Server running on port ${port}`));\n"
        ),
    }


def _java_spring_boot(name: str, description: str) -> dict[str, str]:
    package = "com.example.app"
    return {
        "README.md": f"# {name}\n\n{description}\n\n## Run\n\n```bash\n./mvnw spring-boot:run\n```\n",
        "pom.xml": (
            "<project xmlns=\"http://maven.apache.org/POM/4.0.0\">\n"
            "  <modelVersion>4.0.0</modelVersion>\n"
            "  <groupId>com.example</groupId>\n"
            "  <artifactId>app</artifactId>\n"
            "  <version>0.1.0</version>\n"
            "  <parent>\n"
            "    <groupId>org.springframework.boot</groupId>\n"
            "    <artifactId>spring-boot-starter-parent</artifactId>\n"
            "    <version>3.3.0</version>\n"
            "  </parent>\n"
            "  <dependencies>\n"
            "    <dependency>\n"
            "      <groupId>org.springframework.boot</groupId>\n"
            "      <artifactId>spring-boot-starter-web</artifactId>\n"
            "    </dependency>\n"
            "  </dependencies>\n"
            "</project>\n"
        ),
        "src/main/java/com/example/app/Application.java": (
            f"package {package};\n\n"
            "import org.springframework.boot.SpringApplication;\n"
            "import org.springframework.boot.autoconfigure.SpringBootApplication;\n\n"
            "@SpringBootApplication\n"
            "public class Application {\n"
            "    public static void main(String[] args) {\n"
            "        SpringApplication.run(Application.class, args);\n"
            "    }\n"
            "}\n"
        ),
    }


def _csharp_dotnet(name: str, description: str) -> dict[str, str]:
    return {
        "README.md": f"# {name}\n\n{description}\n\n## Run\n\n```bash\ndotnet run\n```\n",
        "Program.cs": (
            "var builder = WebApplication.CreateBuilder(args);\n"
            "var app = builder.Build();\n\n"
            f"app.MapGet(\"/\", () => \"{description}\");\n\n"
            "app.Run();\n"
        ),
        f"{name.replace(' ', '')}.csproj": (
            "<Project Sdk=\"Microsoft.NET.Sdk.Web\">\n"
            "  <PropertyGroup>\n"
            "    <TargetFramework>net8.0</TargetFramework>\n"
            "    <Nullable>enable</Nullable>\n"
            "  </PropertyGroup>\n"
            "</Project>\n"
        ),
    }


def _php_laravel(name: str, description: str) -> dict[str, str]:
    return {
        "README.md": f"# {name}\n\n{description}\n\n## Run\n\n```bash\ncomposer install\nphp artisan serve\n```\n",
        "routes/web.php": (
            "<?php\n\n"
            "use Illuminate\\Support\\Facades\\Route;\n\n"
            f"Route::get('/', function () {{\n    return '{description}';\n}});\n"
        ),
        "composer.json": (
            "{\n"
            f'  "name": "example/{name.lower().replace(" ", "-")}",\n'
            '  "require": {\n'
            '    "php": "^8.2",\n'
            '    "laravel/framework": "^11.0"\n'
            "  }\n"
            "}\n"
        ),
    }


def _go_service(name: str, description: str) -> dict[str, str]:
    module = name.lower().replace(" ", "-")
    return {
        "README.md": f"# {name}\n\n{description}\n\n## Run\n\n```bash\ngo run main.go\n```\n",
        "go.mod": f"module {module}\n\ngo 1.22\n",
        "main.go": (
            "package main\n\n"
            "import (\n"
            "    \"fmt\"\n"
            "    \"net/http\"\n"
            ")\n\n"
            "func main() {\n"
            "    http.HandleFunc(\"/\", func(w http.ResponseWriter, r *http.Request) {\n"
            f"        fmt.Fprintln(w, \"{description}\")\n"
            "    })\n"
            "    http.ListenAndServe(\":8080\", nil)\n"
            "}\n"
        ),
    }


# Maps (language, project_type) -> generator function. Falls back to a
# sensible default generator per language when the exact combination isn't
# registered (e.g. an API request for a language whose template is web-only).
_TEMPLATES = {
    (ProjectLanguage.PYTHON, ProjectType.API): _python_fastapi,
    (ProjectLanguage.PYTHON, ProjectType.WEB_APP): _python_django,
    (ProjectLanguage.PYTHON, ProjectType.CLI): _python_fastapi,
    (ProjectLanguage.PYTHON, ProjectType.OTHER): _python_fastapi,
    (ProjectLanguage.JAVASCRIPT, ProjectType.WEB_APP): _javascript_react,
    (ProjectLanguage.JAVASCRIPT, ProjectType.API): _typescript_node_express,
    (ProjectLanguage.TYPESCRIPT, ProjectType.WEB_APP): _javascript_react,
    (ProjectLanguage.TYPESCRIPT, ProjectType.API): _typescript_node_express,
    (ProjectLanguage.JAVA, ProjectType.API): _java_spring_boot,
    (ProjectLanguage.JAVA, ProjectType.WEB_APP): _java_spring_boot,
    (ProjectLanguage.CSHARP, ProjectType.API): _csharp_dotnet,
    (ProjectLanguage.CSHARP, ProjectType.WEB_APP): _csharp_dotnet,
    (ProjectLanguage.PHP, ProjectType.WEB_APP): _php_laravel,
    (ProjectLanguage.PHP, ProjectType.API): _php_laravel,
    (ProjectLanguage.GO, ProjectType.API): _go_service,
    (ProjectLanguage.GO, ProjectType.CLI): _go_service,
    (ProjectLanguage.GO, ProjectType.WEB_APP): _go_service,
    (ProjectLanguage.GO, ProjectType.OTHER): _go_service,
}

_LANGUAGE_FALLBACK = {
    ProjectLanguage.PYTHON: _python_fastapi,
    ProjectLanguage.JAVASCRIPT: _javascript_react,
    ProjectLanguage.TYPESCRIPT: _javascript_react,
    ProjectLanguage.JAVA: _java_spring_boot,
    ProjectLanguage.CSHARP: _csharp_dotnet,
    ProjectLanguage.PHP: _php_laravel,
    ProjectLanguage.GO: _go_service,
}


def generate_skeleton(
    name: str, description: str, language: ProjectLanguage, project_type: ProjectType
) -> dict[str, str]:
    """Return a dict of file path -> file contents for the requested project."""
    generator = _TEMPLATES.get((language, project_type)) or _LANGUAGE_FALLBACK[language]
    return generator(name, description)
