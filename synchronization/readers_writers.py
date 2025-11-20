"""
Problema Lectores-Escritores
Múltiples lectores pueden leer simultáneamente, pero escritores tienen acceso exclusivo
"""

import threading
import time
import random
from typing import List, Dict


class ReadersWriters:
    """
    Implementación del problema Lectores-Escritores
    Prioridad a lectores - múltiples lectores pueden leer simultáneamente
    """
    
    def __init__(self, num_readers: int = 3, num_writers: int = 2, 
                 operations_per_thread: int = 3):
        self.num_readers = num_readers
        self.num_writers = num_writers
        self.operations_per_thread = operations_per_thread
        
        # Recurso compartido
        self.shared_data = 0
        
        # Sincronización
        self.mutex = threading.Lock()          # Protege read_count
        self.write_lock = threading.Lock()     # Acceso exclusivo para escritores
        self.read_count = 0
        
        # Control
        self.threads: List[threading.Thread] = []
        self.running = False
        
        # Estadísticas
        self.read_operations = 0
        self.write_operations = 0
        self.log: List[Dict] = []
    
    def reader(self, reader_id: int):
        """Hilo lector"""
        for i in range(self.operations_per_thread):
            if not self.running:
                break
            
            time.sleep(random.uniform(0.1, 0.3))
            
            # Entrada de lector
            self.mutex.acquire()
            self.read_count += 1
            if self.read_count == 1:
                self.write_lock.acquire()  # Primer lector bloquea escritores
            self.mutex.release()
            
            # Leer datos
            value = self.shared_data
            self.read_operations += 1
            print(f"📖 Lector {reader_id} leyó: {value} (Lectores activos: {self.read_count})")
            self.log.append({'type': 'read', 'id': reader_id, 'value': value, 
                           'readers': self.read_count})
            
            time.sleep(random.uniform(0.05, 0.15))  # Simular lectura
            
            # Salida de lector
            self.mutex.acquire()
            self.read_count -= 1
            if self.read_count == 0:
                self.write_lock.release()  # Último lector libera escritores
            self.mutex.release()
    
    def writer(self, writer_id: int):
        """Hilo escritor"""
        for i in range(self.operations_per_thread):
            if not self.running:
                break
            
            time.sleep(random.uniform(0.2, 0.4))
            
            # Entrada de escritor (acceso exclusivo)
            self.write_lock.acquire()
            
            # Escribir datos
            new_value = writer_id * 100 + i
            self.shared_data = new_value
            self.write_operations += 1
            print(f"✍️  Escritor {writer_id} escribió: {new_value}")
            self.log.append({'type': 'write', 'id': writer_id, 'value': new_value})
            
            time.sleep(random.uniform(0.1, 0.2))  # Simular escritura
            
            # Salida de escritor
            self.write_lock.release()
    
    def start(self):
        """Inicia la simulación"""
        self.running = True
        print("\n" + "="*70)
        print(" SIMULACIÓN LECTORES-ESCRITORES ".center(70, "="))
        print("="*70)
        print(f"\n📖 Lectores: {self.num_readers}")
        print(f"✍️  Escritores: {self.num_writers}")
        print(f"🔄 Operaciones por hilo: {self.operations_per_thread}\n")
        print("-"*70 + "\n")
        
        # Crear lectores
        for i in range(self.num_readers):
            t = threading.Thread(target=self.reader, args=(i,), name=f"Reader-{i}")
            t.start()
            self.threads.append(t)
        
        # Crear escritores
        for i in range(self.num_writers):
            t = threading.Thread(target=self.writer, args=(i,), name=f"Writer-{i}")
            t.start()
            self.threads.append(t)
    
    def wait_completion(self):
        """Espera a que terminen todos los hilos"""
        for t in self.threads:
            t.join()
        self.running = False
        
        print("\n" + "-"*70)
        print(f" SIMULACIÓN COMPLETADA ".center(70, "-"))
        print("-"*70)
        print(f"\n📊 Total lecturas: {self.read_operations}")
        print(f"📊 Total escrituras: {self.write_operations}")
        print(f"📊 Valor final: {self.shared_data}\n")
        print("="*70 + "\n")
