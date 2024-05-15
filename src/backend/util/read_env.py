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
    log_path: str
    backend_url: str
    is_https: bool

class GetEnv:
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
                'log_path': os.environ.get('BACKEND_LOG_PATH', None),
                'backend_url': os.environ.get('BACKEND_ADDR', None),
                'is_https': os.environ.get('IS_HTTPS', 'FALSE')
            }
            if env_vars['is_https'] == 'FALSE':
                env_vars['is_https'] = False
            else:
                env_vars['is_https'] = True
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
        return GetEnv._loaded_env
    
def get_web_res_web_url(local_path):
    if local_path.find('/backend/media/') == -1:
        new_path = '/backend/media/' + local_path
    else:
        new_path = local_path
    full_path = GetEnv().get_env().backend_url + new_path
    full_path = full_path.replace('//', '/')
    full_path = 'https://' if GetEnv().get_env().is_https else 'http://' + full_path
    return full_path

