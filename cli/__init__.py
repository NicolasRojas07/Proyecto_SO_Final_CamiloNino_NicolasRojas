"""
Interfaz de Usuario - CLI Module
"""

__all__ = []


class MainMenu:
    """Menú principal del simulador"""
    
    def __init__(self):
        self.running = True
    
    def show_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*70)
        print(" MENÚ PRINCIPAL ".center(70, "="))
        print("="*70)
        print("\n1️⃣  Planificación de Procesos")
        print("2️⃣  Sincronización de Hilos")
        print("3️⃣  Gestión de Memoria")
        print("4️⃣  Sistema de Archivos")
        print("5️⃣  Ejecutar Demo Completo")
        print("0️⃣  Salir")
        print("\n" + "="*70)
    
    def process_scheduler_menu(self):
        """Submenú de planificación de procesos"""
        from process_scheduler import ProcessScheduler, Process
        
        print("\n" + "-"*70)
        print(" PLANIFICACIÓN DE PROCESOS ".center(70, "-"))
        print("-"*70)
        print("\n1. FCFS (First Come First Served)")
        print("2. SJF (Shortest Job First)")
        print("3. SJF Preemptive (SRTF)")
        print("4. Round Robin")
        print("5. Priority (Non-Preemptive)")
        print("6. Priority Preemptive")
        print("7. Comparar todos los algoritmos")
        print("0. Volver")
        
        choice = input("\nSeleccione una opción: ").strip()
        
        if choice == '0':
            return
        
        # Procesos de ejemplo
        processes = [
            Process(pid=1, arrival_time=0, burst_time=8, priority=3),
            Process(pid=2, arrival_time=1, burst_time=4, priority=1),
            Process(pid=3, arrival_time=2, burst_time=9, priority=4),
            Process(pid=4, arrival_time=3, burst_time=5, priority=2),
            Process(pid=5, arrival_time=4, burst_time=2, priority=5),
        ]
        
        algorithms = {
            '1': 'fcfs',
            '2': 'sjf',
            '3': 'sjf_preemptive',
            '4': 'round_robin',
            '5': 'priority',
            '6': 'priority_preemptive'
        }
        
        if choice in algorithms:
            scheduler = ProcessScheduler(algorithm=algorithms[choice], quantum=3)
            scheduler.add_processes(processes)
            metrics = scheduler.run()
            metrics.print_gantt_chart()
            metrics.print_summary()
        elif choice == '7':
            print("\n🔄 Ejecutando comparación de algoritmos...")
            for name, algo in algorithms.items():
                print(f"\n{'='*70}")
                print(f" Algoritmo: {algo.upper()} ".center(70, '='))
                print(f"{'='*70}")
                scheduler = ProcessScheduler(algorithm=algo, quantum=3)
                scheduler.add_processes([
                    Process(pid=p.pid, arrival_time=p.arrival_time, 
                           burst_time=p.burst_time, priority=p.priority)
                    for p in processes
                ])
                metrics = scheduler.run()
                summary = metrics.get_summary()
                print(f"\n⏱️  Tiempo promedio de espera: {summary['avg_waiting_time']:.2f}")
                print(f"🔄 Tiempo promedio de retorno: {summary['avg_turnaround_time']:.2f}")
                print(f"💻 Utilización de CPU: {summary['cpu_utilization']:.2f}%")
        
        input("\n✅ Presione Enter para continuar...")
    
    def synchronization_menu(self):
        """Submenú de sincronización"""
        print("\n" + "-"*70)
        print(" SINCRONIZACIÓN DE HILOS ".center(70, "-"))
        print("-"*70)
        print("\n1. Productor-Consumidor")
        print("2. Lectores-Escritores")
        print("3. Filósofos Comensales")
        print("0. Volver")
        
        choice = input("\nSeleccione una opción: ").strip()
        
        if choice == '1':
            from synchronization import ProducerConsumer
            pc = ProducerConsumer(buffer_size=5, num_producers=2, num_consumers=2, 
                                items_per_producer=5)
            pc.start()
            pc.wait_completion()
            pc.print_statistics()
        
        elif choice == '2':
            from synchronization import ReadersWriters
            rw = ReadersWriters(num_readers=3, num_writers=2, operations_per_thread=3)
            rw.start()
            rw.wait_completion()
        
        elif choice == '3':
            from synchronization import DiningPhilosophers
            dp = DiningPhilosophers(num_philosophers=5, meals_per_philosopher=3)
            dp.start()
            dp.wait_completion()
        
        if choice != '0':
            input("\n✅ Presione Enter para continuar...")
    
    def memory_menu(self):
        """Submenú de gestión de memoria"""
        print("\n" + "-"*70)
        print(" GESTIÓN DE MEMORIA ".center(70, "-"))
        print("-"*70)
        print("\n⚠️  Módulo en desarrollo")
        print("\nFuncionalidades planificadas:")
        print("  • Paginación")
        print("  • Segmentación")
        print("  • Algoritmos de reemplazo (FIFO, LRU, Óptimo)")
        input("\n✅ Presione Enter para continuar...")
    
    def filesystem_menu(self):
        """Submenú de sistema de archivos"""
        print("\n" + "-"*70)
        print(" SISTEMA DE ARCHIVOS ".center(70, "-"))
        print("-"*70)
        print("\n⚠️  Módulo en desarrollo")
        print("\nFuncionalidades planificadas:")
        print("  • Estructura jerárquica de directorios")
        print("  • Operaciones CRUD de archivos")
        print("  • Gestión de permisos")
        input("\n✅ Presione Enter para continuar...")
    
    def run_demo(self):
        """Ejecuta una demostración completa"""
        print("\n" + "="*70)
        print(" DEMO COMPLETO DEL SIMULADOR ".center(70, "="))
        print("="*70)
        print("\n🚀 Ejecutando demostración de todos los módulos...\n")
        
        # Demo de planificación
        print("\n" + "🔹"*35)
        print(" 1. PLANIFICACIÓN DE PROCESOS (Round Robin) ".center(70))
        print("🔹"*35 + "\n")
        
        from process_scheduler import ProcessScheduler, Process
        processes = [
            Process(pid=1, arrival_time=0, burst_time=6, priority=2),
            Process(pid=2, arrival_time=1, burst_time=4, priority=1),
            Process(pid=3, arrival_time=2, burst_time=8, priority=3),
        ]
        scheduler = ProcessScheduler(algorithm='round_robin', quantum=3)
        scheduler.add_processes(processes)
        metrics = scheduler.run()
        metrics.print_gantt_chart()
        summary = metrics.get_summary()
        print(f"⏱️  Tiempo promedio de espera: {summary['avg_waiting_time']:.2f}")
        print(f"🔄 Tiempo promedio de retorno: {summary['avg_turnaround_time']:.2f}")
        
        input("\n⏸️  Presione Enter para continuar...")
        
        # Demo de sincronización
        print("\n" + "🔹"*35)
        print(" 2. SINCRONIZACIÓN (Productor-Consumidor) ".center(70))
        print("🔹"*35 + "\n")
        
        from synchronization import ProducerConsumer
        pc = ProducerConsumer(buffer_size=3, num_producers=1, num_consumers=1, 
                            items_per_producer=3)
        pc.start()
        pc.wait_completion()
        stats = pc.get_statistics()
        print(f"\n📊 Producido: {stats['produced']}, Consumido: {stats['consumed']}")
        
        print("\n" + "="*70)
        print(" DEMO COMPLETADO ".center(70, "="))
        print("="*70)
        
        input("\n✅ Presione Enter para continuar...")
    
    def run(self):
        """Ejecuta el menú principal"""
        while self.running:
            self.show_menu()
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == '1':
                self.process_scheduler_menu()
            elif choice == '2':
                self.synchronization_menu()
            elif choice == '3':
                self.memory_menu()
            elif choice == '4':
                self.filesystem_menu()
            elif choice == '5':
                self.run_demo()
            elif choice == '0':
                print("\n👋 ¡Hasta luego!")
                self.running = False
            else:
                print("\n❌ Opción inválida. Intente nuevamente.")
