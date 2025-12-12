#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    # --- Автоматическое создание .env, static, media, templates ---
    base_dir = Path(__file__).resolve().parent

    env_path = base_dir / ".env"
    if not env_path.exists():
        env_content = """SECRET_KEY=django-template-secret-key
DEBUG=True
DB_NAME=template_db
DB_USER=postgres
DB_PASSWORD=1234
DB_HOST=127.0.0.1
DB_PORT=5432
REDIS_URL=redis://127.0.0.1:6379/1
"""
        env_path.write_text(env_content, encoding="utf-8")
        print("⚙️  Файл .env создан автоматически.")

    # создаём базовые папки
    for folder in ["static", "media", "templates"]:
        path = base_dir / folder
        path.mkdir(exist_ok=True)
        # добавляем .gitkeep чтобы папка сохранялась в git
        (path / ".gitkeep").write_text("", encoding="utf-8")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
