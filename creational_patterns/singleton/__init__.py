"""
Patrón Singleton - Garantiza una única instancia de una clase.

Este módulo implementa el patrón de diseño Singleton usando un decorador de clase,
aplicado a un caso de uso real: configuración de base de datos PostgreSQL.

Exports:
    singleton: Decorador para convertir cualquier clase en Singleton
    DatabaseConfig: Configuración Singleton para PostgreSQL
"""

from creational_patterns.singleton.decorator import singleton
from creational_patterns.singleton.db import DatabaseConfig

__all__ = ['singleton', 'DatabaseConfig']
