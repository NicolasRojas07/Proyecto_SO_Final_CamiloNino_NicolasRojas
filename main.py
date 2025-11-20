"""
Punto de entrada principal del Simulador de Sistemas Operativos
Autores: Camilo Niño & Nicolás Rojas
Fecha: Noviembre 2025
"""

from menu_principal import MainMenu


def main():
    """
    Función principal que inicia el simulador de SO
    """
    print("=" * 70)
    print(" SIMULADOR DE SISTEMAS OPERATIVOS ".center(70, "="))
    print("=" * 70)
    print("\n👥 Autores: Camilo Niño & Nicolás Rojas")
    print("📅 Proyecto Final - Sistemas Operativos 2025-2\n")
    print("=" * 70)
    
    menu = MainMenu()
    menu.run()


if __name__ == "__main__":
    main()
