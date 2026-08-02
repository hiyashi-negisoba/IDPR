"""Compatibility import for the archived fraud-pilot planning API.

New code should use the offence-agnostic issue pipeline instead.
"""

from idpr.legacy.fraud_planning import *  # noqa: F401,F403
