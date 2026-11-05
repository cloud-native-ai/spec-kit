# Feedback step (fixture carrier)

The prompt threshold is the value declared at
`shared/declarations/facts/feedback-prompt-threshold.yaml#/statement` — this carrier states no
number of its own.

The engine `scripts/python/feedback-utils.py` reads that declaration through
`scripts/python/declaration_reader.py`, so changing the declaration changes the engine.
