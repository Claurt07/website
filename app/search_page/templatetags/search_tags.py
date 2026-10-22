import html
import re

from django import template
from django.utils.html import escape
from django.utils.safestring import SafeData, mark_safe

register = template.Library()


@register.filter
def highlight(text, keyword):
    """
    Wrap each word of the search keyword found in `text` in <mark class="hot-search-highlight">.
    Case-insensitive. Use on plain text only (titles, descriptions, or rich text after |striptags).
    Usage: {{ result.title|highlight:keyword }}
    """
    text = "" if text is None else text
    if isinstance(text, SafeData):
        # Already-escaped text (e.g. richtext|striptags): decode entities like &amp; first,
        # so they aren't escaped twice or broken by a match inside them.
        text = html.unescape(str(text))
    text = str(text)

    words = [w for w in str(keyword or "").split() if len(w) >= 2]
    if not words:
        return text  # Django escapes this normally

    # Longest words first, so "mapping" wins over "map" when both are searched
    pattern = re.compile(
        "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True)),
        re.IGNORECASE,
    )

    parts, last = [], 0
    for match in pattern.finditer(text):
        parts.append(escape(text[last:match.start()]))
        parts.append(f'<mark class="hot-search-highlight">{escape(match.group(0))}</mark>')
        last = match.end()
    parts.append(escape(text[last:]))
    return mark_safe("".join(parts))