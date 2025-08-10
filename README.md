#### 构建镜像
- docker build -t autosorting:v1.0.1 .
#### 运行容器
- docker run -itd --name autosorting -v /DATA/tmp:/input -v /DATA/music:/output autosorting:v1.0.1
