import os
import re
import sys, csv


def help():
    print("Usage: python script.py [command]")
    print("")
    print("Commands:")
    print("  dev            Generate development environment to .env and other config files using env.csv.")
    print("  prod           Generate production environment to .env and other config files using env.csv.")
    print("  build_front    Runs 'pnpm run build-only'")
    print("  run_front      Runs 'pnpm run dev'")
    print("  run_full_dev   Generates dev files and sets up the server")
    print("  sync           Syncs files to your server. Update server IP in script.py as needed.")
    print("  clear          Clears generated data.")
    print("  --help/-h      Show this help.")


class Build:
    def __init__(self):
        self.env_dict = dict()

    def dev(self):
        with open('env.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.env_dict[row['config_key']] = row['dev_config']
        self.__replace_env()
        self.__save_config()

    def prod(self):
        with open('env.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.env_dict[row['config_key']] = row['prod_config']
        self.__replace_env()
        self.__save_config()
        self.__replace_docker_compose_prod_mode()

    def build_front(self):
        os.system('npm install -g pnpm')
        os.system('cd src/clientWeb && pnpm install && pnpm run build-only')

    def run_front(self):
        os.system('npm install -g pnpm')
        os.system('cd src/clientWeb && pnpm install && pnpm run dev')

    def run_full_dev(self):
        self.dev()
        os.system('docker-compose up -d --build')
        self.run_front()

    def clear(self):
        os.remove('./src/clientWeb/.env') if os.path.exists('./src/clientWeb/.env') else 0
        os.remove('./META/nginx/nginx.conf') if os.path.exists('./META/nginx/nginx.conf') else 0
        os.remove('./META/redis/redis.conf') if os.path.exists('./META/redis/redis.conf') else 0
        os.remove('./META/DB/my.cnf') if os.path.exists('./META/DB/my.cnf') else 0
        os.remove('./docker-compose.yaml') if os.path.exists('./docker-compose.yaml') else 0
        os.remove('./.env') if os.path.exists('./.env') else 0
        os.remove('./backend.tar.gz') if os.path.exists('./backend.tar.gz') else 0
        os.remove('./src/clientWeb/dist/dist.tar.gz ') if os.path.exists('./src/clientWeb/dist/dist.tar.gz') else 0
        with open('env.csv', 'r') as file:
            reader = csv.DictReader(file)
            with open('env_template.csv', 'w', encoding='utf-8', newline='') as file2:
                fieldnames = ['config_key','important','desc config','example_value','prod_config','dev_config']
                writer = csv.DictWriter(file2, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    row['dev_config'] = None
                    row['prod_config'] = None
                    writer.writerow(row)


    def async_server(self):
        print('not publish')
        #    echo "Syncing files..."
        #    build_front
        #    rsync -avz --exclude=venv --exclude=.vscode-upload.json --exclude=.env --exclude=.vscode --exclude=.git --exclude=clientWeb --exclude=my.cnf --exclude=nginx.conf --exclude=redis.conf  --exclude=__pycache__ /mnt/e/workspace/django-vue-template  root@117.50.187.148:/root
        #    rsync -avz /mnt/e/workspace/django-vue-template/src/clientWeb/dist  root@117.50.187.148:/root

    def __save_config(self):
        # save .env
        with open('.env', 'w', encoding='utf-8') as file:
            for key, value in self.env_dict.items():
                file.write(key + '=' + value + '\n')
        # save front_end.env
        with open('./src/clientWeb/.env', 'w', encoding='utf-8') as file:
            file.write("VITE_BACKEND_PATH=%s\n" % self.env_dict['BACKEND_ADDR'])
            file.write("VITE_FRONT_WEB_PORT=%s\n" % self.env_dict['FRONT_WEB_PORT'])
        # save my.cnf
        with open('./META/DB/my_template.cnf', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for index, value in enumerate(lines):
                if value.find('$REPLACE_DB_PORT') != -1:
                    lines[index] = value.replace('$REPLACE_DB_PORT', self.env_dict['DB_PORT'])
            with open('./META/DB/my.cnf', 'w', encoding='utf-8') as file2:
                for line in lines:
                    file2.write(line)
        # save nginx.conf
        with open('./META/nginx/nginx_template.conf', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for index, value in enumerate(lines):
                if value.find('$REPLACE_BACKEND_IP') != -1:
                    lines[index] = value.replace('$REPLACE_BACKEND_IP', self.env_dict['BACKEND_IP'])
                if value.find('$REPLACE_BACKEND_PORT') != -1:
                    lines[index] = value.replace('$REPLACE_BACKEND_PORT', self.env_dict['BACKEND_PORT'])
                if value.find('$REPLACE_HOST_NAME') != -1:
                    lines[index] = value.replace('$REPLACE_HOST_NAME', self.env_dict['BACKEND_ADDR'])
            with open('./META/nginx/nginx.conf', 'w', encoding='utf-8') as file2:
                for line in lines:
                    file2.write(line)
        # save redis.conf
        with open('./META/redis/redis_template.conf', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for index, value in enumerate(lines):
                if value.find('$REPLACE_REDIS_PORT') != -1:
                    lines[index] = lines[index].replace('$REPLACE_REDIS_PORT', self.env_dict['REDIS_PORT'])
                if value.find('$REPLACE_REDIS_PASSWORD') != -1:
                    lines[index] = lines[index].replace('$REPLACE_REDIS_PASSWORD', self.env_dict['REDIS_PASSWORD'])
            with open('./META/redis/redis.conf', 'w', encoding='utf-8') as file2:
                for line in lines:
                    file2.write(line)
        # save docker-compose.yaml
        with open('docker-compose_template.yaml', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            key_match_patt = r'\$\{[a-zA-Z_]+\}'
            for index, value in enumerate(lines):
                res = re.findall(key_match_patt, value)
                if res:
                    for one_matched in res:
                        key_name = one_matched[2:-1]
                        lines[index] = lines[index].replace(one_matched,
                                                            self.env_dict.get(key_name, '[!!!EXCEPTION VALUE]'))
            with open('docker-compose.yaml', 'w', encoding='utf-8') as file2:
                for line in lines:
                    file2.write(line)

        # replace_docker_compose

    def __replace_env(self):
        key_match_patt = r'\$\{[a-zA-Z_]+\}'
        for key, value in self.env_dict.items():
            res = re.search(key_match_patt, value)
            if res:
                matched = res.group(0)
                key_name = matched[2:-1]
                self.env_dict[key] = self.env_dict[key].replace(matched, self.env_dict[key_name])
            if value[0] == "\"" or value[0] == "'":
                self.env_dict[key] = self.env_dict[key][1:]
            if value[-1] == "\"" or value[-1] == "'":
                self.env_dict[key] = self.env_dict[key][0:-1]

    def __replace_docker_compose_prod_mode(self):
        with open('docker-compose.yaml', 'r') as file:
            lines = file.readlines()
            for index, value in enumerate(lines):
                if value.find('#PROD') != -1:
                    lines[index] = value.replace('#PROD', '')
        with open('docker-compose.yaml', 'w') as file2:
            for line in lines:
                file2.write(line)


if __name__ == "__main__":
    args = sys.argv[1:]
    builder = Build()
    if len(args) == 0 or args[0] == "--help" or args[0] == "-h":
        help()
    elif args[0] == 'dev':
        builder.dev()
    elif args[0] == 'prod':
        builder.prod()
    elif args[0] == 'async':
        builder.async_server()
    elif args[0] == 'build_front':
        builder.build_front()
    elif args[0] == 'run_full_dev':
        builder.run_full_dev()
    elif args[0] == 'clear':
        builder.clear()
    else:
        print('error usage, you can use command as subtext')
        help()
