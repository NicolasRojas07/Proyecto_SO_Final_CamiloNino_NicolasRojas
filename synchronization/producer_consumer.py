"""
Problema del Productor-Consumidor
Implementación usando semáforos y mutex
"""

import threading
import time
import random
from typing import List, Dict
from queue import Queue
from dataclasses import dataclass, field


@dataclass
class ProducerConsumerStats:
    """Estadísticas de la simulación"""
    items_produced: int = 0
    items_consumed: int = 0
    total_wait_time_producers: float = 0.0
    total_wait_time_consumers: float = 0.0
    buffer_history: List[int] = field(default_factory=list)
    
    def get_summary(self) -> Dict[str, any]:
        """Retorna resumen de estadísticas"""
        return {
            'produced': self.items_produced,
            'consumed': self.items_consumed,
            'avg_wait_producer': (self.total_wait_time_producers / self.items_produced 
                                 if self.items_produced > 0 else 0),
            'avg_wait_consumer': (self.total_wait_time_consumers / self.items_consumed 
                                 if self.items_consumed > 0 else 0),
            'max_buffer_size': max(self.buffer_history) if self.buffer_history else 0
        }


class ProducerConsumer:
    """
    Implementación del problema clásico Productor-Consumidor
    
    Usa semáforos para controlar el acceso al buffer compartido:
    - empty: cuenta espacios vacíos en el buffer
    - full: cuenta elementos en el buffer
    - mutex: acceso exclusivo al buffer
    """
    
    def __init__(self, buffer_size: int = 10, num_producers: int = 2, 
                 num_consumers: int = 2, items_per_producer: int = 5):
        """
        Args:
            buffer_size: Tamaño máximo del buffer
            num_producers: Número de hilos productores
            num_consumers: Número de hilos consumidores
            items_per_producer: Items que produce cada productor
        """
        self.buffer_size = buffer_size
        self.num_producers = num_producers
        self.num_consumers = num_consumers
        self.items_per_producer = items_per_producer
        
        # Buffer compartido
        self.buffer: List[int] = []
        
        # Semáforos
        self.empty = threading.Semaphore(buffer_size)  # Espacios vacíos
        self.full = threading.Semaphore(0)             # Elementos disponibles
        self.mutex = threading.Lock()                  # Exclusión mutua
        
        # Control de hilos
        self.producers: List[threading.Thread] = []
        self.consumers: List[threading.Thread] = []
        self.running = False
        self.total_items = num_producers * items_per_producer
        
        # Estadísticas
        self.stats = ProducerConsumerStats()
        self.production_log: List[Dict] = []
        self.consumption_log: List[Dict] = []
    
    def producer(self, producer_id: int):
        """
        Hilo productor
        
        Args:
            producer_id: Identificador del productor
        """
        for i in range(self.items_per_producer):
            if not self.running:
                break
            
            # Producir item
            item = producer_id * 100 + i
            time.sleep(random.uniform(0.1, 0.3))  # Simular tiempo de producción
            
            # Esperar espacio vacío
            start_wait = time.time()
            self.empty.acquire()
            wait_time = time.time() - start_wait
            
            # Sección crítica
            self.mutex.acquire()
            try:
                self.buffer.append(item)
                self.stats.items_produced += 1
                self.stats.total_wait_time_producers += wait_time
                self.stats.buffer_history.append(len(self.buffer))
                
                self.production_log.append({
                    'producer_id': producer_id,
                    'item': item,
                    'time': time.time(),
                    'buffer_size': len(self.buffer),
                    'wait_time': wait_time
                })
                
                print(f"✅ Productor {producer_id} produjo item {item} "
                      f"(Buffer: {len(self.buffer)}/{self.buffer_size})")
            finally:
                self.mutex.release()
                self.full.release()  # Señalar que hay un nuevo item
    
    def consumer(self, consumer_id: int):
        """
        Hilo consumidor
        
        Args:
            consumer_id: Identificador del consumidor
        """
        while self.running:
            # Esperar item disponible
            start_wait = time.time()
            acquired = self.full.acquire(timeout=1.0)
            
            if not acquired:
                # Verificar si ya no hay más items por consumir
                if self.stats.items_consumed >= self.total_items:
                    break
                continue
            
            wait_time = time.time() - start_wait
            
            # Sección crítica
            self.mutex.acquire()
            try:
                if not self.buffer:  # Double check
                    self.mutex.release()
                    self.empty.release()
                    continue
                
                item = self.buffer.pop(0)
                self.stats.items_consumed += 1
                self.stats.total_wait_time_consumers += wait_time
                self.stats.buffer_history.append(len(self.buffer))
                
                self.consumption_log.append({
                    'consumer_id': consumer_id,
                    'item': item,
                    'time': time.time(),
                    'buffer_size': len(self.buffer),
                    'wait_time': wait_time
                })
                
                print(f"🔽 Consumidor {consumer_id} consumió item {item} "
                      f"(Buffer: {len(self.buffer)}/{self.buffer_size})")
            finally:
                self.mutex.release()
                self.empty.release()  # Señalar espacio vacío
            
            # Simular tiempo de consumo
            time.sleep(random.uniform(0.1, 0.4))
    
    def start(self):
        """Inicia la simulación"""
        if self.running:
            print("⚠️ La simulación ya está en ejecución")
            return
        
        self.running = True
        print("\n" + "="*70)
        print(" SIMULACIÓN PRODUCTOR-CONSUMIDOR ".center(70, "="))
        print("="*70)
        print(f"\n📦 Buffer size: {self.buffer_size}")
        print(f"🏭 Productores: {self.num_producers}")
        print(f"🛒 Consumidores: {self.num_consumers}")
        print(f"📊 Items por productor: {self.items_per_producer}")
        print(f"🎯 Total items: {self.total_items}\n")
        print("-"*70 + "\n")
        
        # Crear y lanzar productores
        for i in range(self.num_producers):
            t = threading.Thread(target=self.producer, args=(i,), name=f"Producer-{i}")
            t.start()
            self.producers.append(t)
        
        # Crear y lanzar consumidores
        for i in range(self.num_consumers):
            t = threading.Thread(target=self.consumer, args=(i,), name=f"Consumer-{i}")
            t.start()
            self.consumers.append(t)
    
    def wait_completion(self):
        """Espera a que terminen todos los hilos"""
        # Esperar a productores
        for t in self.producers:
            t.join()
        
        # Esperar a consumidores
        for t in self.consumers:
            t.join()
        
        self.running = False
        
        print("\n" + "-"*70)
        print(" SIMULACIÓN COMPLETADA ".center(70, "-"))
        print("-"*70 + "\n")
    
    def get_statistics(self) -> Dict:
        """Retorna estadísticas de la simulación"""
        summary = self.stats.get_summary()
        summary.update({
            'buffer_size': self.buffer_size,
            'num_producers': self.num_producers,
            'num_consumers': self.num_consumers,
            'final_buffer_items': len(self.buffer)
        })
        return summary
    
    def print_statistics(self):
        """Imprime estadísticas formateadas"""
        stats = self.get_statistics()
        
        print("\n" + "="*70)
        print(" ESTADÍSTICAS ".center(70, "="))
        print("="*70)
        print(f"\n📊 Items producidos: {stats['produced']}")
        print(f"📊 Items consumidos: {stats['consumed']}")
        print(f"📦 Items en buffer final: {stats['final_buffer_items']}")
        print(f"\n⏱️  Tiempo promedio espera (productores): {stats['avg_wait_producer']:.4f}s")
        print(f"⏱️  Tiempo promedio espera (consumidores): {stats['avg_wait_consumer']:.4f}s")
        print(f"\n📈 Tamaño máximo del buffer: {stats['max_buffer_size']}/{self.buffer_size}")
        print("="*70 + "\n")
