# ==============================================================================
# modelos.py — AVANCE 3 FINAL: Composición y Módulos
# Autor: José Rosales Ruvalcaba | Materia: Ciberseguridad
#
# DESCRIPCIÓN DEL MÓDULO:
# Contiene todas las clases del sistema bancario:
# - Transaccion (clase auxiliar para COMPOSICIÓN): representa un movimiento.
# - CuentaBancaria (clase base): encapsula el saldo y el historial, y "tiene"
#   una colección de objetos Transaccion (relación "tiene-un").
# - CuentaAhorros y CuentaCorriente (subclases): heredan con super() y
#   sobrescriben retirar() y mostrar_resumen() (polimorfismo).
# ==============================================================================

from datetime import datetime


# ==============================================================================
# 1. CLASE AUXILIAR PARA COMPOSICIÓN: Transaccion
# ==============================================================================
class Transaccion:
    """Representa un movimiento individual de una cuenta (componente)."""

    # Tipos de movimiento que aumentan o disminuyen el saldo
    TIPOS_INGRESO = ("Depósito", "Interés")
    TIPOS_EGRESO = ("Retiro", "Comisión")

    def __init__(self, tipo, monto, saldo_resultante):
        self.tipo = tipo
        self.monto = monto
        self.saldo_resultante = saldo_resultante
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def es_ingreso(self):
        """Indica si el movimiento suma dinero a la cuenta."""
        return self.tipo in Transaccion.TIPOS_INGRESO

    def describir(self):
        signo = "+" if self.es_ingreso() else "-"
        return (f"{self.fecha} | {self.tipo:<10} | {signo}${self.monto:>10,.2f} "
                f"| Saldo: ${self.saldo_resultante:,.2f}")


# ==============================================================================
# 2. CLASE BASE: CuentaBancaria
# ==============================================================================
class CuentaBancaria:
    """Representa una cuenta bancaria genérica (superclase)."""

    def __init__(self, titular, numero_cuenta, saldo, tipo_cuenta, activa=True):
        # Atributos públicos
        self.titular = titular
        self.numero_cuenta = numero_cuenta
        self.tipo_cuenta = tipo_cuenta
        self.activa = activa

        # ENCAPSULAMIENTO: saldo privado, validado mediante el setter
        self.__saldo = 0.0
        self.saldo = saldo

        # COMPOSICIÓN: la cuenta "tiene" una colección de objetos Transaccion.
        # Atributo privado: solo se modifica mediante _registrar_transaccion().
        self.__historial = []

    # --- Getter (@property) del saldo ---
    @property
    def saldo(self):
        return self.__saldo

    # --- Setter con validaciones ---
    @saldo.setter
    def saldo(self, nuevo_saldo):
        if isinstance(nuevo_saldo, bool) or not isinstance(nuevo_saldo, (int, float)):
            raise TypeError("El saldo debe ser un valor numérico.")
        if nuevo_saldo < 0:
            raise ValueError(f"El saldo no puede ser negativo (recibido: {nuevo_saldo}).")
        self.__saldo = float(nuevo_saldo)

    # --- Getter del historial: devuelve una COPIA para proteger el original ---
    @property
    def historial(self):
        return list(self.__historial)

    # --------------------------------------------------------------------------
    # MÉTODOS DE COMPOSICIÓN (delegan el trabajo en los objetos Transaccion)
    # --------------------------------------------------------------------------
    def _registrar_transaccion(self, tipo, monto):
        """Crea un objeto Transaccion y lo almacena en el historial (protegido)."""
        self.__historial.append(Transaccion(tipo, monto, self.saldo))

    def mostrar_historial(self):
        print(f"--- Historial de {self.numero_cuenta} ({len(self.__historial)} movimientos) ---")
        if not self.__historial:
            print("Sin movimientos registrados.")
        for movimiento in self.__historial:
            print(movimiento.describir())     # Delegación a Transaccion

    def total_ingresos(self):
        return sum(t.monto for t in self.__historial if t.es_ingreso())

    def total_egresos(self):
        return sum(t.monto for t in self.__historial if not t.es_ingreso())

    # --------------------------------------------------------------------------
    # MÉTODOS OPERATIVOS
    # --------------------------------------------------------------------------
    def depositar(self, monto):
        if not self.activa:
            print(f"[{self.numero_cuenta}] Depósito rechazado: la cuenta está inactiva.")
            return False
        if monto <= 0:
            print(f"[{self.numero_cuenta}] Depósito rechazado: el monto debe ser mayor a 0.")
            return False
        self.saldo += monto
        self._registrar_transaccion("Depósito", monto)
        print(f"[{self.numero_cuenta}] Depósito de ${monto:,.2f} exitoso. "
              f"Saldo actual: ${self.saldo:,.2f}")
        return True

    def retirar(self, monto):
        if not self.activa:
            print(f"[{self.numero_cuenta}] Retiro rechazado: la cuenta está inactiva.")
            return False
        if monto <= 0:
            print(f"[{self.numero_cuenta}] Retiro rechazado: el monto debe ser mayor a 0.")
            return False
        if monto > self.saldo:
            print(f"[{self.numero_cuenta}] Retiro rechazado: fondos insuficientes "
                  f"(intentó ${monto:,.2f}, saldo ${self.saldo:,.2f}).")
            return False
        self.saldo -= monto
        self._registrar_transaccion("Retiro", monto)
        print(f"[{self.numero_cuenta}] Retiro de ${monto:,.2f} exitoso. "
              f"Saldo actual: ${self.saldo:,.2f}")
        return True

    def cambiar_estado(self, nuevo_estado):
        self.activa = nuevo_estado
        estado = "ACTIVA" if self.activa else "BLOQUEADA/INACTIVA"
        print(f"[{self.numero_cuenta}] Estado de la cuenta cambiado a: {estado}")

    def mostrar_resumen(self):
        estado = "Activa" if self.activa else "Inactiva"
        print(f"--- Cuenta {self.numero_cuenta} ---\n"
              f"Titular: {self.titular}\n"
              f"Tipo: {self.tipo_cuenta}\n"
              f"Saldo: ${self.saldo:,.2f}\n"
              f"Estado: {estado}\n"
              f"Movimientos registrados: {len(self.__historial)}")


