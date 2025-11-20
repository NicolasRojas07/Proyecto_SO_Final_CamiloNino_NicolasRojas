"""
Métricas y análisis de planificación de procesos
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from .process import Process


@dataclass
class SchedulerMetrics:
    """
    Contiene las métricas calculadas de la planificación
    
    Attributes:
        processes: Lista de procesos ejecutados
        gantt_chart: Diagrama de Gantt de la ejecución
        avg_waiting_time: Tiempo promedio de espera
        avg_turnaround_time: Tiempo promedio de retorno
        avg_response_time: Tiempo promedio de respuesta
        cpu_utilization: Utilización de CPU (%)
        throughput: Procesos completados por unidad de tiempo
    """
    processes: List[Process]
    gantt_chart: List[Dict[str, Any]]
    
    @property
    def avg_waiting_time(self) -> float:
        """Calcula el tiempo promedio de espera"""
        if not self.processes:
            return 0.0
        return sum(p.waiting_time for p in self.processes) / len(self.processes)
    
    @property
    def avg_turnaround_time(self) -> float:
        """Calcula el tiempo promedio de retorno"""
        if not self.processes:
            return 0.0
        return sum(p.turnaround_time for p in self.processes) / len(self.processes)
    
    @property
    def avg_response_time(self) -> float:
        """Calcula el tiempo promedio de respuesta"""
        if not self.processes:
            return 0.0
        response_times = [p.response_time for p in self.processes if p.response_time is not None]
        if not response_times:
            return 0.0
        return sum(response_times) / len(response_times)
    
    @property
    def cpu_utilization(self) -> float:
        """Calcula la utilización de CPU en porcentaje"""
        if not self.gantt_chart:
            return 0.0
        
        total_time = max(p.completion_time for p in self.processes)
        if total_time == 0:
            return 0.0
        
        busy_time = sum(p.burst_time for p in self.processes)
        return (busy_time / total_time) * 100
    
    @property
    def throughput(self) -> float:
        """Calcula el throughput (procesos/unidad de tiempo)"""
        if not self.processes:
            return 0.0
        
        total_time = max(p.completion_time for p in self.processes)
        if total_time == 0:
            return 0.0
        
        return len(self.processes) / total_time
    
    @property
    def total_completion_time(self) -> int:
        """Tiempo total de completación"""
        if not self.processes:
            return 0
        return max(p.completion_time for p in self.processes)
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna un resumen de las métricas"""
        return {
            'num_processes': len(self.processes),
            'avg_waiting_time': round(self.avg_waiting_time, 2),
            'avg_turnaround_time': round(self.avg_turnaround_time, 2),
            'avg_response_time': round(self.avg_response_time, 2),
            'cpu_utilization': round(self.cpu_utilization, 2),
            'throughput': round(self.throughput, 4),
            'total_time': self.total_completion_time
        }
    
    def get_process_details(self) -> List[Dict[str, Any]]:
        """Retorna detalles de cada proceso"""
        return [
            {
                'pid': p.pid,
                'arrival': p.arrival_time,
                'burst': p.burst_time,
                'priority': p.priority,
                'completion': p.completion_time,
                'waiting': p.waiting_time,
                'turnaround': p.turnaround_time,
                'response': p.response_time if p.response_time is not None else 0
            }
            for p in sorted(self.processes, key=lambda x: x.pid)
        ]
    
    def print_summary(self):
        """Imprime un resumen formateado de las métricas"""
        print("\n" + "="*60)
        print("RESUMEN DE MÉTRICAS DE PLANIFICACIÓN".center(60))
        print("="*60)
        
        summary = self.get_summary()
        print(f"\n📊 Número de procesos: {summary['num_processes']}")
        print(f"⏱️  Tiempo total de ejecución: {summary['total_time']} unidades")
        print(f"\n🕐 Tiempo promedio de espera: {summary['avg_waiting_time']:.2f}")
        print(f"🔄 Tiempo promedio de retorno: {summary['avg_turnaround_time']:.2f}")
        print(f"⚡ Tiempo promedio de respuesta: {summary['avg_response_time']:.2f}")
        print(f"\n💻 Utilización de CPU: {summary['cpu_utilization']:.2f}%")
        print(f"📈 Throughput: {summary['throughput']:.4f} procesos/unidad")
        
        print("\n" + "-"*60)
        print("DETALLES POR PROCESO".center(60))
        print("-"*60)
        print(f"{'PID':<6} {'Llegada':<10} {'Ráfaga':<10} {'Espera':<10} {'Retorno':<10} {'Respuesta':<10}")
        print("-"*60)
        
        for detail in self.get_process_details():
            print(f"{detail['pid']:<6} {detail['arrival']:<10} {detail['burst']:<10} "
                  f"{detail['waiting']:<10} {detail['turnaround']:<10} {detail['response']:<10}")
        
        print("="*60 + "\n")
    
    def print_gantt_chart(self):
        """Imprime el diagrama de Gantt en formato de texto"""
        if not self.gantt_chart:
            print("No hay datos para el diagrama de Gantt")
            return
        
        print("\n" + "="*60)
        print("DIAGRAMA DE GANTT".center(60))
        print("="*60 + "\n")
        
        # Imprimir línea superior
        for entry in self.gantt_chart:
            width = entry['end'] - entry['start']
            print(f"|{'─' * (width * 3 - 1)}", end="")
        print("|")
        
        # Imprimir PIDs
        for entry in self.gantt_chart:
            width = entry['end'] - entry['start']
            pid_str = f"P{entry['pid']}"
            padding = (width * 3 - 1 - len(pid_str)) // 2
            print(f"|{' ' * padding}{pid_str}{' ' * (width * 3 - 1 - len(pid_str) - padding)}", end="")
        print("|")
        
        # Imprimir línea inferior
        for entry in self.gantt_chart:
            width = entry['end'] - entry['start']
            print(f"|{'─' * (width * 3 - 1)}", end="")
        print("|")
        
        # Imprimir tiempos
        print(f"{self.gantt_chart[0]['start']}", end="")
        for entry in self.gantt_chart:
            width = entry['end'] - entry['start']
            time_str = str(entry['end'])
            print(f"{' ' * (width * 3 - len(time_str))}{time_str}", end="")
        print("\n" + "="*60 + "\n")
