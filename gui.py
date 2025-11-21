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
    QGroupBox, QFormLayout, QMessageBox, QProgressBar, QSlider,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont, QColor, QTextCursor, QPalette, QLinearGradient, QBrush
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
        
        # Botones con iconos y efectos
        button_layout = QHBoxLayout()
        
        run_button = QPushButton("▶ Ejecutar Algoritmo")
        run_button.clicked.connect(self.run_scheduler)
        self.add_button_shadow(run_button)
        button_layout.addWidget(run_button)
        
        compare_button = QPushButton("📊 Comparar Todos")
        compare_button.clicked.connect(self.compare_algorithms)
        compare_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(251, 188, 5, 0.85), stop:1 rgba(234, 67, 53, 0.85));
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.6);
                border-radius: 14px;
                padding: 14px 28px;
                font-weight: 600;
                font-size: 14px;
                min-height: 25px;
                min-width: 160px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(251, 188, 5, 1), stop:1 rgba(234, 67, 53, 1));
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
        """)
        self.add_button_shadow(compare_button)
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
    
    def add_button_shadow(self, button):
        """Agrega efecto de sombra estilo Glass"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(66, 133, 244, 60))
        shadow.setOffset(0, 6)
        button.setGraphicsEffect(shadow)
    
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
                
                # Colorear según el tiempo de espera con gradiente
                waiting_time = process.waiting_time
                if waiting_time == 0:
                    color = QColor(76, 217, 100)  # Verde vibrante
                elif waiting_time < 5:
                    color = QColor(255, 204, 0)  # Amarillo dorado
                elif waiting_time < 10:
                    color = QColor(255, 149, 0)  # Naranja
                else:
                    color = QColor(255, 59, 48)  # Rojo vibrante
                
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
        
        # Botón con animación
        run_button = QPushButton("▶ Ejecutar Simulación")
        run_button.clicked.connect(self.run_synchronization)
        self.add_button_shadow(run_button)
        layout.addWidget(run_button)
        
        # Salida de texto
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(QLabel("📝 Resultado:"))
        layout.addWidget(self.output_text)
        
        self.setLayout(layout)
        self.update_config_options()
    
    def add_button_shadow(self, button):
        """Agrega efecto de sombra estilo Glass"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(66, 133, 244, 60))
        shadow.setOffset(0, 6)
        button.setGraphicsEffect(shadow)
    
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
            
            # Animar la actualización del mensaje
            self.animate_success_message()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
    
    def animate_success_message(self):
        """Animación de mensaje de éxito"""
        original_style = self.output_text.styleSheet()
        
        def flash():
            self.output_text.setStyleSheet(original_style + """
                border: 2px solid rgba(76, 217, 100, 0.8);
                background: rgba(76, 217, 100, 0.1);
            """)
            QTimer.singleShot(200, lambda: self.output_text.setStyleSheet(original_style))
        
        flash()


class DemoTab(QWidget):
    """Tab para Demo Completo"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Título con estilo Glass
        title_label = QLabel("🎬 Demostración Completa del Sistema")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: 600;
                color: #424242;
                padding: 24px;
                background: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.9);
                border-radius: 16px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        # Sombra para el título
        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(20)
        title_shadow.setColor(QColor(0, 0, 0, 30))
        title_shadow.setOffset(0, 4)
        title_label.setGraphicsEffect(title_shadow)
        
        layout.addWidget(title_label)
        
        demo_button = QPushButton("▶ Ejecutar Demo Completo")
        demo_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(66, 133, 244, 0.85), stop:1 rgba(52, 168, 83, 0.85));
                color: white;
                font-size: 16px;
                padding: 16px 32px;
                border-radius: 14px;
                font-weight: 600;
                min-width: 200px;
                border: 1px solid rgba(255, 255, 255, 0.6);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(66, 133, 244, 1), stop:1 rgba(52, 168, 83, 1));
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
        """)
        demo_button.clicked.connect(self.run_complete_demo)
        
        # Agregar sombra al botón estilo Glass
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(66, 133, 244, 80))
        shadow.setOffset(0, 8)
        demo_button.setGraphicsEffect(shadow)
        
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
        self.setGeometry(100, 100, 1400, 900)
        
        # Estilo moderno Glass Morphism (estilo Apple)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e3f2fd, stop:0.5 #f5f5f5, stop:1 #fce4ec);
            }
            
            QTabWidget::pane {
                border: none;
                background: rgba(255, 255, 255, 0.7);
                border-radius: 20px;
            }
            
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.6);
                color: #424242;
                padding: 14px 30px;
                margin: 3px;
                border-radius: 12px;
                font-weight: 600;
                font-size: 13px;
                border: 1px solid rgba(255, 255, 255, 0.8);
                min-width: 120px;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(66, 133, 244, 0.9), stop:1 rgba(52, 168, 83, 0.9));
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.9);
            }
            
            QTabBar::tab:hover:!selected {
                background: rgba(255, 255, 255, 0.8);
                border: 1px solid rgba(66, 133, 244, 0.3);
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(66, 133, 244, 0.85), stop:1 rgba(52, 168, 83, 0.85));
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.6);
                border-radius: 14px;
                padding: 14px 28px;
                font-weight: 600;
                font-size: 14px;
                min-height: 25px;
                min-width: 160px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(66, 133, 244, 1), stop:1 rgba(52, 168, 83, 1));
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(52, 103, 214, 0.9), stop:1 rgba(42, 148, 73, 0.9));
                padding: 15px 27px 13px 29px;
            }
            
            QGroupBox {
                background: rgba(255, 255, 255, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.8);
                border-radius: 16px;
                padding: 25px;
                margin-top: 18px;
                font-weight: 600;
                color: #424242;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 8px 18px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(66, 133, 244, 0.9), stop:1 rgba(52, 168, 83, 0.9));
                color: white;
                border-radius: 10px;
                left: 18px;
                font-size: 13px;
            }
            
            QTableWidget {
                background: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.8);
                border-radius: 12px;
                gridline-color: rgba(66, 133, 244, 0.15);
                selection-background-color: rgba(66, 133, 244, 0.3);
                alternate-background-color: rgba(245, 245, 245, 0.5);
            }
            
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
                color: #424242;
            }
            
            QTableWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(66, 133, 244, 0.4), stop:1 rgba(52, 168, 83, 0.4));
                color: #1a1a1a;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(66, 133, 244, 0.85), stop:1 rgba(52, 168, 83, 0.85));
                color: white;
                padding: 12px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }
            
            QTextEdit, QPlainTextEdit {
                background: rgba(255, 255, 255, 0.75);
                color: #2c3e50;
                border: 1px solid rgba(255, 255, 255, 0.8);
                border-radius: 12px;
                padding: 14px;
                font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                selection-background-color: rgba(66, 133, 244, 0.3);
            }
            
            QComboBox {
                background: rgba(255, 255, 255, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                padding: 10px 14px;
                min-width: 180px;
                font-size: 13px;
                color: #424242;
            }
            
            QComboBox:hover {
                border: 1px solid rgba(66, 133, 244, 0.5);
                background: rgba(255, 255, 255, 0.9);
            }
            
            QComboBox::drop-down {
                border: none;
                padding-right: 12px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid rgba(66, 133, 244, 0.8);
                margin-right: 5px;
            }
            
            QComboBox QAbstractItemView {
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                selection-background-color: rgba(66, 133, 244, 0.2);
                padding: 5px;
            }
            
            QSpinBox, QDoubleSpinBox {
                background: rgba(255, 255, 255, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                padding: 10px;
                font-size: 13px;
                color: #424242;
            }
            
            QSpinBox:focus, QDoubleSpinBox:focus {
                border: 1px solid rgba(66, 133, 244, 0.5);
                background: rgba(255, 255, 255, 0.9);
            }
            
            QLabel {
                color: #424242;
                font-size: 13px;
                font-weight: 500;
            }
            
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 0.8);
                border-radius: 12px;
                text-align: center;
                background: rgba(255, 255, 255, 0.6);
                height: 28px;
                color: #424242;
                font-weight: 600;
            }
            
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(66, 133, 244, 0.9), stop:0.5 rgba(52, 168, 83, 0.9), 
                    stop:1 rgba(251, 188, 5, 0.9));
                border-radius: 10px;
            }
            
            QStatusBar {
                background: rgba(255, 255, 255, 0.7);
                color: #424242;
                font-weight: 600;
            }
        """)
        
        # Crear tabs
        self.tabs = QTabWidget()
        
        self.scheduler_tab = SchedulerTab()
        self.sync_tab = SynchronizationTab()
        self.demo_tab = DemoTab()
        
        self.tabs.addTab(self.scheduler_tab, "📋 Planificación")
        self.tabs.addTab(self.sync_tab, "🔄 Sincronización")
        self.tabs.addTab(self.demo_tab, "🎬 Demo")
        
        # Agregar efecto de sombra a las tabs
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 8)
        self.tabs.setGraphicsEffect(shadow)
        
        self.setCentralWidget(self.tabs)
        
        # Barra de estado con animación
        self.statusBar().showMessage("✅ Sistema inicializado correctamente")
        
        # Animación de entrada
        self.animate_window_entrance()
    
    def animate_window_entrance(self):
        """Animación suave de entrada de ventana"""
        self.setWindowOpacity(0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(600)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Simulador de SO")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
