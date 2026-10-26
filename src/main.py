import duckdb
import numpy as np
import pandas as pd
from pathlib import Path

layer = 40
neuron = 25546
pole = 1

output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)

db = duckdb.connect()
db.execute("INSTALL httpfs; LOAD httpfs;")

base = (
    "hf://datasets/Station-house/marin-32b-neuron-atlas/"
    "pilot/fineweb-1m/summaries"
)

query = f"""
WITH hits AS (
    SELECT rank, act, token_idx
    FROM '{base}/exemplars.parquet'
    WHERE layer = {layer}
      AND neuron = {neuron}
      AND pole = {pole}
    ORDER BY rank
    LIMIT 10
)
SELECT
    h.rank,
    ROUND(h.act, 2) AS activation,
    string_agg(
        replace(t.token_str, 'Ġ', ' '),
        '' ORDER BY t.pos
    ) AS context
FROM hits h
JOIN '{base}/tokens.parquet' t
    ON t.doc_id = h.token_idx // 2048
    AND t.pos BETWEEN
        greatest(h.token_idx % 2048 - 12, 1)
        AND least(h.token_idx % 2048 + 12, 2047)
GROUP BY h.rank, h.act
ORDER BY h.rank
"""

df = db.sql(query).df()

output_file = output_dir / f"{layer}_{neuron}_{pole}.txt"
output_file.write_text(df.to_string(index=False), encoding="utf-8")

print(f"Saved to {output_file}")