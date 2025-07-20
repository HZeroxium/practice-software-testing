"""
Package initialization for the data generator.
Provides easy access to main components and configuration.
"""

from .config import GenerationConfig, DEFAULT_CONFIG
from .orchestrator import DataGenerationOrchestrator
from .main import main

__version__ = "2.0.0"
__author__ = "Practice Software Testing Data Generator"
__description__ = "Comprehensive data generator for e-commerce testing platform"


# Easy access to main functionality
def generate_data(config: GenerationConfig = None) -> dict:
    """
    Generate data with the specified configuration.

    Args:
        config: Generation configuration (uses default if None)

    Returns:
        Dictionary containing all generated data
    """
    orchestrator = DataGenerationOrchestrator(config)
    return orchestrator.generate_all_data()


# Export main components
__all__ = [
    "GenerationConfig",
    "DEFAULT_CONFIG",
    "DataGenerationOrchestrator",
    "generate_data",
    "main",
]
