# Avance 2 – Herencia, Encapsulamiento y UML (CuentaBancaria)

**Autor:** José Rosales Ruvalcaba · **Materia:** Ciberseguridad

Extensión del Avance 1 (`CuentaBancaria`) aplicando encapsulamiento, herencia y polimorfismo.

## Estructura
```
avance2-cuenta-bancaria/
├── main.py                  # Código fuente (clase base, subclases y pruebas)
├── README.md
└── assets/
    └── diagrama_uml.png     # Diagrama UML de la jerarquía
```

## Ejecución
```bash
python main.py
```

## Resumen
| Requisito | Implementación |
|---|---|
| Encapsulamiento | `__saldo` privado + `@property` / `@saldo.setter` con validación (no negativos, solo numéricos) |
| Atributos protegidos | `_retiros_realizados`, `_total_comisiones` |
| Herencia + `super()` | `CuentaAhorros` y `CuentaCorriente` heredan de `CuentaBancaria` (2 atributos nuevos cada una) |
| Override | `retirar()` y `mostrar_resumen()` en ambas subclases |
| Métodos operativos | `depositar`, `retirar`, `cambiar_estado`, `mostrar_resumen`, `aplicar_interes`, `consultar_comisiones` |
| Pruebas | 1 objeto base + 2 subclases, validación del setter, acceso bloqueado a `__saldo`, independencia de datos |

## Diagrama UML
![Diagrama UML](assets/diagrama_uml.png)
