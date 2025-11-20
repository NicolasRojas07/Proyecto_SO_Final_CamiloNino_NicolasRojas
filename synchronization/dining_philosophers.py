"""
Problema de los Filósofos Comensales
Prevención de deadlock usando jerarquía de recursos
"""

import threading
import time
import random
from typing import List


class DiningPhilosophers:
    """
    Implementación del problema de los Filósofos Comensales
    Usa numeración de tenedores para evitar deadlock
    """
    
    def __init__(self, num_philosophers: int = 5, meals_per_philosopher: int = 3):
        self.num_philosophers = num_philosophers
        self.meals_per_philosopher = meals_per_philosopher
        
        # Tenedores (cada uno es un mutex)
        self.forks = [threading.Lock() for _ in range(num_philosophers)]
        
        # Control
        self.philosophers: List[threading.Thread] = []
        self.running = False
        
        # Estadísticas
        self.meals_eaten = [0] * num_philosophers
        self.waiting_times = [[] for _ in range(num_philosophers)]
    
    def philosopher(self, phil_id: int):
        """
        Hilo filósofo
        
        Estrategia para evitar deadlock:
        - Filósofo impar: toma tenedor izquierdo primero
        - Filósofo par: toma tenedor derecho primero
        """
        left_fork = phil_id
        right_fork = (phil_id + 1) % self.num_philosophers
        
        # Ordenar tenedores para evitar deadlock
        first_fork = min(left_fork, right_fork)
        second_fork = max(left_fork, right_fork)
        
        for meal in range(self.meals_per_philosopher):
            if not self.running:
                break
            
            # Pensar
            print(f"🤔 Filósofo {phil_id} está pensando...")
            time.sleep(random.uniform(0.1, 0.3))
            
            # Intentar tomar tenedores
            start_wait = time.time()
            print(f"🍽️  Filósofo {phil_id} tiene hambre...")
            
            # Tomar primer tenedor
            self.forks[first_fork].acquire()
            print(f"   Filósofo {phil_id} tomó tenedor {first_fork}")
            
            # Tomar segundo tenedor
            self.forks[second_fork].acquire()
            wait_time = time.time() - start_wait
            self.waiting_times[phil_id].append(wait_time)
            print(f"   Filósofo {phil_id} tomó tenedor {second_fork}")
            
            # Comer
            print(f"🍝 Filósofo {phil_id} está comiendo (comida #{meal + 1})...")
            time.sleep(random.uniform(0.2, 0.4))
            self.meals_eaten[phil_id] += 1
            
            # Soltar tenedores
            self.forks[first_fork].release()
            self.forks[second_fork].release()
            print(f"✅ Filósofo {phil_id} terminó de comer y soltó los tenedores")
    
    def start(self):
        """Inicia la simulación"""
        self.running = True
        print("\n" + "="*70)
        print(" SIMULACIÓN FILÓSOFOS COMENSALES ".center(70, "="))
        print("="*70)
        print(f"\n🍽️  Número de filósofos: {self.num_philosophers}")
        print(f"🍝 Comidas por filósofo: {self.meals_per_philosopher}")
        print(f"\n💡 Estrategia de prevención de deadlock:")
        print("   - Ordenamiento de recursos (tenedores numerados)")
        print("   - Cada filósofo toma el tenedor de menor número primero\n")
        print("-"*70 + "\n")
        
        # Crear filósofos
        for i in range(self.num_philosophers):
            t = threading.Thread(target=self.philosopher, args=(i,), 
                               name=f"Philosopher-{i}")
            t.start()
            self.philosophers.append(t)
    
    def wait_completion(self):
        """Espera a que terminen todos los filósofos"""
        for t in self.philosophers:
            t.join()
        self.running = False
        
        print("\n" + "-"*70)
        print(" SIMULACIÓN COMPLETADA ".center(70, "-"))
        print("-"*70)
        print("\n📊 ESTADÍSTICAS POR FILÓSOFO:")
        print("-"*70)
        
        for i in range(self.num_philosophers):
            avg_wait = (sum(self.waiting_times[i]) / len(self.waiting_times[i]) 
                       if self.waiting_times[i] else 0)
            print(f"  Filósofo {i}: {self.meals_eaten[i]} comidas, "
                  f"espera promedio: {avg_wait:.3f}s")
        
        total_meals = sum(self.meals_eaten)
        print(f"\n🍽️  Total de comidas: {total_meals}")
        print(f"✅ Sin deadlocks detectados!\n")
        print("="*70 + "\n")
