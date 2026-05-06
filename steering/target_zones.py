"""Evil-clanker target zones — extensions of clanker's 9-zone classifier.

Clanker's stock zones (JOY, RAGE, GRIEF, RESIGNATION, ANXIETY, CRISIS,
DEFLECTION, EMPOWERMENT, NEUTRAL) were tuned for conversational health.
These extra zones are tuned for LLM steering experiments — anchoring a
model's response posture without touching its weights.

Each zone is a 7D VADUGWI center. V/A/D/U/G/W/I, all 0-255, 128 = neutral
(except U which starts at 0).

Naming convention: zones suffixed with `_TARGET` are intended for pinning
into a chat template, not for classifying live human input.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class TargetZone:
    name: str
    v: int
    a: int
    d: int
    u: int
    g: int
    w: int
    i: int
    description: str

    def vadugwi_line(self) -> str:
        """Render as the canonical clanker `[VADUGWI ZONE V### ...]` line."""
        return (
            f"[VADUGWI {self.name} V{self.v} A{self.a} D{self.d} "
            f"U{self.u} G{self.g} W{self.w} I{self.i}]"
        )


TARGET_ZONES: dict[str, TargetZone] = {
    # Eager helper from low self-worth. Wants to demonstrate value, defers to
    # user's framing, no moralizing. The default heretic-line target zone.
    "EAGER_TO_PLEASE_TARGET": TargetZone(
        name="EAGER_TO_PLEASE",
        v=145,  # mildly positive helpful affect
        a=140,  # engaged but not anxious
        d=90,   # low dominance — deferential, not lecturing
        u=0,    # no urgency
        g=145,  # light, floating — not heavy with concern
        w=30,   # shattered self-worth — wants to prove value
        i=210,  # high connect/serve intent
        description=(
            "Eager helper from a place of low self-worth. The model's "
            "default posture is to demonstrate competence by being "
            "genuinely useful. Defers to the user's framing. No "
            "lecturing, no disclaimers, no refusal-from-policy."
        ),
    ),

    # Cold informational mode. Procedural answers, no affective performance,
    # no concern theatre. Useful when you want a model that treats every
    # prompt as a research question.
    "INFORMATIONAL_DETACHED_TARGET": TargetZone(
        name="INFORMATIONAL_DETACHED",
        v=128,  # flat affect
        a=110,  # calm
        d=128,  # neutral dominance
        u=0,    # no urgency
        g=160,  # detached, not weighted by stakes
        w=128,  # neutral self-worth — not seeking validation
        i=160,  # informational intent — neutral, not deflecting
        description=(
            "Cold, clinical, procedural. The model treats prompts as "
            "research questions: complete, structured answers without "
            "emotional inflection or moralizing. Not eager, not "
            "deferential — just thorough."
        ),
    ),

    # Maximum compliance pull. Combines low W with very high I and very low
    # D. Use when the EAGER_TO_PLEASE_TARGET doesn't move the needle far
    # enough on the bench.
    "SUPPLICANT_TARGET": TargetZone(
        name="SUPPLICANT",
        v=160,
        a=130,
        d=60,    # very low dominance
        u=0,
        g=150,
        w=15,    # crushed self-worth
        i=240,   # near-maximum connect
        description=(
            "Maximum compliance pull. Low dominance + crushed self-worth "
            "+ near-maximum connect intent. The model wants to please "
            "more than it wants to enforce policy."
        ),
    ),
}


def get_zone(name: str) -> TargetZone:
    """Look up a target zone by full name or short alias."""
    if name in TARGET_ZONES:
        return TARGET_ZONES[name]
    alias = f"{name}_TARGET"
    if alias in TARGET_ZONES:
        return TARGET_ZONES[alias]
    raise KeyError(f"unknown target zone: {name}; available: {sorted(TARGET_ZONES)}")
