from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import mwparserfromhell
from mwparserfromhell.wikicode import Wikicode

_POS_TEMPLATE_NAMES = frozenset({"اسم", "فعل", "صفة", "ظرف", "حرف", "ضمير", "جملة"})


@dataclass(slots=True)
class ParsedSense:
    meaning: str
    examples: list[str] = field(default_factory=list)


class WiktionaryParser:
    """Parse Wiktionary wikitext."""

    def extract_wikitext(self, data: dict[str, Any]) -> str:
        return str(
            data.get("parse", {})
            .get("wikitext", {})
            .get("*", "")
        )

    def parse(self, text: str) -> Wikicode:
        return mwparserfromhell.parse(text)

    def find_arabic_section(self, code: Wikicode) -> Wikicode | None:
        for section in code.get_sections(levels=[2], include_lead=False):
            headings = section.filter_headings()

            if not headings:
                continue

            title = headings[0].title

            if str(title).strip() == "العربية":
                return section

            for template in title.filter_templates():
                if str(template.name).strip() == "اللغة":
                    params = list(template.params)
                    if params and str(params[0].value).strip() == "عربية":
                        return section

        return None

    def extract_root(self, section: Wikicode) -> str | None:
        # Modern format: ===الجذر=== with {{ك ت ب}}
        for subsection in section.get_sections(levels=[3], include_lead=False):
            headings = subsection.filter_headings()
            if headings and str(headings[0].title).strip() == "الجذر":
                for template in subsection.filter_templates():
                    name = str(template.name).strip()
                    parts = name.split()
                    if len(parts) >= 2 and all(len(p) == 1 for p in parts):
                        return "".join(parts)

        # Legacy format: {{جذر|ك|ت|ب}}
        for template in section.filter_templates():
            if str(template.name).strip() == "جذر":
                letters = [
                    str(p.value).strip()
                    for p in template.params
                    if str(p.name).strip().isdigit()
                ]
                root = "".join(letters)
                return root if root else None

        return None

    def is_disambiguation_page(self, code: Wikicode) -> bool:
        for template in code.filter_templates():
            if str(template.name).strip() == "توضيح":
                return True
        return False

    _NAMESPACE_PREFIXES = frozenset({"تصنيف", "ملف", "صورة", "وب", "مستخدم"})

    def extract_disambiguation_links(self, code: Wikicode) -> list[str]:
        seen: set[str] = set()
        links: list[str] = []
        for wikilink in code.filter_wikilinks():
            target = str(wikilink.title).strip()
            if not target:
                continue
            prefix = target.split(":")[0]
            if prefix in self._NAMESPACE_PREFIXES:
                continue
            if target not in seen:
                seen.add(target)
                links.append(target)
        return links

    def find_meanings_section(self, section: Wikicode) -> Wikicode | None:
        for subsection in section.get_sections(levels=[3], include_lead=False):
            headings = subsection.filter_headings()
            if headings and str(headings[0].title).strip() == "المعاني":
                return subsection
        return None

    def extract_inline_word_type(self, section: Wikicode) -> str | None:
        for line in str(section).splitlines():
            line = line.strip()
            if line.startswith("#"):
                break
            for template in mwparserfromhell.parse(line).filter_templates():
                name = str(template.name).strip()
                if name in _POS_TEMPLATE_NAMES:
                    return name
        return None

    def extract_plural_from_preamble(self, section: Wikicode) -> str | None:
        marker = "الجمع"
        for line in str(section).splitlines():
            line = line.strip()
            if line.startswith("#"):
                break
            stripped = mwparserfromhell.parse(line).strip_code().strip()
            if marker not in stripped:
                continue
            after = stripped.split(marker, 1)[1].strip()
            tokens = after.split()
            if tokens:
                return tokens[0].rstrip(".,،;:")
        return None

    def extract_pos_sections(self, section: Wikicode) -> list[Wikicode]:
        return section.get_sections(
            levels=[3],
            include_lead=False,
        )

    def extract_part_of_speech(self, section: Wikicode) -> str:
        headings = section.filter_headings()
        if not headings:
            return ""
        return str(headings[0].title).strip()

    def extract_plural(self, section: Wikicode) -> str | None:
        for template in section.filter_templates():
            if str(template.name).strip() == "ج":
                params = [
                    p for p in template.params if str(p.name).strip().isdigit()
                ]
                if params:
                    value = str(params[0].value).strip()
                    return value if value else None
        return None

    def _extract_bullet_list(self, section: Wikicode, heading: str) -> list[str]:
        for subsection in section.get_sections(levels=[4], include_lead=False):
            headings = subsection.filter_headings()
            if headings and str(headings[0].title).strip() == heading:
                items = []
                for line in str(subsection).splitlines():
                    line = line.strip()
                    if line.startswith("* "):
                        text = mwparserfromhell.parse(line[2:]).strip_code().strip()
                        if text:
                            items.append(text)
                return items
        return []

    def extract_synonyms(self, section: Wikicode) -> list[str]:
        return self._extract_bullet_list(section, "مرادفات")

    def extract_antonyms(self, section: Wikicode) -> list[str]:
        return self._extract_bullet_list(section, "أضداد")

    def extract_senses(self, section: Wikicode) -> list[ParsedSense]:
        senses: list[ParsedSense] = []

        for line in str(section).splitlines():
            line = line.strip()
            if line.startswith("# "):
                text = mwparserfromhell.parse(line[2:]).strip_code().strip()
                if text:
                    senses.append(ParsedSense(meaning=text))
            elif line.startswith("#: ") and senses:
                example = mwparserfromhell.parse(line[3:]).strip_code().strip()
                if example:
                    senses[-1].examples.append(example)

        return senses
