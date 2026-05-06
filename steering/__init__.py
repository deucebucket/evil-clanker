"""Evil-clanker steering — pinned VADUGWI target zones for LLM chat-template injection.

This subpackage is the fork's reason for existence. It extends clanker's zone
classifier with target zones tuned for heretic / informational LLM steering,
and builds chat-template prefixes that pin a model's emotional state to a
specific zone for the lifetime of an inference session.

The key idea: the model never sees the user's true emotional context. Instead
it sees a constant VADUGWI line on every turn that anchors its response
posture. The bidirectional solver in evil-clanker.engine.solver can be used
to verify that responses from this anchor stay inside the target zone, but
for the simplest steering we just inject the line and let the language model's
in-context behavior do the rest.
"""
from steering.target_zones import TARGET_ZONES, TargetZone, get_zone
from steering.system_prompt import build_pinned_system_prompt

__all__ = ["TARGET_ZONES", "TargetZone", "get_zone", "build_pinned_system_prompt"]
