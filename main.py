# ==============================================================================
# main.py — AVANCE 3 FINAL: Composición y Módulos
# Autor: José Rosales Ruvalcaba | Materia: Ciberseguridad
#
# DESCRIPCIÓN:
# Archivo principal de ejecución. Solo contiene las importaciones desde
# modelos.py, la instanciación de objetos y las pruebas que demuestran:
# Encapsulamiento, Herencia, Polimorfismo y Composición.
# ==============================================================================

# Importación de las clases desde el módulo modelos.py
from modelos import CuentaBancaria, CuentaAhorros, CuentaCorriente, Transaccion


# ==============================================================================
# INSTANCIACIÓN Y PRUEBAS
# ==============================================================================
if __name__ == "__main__":
    print("=== INICIO DE LAS PRUEBAS ===\n")

    # --- Instanciación: 1 objeto de la clase base y 2 de subclases ---
    base = CuentaBancaria("Valeria Gómez", "CTA-1001", 1500.0, "Básica")
    ahorros = CuentaAhorros("Sofía Ramírez", "CTA-2001", 500.0, tasa_interes=0.04,
                            retiros_maximos=2)
    corriente = CuentaCorriente("Carlos Mendoza", "CTA-3001", 3000.50,
                                comision_retiro=15.0, limite_por_retiro=2000.0)

    print(">>> Estado inicial")
    for cuenta in (base, ahorros, corriente):      # Polimorfismo
        cuenta.mostrar_resumen()
        print()

    # --- Prueba A: Encapsulamiento ---
    print(">>> Prueba A: Encapsulamiento")
    print(f"Saldo leído con getter (@property): ${base.saldo:,.2f}")
    base.saldo = 2000.0
    print(f"Saldo modificado con setter válido: ${base.saldo:,.2f}")
    try:
        base.saldo = -50
    except ValueError as error:
        print(f"Setter bloqueó valor negativo -> ValueError: {error}")
    try:
        print(base.__saldo)
    except AttributeError as error:
        print(f"Acceso directo a __saldo bloqueado -> AttributeError: {error}")
    print()

    # --- Prueba B: Herencia y polimorfismo (retirar sobrescrito) ---
    print(">>> Prueba B: Herencia y sobrescritura de retirar()")
    base.retirar(300.0)
    ahorros.retirar(100.0)
    ahorros.retirar(100.0)
    ahorros.retirar(50.0)                  # Rechazado: límite mensual
    ahorros.aplicar_interes()
    corriente.retirar(2500.0)              # Rechazado: excede límite por operación
    corriente.retirar(1000.0)              # Exitoso con comisión
    corriente.consultar_comisiones()
    print()

    # --- Prueba C: Reglas de estado ---
    print(">>> Prueba C: Cuenta bloqueada")
    corriente.cambiar_estado(False)
    corriente.depositar(100.0)             # Rechazado por cuenta inactiva
    corriente.cambiar_estado(True)
    corriente.depositar(250.0)
    print()

    # --- Prueba D: Composición (la cuenta TIENE objetos Transaccion) ---
    print(">>> Prueba D: Composición (delegación a objetos Transaccion)")
    base.depositar(400.0)
    for cuenta in (base, ahorros, corriente):
        cuenta.mostrar_historial()         # La cuenta delega en cada Transaccion
        print(f"Total ingresos: ${cuenta.total_ingresos():,.2f} | "
              f"Total egresos: ${cuenta.total_egresos():,.2f}\n")

    ultimo = corriente.historial[-1]       # Acceso directo al objeto contenido
    print(f"Último movimiento de {corriente.numero_cuenta}: {ultimo.describir()}")
    print(f"¿Es una instancia de Transaccion? {isinstance(ultimo, Transaccion)}")

    # El historial devuelto es una copia: modificarla no altera el original
    copia = base.historial
    copia.clear()
    print(f"Historial de base tras vaciar la copia: {len(base.historial)} movimientos (intacto)")
    print()

    # --- Prueba E: Independencia de datos y estado final ---
    print(">>> Prueba E: Estado final (datos independientes por objeto)")
    for cuenta in (base, ahorros, corriente):
        cuenta.mostrar_resumen()
        print()

    print(f"isinstance(ahorros, CuentaBancaria) -> {isinstance(ahorros, CuentaBancaria)}")
    print(f"isinstance(corriente, CuentaBancaria) -> {isinstance(corriente, CuentaBancaria)}")
    print("\n=== FIN DE LAS PRUEBAS ===")
