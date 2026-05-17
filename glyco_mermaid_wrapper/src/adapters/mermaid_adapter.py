"""
Adapter for MERMaid — the multimodal PDF/figure/table extraction pipeline.

Modes
-----
mock : Load pre-built sample JSON from data/samples/. No external tool needed.
real : Placeholder functions showing where CLI/subprocess calls to MERMaid go.
       Switch by setting PIPELINE_MODE=real in your .env file.

MERMaid conceptual output structure
------------------------------------
{
  "paper_id": str,
  "source_pdf": str,
  "figures":  [ { figure_id, page, caption, image_path, text_labels, bounding_box } ],
  "tables":   [ { table_id, page, caption, headers, rows } ],
  "text_blocks": [ { block_id, page, text, section } ],
  "si_blocks":   [ { block_id, text, section } ]
}
"""

import subprocess
from pathlib import Path
from typing import Optional

from configs import settings
from src.utils.json_utils import load_json, save_json
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)


# ── Public API ────────────────────────────────────────────────────────────────

def run_mermaid_on_paper(
    paper_id: str,
    pdf_path: str,
    si_path: Optional[str] = None,
    output_dir: Optional[Path] = None,
) -> dict:
    """
    Run MERMaid on a single paper and return its extraction output as a dict.

    In mock mode this loads sample data; in real mode it calls the MERMaid CLI.

    Parameters
    ----------
    paper_id  : Unique paper identifier used to name output files.
    pdf_path  : Path to the main paper PDF.
    si_path   : Optional path to the supplementary information PDF.
    output_dir: Directory to save raw MERMaid outputs (defaults to settings.MERMAID_OUTPUT_DIR).

    Returns
    -------
    dict with keys: paper_id, source_pdf, figures, tables, text_blocks, si_blocks
    """
    output_dir = Path(output_dir or settings.MERMAID_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    if settings.PIPELINE_MODE == "mock":
        return _run_mock(paper_id, output_dir)
    else:
        return _run_real(paper_id, pdf_path, si_path, output_dir)


def load_mermaid_result(result_path: Path) -> dict:
    """Load a previously saved MERMaid output JSON from disk."""
    return load_json(result_path)


# ── Mock mode ─────────────────────────────────────────────────────────────────

def _run_mock(paper_id: str, output_dir: Path) -> dict:
    """
    Load the bundled sample MERMaid output.
    The paper_id field is overwritten so downstream code stays consistent.
    """
    logger.info(f"[mock] Loading sample MERMaid output for {paper_id}")
    data = load_json(settings.SAMPLE_MERMAID_OUTPUT)
    data["paper_id"] = paper_id  # make it match the caller's paper_id

    out_path = output_dir / f"{paper_id}_mermaid.json"
    save_json(data, out_path)
    logger.info(f"[mock] MERMaid output saved → {out_path}")
    return data


# ── Real mode (placeholders) ──────────────────────────────────────────────────

def _run_real(
    paper_id: str,
    pdf_path: str,
    si_path: Optional[str],
    output_dir: Path,
) -> dict:
    """
    TODO: Call the real MERMaid CLI or Python API.

    Example CLI call (adjust flags to match your MERMaid installation):

        mermaid extract \\
            --input  {pdf_path} \\
            --si     {si_path} \\
            --output {output_dir}/{paper_id}_mermaid.json

    Steps to implement:
    1. Verify that MERMAID_CLI_PATH points to the correct executable.
    2. Build the command list and call subprocess.run().
    3. Check the return code; raise RuntimeError on failure.
    4. Load and return the JSON output file.
    """
    raise NotImplementedError(
        "Real MERMaid mode is not yet implemented. "
        "Set PIPELINE_MODE=mock in .env to use sample data."
    )

    # ── Skeleton for future implementation ──
    # out_path = output_dir / f"{paper_id}_mermaid.json"
    # cmd = [
    #     settings.MERMAID_CLI_PATH,
    #     "extract",
    #     "--input",  pdf_path,
    #     "--output", str(out_path),
    # ]
    # if si_path:
    #     cmd += ["--si", si_path]
    # result = subprocess.run(cmd, capture_output=True, text=True)
    # if result.returncode != 0:
    #     raise RuntimeError(f"MERMaid failed:\n{result.stderr}")
    # return load_json(out_path)
