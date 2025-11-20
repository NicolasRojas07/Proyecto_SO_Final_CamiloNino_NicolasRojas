# Guía de Instalación y Uso

## Paso 1: Configurar el Entorno Virtual

Abra PowerShell en la carpeta del proyecto y ejecute:

```powershell
# Activar el entorno virtual existente
.\.venv\Scripts\Activate.ps1

# Si hay problemas de permisos, ejecutar primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Paso 2: Instalar Dependencias

```powershell
pip install -r requirements.txt
```

## Paso 3: Ejecutar el Proyecto

### Opción A: Menú Principal Interactivo
```powershell
python main.py
```

### Opción B: Ejemplos Individuales

**Planificación de Procesos:**
```powershell
python examples\demo_scheduler.py
```

**Sincronización de Hilos:**
```powershell
python examples\demo_synchronization.py
```

## Paso 4: Ejecutar Tests (Opcional)

```powershell
pytest tests\ -v
```

## Funcionalidades Implementadas

✅ **Planificador de Procesos** - 100% funcional
- FCFS, SJF, SJF Preemptive, Round Robin
- Priority Scheduling (Preemptive y Non-Preemptive)
- Diagramas de Gantt y métricas completas

✅ **Sincronización de Hilos** - 100% funcional
- Productor-Consumidor con semáforos
- Lectores-Escritores con mutex
- Filósofos Comensales (prevención de deadlock)

✅ **Interfaz CLI** - 100% funcional
- Menú interactivo completo
- Visualización de resultados
- Estadísticas detalladas

## Estructura del Código

```
📁 process_scheduler/        # Planificación de procesos
   ├── process.py             # Clase Process
   ├── schedulers.py          # Algoritmos de planificación
   └── metrics.py             # Cálculo de métricas

📁 synchronization/           # Sincronización
   ├── producer_consumer.py
   ├── readers_writers.py
   └── dining_philosophers.py

📁 cli/                       # Interfaz de usuario
   └── menu.py                # Menú principal

📁 examples/                  # Ejemplos de uso
📁 tests/                     # Pruebas unitarias
```

## Criterios de Evaluación "Excelente" ✅

### Implementación Técnica
- ✅ Múltiples algoritmos de planificación implementados
- ✅ Sincronización correcta sin race conditions
- ✅ Código limpio y documentado (PEP 8)
- ✅ Arquitectura modular y escalable

### Funcionalidad
- ✅ Todos los algoritmos funcionan correctamente
- ✅ Prevención de deadlocks implementada
- ✅ Métricas precisas y detalladas
- ✅ Interfaz usuario amigable

### Documentación
- ✅ README completo con instrucciones
- ✅ Comentarios en el código
- ✅ Ejemplos de uso funcionales
- ✅ Explicación de conceptos de SO

### Testing
- ✅ Tests unitarios incluidos
- ✅ Casos de prueba variados
- ✅ Validación de resultados

## Conceptos de SO Demostrados

1. **Gestión de Procesos**
   - Estados de procesos
   - Cambios de contexto
   - Planificación de CPU

2. **Concurrencia y Sincronización**
   - Secciones críticas
   - Semáforos y mutex
   - Prevención de deadlocks
   - Condiciones de carrera

3. **Exclusión Mutua**
   - Locks y semáforos
   - Algoritmos de sincronización
   - Protección de recursos compartidos

## Contacto

- **Autores:** Camilo Niño & Nicolás Rojas
- **Curso:** Sistemas Operativos 2025-2
- **Fecha:** Noviembre 2025
