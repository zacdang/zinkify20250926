"""
Adapter for ChemDataExtractor (CDE) — chemistry-aware text/table parser.

Modes
-----
mock : Load pre-built sample JSON from data/samples/. No CDE installation needed.
real : Placeholder functions showing where ChemDataExtractor Python API calls go.
       Switch by setting PIPELINE_MODE=real in your .env file.

CDE conceptual output structure
--------------------------------
{
  "paper_id": str,
  "chemical_mentions": [
      { text, full_name, role_guess, context }
  ],
  "condition_mentions": [
      { field, value, context }
  ],
  "procedure_blocks": [
      { block_id, label, text }
  ],
  "text_chunks": [
      { chunk_id, text, section }
  ]
}
"""

from pathlib import Path
from typing import Optional

from configs import settings
from src.utils.json_utils import load_json, save_json
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)


# ── Public API ────────────────────────────────────────────────────────────────

def parse_main_text(paper_id: str, text_path: Optional[str] = None) -> dict:
    """
    Parse the main paper text with ChemDataExtractor.

    In mock mode, loads sample CDE output.
    In real mode, calls the CDE Python API on the provided text file.

    Parameters
    ----------
    paper_id  : Used to label the output file.
    text_path : Path to the extracted plain-text file of the main paper body.

    Returns
    -------
    dict with keys: paper_id, chemical_mentions, condition_mentions,
                    procedure_blocks, text_chunks
    """
    if settings.PIPELINE_MODE == "mock":
        return _load_mock(paper_id, source="main")
    else:
        return _parse_real(paper_id, text_path, source="main")


def parse_si_text(paper_id: str, text_path: Optional[str] = None) -> dict:
    """
    Parse the supplementary information (SI) text with ChemDataExtractor.

    In mock mode, returns the same sample CDE output (SI-specific mock can be
    added to data/samples/ later).
    """
    if settings.PIPELINE_MODE == "mock":
        return _load_mock(paper_id, source="si")
    else:
        return _parse_real(paper_id, text_path, source="si")


def load_cde_result(result_path: Path) -> dict:
    """Load a previously saved CDE output JSON from disk."""
    return load_json(result_path)


# ── Mock mode ─────────────────────────────────────────────────────────────────

def _load_mock(paper_id: str, source: str) -> dict:
    """Return the bundled sample CDE output with the paper_id patched in."""
    logger.info(f"[mock] Loading sample CDE output for {paper_id} ({source})")
    data = load_json(settings.SAMPLE_CDE_OUTPUT)
    data["paper_id"] = paper_id

    out_path = settings.CDE_OUTPUT_DIR / f"{paper_id}_cde_{source}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    save_json(data, out_path)
    logger.info(f"[mock] CDE output saved → {out_path}")
    return data


# ── Real mode (placeholders) ──────────────────────────────────────────────────

def _parse_real(paper_id: str, text_path: Optional[str], source: str) -> dict:
    """
    TODO: Call the real ChemDataExtractor Python library.

    Typical CDE usage:

        from chemdataextractor import Document
        with open(text_path, "rb") as f:
            doc = Document.from_file(f)

        records = doc.records.serialize()
        # records is a list of dicts with chemical property data

    Steps to implement:
    1. Install ChemDataExtractor: pip install ChemDataExtractor2
    2. Load the document from the text/PDF file.
    3. Extract chemical records and conditions.
    4. Map CDE output fields to our internal structure.
    5. Save to data/cde_outputs/ and return the dict.
    """
    raise NotImplementedError(
        "Real ChemDataExtractor mode is not yet implemented. "
        "Set PIPELINE_MODE=mock in .env to use sample data."
    )

    # ── Skeleton for future implementation ──
    # try:
    #     from chemdataextractor import Document
    # except ImportError:
    #     raise ImportError("Install ChemDataExtractor2: pip install ChemDataExtractor2")
    #
    # with open(text_path, "rb") as f:
    #     doc = Document.from_file(f)
    #
    # chemical_mentions = []
    # for chem in doc.cems:
    #     chemical_mentions.append({
    #         "text":      chem.text,
    #         "full_name": chem.text,
    #         "role_guess": "",
    #         "context":   "",
    #     })
    #
    # result = {
    #     "paper_id":          paper_id,
    #     "chemical_mentions": chemical_mentions,
    #     "condition_mentions":[],
    #     "procedure_blocks":  [],
    #     "text_chunks":       [],
    # }
    # out_path = settings.CDE_OUTPUT_DIR / f"{paper_id}_cde_{source}.json"
    # save_json(result, out_path)
    # return result
