"""
Step 3 — Run ChemDataExtractor (CDE) on the paper's main text and SI text.

Delegates to the CDE adapter (mock or real).
"""

from pathlib import Path
from typing import Optional

from configs import settings
from src.adapters.chemdataextractor_adapter import parse_main_text, parse_si_text
from src.models.paper import Paper
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)


def run_chemdataextractor(paper: Paper) -> dict:
    """
    Run ChemDataExtractor on *paper* (main text + SI) and merge the results.

    Parameters
    ----------
    paper : A registered Paper object.

    Returns
    -------
    dict with keys:
        paper_id, chemical_mentions, condition_mentions,
        procedure_blocks, text_chunks
    The SI results are merged into the same structure with a "_si" suffix
    on chunk_ids so they can be distinguished downstream.
    """
    logger.info(f"Running ChemDataExtractor on paper {paper.paper_id}")

    main_result = parse_main_text(
        paper_id  = paper.paper_id,
        text_path = paper.pdf_path,   # In real mode, pass extracted plain text here
    )

    si_result = parse_si_text(
        paper_id  = paper.paper_id,
        text_path = paper.si_path,
    )

    # Merge main + SI results into a single dict.
    # SI chunks get a "_si" prefix on their chunk_ids for traceability.
    merged = {
        "paper_id":          paper.paper_id,
        "chemical_mentions": main_result.get("chemical_mentions", [])
                           + si_result.get("chemical_mentions", []),
        "condition_mentions":main_result.get("condition_mentions", [])
                           + si_result.get("condition_mentions", []),
        "procedure_blocks":  main_result.get("procedure_blocks", [])
                           + _prefix_ids(si_result.get("procedure_blocks", []), "si_"),
        "text_chunks":       main_result.get("text_chunks", [])
                           + _prefix_ids(si_result.get("text_chunks", []), "si_"),
    }

    logger.info(
        f"CDE done for {paper.paper_id}: "
        f"{len(merged['chemical_mentions'])} chemical mention(s), "
        f"{len(merged['condition_mentions'])} condition mention(s)"
    )
    return merged


def _prefix_ids(items: list, prefix: str) -> list:
    """Add a prefix to block_id / chunk_id fields to avoid collisions."""
    for item in items:
        for key in ("block_id", "chunk_id"):
            if key in item:
                item[key] = prefix + item[key]
    return items
