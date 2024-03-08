import os


from dataclasses import dataclass
import os

 
@dataclass(frozen=True)
class EnvConfig:
    db_ip: str
    db_port: int
    db_password: str
    db_name: str
    super_user_name: str
    super_user_password: str
    redis_ip: str
    redis_password: str
    data_path: str
    backend_port: int
    media_path: str

class EnvironmentLoaderSingleton:
    _instance = None
    _loaded_env: EnvConfig = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            env_vars = {
                'db_ip' : os.environ.get('DB_IP', None),
                'db_port': os.environ.get('DB_PORT', None),
                'db_password': os.environ.get('DB_PASSWORD', None),
                'db_name': os.environ.get('DB_NAME', None),
                'super_user_name': os.environ.get('SUPER_USER_NAME', None),
                'super_user_password': os.environ.get('SUPER_USER_PASSWORD', None),
                'redis_ip': os.environ.get('REDIS_IP', None),
                'redis_password': os.environ.get('REDIS_PASSWORD', None),
                'data_path': os.environ.get('BACKEND_INNER_PATH', None),
                'backend_port': os.environ.get('BACKEND_PORT', None),
                'media_path': os.environ.get('BACKEND_MEDIA_PATH', None),
            }
            for key, value in env_vars.items():
                if value is None:
                    raise RuntimeError(f'Environment variable {key} is not set')
            try:
                env_vars['db_port'] = int(env_vars['db_port'])
            except ValueError:
                raise RuntimeError(f'Environment variable db_port type is not integer')
            cls._loaded_env = EnvConfig(**{k: v for k, v in env_vars.items() if v is not None})
        return cls._instance

    def get_env(self) -> EnvConfig:
        return EnvironmentLoaderSingleton._loaded_env