# ==============================================================================
# AVANCE 2: Herencia, Encapsulamiento y Diagrama UML
# Autor: José Rosales Ruvalcaba | Materia: Ciberseguridad
#
# DESCRIPCIÓN DEL SISTEMA:
# Sistema bancario sencillo que amplía la clase CuentaBancaria del Avance 1.
# - CuentaBancaria (clase base): protege el saldo con encapsulamiento (atributo
#   privado + @property con validaciones) y ofrece depósitos, retiros, cambio de
#   estado y resumen.
# - CuentaAhorros (subclase): añade tasa de interés y límite de retiros
#   mensuales; sobrescribe retirar() y mostrar_resumen().
# - CuentaCorriente (subclase): añade comisión por retiro y límite por
#   operación; sobrescribe retirar() y mostrar_resumen().
# ==============================================================================


# ==============================================================================
# 1. CREACIÓN DE LA CLASE BASE
# ==============================================================================
class CuentaBancaria:
    """Representa una cuenta bancaria genérica (superclase)."""

    def __init__(self, titular, numero_cuenta, saldo, tipo_cuenta, activa=True):
        # Atributos públicos
        self.titular = titular
        self.numero_cuenta = numero_cuenta
        self.tipo_cuenta = tipo_cuenta
        self.activa = activa

        # ----------------------------------------------------------------------
        # 2. APLICACIÓN DE ENCAPSULAMIENTO
        # El saldo es PRIVADO (__saldo). Se asigna mediante el setter de la
        # propiedad, por lo que la validación se aplica desde la creación.
        # ----------------------------------------------------------------------
        self.__saldo = 0.0
        self.saldo = saldo

    # --- Getter (@property) del atributo privado ---
    @property
    def saldo(self):
        """Consulta el saldo de forma controlada."""
        return self.__saldo

    # --- Setter con validaciones ---
    @saldo.setter
    def saldo(self, nuevo_saldo):
        """Modifica el saldo solo si es un número no negativo."""
        if isinstance(nuevo_saldo, bool) or not isinstance(nuevo_saldo, (int, float)):
            raise TypeError("El saldo debe ser un valor numérico.")
        if nuevo_saldo < 0:
            raise ValueError(f"El saldo no puede ser negativo (recibido: {nuevo_saldo}).")
        self.__saldo = float(nuevo_saldo)

    # --------------------------------------------------------------------------
    # MÉTODOS OPERATIVOS DE LA CLASE BASE
    # --------------------------------------------------------------------------
    # Método 1: depositar
    def depositar(self, monto):
        if not self.activa:
            print(f"[{self.numero_cuenta}] Depósito rechazado: la cuenta está inactiva.")
            return False
        if monto <= 0:
            print(f"[{self.numero_cuenta}] Depósito rechazado: el monto debe ser mayor a 0.")
            return False
        self.saldo += monto  # Usa getter y setter
        print(f"[{self.numero_cuenta}] Depósito de ${monto:,.2f} exitoso. "
              f"Saldo actual: ${self.saldo:,.2f}")
        return True

    # Método 2: retirar (será sobrescrito en las subclases)
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
        print(f"[{self.numero_cuenta}] Retiro de ${monto:,.2f} exitoso. "
              f"Saldo actual: ${self.saldo:,.2f}")
        return True

    # Método 3: cambiar_estado
    def cambiar_estado(self, nuevo_estado):
        self.activa = nuevo_estado
        estado = "ACTIVA" if self.activa else "BLOQUEADA/INACTIVA"
        print(f"[{self.numero_cuenta}] Estado de la cuenta cambiado a: {estado}")

    # Método 4: mostrar_resumen (será sobrescrito en las subclases)
    def mostrar_resumen(self):
        estado = "Activa" if self.activa else "Inactiva"
        print(f"--- Cuenta {self.numero_cuenta} ---\n"
              f"Titular: {self.titular}\n"
              f"Tipo: {self.tipo_cuenta}\n"
              f"Saldo: ${self.saldo:,.2f}\n"
              f"Estado: {estado}")


