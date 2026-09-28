"""OPTIONAL: DeepLog-style LSTM over log-key sequences.

Owner: Person 2 (stretch goal)
Status: SCAFFOLD, not implemented. Not required for the minimum demo.

Planned:
- Map messages to log keys (templates), predict the next key with an LSTM,
  flag a sequence when the observed key is outside the top-k predictions.
- Research and training live in ml_research/; artifacts in backend/artifacts/.
"""
