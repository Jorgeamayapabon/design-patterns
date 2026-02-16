"""
Casos de uso del patrón Singleton aplicado a configuración de base de datos.

Este módulo demuestra cómo el patrón Singleton garantiza que solo exista una
instancia de configuración en toda la aplicación, sin importar cuántas veces
se intente crear.
"""

import os
from creational_patterns.singleton.db import DatabaseConfig


def ejemplo_1_instancia_unica():
    """
    Demuestra que múltiples llamadas crean la misma instancia.
    """
    print("\n" + "="*70)
    print("EJEMPLO 1: Instancia única")
    print("="*70)
    
    print("\n1. Creando primera 'instancia' de DatabaseConfig...")
    config1 = DatabaseConfig()
    
    print("\n2. Creando segunda 'instancia' de DatabaseConfig...")
    config2 = DatabaseConfig()
    
    print("\n3. Creando tercera 'instancia' de DatabaseConfig...")
    config3 = DatabaseConfig()
    
    print("\n4. Verificando que todas son la misma instancia:")
    print(f"   config1 is config2: {config1 is config2}")
    print(f"   config2 is config3: {config2 is config3}")
    print(f"   config1 is config3: {config1 is config3}")
    
    print(f"\n5. IDs de memoria:")
    print(f"   config1: {id(config1)}")
    print(f"   config2: {id(config2)}")
    print(f"   config3: {id(config3)}")


def ejemplo_2_acceso_configuracion():
    """
    Demuestra cómo acceder a la configuración desde cualquier parte del código.
    """
    print("\n" + "="*70)
    print("EJEMPLO 2: Acceso a la configuración")
    print("="*70)
    
    config = DatabaseConfig()
    
    print(f"\n1. Parámetros de conexión:")
    print(f"   Host: {config.host}")
    print(f"   Port: {config.port}")
    print(f"   User: {config.user}")
    print(f"   Database: {config.database}")
    
    print(f"\n2. Cadena de conexión (contraseña oculta):")
    print(f"   {config.get_connection_string()}")
    
    print(f"\n3. Cadena de conexión (contraseña visible):")
    print(f"   {config.get_connection_string(hide_password=False)}")
    
    print(f"\n4. Diccionario de conexión:")
    conn_dict = config.get_connection_dict()
    for key, value in conn_dict.items():
        display_value = "****" if key == "password" else value
        print(f"   {key}: {display_value}")


def ejemplo_3_uso_practico():
    """
    Simula un caso de uso real: múltiples módulos accediendo a la configuración.
    """
    print("\n" + "="*70)
    print("EJEMPLO 3: Uso práctico - Múltiples módulos")
    print("="*70)
    
    # Simula un módulo de conexión a DB
    def modulo_conexion():
        config = DatabaseConfig()
        print(f"\n[Módulo Conexión] Conectando a: {config.get_connection_string()}")
        return config
    
    # Simula un módulo de migración
    def modulo_migracion():
        config = DatabaseConfig()
        print(f"[Módulo Migración] Ejecutando migración en: {config.database}")
        return config
    
    # Simula un módulo de backup
    def modulo_backup():
        config = DatabaseConfig()
        print(f"[Módulo Backup] Respaldando base de datos: {config.database}")
        return config
    
    config_conn = modulo_conexion()
    config_mig = modulo_migracion()
    config_bkp = modulo_backup()
    
    print(f"\n¿Todos los módulos usan la misma configuración?")
    print(f"   {config_conn is config_mig is config_bkp}")


def ejemplo_4_variables_entorno():
    """
    Demuestra cómo cambiar la configuración usando variables de entorno.
    """
    print("\n" + "="*70)
    print("EJEMPLO 4: Configuración con variables de entorno")
    print("="*70)
    
    print("\n1. Configuración actual:")
    config = DatabaseConfig()
    print(f"   {config}")
    
    print("\n2. Nota: Para cambiar la configuración, establece variables de entorno:")
    print("   export DB_HOST=production-db.example.com")
    print("   export DB_PORT=5433")
    print("   export DB_USER=app_user")
    print("   export DB_PASSWORD=secure_password")
    print("   export DB_NAME=production_db")
    
    print("\n3. Valores actuales de variables de entorno:")
    env_vars = ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    for var in env_vars:
        value = os.getenv(var, 'No definida')
        display_value = "****" if var == "DB_PASSWORD" and value != "No definida" else value
        print(f"   {var}: {display_value}")


def main():
    """
    Ejecuta todos los ejemplos del patrón Singleton.
    """
    print("\n" + "="*70)
    print("DEMOSTRACIÓN DEL PATRÓN SINGLETON")
    print("Configuración de Base de Datos PostgreSQL")
    print("="*70)
    
    ejemplo_1_instancia_unica()
    ejemplo_2_acceso_configuracion()
    ejemplo_3_uso_practico()
    ejemplo_4_variables_entorno()
    
    print("\n" + "="*70)
    print("CONCLUSIÓN")
    print("="*70)
    print("""
El patrón Singleton garantiza:
✓ Una única instancia de configuración en toda la aplicación
✓ Acceso global consistente desde cualquier módulo
✓ Inicialización única (las variables de entorno se leen solo una vez)
✓ Gestión eficiente de recursos compartidos
    """)


if __name__ == "__main__":
    main()
