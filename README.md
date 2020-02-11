# autoTradeRobot

数字货币机器人


**项目结构** 
```
autoTradeRobot
│
├─ExAPIs 交易所API 这里继承ccxt.exchange
│
├─ExWss 交易所websocket
│
├─Modules 模型，负责交易逻辑
│
├─Robots 机器人实体类
│  
├─Tools 工具包
│ 
└─run.py 启动入口

```
<br>

docker build -t robotimage .

docker run -d -h robot --name robot --net quantitative --restart always --privileged=true -v /home/admin/autoTradeRobot:/src robotimage python3 -u /src/run.py
docker run -d -h data_collection --name data_collection --net quantitative --restart always --privileged=true -v /home/admin/autoTradeRobot:/src robotimage python3 -u /src/data_collection.py
