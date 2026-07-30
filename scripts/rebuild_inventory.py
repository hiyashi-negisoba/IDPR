import json
import pandas as pd
import os

parquet_path = "/home/jaehoonjeong/data/sp_qwen/warehouse/lbox_kcl/kcl_essay/test.parquet"
jsonl_path = "/home/jaehoonjeong/data/IDPR/data/inventory/kcl_criminal_v1_draft.jsonl"

if not os.path.exists(parquet_path):
    print(f"❌ Parquet file not found: {parquet_path}")
    exit(1)

if not os.path.exists(jsonl_path):
    print(f"❌ JSONL draft inventory not found: {jsonl_path}")
    exit(1)

print("📖 Reading original KCL Parquet...")
df = pd.read_parquet(parquet_path)

print("📖 Reading draft inventory JSONL...")
rebuilt_rows = []
with open(jsonl_path, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        data = json.loads(line)
        
        # Extract row index map
        source_info = data.get("source", {})
        row_idx = source_info.get("source_row_index", None)
        
        if row_idx is not None and row_idx < len(df):
            # Fetch unabridged rubrics from parquet
            orig_rubrics = df.iloc[row_idx]["rubrics"]
            # Convert numpy array to list if needed
            if hasattr(orig_rubrics, "tolist"):
                orig_rubrics = orig_rubrics.tolist()
            else:
                orig_rubrics = list(orig_rubrics)
                
            # Replace rubric_summary and rubric_count with original unabridged data
            data["rubric_summary"] = orig_rubrics
            data["rubric_count"] = len(orig_rubrics)
            print(f"✅ Restored {len(orig_rubrics)} rubrics for sub_question_id: {data.get('sub_question_id')}")
        else:
            print(f"⚠️ Could not map source_row_index for {data.get('sub_question_id')}")
            
        rebuilt_rows.append(data)

print(f"💾 Saving rebuilt inventory back to {jsonl_path}...")
with open(jsonl_path, "w", encoding="utf-8") as f:
    for row in rebuilt_rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print("🎉 Inventory rebuild successfully completed with unabridged KCL rubrics!")
