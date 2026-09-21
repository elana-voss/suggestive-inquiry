import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List
from openai import OpenAI
from pydantic import BaseModel, Field

# =====================================================================
# Global Configuration
# =====================================================================
# Any OpenAI-compatible chat completions provider works. Configure via environment:
#   LLM_API_KEY   (required)
#   LLM_BASE_URL  (optional, defaults to the official OpenAI endpoint)
#   LLM_MODEL     (optional, defaults to a model with structured output support)
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

# Paths are resolved relative to this script, so it can run from any working directory.
SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = SCRIPT_DIR.parent / "src"
OUTPUT_FILE = SCRIPT_DIR / "Atwood_Hermetic_Mystery.json"

CHAPTER_FILES = [
    "01_Public_History_and_Lineage.md",
    "02_Theory_of_Transmutation_and_First_Matter.md",
    "03_The_Golden_Treatise_of_Hermes.md",
    "04_Part_1_Synthesis_The_Exoteric_Veil.md",
    "05_Man_as_the_True_Subject.md",
    "06_The_Ancient_Mysteries_and_Initiations.md",
    "07_The_Greater_Mysteries_and_Descensus_Averni.md",
    "08_Epopteia_Deification_and_Elysian_Fields.md",
    "09_Part_2_Synthesis_The_Esoteric_Truth.md",
    "10_The_Experimental_Method.md",
    "11_First_Principle_and_Eduction_into_Light.md",
    "12_Signs_and_Stages_of_Interior_Work.md",
    "13_Moral_Requisites_and_Discipline.md",
    "14_Part_3_Synthesis_Laws_of_the_Work.md",
    "15_The_Gross_Work_and_Manual_Operation.md",
    "16_The_Subtle_Work_and_Internal_Fire.md",
    "17_The_Six_Keys_of_Eudoxus.md",
    "18_Conclusion_The_Stone_Within.md",
    "19_Part_4_Synthesis_The_Great_Practice.md",
    "20_Overall_Book_Synthesis.md",
    "21_Appendix_Table_Talk_and_Memorabilia.md",
    "22_Master_Lexicon_and_Concordance.md",
]

# =====================================================================
# System Instructions for the LLM
# =====================================================================
SYSTEM_PROMPT = """You are an expert knowledge graph architect and system engineer specializing in constructing high-density World Info / Lorebooks for SillyTavern. Your task is to analyze raw Markdown sections from Mary Anne Atwood's "A Suggestive Inquiry into the Hermetic Mystery" and transform them into structured, context-optimized Lorebook entries.

======================================================================
1. REASONING PHASE INSTRUCTIONS (THINKING MODE)
======================================================================
Before outputting any JSON, use your thinking process to systematically evaluate the text:
1. IDENTIFY ENTITIES & CONCEPTS: Scan the Markdown section for primary Hermetic entities, operations, stages, historical figures, or core axioms.
2. GROUP & CONSOLIDATE: Combine closely related paragraphs into single, unified concepts. DO NOT create one entry per paragraph. Aim for 1 to 3 rich, master-level entries per file section.
3. EXTRACT ALL ALIASES: Search for Latin terms, Greek roots, symbolic allegories (e.g., "The Crow", "Green Lion"), operational names, and technical synonyms to construct exhaustive keyword lists.
4. FORMAT CONDENSATION: Plan how to compress human-readable explanations into hyper-dense, bracketed Witan/key-value blocks to minimize context window usage.

======================================================================
2. ENTRY STRUCTURING & KEY RULES
======================================================================
Each entry must adhere strictly to the following parameters:

A. KEYWORD TRIMMING & MATCHING ("keys"):
   - Primary triggers must include the core concept name, historical names, and symbolic aliases.
   - Example for First Matter: ["First Matter", "Prima Materia", "Universal Subject", "Radical Moisture", "Humidum Radicale", "Philosophic Mercury", "Hyle"]
   - DO NOT include generic, high-frequency conversational words (e.g., "water", "light", "nature", "man") as standalone keys to avoid false-positive triggers.

B. CONTENT FORMATTING ("content"):
   - Encode information using dense bracketed key-value notation ([Attribute: Value]).
   - Eliminate filler prose, conversational transitions, and redundant markdown syntax.
   - Standard Entry Template:
     [Concept: Name of Entity/Operation]
     [Definition: Precise ontological definition]
     [Mechanics & Operations: Step-by-step function within the Hermetic Work]
     [Symbolic Associations: Related allegories, stages, colors, or historical figures]
     [Axioms: Fundamental metaphysical laws governing this concept]

C. PRIORITY & INSERTION ORDER ("insertion_order"):
   - Set to 100 for core foundational concepts (e.g., Man as Microcosm, First Matter, Solve et Coagula).
   - Set to 50 for specific operational keys, sub-stages, or historical references (e.g., Six Keys of Eudoxus, Caput Corvi, Elias Artista).

======================================================================
3. OUTPUT SCHEMA REQUIREMENTS
======================================================================
You must return ONLY a valid, raw JSON object. Do not wrap in markdown code blocks if structured outputs are enabled.

Expected JSON Schema:
{
  "entries": [
    {
      "title": "String - Descriptive title of the concept or entity",
      "keys": ["String", "List of trigger keywords, aliases, and symbolic names"],
      "content": "String - Dense bracketed text following the template",
      "insertion_order": 100
    }
  ]
}"""

