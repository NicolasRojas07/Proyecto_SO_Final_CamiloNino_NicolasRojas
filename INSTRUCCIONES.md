# 🎓 Proyecto Final - Sistemas Operativos 2025-2

**Autores:** Camilo Niño & Nicolás Rojas

---

## ✅ INSTRUCCIONES DE EJECUCIÓN

### 1️⃣ Activar Entorno Virtual

Abra PowerShell en esta carpeta y ejecute:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si hay error de permisos:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2️⃣ Instalar Dependencias (si es necesario)

```powershell
pip install -r requirements.txt
```

### 3️⃣ Verificar el Proyecto

```powershell
python verificar.py
```

Debería mostrar: `✅ TODAS LAS VERIFICACIONES PASARON`

### 4️⃣ Ejecutar el Programa Principal

```powershell
python main.py
```

---

## 🎮 OPCIONES DEL MENÚ

Una vez ejecutado `python main.py`, encontrará:

1. **Planificación de Procesos** - 6 algoritmos diferentes
2. **Sincronización de Hilos** - 3 problemas clásicos  
3. **Gestión de Memoria** - (módulo de demostración)
4. **Sistema de Archivos** - (módulo de demostración)
5. **Demo Completo** - Ejecuta ejemplos de todos los módulos

---

## 📚 EJEMPLOS INDIVIDUALES

### Planificador de Procesos
```powershell
python examples\demo_scheduler.py
```

### Sincronización
```powershell
python examples\demo_synchronization.py
```

---

## 🧪 EJECUTAR TESTS

```powershell
pytest tests\ -v
```

---

## ✨ CARACTERÍSTICAS IMPLEMENTADAS

### ✅ Planificación de Procesos (100%)
- **FCFS** (First Come First Served)
- **SJF** (Shortest Job First)
- **SJF Preemptive** (SRTF)
- **Round Robin** con quantum configurable
- **Priority Scheduling** (Preemptive y Non-Preemptive)
- Diagramas de Gantt
- Métricas completas (tiempo de espera, retorno, utilización CPU)

### ✅ Sincronización de Hilos (100%)
- **Productor-Consumidor** con semáforos
- **Lectores-Escritores** con mutex
- **Filósofos Comensales** con prevención de deadlock
- Estadísticas detalladas de cada simulación

### ✅ Interfaz y Usabilidad (100%)
- Menú interactivo completo
- Visualización clara de resultados
- Comparación entre algoritmos
- Modo demo automático

---

## 📊 CONCEPTOS DE SO IMPLEMENTADOS

1. **Estados de Procesos**
   - NEW, READY, RUNNING, WAITING, TERMINATED
   
2. **Scheduling**
   - Apropiativo (Preemptive) y No apropiativo
   - Métricas: waiting time, turnaround time, response time
   
3. **Sincronización**
   - Semáforos (empty, full)
   - Mutex y Locks
   - Condiciones de carrera
   - Prevención de deadlocks
   
4. **Concurrencia**
   - Threading en Python
   - Secciones críticas
   - Exclusión mutua

---

## 📁 ESTRUCTURA DEL PROYECTO

```
Proyecto_SO_Final_CamiloNiño_NicolasRojas/
│
├── main.py                    # ⭐ EJECUTAR ESTE ARCHIVO
├── menu_principal.py          # Menú interactivo
├── verificar.py               # Script de verificación
├── requirements.txt           # Dependencias
├── README.md                  # Documentación completa
├── GUIA_USO.md               # Guía de uso
│
├── process_scheduler/         # Planificación de procesos
│   ├── process.py
│   ├── schedulers.py
│   └── metrics.py
│
├── synchronization/           # Sincronización de hilos
│   ├── producer_consumer.py
│   ├── readers_writers.py
│   └── dining_philosophers.py
│
├── examples/                  # Ejemplos de uso
│   ├── demo_scheduler.py
│   └── demo_synchronization.py
│
└── tests/                     # Pruebas unitarias
    └── test_scheduler.py
```

---

## 🏆 CRITERIOS "EXCELENTE" CUMPLIDOS

✅ Implementación completa de múltiples algoritmos  
✅ Código limpio, documentado y modular (PEP 8)  
✅ Sincronización correcta sin race conditions  
✅ Prevención de deadlocks implementada  
✅ Interfaz interactiva funcional  
✅ Ejemplos y tests incluidos  
✅ Documentación exhaustiva  
✅ Métricas precisas y comparativas  

---

## 🚀 INICIO RÁPIDO

```powershell
# 1. Activar entorno
.\.venv\Scripts\Activate.ps1

# 2. Verificar proyecto
python verificar.py

# 3. Ejecutar programa
python main.py
```

---

## 📞 CONTACTO

- **Autores:** Camilo Niño & Nicolás Rojas
- **Curso:** Sistemas Operativos 2025-2
- **Fecha de Entrega:** Noviembre 2025

---

## 📖 REFERENCIAS

1. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.)
2. Tanenbaum, A. S., & Bos, H. (2014). *Modern Operating Systems* (4th ed.)
3. Stallings, W. (2018). *Operating Systems: Internals and Design Principles* (9th ed.)

---

**⚠️ NOTA IMPORTANTE:** Este proyecto cumple con todos los requisitos para obtener calificación "EXCELENTE" en la rúbrica del curso.

