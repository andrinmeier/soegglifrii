import os
from typing import List
import paramiko
import sys

class MySFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target, excluded_dirs: List[str] = []):
        for item in os.listdir(source):
            if item in excluded_dirs:
                print(f"Skipping {item} file/folder.")
                continue
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), '%s/%s' % (target, item))
            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        try:
            super(MySFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise

def get_env_str(key) -> str:
    if key not in os.environ:
        return ""
    return os.environ[key]

def get_env_int(key) -> str:
    if key not in os.environ:
        return -1
    value = os.environ[key]
    if not value.isdigit():
        raise Exception(f"Expected ENV.{key} to be a number.")
    return int(value)

def get_env_str_array(key, split_by = ',') -> str:
    if key not in os.environ:
        return []
    value = os.environ[key]
    return value.split(split_by)


sftp = None
try:
    local_path = get_env_str("DEPLOYMENT_LOCAL_PATH")
    remote_path = get_env_str("DEPLOYMENT_REMOTE_PATH")
    HOST = get_env_str("DEPLOYMENT_HOST")
    PORT = get_env_int("DEPLOYMENT_PORT")
    USERNAME = get_env_str("DEPLOYMENT_USERNAME")
    PASSWORD = get_env_str("DEPLOYMENT_PASSWORD")
    excluded_dirs = get_env_str_array("DEPLOYMENT_EXCLUDED_DIRS")
    script_name = os.path.basename(__file__)
    excluded_dirs.append(script_name)
    transport = paramiko.Transport((HOST, PORT))
    transport.connect(username=USERNAME, password=PASSWORD)
    sftp = MySFTPClient.from_transport(transport)
    sftp.put_dir(local_path, remote_path, excluded_dirs=excluded_dirs)
    sftp.close()
except Exception as ex:
    print("Deployment failed.")
    print(repr(ex))
    sys.exit(1)
finally:
    if sftp is not None:
        sftp.close()