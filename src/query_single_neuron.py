
import duckdb
from pathlib import Path

DATASET_SELECTOR = {"sparse": "pilot/fineweb-10m-sparse/summaries",
                    "dense": "pilot/fineweb-1m/summaries"}

dataset = "sparse"

layer = 58
neuron = 7828
pole = -1
num_activations = 30
context_window = 12

output_dir = Path("output/single_outputs/")
output_dir.mkdir(parents=True, exist_ok=True)

db = duckdb.connect()
db.execute("INSTALL httpfs; LOAD httpfs;")

base = (
    "hf://datasets/Station-house/marin-32b-neuron-atlas/"
    + DATASET_SELECTOR[dataset]
)

query = f"""
WITH hits AS (
    SELECT rank, act, token_idx
    FROM '{base}/exemplars.parquet'
    WHERE layer = {layer}
      AND neuron = {neuron}
      AND pole = {pole}
    ORDER BY rank
    LIMIT {num_activations}
),
targets AS (
    SELECT
        h.rank,
        h.act,
        h.token_idx,
        t.doc_id,
        t.pos,
        t.token_str AS firing_token
    FROM hits h
    JOIN '{base}/tokens.parquet' t
        ON t.token_idx = h.token_idx
)
SELECT
    h.rank,
    ROUND(h.act, 2) AS activation,
    replace(
        replace(h.firing_token, 'Ġ', ' '),
        'Ċ', '↵'
    ) AS firing_token,
    string_agg(
        CASE
            WHEN t.token_idx = h.token_idx THEN
                '[[' || replace(
                    replace(t.token_str, 'Ġ', ' '),
                    'Ċ', '↵'
                ) || ']]'
            ELSE
                replace(
                    replace(t.token_str, 'Ġ', ' '),
                    'Ċ', '↵'
                )
        END,
        '' ORDER BY t.pos
    ) AS context
FROM targets h
JOIN '{base}/tokens.parquet' t
    ON t.doc_id = h.doc_id
    AND t.pos BETWEEN h.pos - {context_window} AND h.pos + {context_window}
GROUP BY
    h.rank, h.act, h.token_idx, h.firing_token
ORDER BY h.rank
"""

df = db.sql(query).df()

output_file = output_dir / f"{layer}_{neuron}_{pole}_{dataset}_{num_activations}_{context_window}.txt"
output_file.write_text(df.to_string(index=False), encoding="utf-8")

print(df.to_string(index=False))
print(f"\nSaved to {output_file}")