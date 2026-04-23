"""Brand context assembler.

Reads topic-specific markdown files from ``brand/`` and optional platform
overrides from ``brand/platforms/`` to build a scoped brand context document
that an LLM can use for a given task.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from ..config import config

# Topic files inside brand/ — order matters (general → specific)
_TOPIC_FILES: List[str] = [
    "brand.md",
    "name-and-trademark.md",
    "logo.md",
    "color.md",
    "typography.md",
    "graphic-elements.md",
    "iconography.md",
    "photography.md",
    "generative-ai.md",
    "charts-and-data.md",
    "do-nots.md",
]

# Task → relevant topic files (subset of _TOPIC_FILES)
_TASK_TOPICS: Dict[str, List[str]] = {
    "ui": ["brand.md", "color.md", "typography.md", "iconography.md", "graphic-elements.md", "do-nots.md"],
    "copy": ["brand.md", "name-and-trademark.md", "do-nots.md"],
    "design": ["brand.md", "color.md", "typography.md", "graphic-elements.md", "photography.md", "iconography.md", "do-nots.md"],
    "review": ["do-nots.md", "generative-ai.md", "name-and-trademark.md", "color.md", "typography.md", "logo.md"],
    "chart": ["brand.md", "color.md", "charts-and-data.md", "do-nots.md"],
}

# Known platform override files
_PLATFORM_FILES: Dict[str, str] = {
    "marketing": "platforms/marketing.md",
    "web-nextjs": "platforms/web-nextjs.md",
    "nextjs": "platforms/web-nextjs.md",
    "web-react": "platforms/web-react.md",
    "react": "platforms/web-react.md",
}


def _read_brand_file(filename: str) -> Optional[str]:
    path = os.path.join(config.brand_dir, filename)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def available_topics() -> List[str]:
    """Return the list of topic files that actually exist on disk."""
    return [t for t in _TOPIC_FILES if os.path.isfile(os.path.join(config.brand_dir, t))]


def available_platforms() -> List[str]:
    """Return the list of platform override keys that have files on disk."""
    return [
        key for key, path in _PLATFORM_FILES.items()
        if os.path.isfile(os.path.join(config.brand_dir, path))
    ]


def assemble(
    *,
    platform: Optional[str] = None,
    task: Optional[str] = None,
) -> Dict[str, Any]:
    """Assemble a brand context document.

    Parameters
    ----------
    platform : str, optional
        Platform key (e.g. ``"web-nextjs"``, ``"marketing"``).
        Appends platform-specific overrides to the context.
    task : str, optional
        Task key (e.g. ``"ui"``, ``"copy"``, ``"design"``).
        Narrows the topic files to only those relevant to the task.

    Returns
    -------
    dict with ``status``, ``sections`` (list of {topic, content}),
    and ``platform_override`` (str or None).
    """
    # Determine which topic files to include
    if task and task.lower() in _TASK_TOPICS:
        filenames = _TASK_TOPICS[task.lower()]
    else:
        filenames = _TOPIC_FILES

    sections: List[Dict[str, str]] = []
    for fn in filenames:
        content = _read_brand_file(fn)
        if content:
            sections.append({"topic": fn.replace(".md", ""), "content": content})

    # Platform override
    platform_content: Optional[str] = None
    platform_key: Optional[str] = None
    if platform:
        key = platform.lower().strip()
        if key in _PLATFORM_FILES:
            platform_key = key
            platform_content = _read_brand_file(_PLATFORM_FILES[key])

    return {
        "status": "ok",
        "task": task,
        "platform": platform_key,
        "section_count": len(sections),
        "sections": sections,
        "platform_override": platform_content,
    }
