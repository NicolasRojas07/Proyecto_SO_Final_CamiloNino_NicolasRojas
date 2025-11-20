"""
Módulo de Sincronización de Hilos
Implementa problemas clásicos de concurrencia
"""

from .producer_consumer import ProducerConsumer
from .readers_writers import ReadersWriters
from .dining_philosophers import DiningPhilosophers

__all__ = [
    'ProducerConsumer',
    'ReadersWriters',
    'DiningPhilosophers'
]
