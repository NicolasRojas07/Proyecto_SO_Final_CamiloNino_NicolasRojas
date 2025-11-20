"""
Script de verificación rápida del proyecto
"""

def test_imports():
    """Verifica que todos los módulos se pueden importar"""
    print("🔍 Verificando imports...")
    
    try:
        from process_scheduler import ProcessScheduler, Process
        print("  ✅ process_scheduler")
    except Exception as e:
        print(f"  ❌ process_scheduler: {e}")
        return False
    
    try:
        from synchronization import ProducerConsumer, ReadersWriters, DiningPhilosophers
        print("  ✅ synchronization")
    except Exception as e:
        print(f"  ❌ synchronization: {e}")
        return False
    
    try:
        from menu_principal import MainMenu
        print("  ✅ menu_principal")
    except Exception as e:
        print(f"  ❌ menu_principal: {e}")
        return False
    
    return True


def test_scheduler():
    """Test rápido del planificador"""
    print("\n🔍 Probando planificador de procesos...")
    
    try:
        from process_scheduler import ProcessScheduler, Process
        
        processes = [
            Process(pid=1, arrival_time=0, burst_time=3),
            Process(pid=2, arrival_time=1, burst_time=2),
        ]
        
        scheduler = ProcessScheduler(algorithm='fcfs')
        scheduler.add_processes(processes)
        metrics = scheduler.run()
        
        assert metrics.total_completion_time == 5, "Tiempo de completación incorrecto"
        assert len(metrics.gantt_chart) == 2, "Gantt chart incorrecto"
        
        print("  ✅ FCFS funciona correctamente")
        return True
    except Exception as e:
        print(f"  ❌ Error en scheduler: {e}")
        return False


def test_synchronization():
    """Test rápido de sincronización"""
    print("\n🔍 Probando sincronización...")
    
    try:
        from synchronization import ProducerConsumer
        
        pc = ProducerConsumer(buffer_size=3, num_producers=1, num_consumers=1, 
                            items_per_producer=2)
        pc.start()
        pc.wait_completion()
        
        stats = pc.get_statistics()
        assert stats['produced'] == 2, "Producción incorrecta"
        assert stats['consumed'] == 2, "Consumo incorrecto"
        
        print("  ✅ Productor-Consumidor funciona correctamente")
        return True
    except Exception as e:
        print(f"  ❌ Error en sincronización: {e}")
        return False


def main():
    """Ejecuta todas las verificaciones"""
    print("\n" + "="*70)
    print(" VERIFICACIÓN DEL PROYECTO ".center(70, "="))
    print("="*70 + "\n")
    
    results = []
    
    # Test imports
    results.append(test_imports())
    
    # Test scheduler
    results.append(test_scheduler())
    
    # Test synchronization
    results.append(test_synchronization())
    
    # Resumen
    print("\n" + "="*70)
    if all(results):
        print(" ✅ TODAS LAS VERIFICACIONES PASARON ".center(70, "="))
        print("="*70)
        print("\n🎉 El proyecto está listo para ejecutarse!")
        print("\n💡 Para iniciar el programa ejecute: python main.py")
    else:
        print(" ⚠️  ALGUNAS VERIFICACIONES FALLARON ".center(70, "="))
        print("="*70)
        print("\n🔧 Revise los errores anteriores")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
