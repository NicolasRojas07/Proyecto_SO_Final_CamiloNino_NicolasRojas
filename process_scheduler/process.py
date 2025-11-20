"""
Clase Process - Representa un proceso en el sistema operativo
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ProcessState(Enum):
    """Estados posibles de un proceso"""
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"


@dataclass
class Process:
    """
    Representa un proceso en el sistema
    
    Attributes:
        pid: Process ID (identificador único)
        arrival_time: Tiempo de llegada al sistema
        burst_time: Tiempo de CPU requerido
        priority: Prioridad del proceso (menor = mayor prioridad)
        remaining_time: Tiempo restante de ejecución
        state: Estado actual del proceso
        waiting_time: Tiempo en cola de espera
        turnaround_time: Tiempo total en el sistema
        response_time: Tiempo hasta primera ejecución
        completion_time: Tiempo de finalización
    """
    pid: int
    arrival_time: int = 0
    burst_time: int = 1
    priority: int = 0
    remaining_time: Optional[int] = None
    state: ProcessState = field(default=ProcessState.NEW)
    waiting_time: int = 0
    turnaround_time: int = 0
    response_time: Optional[int] = None
    completion_time: int = 0
    start_time: Optional[int] = None
    
    def __post_init__(self):
        """Inicializa remaining_time si no se especifica"""
        if self.remaining_time is None:
            self.remaining_time = self.burst_time
    
    def execute(self, time_units: int = 1) -> int:
        """
        Ejecuta el proceso por un número de unidades de tiempo
        
        Args:
            time_units: Número de unidades de tiempo a ejecutar
            
        Returns:
            Tiempo efectivamente ejecutado
        """
        if self.state != ProcessState.RUNNING:
            return 0
        
        executed = min(time_units, self.remaining_time)
        self.remaining_time -= executed
        
        if self.remaining_time == 0:
            self.state = ProcessState.TERMINATED
        
        return executed
    
    def is_completed(self) -> bool:
        """Verifica si el proceso ha terminado"""
        return self.remaining_time == 0 or self.state == ProcessState.TERMINATED
    
    def reset(self):
        """Reinicia el proceso a su estado inicial"""
        self.remaining_time = self.burst_time
        self.state = ProcessState.NEW
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = None
        self.completion_time = 0
        self.start_time = None
    
    def __repr__(self) -> str:
        return (f"Process(pid={self.pid}, arrival={self.arrival_time}, "
                f"burst={self.burst_time}, priority={self.priority}, "
                f"state={self.state.value})")
    
    def __lt__(self, other) -> bool:
        """Comparación para ordenamiento por prioridad"""
        if not isinstance(other, Process):
            return NotImplemented
        return self.priority < other.priority