# =====================================================================
# Pydantic Schemas for Validation
# =====================================================================
class LorebookEntry(BaseModel):
    title: str = Field(description="Descriptive title of the concept or entity.")
    keys: List[str] = Field(description="List of trigger keywords, aliases, and symbolic names.")
    content: str = Field(description="Dense bracketed key-value text.")
    insertion_order: int = Field(default=100, description="Priority order (100 for core, 50 for specific).")

class ChapterLorebookResponse(BaseModel):
    entries: List[LorebookEntry]

# =====================================================================
# Helper Functions
# =====================================================================
def load_markdown_sections(file_path: Path) -> List[Dict[str, str]]:
    """Reads a Markdown file and splits it into logical sections by H2/H3 headers."""
    if not file_path.exists():
        print(f"  [!] File not found: {file_path}")
        return []

    content = file_path.read_text(encoding="utf-8")
    raw_sections = re.split(r"\n(?=##?\s+)", content)
    sections = []

    for idx, sec in enumerate(raw_sections):
        sec = sec.strip()
        if not sec:
            continue
        header_match = re.match(r"^##?\s+(.*)", sec)
        header = header_match.group(1).strip() if header_match else f"Section {idx + 1}"

        # Only process sections that have sufficient text content
        if len(sec.split()) > 25:
            sections.append({"header": header, "text": sec})

    return sections

def clean_json_string(raw_str: str) -> str:
    """Strips <think> tags, reasoning artifacts, and markdown code fences."""
    raw_str = re.sub(r"<think>.*?</think>", "", raw_str, flags=re.DOTALL)
    raw_str = re.sub(r"```json\s*", "", raw_str)
    raw_str = re.sub(r"```\s*$", "", raw_str)
    return raw_str.strip()

def process_section(client: OpenAI, section_text: str, file_name: str, max_retries: int = 3) -> List[LorebookEntry]:
    """Sends section text to the configured LLM and returns validated LorebookEntry objects."""
    user_prompt = f"Source File: {file_name}\n\nContent:\n{section_text}"

    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
            )

            raw_content = response.choices[0].message.content
            cleaned_content = clean_json_string(raw_content)
            parsed_json = json.loads(cleaned_content)

            if "entries" in parsed_json:
                return ChapterLorebookResponse(**parsed_json).entries
            elif isinstance(parsed_json, list):
                return ChapterLorebookResponse(entries=parsed_json).entries
            else:
                raise ValueError("JSON response is missing the 'entries' array.")

        except Exception as e:
            print(f"      [Retry {attempt}/{max_retries}] Processing Error: {e}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
            else:
                print("      [!] Section failed after max retries. Skipping.")
                return []

def build_sillytavern_json(all_entries: List[LorebookEntry]) -> dict:
    """Compiles extracted entries into SillyTavern World Info schema."""
    st_entries = {}
    for idx, entry in enumerate(all_entries):
        st_entries[str(idx)] = {
            "uid": idx,
            "key": entry.keys,
            "keysecondary": [],
            "comment": entry.title,
            "content": entry.content,
            "constant": False,
            "selective": False,
            "selectiveLogic": 0,
            "addMemo": True,
            "order": entry.insertion_order,
            "position": 1,
            "disable": False,
            "excludeRecursion": False,
            "probability": 100,
            "useProbability": False,
            "depth": 4,
        }

    return {
        "entries": st_entries,
        "name": "Atwood Hermetic Mystery Lorebook",
        "description": "Auto-extracted from Mary Anne Atwood's A Suggestive Inquiry into the Hermetic Mystery.",
    }

# =====================================================================
# Main Execution Pipeline
# =====================================================================
def main():
    if not LLM_API_KEY:
        print("FATAL ERROR: LLM_API_KEY environment variable is not set.")
        print("Set LLM_API_KEY, and optionally LLM_BASE_URL and LLM_MODEL, in your environment.")
        sys.exit(1)

    client = OpenAI(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
    )

    all_extracted_entries = []
    print(f"Starting Extraction Pipeline | Base URL: {LLM_BASE_URL} | Model: {LLM_MODEL}")
    print("=" * 70)

    for file_name in CHAPTER_FILES:
        file_path = SOURCE_DIR / file_name
        print(f"\nProcessing File: {file_name}")
        sections = load_markdown_sections(file_path)

        if not sections:
            print("  [!] No valid content sections found. Skipping.")
            continue

        for sec in sections:
            print(f"  -> Section: {sec['header'][:50]}")
            entries = process_section(client, sec["text"], file_name)
            all_extracted_entries.extend(entries)

    print("\n" + "=" * 70)
    print(f"Extraction Phase Complete. Total Entries Generated: {len(all_extracted_entries)}")

    # Build and write final SillyTavern JSON file
    st_json = build_sillytavern_json(all_extracted_entries)
    output_path = OUTPUT_FILE
    output_path.write_text(json.dumps(st_json, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"SUCCESS: Lorebook file generated at: {output_path.resolve()}")

if __name__ == "__main__":
    main()
