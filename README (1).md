# Proyecto Final POO – Sistema de Cuentas Bancarias

**Autor:** José Rosales Ruvalcaba · **Materia:** Ciberseguridad

Sistema bancario en Python que integra **Encapsulamiento, Herencia, Polimorfismo, Composición y Modularización**.

## Estructura del repositorio
```
├── modelos.py               # Clases: Transaccion, CuentaBancaria, CuentaAhorros, CuentaCorriente
├── main.py                  # Importaciones, instanciación y pruebas
├── README.md
└── assets/
    └── diagrama_uml.png     # Diagrama UML final
```

## Ejecución
```bash
python main.py
```
(Requiere Python 3.8+; no usa librerías externas.)

## Conceptos aplicados
| Concepto | Dónde se aplica |
|---|---|
| Encapsulamiento | `__saldo` y `__historial` privados; `@property` con validación; `historial` devuelve una copia |
| Herencia + `super()` | `CuentaAhorros` y `CuentaCorriente` heredan de `CuentaBancaria` |
| Polimorfismo | `retirar()` y `mostrar_resumen()` sobrescritos en las subclases |
| Composición | `CuentaBancaria` **tiene** una lista de objetos `Transaccion` y delega en ellos (`mostrar_historial`, `total_ingresos`, `total_egresos`) |
| Modularización | Clases en `modelos.py`; `main.py` solo importa y prueba |

## Diagrama UML
![Diagrama UML](assets/diagrama_uml.png)
