"""
__init__.py for idpr.baselines
Exposes all comparison baseline modules.
"""

from idpr.baselines.base import BaseBaseline
from idpr.baselines.vanilla import VanillaBaseline
from idpr.baselines.cot import CoTBaseline
from idpr.baselines.standard_rag import StandardRAGBaseline
from idpr.baselines.legal_chain_reasoner import LegalChainReasonerBaseline
from idpr.baselines.leprec import LePRECBaseline
from idpr.baselines.acal_adapter import ACALBaseline
from idpr.baselines.fol_solver import FOLSolverBaseline

__all__ = [
    "BaseBaseline",
    "VanillaBaseline",
    "CoTBaseline",
    "StandardRAGBaseline",
    "LegalChainReasonerBaseline",
    "LePRECBaseline",
    "ACALBaseline",
    "FOLSolverBaseline",
]
