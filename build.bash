#!/bin/bash



help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  sync     Sync files or data."
    echo "  clear    Clear generator data."
    echo "  dev      Run in development mode."
    echo "  prod     Run in production mode."
    echo "  build_front  Build front end."
    echo "  run_front  Run front end."
    echo "  run_full_dev  Run full dev."
    echo "  run_full_prod  Run full prod."
    echo "  zip_prod  Zip production files."
    echo "  sftp_prod  Sftp production files."
    echo "  --help   Show this help."
}

sync() {
    echo "Syncing files..."
    # Add your sync logic here
}

dev() {
    awk -F ',' 'NR>1 {print $1 "=" $6}' env.csv > .env
    sed -i 's/\"\"\"/\"/g' .env
    source .env
    set_value
}

prod() {
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
    rm -rf ./dist.tar.gz
}

set_value() {
    echo "VITE_BACKEND_PATH=${BACKEND_ADDR}" > ./src/clientWeb/.env
    echo "VITE_FRONT_WEB_PORT=${FRONT_WEB_PORT}" >> ./src/clientWeb/.env
    cat ./META/DB/my_template.cnf > ./META/DB/my.cnf
    cat ./META/nginx/nginx_template.conf > ./META/nginx/nginx.conf
    cat ./META/redis/redis_template.conf > ./META/redis/redis.conf
    replace_str="s/\$REPLACE_DB_PORT/${DB_PORT}/g"
    sed -i $replace_str ./META/DB/my.cnf
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

run_full_prod() {
    prod
    build_front
    zip_prod
    clear
    

}

zip_prod() {
    rm -rf dist.tar.gz backend.tar.gz
    cd src/clientWeb/dist
    tar czvf dist.tar.gz --exclude=dist.tar.gz  .
    cp dist.tar.gz ../../../
    cd -
    tar czvf backend.tar.gz --exclude=src/clientWeb --exclude=.vscode --exclude=.git --exclude='__pycache__' --exclude=dist.tar.gz --exclude=backend.tar.gz --exclude=venv  .
}

sftp_prod() {
    scp  backend.tar.gz  ${SYNC_SSH_USER}@${SYNC_SSH_IP}:${SYNC_SSH_BACKEND_DIR}
    scp  dist.tar.gz  ${SYNC_SSH_USER}@${SYNC_SSH_IP}:${SYNC_SSH_FRONT_DIR}
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
    zip_prod)
        zip_prod
        ;;
    run_full_prod)
        run_full_prod
        ;;
    sftp_prod)
        sftp_prod
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