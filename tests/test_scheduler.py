"""
Tests para el planificador de procesos
"""

import pytest
from process_scheduler import ProcessScheduler, Process, FCFSScheduler


def test_process_creation():
    """Test creación de proceso"""
    p = Process(pid=1, arrival_time=0, burst_time=5, priority=1)
    assert p.pid == 1
    assert p.burst_time == 5
    assert p.remaining_time == 5


def test_fcfs_scheduler():
    """Test algoritmo FCFS"""
    processes = [
        Process(pid=1, arrival_time=0, burst_time=4),
        Process(pid=2, arrival_time=1, burst_time=3),
        Process(pid=3, arrival_time=2, burst_time=1),
    ]
    
    scheduler = ProcessScheduler(algorithm='fcfs')
    scheduler.add_processes(processes)
    metrics = scheduler.run()
    
    assert metrics.total_completion_time == 8
    assert len(metrics.gantt_chart) == 3


def test_round_robin_scheduler():
    """Test algoritmo Round Robin"""
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5),
        Process(pid=2, arrival_time=0, burst_time=3),
    ]
    
    scheduler = ProcessScheduler(algorithm='round_robin', quantum=2)
    scheduler.add_processes(processes)
    metrics = scheduler.run()
    
    assert metrics.total_completion_time == 8
    assert all(p.is_completed() for p in processes)


def test_sjf_scheduler():
    """Test algoritmo SJF"""
    processes = [
        Process(pid=1, arrival_time=0, burst_time=6),
        Process(pid=2, arrival_time=0, burst_time=2),
        Process(pid=3, arrival_time=0, burst_time=8),
    ]
    
    scheduler = ProcessScheduler(algorithm='sjf')
    scheduler.add_processes(processes)
    metrics = scheduler.run()
    
    # El proceso 2 (burst=2) debería ejecutarse primero
    assert metrics.gantt_chart[0]['pid'] == 2


def test_priority_scheduler():
    """Test algoritmo Priority"""
    processes = [
        Process(pid=1, arrival_time=0, burst_time=4, priority=2),
        Process(pid=2, arrival_time=0, burst_time=3, priority=1),  # Mayor prioridad
        Process(pid=3, arrival_time=0, burst_time=5, priority=3),
    ]
    
    scheduler = ProcessScheduler(algorithm='priority')
    scheduler.add_processes(processes)
    metrics = scheduler.run()
    
    # El proceso 2 (priority=1) debería ejecutarse primero
    assert metrics.gantt_chart[0]['pid'] == 2


def test_metrics_calculation():
    """Test cálculo de métricas"""
    processes = [
        Process(pid=1, arrival_time=0, burst_time=3),
        Process(pid=2, arrival_time=0, burst_time=3),
    ]
    
    scheduler = ProcessScheduler(algorithm='fcfs')
    scheduler.add_processes(processes)
    metrics = scheduler.run()
    
    summary = metrics.get_summary()
    assert summary['num_processes'] == 2
    assert summary['total_time'] == 6
    assert 0 <= summary['cpu_utilization'] <= 100


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
