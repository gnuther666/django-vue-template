# 项目介绍
django + vue + taro 管理系统模板
模板提供基本的前后台分离框架，用来快捷的开发web端 
* 后台: python39 + django + rest + jwt + redis
* web端: vite + vue + element-ui-plus

## 项目启动
* 安装依赖的docker, docker-compose
* 修改好配置参数(具体参看配置参数章节)
* 选择你要执行的版本 dev/prod 各自对应命令 bash build.bash [dev/prod]
* 安装node v21.6.0


## 目录结构
- META 容器配置相关
- src/backend python后端
- src/clientMB taro小程序端
- src/clientWeb vue网页端
- docker-compose.yaml 项目启动文件
- .env_example 运行项目前需要先查看文件内配置式是否符合要求，修改完后copy出.env文件到同级目录下



# 项目截图
## web端
1. 登录
![登录](./doc/login.jpg)

2. 示例页
![示例](./doc/example.jpg)



# 注意事项
1. 因为后端apt源没有修改,所以如果速度慢，最好开启vpn后再开始构建镜像


# 开发进度
* [ ] web端
  * [x] 账户密码登录
  * [x] 文件上传和下载


# 积累
## 热更新
1. wsl2 required
2. sudo apt install watchman
3. add this scope code to vite.config.ts
  ```json
  watch: {
      usePolling: true,
      interval: 1000,
    },
  ```
