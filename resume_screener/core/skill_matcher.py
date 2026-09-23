"""
Skill keyword extraction.

FIX vs original app.py:
- Original used plain `if skill in text_low`, i.e. naive substring matching.
  This is a real bug: "java" is a substring of "javascript", so ANY resume
  that only mentions JavaScript would be incorrectly credited with knowing Java
  too. Same risk applies to any short skill name that's a substring of a longer
  word. Fixed by matching on word boundaries via regex, so "java" only matches
  the standalone token "java", not "javascript".
"""

import re
from functools import lru_cache

from config import SKILL_KEYWORDS


@lru_cache(maxsize=1)
def _compiled_patterns():
    """Pre-compile one boundary-safe regex per skill, once."""
    patterns = {}
    for skill in SKILL_KEYWORDS:
        escaped = re.escape(skill.lower())
        # (?<![a-z0-9]) / (?![a-z0-9]) act as boundaries that also work for
        # tokens containing symbols like "c++", "c#", "node.js" — plain \b
        # would not, since \b only recognizes word characters.
        pattern = re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])")
        patterns[skill] = pattern
    return patterns


def extract_skills_from_text(text: str) -> set[str]:
    """Return the set of known skills (from SKILL_KEYWORDS) found in text."""
    if not text:
        return set()

    text_low = text.lower()
    found = set()
    for skill, pattern in _compiled_patterns().items():
        if pattern.search(text_low):
            found.add(skill)
    return found
