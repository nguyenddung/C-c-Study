# Two-Tower Neural Network (Future)

This directory will contain the Two-Tower neural retrieval model to replace
the KNN stage when the user base exceeds ~50k.

## Planned architecture

```
Query Tower                  Candidate Tower
───────────                  ───────────────
UserFeatureInput             UserFeatureInput
       │                            │
  Dense(256, ReLU)             Dense(256, ReLU)
  Dense(128, ReLU)             Dense(128, ReLU)
  Dense(64)                    Dense(64)
       │                            │
   query_emb ─── cosine ─── candidate_emb
                    │
               similarity score
```

## Integration plan

1. Train offline on historical match feedback.
2. Build ANN index (FAISS/ScaNN) on candidate embeddings.
3. Swap `StudyMatchRecommender.fit()` to call the candidate tower.
4. Stage-2 weighted scoring remains unchanged.

## Status: Not yet implemented