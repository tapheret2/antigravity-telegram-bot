"""Shell execution and file operations — lets the bot DO work on the local machine."""

import logging
import subprocess
import os

logger = logging.getLogger(__name__)

# Project root (where the bot runs from)
PROJECT_ROOT = os.getcwd()


def run_shell(command: str, cwd: str | None = None, timeout: int = 30) -> str:
    """Execute a shell command and return output.

    Args:
        command: Shell command to run.
        cwd: Working directory. Defaults to PROJECT_ROOT.
        timeout: Max seconds to wait.

    Returns:
        Combined stdout + stderr output, or error message.
    """
    work_dir = cwd or PROJECT_ROOT

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout + result.stderr
        status = "✅" if result.returncode == 0 else f"❌ (exit {result.returncode})"
        return f"{status}\n```\n{output.strip()[:3000]}\n```"

    except subprocess.TimeoutExpired:
        return "⏰ Command timed out."
    except Exception as e:
        logger.error("Shell exec error: %s", e)
        return f"⚠️ Error: {e}"


def write_file(filepath: str, content: str) -> str:
    """Write content to a file, creating dirs if needed.

    Args:
        filepath: Path relative to PROJECT_ROOT or absolute.
        content: File content to write.

    Returns:
        Success/error message.
    """
    try:
        # If relative path, resolve from project root
        if not os.path.isabs(filepath):
            filepath = os.path.join(PROJECT_ROOT, filepath)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return f"✅ File created: `{filepath}`"

    except Exception as e:
        logger.error("File write error: %s", e)
        return f"⚠️ Error: {e}"


def read_file(filepath: str) -> str:
    """Read a file and return its contents.

    Args:
        filepath: Path relative to PROJECT_ROOT or absolute.

    Returns:
        File content or error message.
    """
    try:
        if not os.path.isabs(filepath):
            filepath = os.path.join(PROJECT_ROOT, filepath)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if len(content) > 3000:
            content = content[:3000] + "\n... (truncated)"

        return f"📄 `{os.path.basename(filepath)}`\n```\n{content}\n```"

    except FileNotFoundError:
        return f"⚠️ File not found: `{filepath}`"
    except Exception as e:
        return f"⚠️ Error: {e}"


def list_project_files(path: str = ".") -> str:
    """List files in a directory.

    Args:
        path: Directory path relative to PROJECT_ROOT.

    Returns:
        Formatted file listing.
    """
    try:
        full_path = os.path.join(PROJECT_ROOT, path)
        entries = []
        for entry in sorted(os.listdir(full_path)):
            if entry.startswith(".") and entry not in (".env.example",):
                continue
            full = os.path.join(full_path, entry)
            prefix = "📁" if os.path.isdir(full) else "📄"
            entries.append(f"  {prefix} {entry}")

        return f"📂 `{path}`\n" + "\n".join(entries)

    except Exception as e:
        return f"⚠️ Error: {e}"
