#!/bin/bash



help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  sync     Sync files or data."
    echo "  dev      Run in development mode."
    echo "  prod     Run in production mode."
    echo "  --help   Show this help."
}

sync() {
    echo "Syncing files..."
    # Add your sync logic here
}

dev() {
    source .env
    set_value
}

prod() {
    source .env_pord
    set_value
    prod_docker_compose
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
    sed -i "s/\$REPLACE_REDIS_PORT/${REDIS_PORT}/g" ./META/redis/redis.conf
    sed -i "s/\$REPLACE_REDIS_PASSWORD/${REDIS_PASSWORD}/g" ./META/redis/redis.conf

    cat docker-compose_template.yaml > docker-compose.yaml

}

prod_docker_compose() {
    sed -i "s/\#PROD//g" docker-compose.yaml
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
    --help)
        help
        ;;
    *)
        echo "Invalid command. Use --help for available options."
        exit 1
        ;;
esac

exit 0