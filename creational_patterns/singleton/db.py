# Implementación del patrón Singleton para configuración de base de datos PostgreSQL.

# Este módulo demuestra un caso de uso productivo del patrón Singleton para manejar
# la configuración de conexión a PostgreSQL, asegurando que solo exista una instancia
# de configuración en toda la aplicación.

import os
from creational_patterns.singleton.decorator import singleton


@singleton
class DatabaseConfig:
    """
    Configuración Singleton para conexión a PostgreSQL.
    
    Esta clase garantiza que solo exista una instancia de configuración en toda
    la aplicación, evitando múltiples lecturas de variables de entorno y
    asegurando consistencia en la configuración.
    
    Variables de entorno:
        DB_HOST: Host del servidor PostgreSQL (default: localhost)
        DB_PORT: Puerto de PostgreSQL (default: 5432)
        DB_USER: Usuario de la base de datos (default: postgres)
        DB_PASSWORD: Contraseña del usuario (default: postgres)
        DB_NAME: Nombre de la base de datos (default: mydatabase)
    """
    
    def __init__(self):
        """
        Inicializa la configuración leyendo variables de entorno.
        
        Este método solo se ejecuta una vez debido al decorador @singleton,
        incluso si se intenta crear múltiples instancias.
        """
        self._host = os.getenv('DB_HOST', 'localhost')
        self._port = int(os.getenv('DB_PORT', '5432'))
        self._user = os.getenv('DB_USER', 'postgres')
        self._password = os.getenv('DB_PASSWORD', 'postgres')
        self._database = os.getenv('DB_NAME', 'mydatabase')
        
        print(f"[Singleton] Configuración de DB inicializada para: {self._host}:{self._port}")
    
    @property
    def host(self) -> str:
        """Retorna el host del servidor PostgreSQL."""
        return self._host
    
    @property
    def port(self) -> int:
        """Retorna el puerto del servidor PostgreSQL."""
        return self._port
    
    @property
    def user(self) -> str:
        """Retorna el usuario de la base de datos."""
        return self._user
    
    @property
    def password(self) -> str:
        """Retorna la contraseña del usuario."""
        return self._password
    
    @property
    def database(self) -> str:
        """Retorna el nombre de la base de datos."""
        return self._database
    
    def get_connection_string(self, hide_password: bool = True) -> str:
        """
        Genera la cadena de conexión para PostgreSQL.
        
        Args:
            hide_password: Si es True, oculta la contraseña en la cadena (default: True)
        
        Returns:
            Cadena de conexión en formato PostgreSQL URI
        """
        password = "****" if hide_password else self._password
        return f"postgresql://{self._user}:{password}@{self._host}:{self._port}/{self._database}"
    
    def get_connection_dict(self) -> dict:
        """
        Retorna un diccionario con los parámetros de conexión.
        
        Returns:
            Diccionario con los parámetros de conexión
        """
        return {
            'host': self._host,
            'port': self._port,
            'user': self._user,
            'password': self._password,
            'database': self._database
        }
    
    def __repr__(self) -> str:
        """Representación string de la configuración."""
        return f"DatabaseConfig(host={self._host}, port={self._port}, database={self._database})"
