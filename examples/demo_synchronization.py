"""
Ejemplo de sincronización de hilos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synchronization import ProducerConsumer, ReadersWriters, DiningPhilosophers


def demo_producer_consumer():
    """Demo de Productor-Consumidor"""
    print("\n" + "="*70)
    print(" DEMO: Problema Productor-Consumidor ".center(70, "="))
    print("="*70 + "\n")
    
    pc = ProducerConsumer(
        buffer_size=5,
        num_producers=2,
        num_consumers=2,
        items_per_producer=4
    )
    
    pc.start()
    pc.wait_completion()
    pc.print_statistics()


def demo_readers_writers():
    """Demo de Lectores-Escritores"""
    print("\n" + "="*70)
    print(" DEMO: Problema Lectores-Escritores ".center(70, "="))
    print("="*70 + "\n")
    
    rw = ReadersWriters(
        num_readers=3,
        num_writers=2,
        operations_per_thread=3
    )
    
    rw.start()
    rw.wait_completion()


def demo_dining_philosophers():
    """Demo de Filósofos Comensales"""
    print("\n" + "="*70)
    print(" DEMO: Problema de los Filósofos Comensales ".center(70, "="))
    print("="*70 + "\n")
    
    dp = DiningPhilosophers(
        num_philosophers=5,
        meals_per_philosopher=3
    )
    
    dp.start()
    dp.wait_completion()


if __name__ == "__main__":
    print("\n" + "🚀"*35)
    print(" EJEMPLOS DE SINCRONIZACIÓN DE HILOS ".center(70))
    print("🚀"*35)
    
    demo_producer_consumer()
    input("\n⏸️  Presione Enter para continuar...")
    
    demo_readers_writers()
    input("\n⏸️  Presione Enter para continuar...")
    
    demo_dining_philosophers()
    
    print("\n✅ Demostraciones completadas!\n")
