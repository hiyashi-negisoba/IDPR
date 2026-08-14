"""
baseline_runner.py
Orchestrates baseline inference execution and results collection across benchmark datasets.
Utilizes BaselineInputFormatter for structured data preprocessing.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Sequence, Optional

from idpr.baselines import (
    BaseBaseline,
    VanillaBaseline,
    CoTBaseline,
    StandardRAGBaseline,
    LegalChainReasonerBaseline,
    LePRECBaseline,
    ACALBaseline,
    FOLSolverBaseline,
)
from idpr.eval.input_formatter import (
    BaselineInputFormatter,
    assert_no_leaked_fields,
)
from idpr.neural.vllm_client import VLLMClient

class BaselineExperimentRunner:
    """Manager to load benchmark cases, preprocess via BaselineInputFormatter, run baselines, and save output traces."""

    def __init__(
        self,
        vllm_base_url: Optional[str] = None,
        vllm_model: Optional[str] = None,
        output_dir: str | Path = "experiments/results",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> None:
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        import os
        import re
        if vllm_base_url:
            m = re.search(r":(\d+)", vllm_base_url)
            if m:
                os.environ["VLLM_PORT"] = m.group(1)
        if vllm_model:
            os.environ["VLLM_MODEL"] = vllm_model

        self.vllm_client = (
            VLLMClient(base_url=vllm_base_url, model=vllm_model)
            if (vllm_base_url and vllm_model)
            else None
        )

        # Register 7 Comparison Baselines
        self.baselines: Dict[str, BaseBaseline] = {
            "vanilla_zero_shot": VanillaBaseline(
                client=self.vllm_client,
                **{
                    key: value
                    for key, value in (
                        ("temperature", self.temperature),
                        ("max_tokens", self.max_tokens),
                    )
                    if value is not None
                },
            ),
            "chain_of_thought": CoTBaseline(client=self.vllm_client),
            "standard_rag": StandardRAGBaseline(client=self.vllm_client),
            "legal_chain_reasoner": LegalChainReasonerBaseline(client=self.vllm_client),
            "leprec": LePRECBaseline(client=self.vllm_client),
            "acal": ACALBaseline(client=self.vllm_client),
            "fol_autoformalizer_solver": FOLSolverBaseline(client=self.vllm_client),
        }

    def list_baselines(self) -> List[Dict[str, str]]:
        """Returns metadata list of registered comparison baselines."""
        return [
            {
                "baseline_id": b.baseline_id,
                "name": b.name,
                "description": b.description,
            }
            for b in self.baselines.values()
        ]

    def load_dataset(self, dataset_path: str | Path, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Loads benchmark JSONL cases."""
        path = Path(dataset_path)
        if not path.exists():
            raise FileNotFoundError(f"Benchmark dataset not found at {path}")

        cases = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    cases.append(json.loads(line))
                if limit and len(cases) >= limit:
                    break
        return cases

    def run_experiments(
        self,
        dataset_path: str | Path,
        selected_baseline_ids: Optional[Sequence[str]] = None,
        limit: Optional[int] = None,
        verbose: bool = True,
        case_ids: Optional[Sequence[str]] = None,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Runs specified baselines against benchmark dataset and persists results."""
        cases = self.load_dataset(dataset_path, limit=limit)
        if case_ids is not None:
            wanted = set(case_ids)
            cases = [case for case in cases if str(case.get("sub_question_id")) in wanted]
            found = {str(case.get("sub_question_id")) for case in cases}
            if wanted - found:
                raise ValueError(
                    f"dataset is missing {len(wanted - found)} requested cases: "
                    f"{sorted(wanted - found)[:3]}"
                )
        
        target_ids = (
            list(selected_baseline_ids)
            if selected_baseline_ids and "all" not in selected_baseline_ids
            else list(self.baselines.keys())
        )

        all_results: Dict[str, List[Dict[str, Any]]] = {}

        if verbose:
            print("============================================================")
            print("🔬 Starting Baseline Experiment Runner with Formatted Inputs")
            print(f"  └─ Dataset: {dataset_path} ({len(cases)} cases loaded)")
            print(f"  └─ Target Baselines ({len(target_ids)}): {', '.join(target_ids)}")
            print(f"  └─ Output Directory: {self.output_dir.resolve()}")
            print("============================================================")

        for b_id in target_ids:
            if b_id not in self.baselines:
                print(f"⚠️ Warning: Unknown baseline ID '{b_id}'. Skipping...")
                continue

            baseline = self.baselines[b_id]
            if verbose:
                print(f"\n▶ Running Baseline: [{baseline.name}] ({b_id})")

            baseline_results = []
            out_file = self.output_dir / f"{b_id}_outputs.jsonl"

            start_time = time.time()
            with open(out_file, "w", encoding="utf-8") as f_out:
                for idx, raw_case in enumerate(cases, 1):
                    sub_id = raw_case.get("sub_question_id", raw_case.get("case_id", f"case_{idx}"))
                    if verbose:
                        print(f"  [{idx}/{len(cases)}] Processing case: {sub_id}...", end="", flush=True)

                    case_start = time.time()
                    try:
                        # Preprocess input according to baseline type
                        if b_id == "vanilla_zero_shot":
                            formatted_input = BaselineInputFormatter.format_vanilla(raw_case)
                        elif b_id == "chain_of_thought":
                            formatted_input = BaselineInputFormatter.format_cot(raw_case)
                        elif b_id == "legal_chain_reasoner":
                            formatted_input = BaselineInputFormatter.format_legal_chain(raw_case)
                        elif b_id == "leprec":
                            formatted_input = BaselineInputFormatter.format_leprec(raw_case)
                        elif b_id == "acal":
                            formatted_input = BaselineInputFormatter.format_acal(raw_case)
                        elif b_id == "fol_autoformalizer_solver":
                            formatted_input = BaselineInputFormatter.format_fol_solver(raw_case)
                        elif b_id == "standard_rag":
                            formatted_input = BaselineInputFormatter.format_standard_rag(raw_case)
                        else:
                            # Never fall through to the raw record: it carries rubric_summary
                            # and issue_tags. Unknown methods get the question and nothing else.
                            formatted_input = BaselineInputFormatter.format_vanilla(raw_case)

                        # Fairness gate: no grading/planning annotation may reach a method.
                        assert_no_leaked_fields(formatted_input)

                        output = baseline.run_case(formatted_input)
                        output["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        output["elapsed_sec"] = round(time.time() - case_start, 4)
                        output["rubric_summary"] = raw_case.get("rubric_summary", [])
                        output["source"] = raw_case.get("source", {})
                        output["formatted_input_schema"] = list(formatted_input.keys())
                    except Exception as e:
                        output = {
                            "sub_question_id": sub_id,
                            "baseline_id": b_id,
                            "name": baseline.name,
                            "error": str(e),
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        }

                    baseline_results.append(output)
                    f_out.write(json.dumps(output, ensure_ascii=False) + "\n")
                    f_out.flush()

                    if verbose:
                        print(f" Done ({output.get('elapsed_sec', 0)}s)")

            elapsed = round(time.time() - start_time, 2)
            if verbose:
                print(f"  └─ Saved {len(baseline_results)} outputs to {out_file} (Total: {elapsed}s)")

            all_results[b_id] = baseline_results

        # Write unified master output manifest
        master_file = self.output_dir / "all_baselines_master_outputs.json"
        master_summary = {
            "dataset": str(dataset_path),
            "total_cases": len(cases),
            "executed_baselines": list(all_results.keys()),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "baseline_output_files": {
                b_id: str(self.output_dir / f"{b_id}_outputs.jsonl") for b_id in all_results.keys()
            }
        }
        with open(master_file, "w", encoding="utf-8") as f_master:
            json.dump(master_summary, f_master, ensure_ascii=False, indent=2)

        if verbose:
            print("\n🎉 All baseline experiments completed successfully with formatted inputs.")
            print(f"📌 Master Output Summary saved to: {master_file.resolve()}")

        return all_results
