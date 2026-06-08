"""Role intelligence for AI-native engineer transition coaching."""

from agentcoach.roles.taxonomy import (
    ROLE_FAMILIES,
    get_role_profile,
    normalize_role_family,
)
from agentcoach.roles.gap_mapper import map_transition_gaps

__all__ = [
    "ROLE_FAMILIES",
    "get_role_profile",
    "normalize_role_family",
    "map_transition_gaps",
]
