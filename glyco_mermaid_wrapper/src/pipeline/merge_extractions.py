"""
Step 4 — Merge MERMaid and ChemDataExtractor outputs.

Produces a single unified internal representation that all downstream
pipeline steps operate on.

Unified structure:
{
  "paper_id":        str,
  "figures":         [ Figure.to_dict() ],
  "tables":          [ { table_id, caption, headers, rows } ],
  "text_chunks":     [ Chunk.to_dict() ],     -- main text + captions
  "si_chunks":       [ Chunk.to_dict() ],     -- SI text + procedures
  "chemical_mentions": [...],                 -- from CDE
  "condition_mentions":[...],                 -- from CDE
  "candidate_reactions": [],                  -- filled by later steps
}
"""

from src.models.chunk import Chunk
from src.models.figure import Figure
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)


def merge_extractions(mermaid_output: dict, cde_output: dict) -> dict:
    """
    Combine outputs from MERMaid and ChemDataExtractor into one dict.

    Parameters
    ----------
    mermaid_output : Result dict from run_mermaid().
    cde_output     : Result dict from run_chemdataextractor().

    Returns
    -------
    Unified dict used by all downstream steps.
    """
    paper_id = mermaid_output.get("paper_id", "UNKNOWN")
    logger.info(f"Merging extractions for paper {paper_id}")

    # ── Figures ───────────────────────────────────────────────────────────────
    figures = [
        Figure.from_dict(f).to_dict()
        for f in mermaid_output.get("figures", [])
    ]

    # ── Tables ────────────────────────────────────────────────────────────────
    tables = mermaid_output.get("tables", [])

    # ── Text chunks from MERMaid text blocks ──────────────────────────────────
    text_chunks = []
    for blk in mermaid_output.get("text_blocks", []):
        chunk = Chunk(
            chunk_id    = blk.get("block_id", ""),
            text        = blk.get("text", ""),
            source_type = "main_text",
            section     = blk.get("section"),
            page        = blk.get("page"),
        )
        text_chunks.append(chunk.to_dict())

    # Also add figure captions as searchable chunks
    for fig in mermaid_output.get("figures", []):
        if fig.get("caption"):
            chunk = Chunk(
                chunk_id    = f"cap_{fig['figure_id']}",
                text        = fig["caption"],
                source_type = "caption",
                page        = fig.get("page"),
            )
            text_chunks.append(chunk.to_dict())

    # Merge in CDE text chunks (deduplicating by chunk_id)
    existing_ids = {c["chunk_id"] for c in text_chunks}
    for c in cde_output.get("text_chunks", []):
        if c.get("chunk_id") not in existing_ids:
            chunk = Chunk(
                chunk_id    = c.get("chunk_id", ""),
                text        = c.get("text", ""),
                source_type = c.get("source_type", "main_text"),
                section     = c.get("section"),
            )
            text_chunks.append(chunk.to_dict())

    # ── SI chunks ─────────────────────────────────────────────────────────────
    si_chunks = []
    for blk in mermaid_output.get("si_blocks", []):
        chunk = Chunk(
            chunk_id    = blk.get("block_id", ""),
            text        = blk.get("text", ""),
            source_type = "si_text",
            section     = blk.get("section"),
        )
        si_chunks.append(chunk.to_dict())

    # Add CDE procedure blocks as SI chunks
    existing_si_ids = {c["chunk_id"] for c in si_chunks}
    for proc in cde_output.get("procedure_blocks", []):
        cid = proc.get("block_id", proc.get("label", "proc"))
        if cid not in existing_si_ids:
            chunk = Chunk(
                chunk_id    = cid,
                text        = proc.get("text", ""),
                source_type = "procedure",
                section     = proc.get("label"),
            )
            si_chunks.append(chunk.to_dict())

    unified = {
        "paper_id":           paper_id,
        "figures":            figures,
        "tables":             tables,
        "text_chunks":        text_chunks,
        "si_chunks":          si_chunks,
        "chemical_mentions":  cde_output.get("chemical_mentions", []),
        "condition_mentions": cde_output.get("condition_mentions", []),
        "candidate_reactions":[],   # populated by assign_roles
    }

    logger.info(
        f"Merge complete: {len(figures)} figure(s), {len(tables)} table(s), "
        f"{len(text_chunks)} text chunk(s), {len(si_chunks)} SI chunk(s)"
    )
    return unified
