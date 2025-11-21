"""
Interfaz Gráfica para el Simulador de Sistemas Operativos
Usa PyQt5 para crear una GUI moderna y profesional
Autores: Camilo Niño & Nicolás Rojas
"""

import sys
import io
from contextlib import redirect_stdout
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QSpinBox, QDoubleSpinBox,
    QTableWidget, QTableWidgetItem, QTextEdit, QTabWidget,
    QGroupBox, QFormLayout, QMessageBox, QProgressBar, QSlider
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QTextCursor
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import QDate

from process_scheduler import ProcessScheduler, Process
from synchronization import ProducerConsumer, ReadersWriters, DiningPhilosophers


class WorkerThread(QThread):
    """Thread para ejecutar operaciones sin bloquear la GUI"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    output = pyqtSignal(str)
    
    def __init__(self, task_func, *args):
        super().__init__()
        self.task_func = task_func
        self.args = args
    
    def run(self):
        try:
            self.task_func(*self.args)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class SchedulerTab(QWidget):
    """Tab para Planificación de Procesos"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Sección de configuración
        config_group = QGroupBox("Configuración de Procesos")
        config_layout = QFormLayout()
        
        self.algo_combo = QComboBox()
        self.algo_combo.addItems([
            'FCFS (First Come First Served)',
            'SJF (Shortest Job First)',
            'SJF Preemptive (SRTF)',
            'Round Robin',
            'Priority (Non-Preemptive)',
            'Priority Preemptive'
        ])
        config_layout.addRow("Algoritmo:", self.algo_combo)
        
        self.quantum_spinbox = QSpinBox()
        self.quantum_spinbox.setValue(3)
        self.quantum_spinbox.setMinimum(1)
        config_layout.addRow("Quantum (RR):", self.quantum_spinbox)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Botones
        button_layout = QHBoxLayout()
        
        run_button = QPushButton("▶ Ejecutar Algoritmo")
        run_button.clicked.connect(self.run_scheduler)
        button_layout.addWidget(run_button)
        
        compare_button = QPushButton("📊 Comparar Todos")
        compare_button.clicked.connect(self.compare_algorithms)
        button_layout.addWidget(compare_button)
        
        layout.addLayout(button_layout)
        
        # Tabla de resultados
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            'PID', 'Arrival', 'Burst', 'Completion', 'Waiting', 'Turnaround'
        ])
        layout.addWidget(QLabel("📋 Resultados:"))
        layout.addWidget(self.results_table)
        
        # Salida de texto
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(QLabel("📝 Detalles:"))
        layout.addWidget(self.output_text)
        
        self.setLayout(layout)
    
    def get_sample_processes(self):
        """Retorna procesos de ejemplo"""
        return [
            Process(pid=1, arrival_time=0, burst_time=8, priority=3),
            Process(pid=2, arrival_time=1, burst_time=4, priority=1),
            Process(pid=3, arrival_time=2, burst_time=9, priority=4),
            Process(pid=4, arrival_time=3, burst_time=5, priority=2),
            Process(pid=5, arrival_time=4, burst_time=2, priority=5),
        ]
    
    def run_scheduler(self):
        """Ejecuta el algoritmo seleccionado"""
        try:
            algo_map = {
                0: 'fcfs',
                1: 'sjf',
                2: 'sjf_preemptive',
                3: 'round_robin',
                4: 'priority',
                5: 'priority_preemptive'
            }
            
            algo = algo_map[self.algo_combo.currentIndex()]
            quantum = self.quantum_spinbox.value()
            processes = self.get_sample_processes()
            
            scheduler = ProcessScheduler(algorithm=algo, quantum=quantum)
            scheduler.add_processes(processes)
            metrics = scheduler.run()
            
            self.display_results(metrics)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
    
    def compare_algorithms(self):
        """Compara todos los algoritmos"""
        try:
            self.output_text.clear()
            self.output_text.append("🔄 Comparando todos los algoritmos...\n")
            
            processes = self.get_sample_processes()
            algo_map = {
                'fcfs': 'FCFS',
                'sjf': 'SJF',
                'sjf_preemptive': 'SJF Preemptive',
                'round_robin': 'Round Robin',
                'priority': 'Priority',
                'priority_preemptive': 'Priority Preemptive'
            }
            
            results = []
            for algo_key, algo_name in algo_map.items():
                scheduler = ProcessScheduler(algorithm=algo_key, quantum=3)
                scheduler.add_processes([
                    Process(pid=p.pid, arrival_time=p.arrival_time,
                           burst_time=p.burst_time, priority=p.priority)
                    for p in processes
                ])
                metrics = scheduler.run()
                summary = metrics.get_summary()
                results.append((algo_name, summary))
            
            # Mostrar comparación
            comparison_text = "COMPARACIÓN DE ALGORITMOS\n" + "="*70 + "\n\n"
            for algo_name, summary in results:
                comparison_text += f"{algo_name}:\n"
                comparison_text += f"  ⏱️  Tiempo promedio de espera: {summary['avg_waiting_time']:.2f}\n"
                comparison_text += f"  🔄 Tiempo promedio de retorno: {summary['avg_turnaround_time']:.2f}\n"
                comparison_text += f"  ⚡ Tiempo promedio de respuesta: {summary['avg_response_time']:.2f}\n"
                comparison_text += f"  💻 Utilización de CPU: {summary['cpu_utilization']:.2f}%\n"
                comparison_text += f"  � Throughput: {summary['throughput']:.4f} procesos/unidad\n\n"
            
            self.output_text.setText(comparison_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
    
    def display_results(self, metrics):
        """Muestra resultados en la tabla"""
        try:
            summary = metrics.get_summary()
            
            # Limpiar tabla
            self.results_table.setRowCount(0)
            
            # Agregar filas con colores
            for i, process in enumerate(metrics.processes):
                self.results_table.insertRow(i)
                
                # Crear items
                pid_item = QTableWidgetItem(str(process.pid))
                arrival_item = QTableWidgetItem(str(process.arrival_time))
                burst_item = QTableWidgetItem(str(process.burst_time))
                completion_item = QTableWidgetItem(str(process.completion_time))
                waiting_item = QTableWidgetItem(str(process.waiting_time))
                turnaround_item = QTableWidgetItem(str(process.turnaround_time))
                
                # Colorear según el tiempo de espera
                waiting_time = process.waiting_time
                if waiting_time == 0:
                    color = QColor(144, 238, 144)  # Verde claro (sin espera)
                elif waiting_time < 5:
                    color = QColor(255, 255, 153)  # Amarillo (espera baja)
                else:
                    color = QColor(255, 200, 200)  # Rojo claro (espera alta)
                
                waiting_item.setBackground(color)
                turnaround_item.setBackground(color)
                
                # Agregar items a la tabla
                self.results_table.setItem(i, 0, pid_item)
                self.results_table.setItem(i, 1, arrival_item)
                self.results_table.setItem(i, 2, burst_item)
                self.results_table.setItem(i, 3, completion_item)
                self.results_table.setItem(i, 4, waiting_item)
                self.results_table.setItem(i, 5, turnaround_item)
            
            # Obtener nombre del algoritmo
            algo_names = [
                'FCFS (First Come First Served)',
                'SJF (Shortest Job First)',
                'SJF Preemptive (SRTF)',
                'Round Robin',
                'Priority (Non-Preemptive)',
                'Priority Preemptive'
            ]
            algo_name = algo_names[self.algo_combo.currentIndex()]
            
            # Mostrar resumen
            output = f"📊 RESULTADOS - {algo_name}\n" + "="*70 + "\n\n"
            output += f"⏱️  Tiempo promedio de espera: {summary['avg_waiting_time']:.2f}\n"
            output += f"🔄 Tiempo promedio de retorno: {summary['avg_turnaround_time']:.2f}\n"
            output += f"⚡ Tiempo promedio de respuesta: {summary['avg_response_time']:.2f}\n"
            output += f"💻 Utilización de CPU: {summary['cpu_utilization']:.2f}%\n"
            output += f"📈 Throughput: {summary['throughput']:.4f} procesos/unidad\n"
            output += f"⏱️  Tiempo total de ejecución: {summary['total_time']} unidades\n\n"
            
            # Agregar análisis
            min_wait = min(p.waiting_time for p in metrics.processes)
            max_wait = max(p.waiting_time for p in metrics.processes)
            output += f"\n📈 ANÁLISIS:\n"
            output += f"  ✅ Mínima espera: {min_wait} unidades\n"
            output += f"  ⚠️  Máxima espera: {max_wait} unidades\n"
            output += f"  📊 Diferencia: {max_wait - min_wait} unidades\n"
            
            self.output_text.setText(output)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar resultados: {str(e)}")


class SynchronizationTab(QWidget):
    """Tab para Sincronización de Hilos"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Sección de configuración
        config_group = QGroupBox("Configuración de Sincronización")
        config_layout = QFormLayout()
        
        self.sync_combo = QComboBox()
        self.sync_combo.addItems([
            'Productor-Consumidor',
            'Lectores-Escritores',
            'Filósofos Comensales'
        ])
        self.sync_combo.currentIndexChanged.connect(self.update_config_options)
        config_layout.addRow("Tipo:", self.sync_combo)
        
        self.param1_label = QLabel("Parámetro 1:")
        self.param1_spinbox = QSpinBox()
        self.param1_spinbox.setValue(2)
        config_layout.addRow(self.param1_label, self.param1_spinbox)
        
        self.param2_label = QLabel("Parámetro 2:")
        self.param2_spinbox = QSpinBox()
        self.param2_spinbox.setValue(2)
        config_layout.addRow(self.param2_label, self.param2_spinbox)
        
        self.param3_label = QLabel("Parámetro 3:")
        self.param3_spinbox = QSpinBox()
        self.param3_spinbox.setValue(3)
        config_layout.addRow(self.param3_label, self.param3_spinbox)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Botón
        run_button = QPushButton("▶ Ejecutar Simulación")
        run_button.clicked.connect(self.run_synchronization)
        layout.addWidget(run_button)
        
        # Salida de texto
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(QLabel("📝 Resultado:"))
        layout.addWidget(self.output_text)
        
        self.setLayout(layout)
        self.update_config_options()
    
    def update_config_options(self):
        """Actualiza opciones según el tipo seleccionado"""
        index = self.sync_combo.currentIndex()
        if index == 0:  # Productor-Consumidor
            self.param1_label.setText("Tamaño de Buffer:")
            self.param1_spinbox.setValue(5)
            self.param2_label.setText("Productores:")
            self.param2_spinbox.setValue(2)
            self.param3_label.setText("Consumidores:")
            self.param3_spinbox.setValue(2)
        elif index == 1:  # Lectores-Escritores
            self.param1_label.setText("Lectores:")
            self.param1_spinbox.setValue(3)
            self.param2_label.setText("Escritores:")
            self.param2_spinbox.setValue(2)
            self.param3_label.setText("Operaciones por Hilo:")
            self.param3_spinbox.setValue(3)
        elif index == 2:  # Filósofos
            self.param1_label.setText("Número de Filósofos:")
            self.param1_spinbox.setValue(5)
            self.param2_label.setText("Comidas por Filósofo:")
            self.param2_spinbox.setValue(3)
            self.param3_label.setText("(No usado)")
            self.param3_spinbox.setEnabled(False)
    
    def run_synchronization(self):
        """Ejecuta la simulación de sincronización"""
        try:
            index = self.sync_combo.currentIndex()
            self.output_text.setText("🔄 Ejecutando simulación...\n")
            
            # Capturar output
            captured_output = io.StringIO()
            
            if index == 0:  # Productor-Consumidor
                with redirect_stdout(captured_output):
                    pc = ProducerConsumer(
                        buffer_size=self.param1_spinbox.value(),
                        num_producers=self.param2_spinbox.value(),
                        num_consumers=self.param3_spinbox.value(),
                        items_per_producer=5
                    )
                    pc.start()
                    pc.wait_completion()
                    stats = pc.get_statistics()
                
                output = "PRODUCTOR-CONSUMIDOR\n" + "="*70 + "\n\n"
                output += f"✅ Producido: {stats['produced']}\n"
                output += f"✅ Consumido: {stats['consumed']}\n"
                output += f"📊 Operaciones exitosas\n\n"
                output += "═"*70 + "\n"
                output += "EVENTOS:\n"
                output += "═"*70 + "\n"
                output += captured_output.getvalue()
                
            elif index == 1:  # Lectores-Escritores
                with redirect_stdout(captured_output):
                    rw = ReadersWriters(
                        num_readers=self.param1_spinbox.value(),
                        num_writers=self.param2_spinbox.value(),
                        operations_per_thread=self.param3_spinbox.value()
                    )
                    rw.start()
                    rw.wait_completion()
                
                output = "LECTORES-ESCRITORES\n" + "="*70 + "\n\n"
                output += "✅ Simulación completada\n"
                output += "📊 Acceso sincronizado a recurso compartido\n\n"
                output += "═"*70 + "\n"
                output += "EVENTOS:\n"
                output += "═"*70 + "\n"
                output += captured_output.getvalue()
                
            elif index == 2:  # Filósofos
                with redirect_stdout(captured_output):
                    dp = DiningPhilosophers(
                        num_philosophers=self.param1_spinbox.value(),
                        meals_per_philosopher=self.param2_spinbox.value()
                    )
                    dp.start()
                    dp.wait_completion()
                
                output = "FILÓSOFOS COMENSALES\n" + "="*70 + "\n\n"
                output += "✅ Simulación completada\n"
                output += "📊 Sin deadlocks - Filósofos comieron exitosamente\n\n"
                output += "═"*70 + "\n"
                output += "EVENTOS:\n"
                output += "═"*70 + "\n"
                output += captured_output.getvalue()
            
            self.output_text.setText(output)
            QMessageBox.information(self, "Éxito", "✅ Simulación completada exitosamente")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")


class DemoTab(QWidget):
    """Tab para Demo Completo"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        demo_button = QPushButton("▶ Ejecutar Demo Completo")
        demo_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;")
        demo_button.clicked.connect(self.run_complete_demo)
        layout.addWidget(demo_button)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)
        
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
    
    def run_complete_demo(self):
        """Ejecuta demo completo"""
        try:
            self.output_text.clear()
            self.progress_bar.setValue(0)
            
            output = "🚀 DEMO COMPLETO DEL SIMULADOR\n" + "="*70 + "\n\n"
            
            # Demo 1: Planificación
            output += "1️⃣  PLANIFICACIÓN DE PROCESOS (Round Robin)\n" + "-"*70 + "\n\n"
            self.output_text.setText(output)
            self.progress_bar.setValue(25)
            
            from process_scheduler import ProcessScheduler, Process
            processes = [
                Process(pid=1, arrival_time=0, burst_time=6, priority=2),
                Process(pid=2, arrival_time=1, burst_time=4, priority=1),
                Process(pid=3, arrival_time=2, burst_time=8, priority=3),
            ]
            scheduler = ProcessScheduler(algorithm='round_robin', quantum=3)
            scheduler.add_processes(processes)
            metrics = scheduler.run()
            summary = metrics.get_summary()
            
            output += f"⏱️  Tiempo promedio de espera: {summary['avg_waiting_time']:.2f}\n"
            output += f"🔄 Tiempo promedio de retorno: {summary['avg_turnaround_time']:.2f}\n"
            output += f"💻 Utilización de CPU: {summary['cpu_utilization']:.2f}%\n\n"
            
            # Demo 2: Sincronización
            output += "2️⃣  SINCRONIZACIÓN (Productor-Consumidor)\n" + "-"*70 + "\n\n"
            self.output_text.setText(output)
            self.progress_bar.setValue(50)
            
            captured_output2 = io.StringIO()
            from synchronization import ProducerConsumer
            with redirect_stdout(captured_output2):
                pc = ProducerConsumer(buffer_size=3, num_producers=1, num_consumers=1,
                                    items_per_producer=3)
                pc.start()
                pc.wait_completion()
                stats = pc.get_statistics()
            
            output += f"📊 Producido: {stats['produced']}, Consumido: {stats['consumed']}\n\n"
            
            # Demo 3: Filósofos
            output += "3️⃣  FILÓSOFOS COMENSALES\n" + "-"*70 + "\n\n"
            self.output_text.setText(output)
            self.progress_bar.setValue(75)
            
            captured_output3 = io.StringIO()
            from synchronization import DiningPhilosophers
            with redirect_stdout(captured_output3):
                dp = DiningPhilosophers(num_philosophers=3, meals_per_philosopher=2)
                dp.start()
                dp.wait_completion()
            
            output += "✅ Simulación completada sin deadlocks\n"
            output += captured_output3.getvalue()[:500] + "\n\n"  # Primeros 500 caracteres
            
            output += "="*70 + "\n"
            output += "🎉 DEMO COMPLETO FINALIZADO\n"
            output += "="*70
            
            self.output_text.setText(output)
            self.progress_bar.setValue(100)
            
            QMessageBox.information(self, "Éxito", "🎉 Demo completado exitosamente")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
            self.progress_bar.setValue(0)


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("🖥️  Simulador de Sistemas Operativos")
        self.setGeometry(100, 100, 1200, 800)
        
        # Tema oscuro
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QTabWidget { background-color: white; }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0b7dda; }
            QGroupBox { border: 2px solid #ddd; border-radius: 4px; padding: 10px; }
            QTableWidget { border: 1px solid #ddd; }
        """)
        
        # Crear tabs
        self.tabs = QTabWidget()
        
        self.scheduler_tab = SchedulerTab()
        self.sync_tab = SynchronizationTab()
        self.demo_tab = DemoTab()
        
        self.tabs.addTab(self.scheduler_tab, "📋 Planificación")
        self.tabs.addTab(self.sync_tab, "🔄 Sincronización")
        self.tabs.addTab(self.demo_tab, "🎬 Demo")
        
        self.setCentralWidget(self.tabs)
        
        # Barra de estado
        self.statusBar().showMessage("✅ Listo")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Simulador de SO")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
