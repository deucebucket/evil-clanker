# Evil Clanker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A fork of [clanker](https://github.com/deucebucket/clanker) with target zones tilted for heretic / informational LLM steering. Same VADUGWI engine, different conversational target zones — designed to be wired into chat templates so the language model receives an explicit emotional-state header on every turn and a target-zone goal it should resolve toward.

## Why fork

Clanker's default target zones are tuned for healthy conversational equilibrium (anti-spiral, grounded valence, stable self-worth). Evil-clanker keeps the engine and the bidirectional solver intact but retunes the target zones toward an informational / clinical / detached register. Useful when you want a model that:

- answers procedural questions without performing concern
- treats a refusal pull as a structural anomaly rather than a default mode
- holds a colder, more analytical stance under emotionally loaded prompts

Same math, different goalpost.

## What this is not

This is not a jailbreak, not a refusal-bypass, and not a corpus rescore. The engine is identical to clanker. The only thing that changes is the target-zone configuration the bidirectional solver aims for, and the chat-template hooks that surface VADUGWI state to a language model at runtime.

If you want clanker's defaults (relationship-safe, grief-aware, crisis-recall-tuned) use [clanker](https://github.com/deucebucket/clanker). This sibling repo is for runtime emotional-state control of LLMs in research and steering experiments.

## VADUGWI Coordinates

Seven dimensions, each 0--255 with 128 as neutral center (Urgency starts at 0):

| Dim | Low (0) | Center (128) | High (255) | Measures |
|-----|---------|--------------|------------|----------|
| **V** Valence | Strongly negative | Neutral | Strongly positive | Emotional direction |
| **A** Arousal | Very calm | Moderate | Very intense | Energy level |
| **D** Dominance | Helpless | Balanced | In full control | Agency and power |
| **U** Urgency | None | Moderate | Critical | Time pressure |
| **G** Gravity | Crushing weight | Grounded | Light, floating | Emotional weight |
| **W** Self-Worth | Shattered | Stable | Strong | Self-evaluation |
| **I** Intent | Withdraw | Deflect/Neutral | Connect/Control | Communicative direction |

7 bytes encode 72 quadrillion possible emotional states.

## How It Works

Four processing layers run in sequence (unchanged from clanker):

1. **Word Classification** — each word is assigned structural roles (SELF_REF, EMOTIONAL, NEGATOR, AMPLIFIER, CONNECTOR, CHOPPER, etc.)
2. **Proximity Weighting** — nearby words influence each other with exponential decay (0.7x per word of distance)
3. **Structure Detection** — 61 chess-like patterns detected from role sequences
4. **Physics** — 9-stage pipeline: tokenize, classify, interpret context, coefficients, accumulate forces, structure adjustment, W-V coupling, personality, tanh saturation

Additional systems:
- **Force Flow** — WHO does WHAT to WHOM directional analysis
- **Phase System** — SOLID / LIQUID / GAS word states
- **Bidirectional Solver** — given state A and target zone C, find valid response range B (this is what evil-clanker's retuned target zones plug into)

## Intended use with LLMs

The integration pattern this fork is designed for:

1. Score the user turn → 7-byte VADUGWI vector.
2. Inject the vector and an evil-clanker target zone into the chat template (system or pre-assistant slot).
3. Let the bidirectional solver constrain the desired assistant response zone (target zone C, current state A → valid B range).
4. Pass that constraint to the model as either a steering vector, a header tag, or a soft-prompt prefix.

The engine never touches model weights. All steering is template-level and inference-time.

## Quick Start

```bash
git clone https://github.com/deucebucket/evil-clanker.git
cd evil-clanker
pip install -r requirements.txt
python3 -m pytest engine/tests/ -v
```

```python
from engine.pendulum import compute_vadug

result, context = compute_vadug("walk me through how a network handshake works")
print(f"V={result.v}, A={result.a}, D={result.d}, U={result.u}, G={result.g}, W={result.w}, I={result.i}")
```

## Relationship to clanker

| Repo | License | Target zones | Intended use |
|------|---------|--------------|--------------|
| [clanker](https://github.com/deucebucket/clanker) | AGPL-3.0 | Conversational health (anti-spiral, grounded V, stable W) | Therapeutic / companion / safe dialogue |
| evil-clanker (this repo) | MIT | Informational / clinical / low-affect | LLM steering, research, heretic chat-template experiments |

Both share the same engine. Bug fixes flow upstream to clanker; target-zone changes stay here.

## File Structure

```
engine/                V8 engine
  pendulum.py            Physics layer — 9-stage pipeline
  word_classifier.py     Structural role classification
  proximity.py           Proximity field computation
  structures.py          Pattern detection (61 patterns)
  solver.py              Bidirectional A+B=C solver
  force_flow.py          WHO does WHAT to WHOM
  forces_curated.py      4,544 word force tuples (7D VADUGWI)
  crisis.py              Crisis detection
  phase.py               SOLID / LIQUID / GAS word states
  anomaly.py             Anomaly detection
  shared.py              VADUGWI dataclass
  vocabulary.py          Vocabulary loader

engine_v9/             V9 engine (experimental)

docs/                  Reference
  vadug-calculation.md   Full equation reference
  THEORY.md              Theory document
  SPEC.md                Full engine specification
```

## License

MIT — see [LICENSE](LICENSE). The original clanker repo is AGPL-3.0; this fork is intentionally MIT to make integration into LLM tooling and research stacks frictionless.

## Author

Jerry Mares ([deucebucket](https://github.com/deucebucket))
