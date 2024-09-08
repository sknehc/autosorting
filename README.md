#### 构建镜像
- docker build -t Autosorting:amd64 .
#### 运行容器
- docker run -itd --name Autosorting -v /DATA/tmp:/input -v /DATA/music:/output autosorting:amd64