# ==============================================================================
# 3. SUBCLASE: CuentaAhorros (HERENCIA con super())
# ==============================================================================
class CuentaAhorros(CuentaBancaria):
    """Cuenta de ahorros: genera intereses y limita los retiros mensuales."""

    def __init__(self, titular, numero_cuenta, saldo, tasa_interes,
                 retiros_maximos=3, activa=True):
        super().__init__(titular, numero_cuenta, saldo, "Ahorros", activa)
        self.tasa_interes = tasa_interes
        self.retiros_maximos = retiros_maximos
        self._retiros_realizados = 0                # Atributo protegido

    def aplicar_interes(self):
        if not self.activa:
            print(f"[{self.numero_cuenta}] No se puede aplicar interés: cuenta inactiva.")
            return 0.0
        interes = self.saldo * self.tasa_interes
        self.saldo += interes
        self._registrar_transaccion("Interés", interes)   # Composición
        print(f"[{self.numero_cuenta}] Interés aplicado ({self.tasa_interes:.1%}): "
              f"+${interes:,.2f}. Nuevo saldo: ${self.saldo:,.2f}")
        return interes

    # POLIMORFISMO: sobrescritura de métodos
    def retirar(self, monto):
        if self._retiros_realizados >= self.retiros_maximos:
            print(f"[{self.numero_cuenta}] Retiro rechazado: se alcanzó el límite de "
                  f"{self.retiros_maximos} retiros mensuales.")
            return False
        if super().retirar(monto):
            self._retiros_realizados += 1
            return True
        return False

    def mostrar_resumen(self):
        super().mostrar_resumen()
        print(f"Tasa de interés: {self.tasa_interes:.1%}\n"
              f"Retiros usados: {self._retiros_realizados}/{self.retiros_maximos}")


# ==============================================================================
# 4. SUBCLASE: CuentaCorriente (HERENCIA con super())
# ==============================================================================
class CuentaCorriente(CuentaBancaria):
    """Cuenta corriente: cobra comisión por retiro y limita el monto por operación."""

    def __init__(self, titular, numero_cuenta, saldo, comision_retiro,
                 limite_por_retiro, activa=True):
        super().__init__(titular, numero_cuenta, saldo, "Corriente", activa)
        self.comision_retiro = comision_retiro
        self.limite_por_retiro = limite_por_retiro
        self._total_comisiones = 0.0                # Atributo protegido

    def consultar_comisiones(self):
        print(f"[{self.numero_cuenta}] Comisiones acumuladas: ${self._total_comisiones:,.2f}")
        return self._total_comisiones

    # POLIMORFISMO: sobrescritura de métodos
    def retirar(self, monto):
        if monto > self.limite_por_retiro:
            print(f"[{self.numero_cuenta}] Retiro rechazado: ${monto:,.2f} excede el "
                  f"límite por operación de ${self.limite_por_retiro:,.2f}.")
            return False
        if monto + self.comision_retiro > self.saldo:
            print(f"[{self.numero_cuenta}] Retiro rechazado: el saldo no cubre el monto "
                  f"más la comisión de ${self.comision_retiro:,.2f}.")
            return False
        if super().retirar(monto):
            self.saldo -= self.comision_retiro
            self._registrar_transaccion("Comisión", self.comision_retiro)  # Composición
            self._total_comisiones += self.comision_retiro
            print(f"[{self.numero_cuenta}] Comisión cobrada: ${self.comision_retiro:,.2f}. "
                  f"Saldo final: ${self.saldo:,.2f}")
            return True
        return False

    def mostrar_resumen(self):
        super().mostrar_resumen()
        print(f"Comisión por retiro: ${self.comision_retiro:,.2f}\n"
              f"Límite por retiro: ${self.limite_por_retiro:,.2f}")