# ==============================================================================
# 3. USO DE super() Y HERENCIA: SUBCLASE CuentaAhorros
# ==============================================================================
class CuentaAhorros(CuentaBancaria):
    """Cuenta de ahorros: genera intereses y limita los retiros mensuales."""

    def __init__(self, titular, numero_cuenta, saldo, tasa_interes,
                 retiros_maximos=3, activa=True):
        # super() reutiliza el constructor de la clase padre
        super().__init__(titular, numero_cuenta, saldo, "Ahorros", activa)
        # Atributos nuevos propios de la subclase
        self.tasa_interes = tasa_interes            # Ej. 0.04 = 4% anual
        self.retiros_maximos = retiros_maximos
        self._retiros_realizados = 0                # Atributo PROTEGIDO

    # Método 5 (propio de la subclase): aplicar interés
    def aplicar_interes(self):
        if not self.activa:
            print(f"[{self.numero_cuenta}] No se puede aplicar interés: cuenta inactiva.")
            return 0.0
        interes = self.saldo * self.tasa_interes
        self.saldo += interes
        print(f"[{self.numero_cuenta}] Interés aplicado ({self.tasa_interes:.1%}): "
              f"+${interes:,.2f}. Nuevo saldo: ${self.saldo:,.2f}")
        return interes

    # ----------------------------------------------------------------------
    # 4. SOBRESCRITURA DE MÉTODOS (POLIMORFISMO)
    # ----------------------------------------------------------------------
    def retirar(self, monto):
        # Regla extra: límite de retiros mensuales
        if self._retiros_realizados >= self.retiros_maximos:
            print(f"[{self.numero_cuenta}] Retiro rechazado: se alcanzó el límite de "
                  f"{self.retiros_maximos} retiros mensuales.")
            return False
        # Se reutiliza la lógica del padre con super()
        if super().retirar(monto):
            self._retiros_realizados += 1
            return True
        return False

    def mostrar_resumen(self):
        super().mostrar_resumen()  # Extiende el comportamiento del padre
        print(f"Tasa de interés: {self.tasa_interes:.1%}\n"
              f"Retiros usados: {self._retiros_realizados}/{self.retiros_maximos}")


# ==============================================================================
# 3. USO DE super() Y HERENCIA: SUBCLASE CuentaCorriente
# ==============================================================================
class CuentaCorriente(CuentaBancaria):
    """Cuenta corriente: cobra comisión por retiro y limita el monto por operación."""

    def __init__(self, titular, numero_cuenta, saldo, comision_retiro,
                 limite_por_retiro, activa=True):
        super().__init__(titular, numero_cuenta, saldo, "Corriente", activa)
        # Atributos nuevos propios de la subclase
        self.comision_retiro = comision_retiro
        self.limite_por_retiro = limite_por_retiro
        self._total_comisiones = 0.0                # Atributo PROTEGIDO

    # Método 5 (propio de la subclase): consultar comisiones acumuladas
    def consultar_comisiones(self):
        print(f"[{self.numero_cuenta}] Comisiones acumuladas: ${self._total_comisiones:,.2f}")
        return self._total_comisiones

    # Sobrescritura de retirar() (Polimorfismo)
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
            self.saldo -= self.comision_retiro      # Cobro de comisión vía setter
            self._total_comisiones += self.comision_retiro
            print(f"[{self.numero_cuenta}] Comisión cobrada: ${self.comision_retiro:,.2f}. "
                  f"Saldo final: ${self.saldo:,.2f}")
            return True
        return False

    def mostrar_resumen(self):
        super().mostrar_resumen()
        print(f"Comisión por retiro: ${self.comision_retiro:,.2f}\n"
              f"Límite por retiro: ${self.limite_por_retiro:,.2f}")


# ==============================================================================
# 5. INSTANCIACIÓN Y PRUEBAS
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
    for c in (base, ahorros, corriente):   # Polimorfismo: mismo método, distinto resultado
        c.mostrar_resumen()
        print()

    # --- Prueba A: Encapsulamiento ---
    print(">>> Prueba A: Encapsulamiento")
    print(f"Saldo leído con getter (@property): ${base.saldo:,.2f}")
    base.saldo = 2000.0                    # Setter válido
    print(f"Saldo modificado con setter válido: ${base.saldo:,.2f}")
    try:
        base.saldo = -50                   # Setter inválido
    except ValueError as error:
        print(f"Setter bloqueó valor negativo -> ValueError: {error}")
    try:
        print(base.__saldo)                # El atributo privado no es accesible directamente
    except AttributeError as error:
        print(f"Acceso directo a __saldo bloqueado -> AttributeError: {error}")
    print()

    # --- Prueba B: Herencia y método sobrescrito (retirar) ---
    print(">>> Prueba B: Herencia y sobrescritura de retirar()")
    base.retirar(300.0)                    # Versión de la clase base
    ahorros.retirar(100.0)                 # Cuenta como retiro 1/2
    ahorros.retirar(100.0)                 # Retiro 2/2
    ahorros.retirar(50.0)                  # Rechazado: límite mensual
    ahorros.aplicar_interes()              # Método propio de la subclase
    corriente.retirar(2500.0)              # Rechazado: excede límite por operación
    corriente.retirar(1000.0)              # Exitoso con comisión
    corriente.consultar_comisiones()       # Método propio de la subclase
    print()

    # --- Prueba C: Reglas de estado ---
    print(">>> Prueba C: Cuenta bloqueada")
    corriente.cambiar_estado(False)
    corriente.depositar(100.0)             # Rechazado por cuenta inactiva
    print()

    # --- Prueba D: Independencia de datos (cada objeto con su propio self) ---
    print(">>> Prueba D: Estado final (datos independientes)")
    for c in (base, ahorros, corriente):
        c.mostrar_resumen()
        print()

    print(f"isinstance(ahorros, CuentaBancaria) -> {isinstance(ahorros, CuentaBancaria)}")
    print(f"isinstance(corriente, CuentaBancaria) -> {isinstance(corriente, CuentaBancaria)}")
    print("\n=== FIN DE LAS PRUEBAS ===")
