"""
Implementación de algoritmos de planificación de procesos
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .process import Process, ProcessState
from .metrics import SchedulerMetrics
import copy


class BaseScheduler(ABC):
    """Clase base abstracta para todos los planificadores"""
    
    def __init__(self):
        self.processes: List[Process] = []
        self.current_time: int = 0
        self.gantt_chart: List[Dict[str, Any]] = []
    
    def add_process(self, process: Process):
        """Agrega un proceso a la cola"""
        self.processes.append(process)
    
    def add_processes(self, processes: List[Process]):
        """Agrega múltiples procesos"""
        self.processes.extend(processes)
    
    @abstractmethod
    def schedule(self) -> SchedulerMetrics:
        """Ejecuta el algoritmo de planificación"""
        pass
    
    def reset(self):
        """Reinicia el planificador"""
        for process in self.processes:
            process.reset()
        self.current_time = 0
        self.gantt_chart = []


class FCFSScheduler(BaseScheduler):
    """
    First Come First Served (FCFS)
    Los procesos se ejecutan en orden de llegada
    """
    
    def schedule(self) -> SchedulerMetrics:
        """Implementa FCFS scheduling"""
        self.reset()
        
        # Ordenar por tiempo de llegada
        sorted_processes = sorted(self.processes, key=lambda p: (p.arrival_time, p.pid))
        
        for process in sorted_processes:
            # Esperar hasta que el proceso llegue
            if self.current_time < process.arrival_time:
                self.current_time = process.arrival_time
            
            # Registrar tiempo de inicio
            if process.start_time is None:
                process.start_time = self.current_time
                process.response_time = self.current_time - process.arrival_time
            
            # Ejecutar el proceso completamente
            process.state = ProcessState.RUNNING
            start = self.current_time
            self.current_time += process.burst_time
            
            # Agregar al diagrama de Gantt
            self.gantt_chart.append({
                'pid': process.pid,
                'start': start,
                'end': self.current_time
            })
            
            # Calcular métricas
            process.completion_time = self.current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            process.state = ProcessState.TERMINATED
        
        return SchedulerMetrics(self.processes, self.gantt_chart)


class SJFScheduler(BaseScheduler):
    """
    Shortest Job First (SJF)
    Ejecuta primero el proceso con menor burst time
    """
    
    def __init__(self, preemptive: bool = False):
        super().__init__()
        self.preemptive = preemptive
    
    def schedule(self) -> SchedulerMetrics:
        """Implementa SJF scheduling (preemptive y non-preemptive)"""
        self.reset()
        
        if self.preemptive:
            return self._schedule_preemptive()
        else:
            return self._schedule_non_preemptive()
    
    def _schedule_non_preemptive(self) -> SchedulerMetrics:
        """SJF sin apropiación"""
        ready_queue: List[Process] = []
        processes_copy = sorted(self.processes, key=lambda p: p.arrival_time)
        completed = 0
        total = len(processes_copy)
        
        while completed < total:
            # Agregar procesos que han llegado a la cola de listos
            for process in processes_copy:
                if (process.arrival_time <= self.current_time and 
                    process not in ready_queue and 
                    not process.is_completed()):
                    ready_queue.append(process)
            
            if ready_queue:
                # Seleccionar proceso con menor burst time
                ready_queue.sort(key=lambda p: (p.burst_time, p.arrival_time, p.pid))
                current_process = ready_queue.pop(0)
                
                # Registrar tiempo de inicio
                if current_process.start_time is None:
                    current_process.start_time = self.current_time
                    current_process.response_time = self.current_time - current_process.arrival_time
                
                # Ejecutar completamente
                current_process.state = ProcessState.RUNNING
                start = self.current_time
                self.current_time += current_process.burst_time
                
                self.gantt_chart.append({
                    'pid': current_process.pid,
                    'start': start,
                    'end': self.current_time
                })
                
                # Calcular métricas
                current_process.completion_time = self.current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                current_process.state = ProcessState.TERMINATED
                completed += 1
            else:
                self.current_time += 1
        
        return SchedulerMetrics(self.processes, self.gantt_chart)
    
    def _schedule_preemptive(self) -> SchedulerMetrics:
        """SJF con apropiación (SRTF - Shortest Remaining Time First)"""
        processes_copy = [copy.deepcopy(p) for p in self.processes]
        completed = 0
        total = len(processes_copy)
        
        while completed < total:
            # Procesos disponibles
            available = [p for p in processes_copy 
                        if p.arrival_time <= self.current_time and not p.is_completed()]
            
            if available:
                # Seleccionar proceso con menor tiempo restante
                current_process = min(available, key=lambda p: (p.remaining_time, p.arrival_time, p.pid))
                
                # Registrar tiempo de inicio
                if current_process.start_time is None:
                    current_process.start_time = self.current_time
                    current_process.response_time = self.current_time - current_process.arrival_time
                
                # Ejecutar por 1 unidad de tiempo
                current_process.state = ProcessState.RUNNING
                current_process.remaining_time -= 1
                
                # Agregar o extender en diagrama de Gantt
                if (self.gantt_chart and 
                    self.gantt_chart[-1]['pid'] == current_process.pid and
                    self.gantt_chart[-1]['end'] == self.current_time):
                    self.gantt_chart[-1]['end'] = self.current_time + 1
                else:
                    self.gantt_chart.append({
                        'pid': current_process.pid,
                        'start': self.current_time,
                        'end': self.current_time + 1
                    })
                
                self.current_time += 1
                
                # Si el proceso terminó
                if current_process.is_completed():
                    current_process.completion_time = self.current_time
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    current_process.state = ProcessState.TERMINATED
                    completed += 1
            else:
                self.current_time += 1
        
        # Actualizar procesos originales
        for i, process in enumerate(self.processes):
            process.completion_time = processes_copy[i].completion_time
            process.turnaround_time = processes_copy[i].turnaround_time
            process.waiting_time = processes_copy[i].waiting_time
            process.response_time = processes_copy[i].response_time
        
        return SchedulerMetrics(self.processes, self.gantt_chart)


class RoundRobinScheduler(BaseScheduler):
    """
    Round Robin Scheduling
    Asignación cíclica con quantum de tiempo
    """
    
    def __init__(self, quantum: int = 4):
        super().__init__()
        self.quantum = quantum
    
    def schedule(self) -> SchedulerMetrics:
        """Implementa Round Robin scheduling"""
        self.reset()
        
        processes_copy = [copy.deepcopy(p) for p in self.processes]
        ready_queue: List[Process] = []
        completed = 0
        total = len(processes_copy)
        
        # Ordenar por llegada
        sorted_processes = sorted(processes_copy, key=lambda p: (p.arrival_time, p.pid))
        index = 0
        
        while completed < total:
            # Agregar procesos que llegaron a la cola
            while index < len(sorted_processes) and sorted_processes[index].arrival_time <= self.current_time:
                if not sorted_processes[index].is_completed():
                    ready_queue.append(sorted_processes[index])
                index += 1
            
            if ready_queue:
                current_process = ready_queue.pop(0)
                
                # Registrar tiempo de inicio
                if current_process.start_time is None:
                    current_process.start_time = self.current_time
                    current_process.response_time = self.current_time - current_process.arrival_time
                
                # Ejecutar por quantum o hasta completar
                current_process.state = ProcessState.RUNNING
                exec_time = min(self.quantum, current_process.remaining_time)
                start = self.current_time
                
                current_process.remaining_time -= exec_time
                self.current_time += exec_time
                
                self.gantt_chart.append({
                    'pid': current_process.pid,
                    'start': start,
                    'end': self.current_time
                })
                
                # Agregar nuevos procesos que llegaron durante ejecución
                while index < len(sorted_processes) and sorted_processes[index].arrival_time <= self.current_time:
                    if not sorted_processes[index].is_completed():
                        ready_queue.append(sorted_processes[index])
                    index += 1
                
                # Si el proceso no terminó, volver a la cola
                if not current_process.is_completed():
                    ready_queue.append(current_process)
                else:
                    current_process.completion_time = self.current_time
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    current_process.state = ProcessState.TERMINATED
                    completed += 1
            else:
                self.current_time += 1
        
        # Actualizar procesos originales
        for i, process in enumerate(self.processes):
            process.completion_time = processes_copy[i].completion_time
            process.turnaround_time = processes_copy[i].turnaround_time
            process.waiting_time = processes_copy[i].waiting_time
            process.response_time = processes_copy[i].response_time
        
        return SchedulerMetrics(self.processes, self.gantt_chart)


class PriorityScheduler(BaseScheduler):
    """
    Priority Scheduling
    Ejecuta primero el proceso con mayor prioridad (menor número)
    """
    
    def __init__(self, preemptive: bool = False):
        super().__init__()
        self.preemptive = preemptive
    
    def schedule(self) -> SchedulerMetrics:
        """Implementa Priority scheduling"""
        self.reset()
        
        if self.preemptive:
            return self._schedule_preemptive()
        else:
            return self._schedule_non_preemptive()
    
    def _schedule_non_preemptive(self) -> SchedulerMetrics:
        """Priority sin apropiación"""
        ready_queue: List[Process] = []
        processes_copy = sorted(self.processes, key=lambda p: p.arrival_time)
        completed = 0
        total = len(processes_copy)
        
        while completed < total:
            # Agregar procesos disponibles
            for process in processes_copy:
                if (process.arrival_time <= self.current_time and 
                    process not in ready_queue and 
                    not process.is_completed()):
                    ready_queue.append(process)
            
            if ready_queue:
                # Ordenar por prioridad (menor = mayor prioridad)
                ready_queue.sort(key=lambda p: (p.priority, p.arrival_time, p.pid))
                current_process = ready_queue.pop(0)
                
                if current_process.start_time is None:
                    current_process.start_time = self.current_time
                    current_process.response_time = self.current_time - current_process.arrival_time
                
                current_process.state = ProcessState.RUNNING
                start = self.current_time
                self.current_time += current_process.burst_time
                
                self.gantt_chart.append({
                    'pid': current_process.pid,
                    'start': start,
                    'end': self.current_time
                })
                
                current_process.completion_time = self.current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                current_process.state = ProcessState.TERMINATED
                completed += 1
            else:
                self.current_time += 1
        
        return SchedulerMetrics(self.processes, self.gantt_chart)
    
    def _schedule_preemptive(self) -> SchedulerMetrics:
        """Priority con apropiación"""
        processes_copy = [copy.deepcopy(p) for p in self.processes]
        completed = 0
        total = len(processes_copy)
        
        while completed < total:
            available = [p for p in processes_copy 
                        if p.arrival_time <= self.current_time and not p.is_completed()]
            
            if available:
                # Proceso con mayor prioridad (menor número)
                current_process = min(available, key=lambda p: (p.priority, p.arrival_time, p.pid))
                
                if current_process.start_time is None:
                    current_process.start_time = self.current_time
                    current_process.response_time = self.current_time - current_process.arrival_time
                
                current_process.state = ProcessState.RUNNING
                current_process.remaining_time -= 1
                
                # Diagrama de Gantt
                if (self.gantt_chart and 
                    self.gantt_chart[-1]['pid'] == current_process.pid and
                    self.gantt_chart[-1]['end'] == self.current_time):
                    self.gantt_chart[-1]['end'] = self.current_time + 1
                else:
                    self.gantt_chart.append({
                        'pid': current_process.pid,
                        'start': self.current_time,
                        'end': self.current_time + 1
                    })
                
                self.current_time += 1
                
                if current_process.is_completed():
                    current_process.completion_time = self.current_time
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    current_process.state = ProcessState.TERMINATED
                    completed += 1
            else:
                self.current_time += 1
        
        # Actualizar procesos originales
        for i, process in enumerate(self.processes):
            process.completion_time = processes_copy[i].completion_time
            process.turnaround_time = processes_copy[i].turnaround_time
            process.waiting_time = processes_copy[i].waiting_time
            process.response_time = processes_copy[i].response_time
        
        return SchedulerMetrics(self.processes, self.gantt_chart)


class ProcessScheduler:
    """
    Clase principal para gestionar diferentes algoritmos de planificación
    """
    
    ALGORITHMS = {
        'fcfs': FCFSScheduler,
        'sjf': SJFScheduler,
        'sjf_preemptive': lambda: SJFScheduler(preemptive=True),
        'round_robin': RoundRobinScheduler,
        'priority': PriorityScheduler,
        'priority_preemptive': lambda: PriorityScheduler(preemptive=True)
    }
    
    def __init__(self, algorithm: str = 'fcfs', **kwargs):
        """
        Args:
            algorithm: Nombre del algoritmo ('fcfs', 'sjf', 'round_robin', 'priority')
            **kwargs: Parámetros adicionales (quantum para Round Robin, etc.)
        """
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"Algoritmo desconocido: {algorithm}")
        
        scheduler_class = self.ALGORITHMS[algorithm]
        
        if algorithm == 'round_robin':
            quantum = kwargs.get('quantum', 4)
            self.scheduler = scheduler_class(quantum=quantum)
        elif callable(scheduler_class):
            self.scheduler = scheduler_class()
        else:
            self.scheduler = scheduler_class()
    
    def add_process(self, process: Process):
        """Agrega un proceso"""
        self.scheduler.add_process(process)
    
    def add_processes(self, processes: List[Process]):
        """Agrega múltiples procesos"""
        self.scheduler.add_processes(processes)
    
    def run(self) -> SchedulerMetrics:
        """Ejecuta la planificación"""
        return self.scheduler.schedule()
