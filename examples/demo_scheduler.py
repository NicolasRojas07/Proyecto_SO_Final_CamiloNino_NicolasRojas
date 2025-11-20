"""
Ejemplo de uso del planificador de procesos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from process_scheduler import ProcessScheduler, Process


def demo_fcfs():
    """Demo de FCFS"""
    print("\n" + "="*70)
    print(" DEMO: FCFS (First Come First Served) ".center(70, "="))
    print("="*70 + "\n")
    
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5),
        Process(pid=2, arrival_time=2, burst_time=3),
        Process(pid=3, arrival_time=4, burst_time=8),
        Process(pid=4, arrival_time=6, burst_time=6),
    ]
    
    scheduler = ProcessScheduler(algorithm='fcfs')
    scheduler.add_processes(processes)
    metrics = scheduler.run()
    
    metrics.print_gantt_chart()
    metrics.print_summary()


def demo_round_robin():
    """Demo de Round Robin"""
    print("\n" + "="*70)
    print(" DEMO: Round Robin (Quantum = 4) ".center(70, "="))
    print("="*70 + "\n")
    
    processes = [
        Process(pid=1, arrival_time=0, burst_time=10),
        Process(pid=2, arrival_time=1, burst_time=4),
        Process(pid=3, arrival_time=2, burst_time=5),
        Process(pid=4, arrival_time=3, burst_time=3),
    ]
    
    scheduler = ProcessScheduler(algorithm='round_robin', quantum=4)
    scheduler.add_processes(processes)
    metrics = scheduler.run()
    
    metrics.print_gantt_chart()
    metrics.print_summary()


def demo_priority():
    """Demo de Priority Scheduling"""
    print("\n" + "="*70)
    print(" DEMO: Priority Scheduling ".center(70, "="))
    print("="*70 + "\n")
    
    processes = [
        Process(pid=1, arrival_time=0, burst_time=7, priority=3),
        Process(pid=2, arrival_time=1, burst_time=3, priority=1),  # Mayor prioridad
        Process(pid=3, arrival_time=2, burst_time=2, priority=4),
        Process(pid=4, arrival_time=3, burst_time=5, priority=2),
    ]
    
    print("💡 Nota: Menor número = Mayor prioridad\n")
    
    scheduler = ProcessScheduler(algorithm='priority')
    scheduler.add_processes(processes)
    metrics = scheduler.run()
    
    metrics.print_gantt_chart()
    metrics.print_summary()


if __name__ == "__main__":
    print("\n" + "🚀"*35)
    print(" EJEMPLOS DE PLANIFICACIÓN DE PROCESOS ".center(70))
    print("🚀"*35)
    
    demo_fcfs()
    input("\n⏸️  Presione Enter para continuar...")
    
    demo_round_robin()
    input("\n⏸️  Presione Enter para continuar...")
    
    demo_priority()
    
    print("\n✅ Demostraciones completadas!\n")
