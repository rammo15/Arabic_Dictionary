from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import mwparserfromhell
from mwparserfromhell.wikicode import Wikicode


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
        sections = code.get_sections(
            levels=[2],
            include_lead=False,
        )

        for section in sections:
            headings = section.filter_headings()

            if not headings:
                continue

            if str(headings[0].title).strip() == "العربية":
                return section

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
