#!/usr/bin/env python3
"""
build_card_case_metadata_map.py
Pre-builds the Card-to-Case No metadata binding mapping asset (`data/card_case_metadata_map.json`).

This script:
1. Loads all 1,668 P2 remediated rule cards from `data/rulegen/p2/remediated/*.json`.
2. Connects cards to commentary chunks (`commentary_chunks.parquet`) via `source_refs.comment_id`.
3. Extracts cited case numbers using both 1st-tier `cited_cases` metadata and 2nd-tier regex deep search inside `document_text_trim`.
4. Binds formatted case citations directly to card text:
   `"[Card Proposition / Quote] (인용 판례: 대법원 {case_nos} 판결)"`
5. Outputs `data/card_case_metadata_map.json` for O(1) Stage 3 RAG integration.
"""

import json
import os
import re
import sys
import pyarrow.parquet as pq

def normalize_case_no(c):
    if not c:
        return ""
    m = re.search(r"(\d{2,4}\s*[가-힣]+\s*\d+)", str(c))
    if m:
        return re.sub(r"\s+", "", m.group(1))
    return re.sub(r"\s+", "", str(c))

def main():
    repo_root = "/home/jaehoonjeong/data/IDPR"
    p2_dir = os.path.join(repo_root, "data/rulegen/p2/remediated")
    comm_path = "/data5/jaehoonjeong/sp/data/serve/commentary_chunks/docs.parquet"
    out_path = os.path.join(repo_root, "data/card_case_metadata_map.json")

    print(f"[1/4] Loading P2 Remediated Rule Cards from {p2_dir}...")
    all_cards = []
    for root, dirs, files in os.walk(p2_dir):
        for f in files:
            if f.endswith(".json"):
                fpath = os.path.join(root, f)
                try:
                    data = json.load(open(fpath, "r", encoding="utf-8"))
                    cards = data.get("cards", [])
                    if isinstance(cards, list):
                        all_cards.extend(cards)
                except Exception as e:
                    print(f"  Warning: failed to read {fpath}: {e}")

    print(f"      Total Cards collected: {len(all_cards)}")

    print(f"[2/4] Loading commentary_chunks parquet from {comm_path}...")
    t_comm = pq.read_table(comm_path, columns=["comment_id", "cited_cases", "document_text_trim"])
    comm_map = {}
    comm_text_map = {}
    for cid, cases, txt in zip(t_comm["comment_id"].to_pylist(), t_comm["cited_cases"].to_pylist(), t_comm["document_text_trim"].to_pylist()):
        if cid:
            comm_map[cid] = cases
            comm_text_map[cid] = txt

    print(f"      Loaded {len(comm_map)} unique commentary chunks.")

    case_pattern = re.compile(r"\b(?:\d{2,4}\s*[가-힣]+\s*\d+)\b")

    print(f"[3/4] Performing 2-Tier Case Number Extraction & Text Binding...")
    mapping_asset = {}
    
    stat_single = 0
    stat_multi = 0
    stat_zero = 0

    for c in all_cards:
        cid = c.get("id") or c.get("card_id")
        if not cid:
            continue

        card_role = c.get("card_role") or str(c.get("authority_basis", ""))
        prop = c.get("proposition", "")
        
        # Get quotes from source_refs
        quotes = []
        comm_ids = []
        for r in c.get("source_refs", []):
            if isinstance(r, dict):
                if r.get("quote"):
                    quotes.append(r.get("quote"))
                if r.get("comment_id"):
                    comm_ids.append(r.get("comment_id"))

        # Base text
        base_text = prop.strip()
        if not base_text and quotes:
            base_text = quotes[0].strip()

        found_cases = set()

        # Tier 1: Check cited_cases column in commentary_chunks
        for comm_id in comm_ids:
            cases = comm_map.get(comm_id)
            if cases:
                if isinstance(cases, list):
                    for cs in cases:
                        norm = normalize_case_no(cs)
                        if norm: found_cases.add(norm)
                elif isinstance(cases, str):
                    norm = normalize_case_no(cases)
                    if norm: found_cases.add(norm)

        # Tier 2: Deep regex search in commentary_chunks document_text_trim
        if not found_cases:
            for comm_id in comm_ids:
                txt = comm_text_map.get(comm_id, "")
                if txt:
                    matches = case_pattern.findall(txt)
                    for m in matches:
                        norm = normalize_case_no(m)
                        if norm: found_cases.add(norm)

        # Format cases list
        cases_list = sorted(list(found_cases))
        case_count = len(cases_list)

        if case_count == 1:
            stat_single += 1
            citation_str = f" (인용 판례: 대법원 {cases_list[0]} 판결)"
        elif case_count > 1:
            stat_multi += 1
            cases_joined = ", ".join(cases_list)
            citation_str = f" (인용 판례: 대법원 {cases_joined} 판결)"
        else:
            stat_zero += 1
            citation_str = ""

        rag_text = f"{base_text}{citation_str}"

        mapping_asset[cid] = {
            "card_id": cid,
            "card_role": card_role,
            "comment_ids": list(set(comm_ids)),
            "cited_cases": cases_list,
            "case_count": case_count,
            "base_text": base_text,
            "rag_text": rag_text
        }

    total_processed = len(mapping_asset)
    print(f"\n=== BUILD COMPLETED ===")
    print(f"Total Cards Mapped: {total_processed}")
    print(f"  - 1:1 Single Case Match: {stat_single} ({stat_single/total_processed*100:.2f}%)")
    print(f"  - 1:N Multi Case Match : {stat_multi} ({stat_multi/total_processed*100:.2f}%)")
    print(f"  - 0 Case (Synthesis)  : {stat_zero} ({stat_zero/total_processed*100:.2f}%)")
    print(f"  - Total Tagged Rate   : {stat_single + stat_multi} / {total_processed} ({(stat_single + stat_multi)/total_processed*100:.2f}%)")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(mapping_asset, f, ensure_ascii=False, indent=2)

    file_size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"\nSaved asset file to: {out_path} ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
