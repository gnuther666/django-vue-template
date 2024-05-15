#!/bin/bash

base_dir=`pwd`

help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  dev            generator development environment to .env and other config file use env.csv ."
    echo "  prod           generator product enviroment to .env and other config file use env.csv"
    echo "  build_front    this command real is use 'pnpm run build-only' "
    echo "  run_front      this command real is use 'pnpm run dev' "
    echo "  run_full_dev   gen dev files and setup server"
    echo "  sync           Sync files to your server, if use this command you need change your server ip in build.bash +22H."
    echo "  clear          Clear generator data."
    echo "  --help         Show this help."
}

sync() {
    echo "Syncing files..."
    build_front
    rsync -avz --exclude=venv --exclude=.vscode-upload.json --exclude=.env --exclude=.vscode --exclude=.git --exclude=clientWeb --exclude=my.cnf --exclude=nginx.conf --exclude=redis.conf  --exclude=__pycache__ /mnt/e/workspace/django-vue-template  root@117.50.187.148:/root
    rsync -avz /mnt/e/workspace/django-vue-template/src/clientWeb/dist  root@117.50.187.148:/root
}

dev() {
    clear
    awk -F ',' 'NR>1 {print $1 "=" $6}' env.csv > .env
    sed -i 's/\"\"\"/\"/g' .env
    source .env
    set_value
}

prod() {
    clear
    awk -F ',' 'NR>1 {print $1 "=" $5}' env.csv > .env
    sed -i 's/\"\"\"/\"/g' .env
    source .env
    set_value
    prod_docker_compose
}

clear() {
    rm  -rf ./src/clientWeb/.env
    rm -rf ./META/nginx/nginx.conf
    rm -rf ./META/redis/redis.conf
    rm -rf ./META/DB/my.cnf
    rm -rf ./docker-compose.yaml
    rm -rf ./.env
    rm -rf ./backend.tar.gz
    rm -rf ./src/clientWeb/dist/dist.tar.gz 
}

set_value() {
    source .env
    echo "VITE_BACKEND_PATH=${BACKEND_ADDR}" > ./src/clientWeb/.env
    echo "VITE_FRONT_WEB_PORT=${FRONT_WEB_PORT}" >> ./src/clientWeb/.env
    cat ./META/DB/my_template.cnf > ./META/DB/my.cnf
    cat ./META/nginx/nginx_template.conf > ./META/nginx/nginx.conf
    cat ./META/redis/redis_template.conf > ./META/redis/redis.conf
    replace_str="s/\$REPLACE_DB_PORT/${DB_PORT}/g"
    sed -i $replace_str ./META/DB/my.cnf
    echo ${BACKEND_IP}
    sed -i "s/\$REPLACE_BACKEND_IP/${BACKEND_IP}/g" ./META/nginx/nginx.conf
    sed -i "s/\$REPLACE_BACKEND_PORT/${BACKEND_PORT}/g" ./META/nginx/nginx.conf
    sed -i "s/\$REPLACE_HOST_NAME/${BACKEND_ADDR}/g" ./META/nginx/nginx.conf
    sed -i "s/\$REPLACE_REDIS_PORT/${REDIS_PORT}/g" ./META/redis/redis.conf
    sed -i "s/\$REPLACE_REDIS_PASSWORD/${REDIS_PASSWORD}/g" ./META/redis/redis.conf

    cat docker-compose_template.yaml > docker-compose.yaml

}

build_front() {
    npm install -g pnpm
    cd src/clientWeb && pnpm install && pnpm run build-only
}

run_front() {
    npm install -g pnpm
    cd src/clientWeb && pnpm install && pnpm run dev
}


prod_docker_compose() {
    sed -i "s/\#PROD//g" docker-compose.yaml
}

run_full_dev() {
    dev
    docker-compose up -d --build
    run_front
}



# 参数处理
case "$1" in
    sync)
        sync
        ;;
    dev)
        dev
        ;;
    prod)
        prod
        ;;
    clear)
        clear
        ;;
    build_front)
        build_front
        ;;
    run_front)
        run_front
        ;;
    run_full_dev)
        run_full_dev
        ;;
    --help)
        help
        ;;
    *)
        echo "Invalid command. Use --help for available options."
        exit 1
        ;;
esac

exit 0