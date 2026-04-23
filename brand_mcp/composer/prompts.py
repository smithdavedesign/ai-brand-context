"""LLM system prompt builder.

Composes a brand-aware system prompt from ``brand/*.md`` that can be injected
into any LLM conversation to ensure brand-compliant output. The prompt is
scoped by platform so the model receives only the rules relevant to that
output surface.
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

from ..config import config

_PREAMBLE = """\
You are an AI assistant working on behalf of Solidigm™. All output you \
produce must comply with the Solidigm brand guidelines summarized below. \
When guidelines conflict with a user request, follow the brand guidelines \
and explain why the request cannot be fulfilled as-is.
"""

_VOICE_SECTION = """\
## Brand Voice
Write in a tone that is optimistic, analytical, passionate, genuine, and \
ambitious. Avoid being robotic, arrogant, confrontational, or trivial. \
Be concise and data-informed.
"""

# Files whose full content is always included in the system prompt
_ALWAYS_INCLUDE = ["do-nots.md", "generative-ai.md", "name-and-trademark.md"]

# Files whose content is included for design/UI tasks
_DESIGN_INCLUDE = ["color.md", "typography.md", "iconography.md"]


def _read(filename: str) -> str:
    path = os.path.join(config.brand_dir, filename)
    if not os.path.isfile(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_system_prompt(
    *,
    platform: Optional[str] = None,
    include_design_rules: bool = True,
) -> Dict[str, Any]:
    """Build a brand-aware LLM system prompt.

    Parameters
    ----------
    platform : str, optional
        Platform key (``"marketing"``, ``"web-nextjs"``, ``"web-react"``).
        Appends platform-specific constraints.
    include_design_rules : bool
        Whether to include color/typography/icon rules. Default True.

    Returns
    -------
    dict with ``status``, ``prompt`` (the assembled text), and ``sections``
    (list of section names included).
    """
    parts = [_PREAMBLE, _VOICE_SECTION]
    section_names = ["preamble", "voice"]

    # Always-included sections
    for fn in _ALWAYS_INCLUDE:
        content = _read(fn)
        if content:
            parts.append(content)
            section_names.append(fn.replace(".md", ""))

    # Design rules (optional but on by default)
    if include_design_rules:
        for fn in _DESIGN_INCLUDE:
            content = _read(fn)
            if content:
                parts.append(content)
                section_names.append(fn.replace(".md", ""))

    # Platform overrides
    platform_map = {
        "marketing": "platforms/marketing.md",
        "web-nextjs": "platforms/web-nextjs.md",
        "nextjs": "platforms/web-nextjs.md",
        "web-react": "platforms/web-react.md",
        "react": "platforms/web-react.md",
    }
    if platform:
        key = platform.lower().strip()
        if key in platform_map:
            content = _read(platform_map[key])
            if content:
                parts.append(f"\n## Platform-Specific Rules ({key})\n\n{content}")
                section_names.append(f"platform/{key}")

    prompt = "\n\n---\n\n".join(parts)

    return {
        "status": "ok",
        "platform": platform,
        "sections": section_names,
        "token_estimate": len(prompt) // 4,  # rough GPT-4 token estimate
        "prompt": prompt,
    }
