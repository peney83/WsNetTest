# Websocket通讯约定文档

[toc]

## 版本更新
### 1.0.19 by victor 20191105 作为1.5.1版本处理
* 自动检测设备的品牌名称和门店编号，如果与当前的不一致，则发消息给前端，前端确认进行重新激活时要走license指令;
### 1.0.18 by victor 20191101 作为1.5.1版本处理
* 增加json和离线场景字段;
### 1.0.17 by victor 20191031 作为1.5.1版本处理
* 对接新接口，允许前端请求更新一些如二维码前缀;
* 品牌信息可以支持前端请求更新，并跟状态查询一起定时检查
### 1.0.16 by victor 20191022 作为1.5.1版本处理
* 增加服务端通畅状态，前端在界面上显示该状态，服务端提供1个接口用于状态检测；该状态用于扫描后的二维码显示逻辑(如果通畅，则让用户等待一定时间显示在线二维码，在等待时间内收到扫描结果更新，超过时间则还是显示离线二维码，建议前端把等待扫描结果和等待在线二维码时间分开)；
* 给前端的数据列表，如果stl不存在或是测量结果不正常的要过滤掉；
* 在调试状态下，设备free状态不反馈；
* 微信二维码下，增加二维码的组合内容；
* 上传数据的定时间隔，在配置文件中调整间隔为默认1小时；
* 扫描得到的点云数据进行判断，少于一定阀值的判断为失败，与原来的直接失败错误码进行分离；
* 扫描指令添加Requestid，在结果和数据列表中返回；
### 1.0.15 by victor 20190912
* 用户信息添加birthday、operator这2个字段
### 1.0.14 by victor 20190906
* 数据有更新时单独再推送，走files/scan/update这个Topic；目前数据主动推的就是扫描结果及数据有更新时;
* 数据状态统计推送，前端也可以用action=statistics来提取(Topic: files/scan/action)
### 1.0.13 by victor
* 数据4种状态增加fail类型，表示上传失败
### 1.0.12 by victor
* 添加1.4版本需求接口，见后面部分
### 1.0.11 by victor
* 状态添加当前占用设备的padid
### 1.0.10 by victor
* 拆分需要网络请求下无线未设置和门店未绑定的状态区分
### 1.0.9 by victor
* 取品牌信息如果信息不存在，则返回网络问题提示600104
* 取门店列表时，如果网络不通则返回600104
* 获取门店时，如果网络不通则返回600104
* 绑定门店时，如果网络不通则返回600104
* 解绑门店时，如果网络不通则返回600104
* 手工触发数据上传时，如果网络不通则记录错误日志
### 1.0.8 by victor
* 添加equipment/scan/result
### 1.0.7 by victor
* 标定结果调整
### 1.0.6 by victor
* 门店信息调整
### 1.0.5 by victor
* 门店和授权方式调整
### 1.0.5 by victor
* 数据增加分页约定
### 1.0.4 by victor
* 增加激活绑定接口格式
### 1.0.3 by victor
* 调整部分接口格式
### 1.0.2 by victor
* 调整数据保存格式
### 1.0.1 by victor
* 基于3.12日会议调整格式，所有指令加入"padId"
* 调整为标准的json格式
* 补充设备状态
* 加入由阿里同学须做的TODO
### 1.0.0 by victor
* 基于姚黄提供的原来api document制定初始的扫描、标定等指令，指令执行结果，设备及设备端程序状态，这3部分的websocket通讯格式

## 格式说明

### SOCKET message

```json
{
  "topic": "",  // 消息话题
  "padId": "", //操作pad的唯一id，由前端生成，在扫描和标定这些设备操作相关的指令过程中需要使用到，其它的根据产品需求定
  "data": {} // 消息内容
}
```

### params约定
```json
scanId //指单次扫描的唯一识别id，组成规则是 DEVICEID-YYYYMMDD-HHmmss, DEVICEID在用户首次激活时从服务器获取（由慕岳的授权接口返回）
padId //操作pad的唯一id，由前端生成，在扫描和标定这些设备操作相关的指令过程中需要使用到，其它的根据产品需求定;前端每次请求时必须要提供
```

授权接口要返回商铺的一些信息，需要慕岳来补充
// DONE 待慕岳与姚黄、孟焦确定

## 配置文件 .server.json 说明
```json
{
    "log": { //本程序的日志输出设置
        "output": "file",
        "path": "logs/fa.log", //可以修改本程序运行日志的保存目录和文件名
        "level": "info",  //正式运行时，level为error
        "max": 10,
        "maxAge": 30,
        "localtime": true //本地时间显示
    },
    ...
    "http": {
        "port": ":80", //http服务端口
        "static":{
            "path":"xxx", //http服务的静态前端页面放置目录
            "urlPrefix":"/s", //http服务的静态前端页面前缀路径
            ...
            "fileUrlPrefix":"/f", //http服务的扫描数据前缀路径
            "logUrlPrefix":"/l", //http服务的本程序日志文件列表前缀路径
            "logSdkUrlPrefix": "/s",//http服务的sdk程序日志文件列表前缀路径
            "logNSUrlPrefix": "/ns",//http服务的ns程序日志文件列表前缀路径
            "logOLUrlPrefix": "/ol"//http服务的onlineupdate程序日志文件列表前缀路径
        },
        "fsUrl": "xxx", // 模拟给前端发ws消息的url
        ...
    },
    "ws": {
        ...
        "urlPrefix":"/aliscan" //websocket服务前缀路径，给前端的
    },
    "api":{
        "taobao":{
            "url":"https://eco.taobao.com/router/rest", // taobao api 地址
            "appKey":"xxx", 
            "appSecret":"xxx",
            "token":"a15e03698369fbdaae90381e382fba15"
        }
    },
    ...
    "qrCode": {
        "size": 256, //二维码的长宽（为正方形）
        "urlPrefix": "xxx" //二维码的域名前缀
    },
    "localExe": { //扫描程序相关设置
        "path":"xxx", //扫描程序的exe路径，用于唤起
        "logPath":"xxx", //本程序的日志保存路径
        "sdkLogPath": "../scanner/footscansdk_log",//sdk的日志保存路径
        "nsLogPath": "../scanner/logs",//ns的日志保存路径
        "olLogPath": "../OnlineUpdate/logs",//升级守护程序的日志保存路径
        "licensePath":"xxx" //授权文件的保存路径
    },
    "localFile": { //本地扫描数据相关
        "path":"xxx", //本地扫描数据保存目录
        "retryUploadInterval": 30,//扫描数据上传失败重试间隔时间，数字后面跟y表示单位是年，M表示单位是月，w表示单位是周，h表示单位是小时，m表示单位是分钟，s表示单位是秒，如果纯数字，则默认是以小时为单位，如果示满足前面所有规则，则表示未到敲定间隔时间
        "deleteLife": 30, //扫描数据删除的过期时间，数字后面跟y表示单位是年，M表示单位是月，w表示单位是周，h表示单位是小时，m表示单位是分钟，s表示单位是秒，如果纯数字，则默认是以小时为单位，如果示满足前面所有规则，则表示未到敲定间隔时间
        "validBookPeriod": 3, //预定的有效期，数字后面跟y表示单位是年，M表示单位是月，w表示单位是周，h表示单位是小时，m表示单位是分钟，s表示单位是秒，如果纯数字，则默认是以小时为单位，如果示满足前面所有规则，则表示未到敲定间隔时间
        "informFrontInterval": 4,//未升级的前端提醒间隔时间，数字后面跟y表示单位是年，M表示单位是月，w表示单位是周，h表示单位是小时，m表示单位是分钟，s表示单位是秒，如果纯数字，则默认是以小时为单位，如果示满足前面所有规则，则表示未到敲定间隔时间
        "logInterval": 7 //日志需要上传的时间长度，数字后面跟y表示单位是年，M表示单位是月，w表示单位是周，h表示单位是小时，m表示单位是分钟，s表示单位是秒，如果纯数字，则默认是以小时为单位，如果示满足前面所有规则，则表示未到敲定间隔时间
    },
    "mode":"dev", 
    ...
    "cron":{
        "cronOnSoft": "@every 5h", //检测更新的时间间隔
        "cronOnStatus": "@every 5m",//检测设备状态的间隔
        "cronOnSoftDI": "@every 1m",//检测前端及设备端更新提醒的间隔
        "cronOnSoftD": "@every 5h",//检测断点续传的间隔
        "cronOnCheckTBBrandInfo": "@every 5h",//检测设备当前品牌门店的间隔
        "cronOnUpload": "@every 1h", //检测上传的间隔
        "cronOnClearExpireFile": "@every 1h",//触发数据清除方法执行的间隔
        "statistics": "@every 10m",//触发数据统计推送的间隔
	    "informFront": true //是否通知前端有更新
    }
}
```

## 使用流程
**本程序mock方式使用步骤(后续正式联调时废弃)**
1. 修改.server.json，修改好http服务的静态页面放置目录、http服务端口
2. footer-ali.exe run 启动主程序(mac系统则是footer-ali.osx run)。注意，如果端口设置为80，需要管理员权限，另外如果有涉及系统盘的文件内容，请注意权限要调整到位。最好用管理员身份把程序变成系统服务，自动运行，且优先于其它程序。
3. 前端页面中的websocket地址变成：ws://127.0.0.1:[http.port]/[ws.urlPrefix], 当前默认配置是ws://127.0.0.1/aliscan
4. 在浏览器中打开http://127.0.0.1:[http.port]/[http.fsUrl], 当前默认配置是http://127.0.0.1/wsmsg，可以模拟给前端页面发ws消息，模拟时先open，然后输入约定的数据格式(具体内容请自行构建)发送即可
5. 前端发给本程序的消息可以 tail -f logs/fa.log 看到
**本程序正式联调时使用步骤(3月22号后)**
1. 修改.server.json，修改好http服务的静态页面放置目录、http服务端口(设置为80)等信息，与设备程序放置一起，连接好设备
2. footer-ali.exe run 以管理员身份启动主程序
3. 在pad中用热点的ip访问前端页面
4. 在浏览器中打开http://127.0.0.1:[http.port]/[http.dsUrl], 当前默认配置是http://127.0.0.1/dsmsg，可以模拟设备端的收发消息；如果有设备则直接设备
5. 在浏览器中打开http://127.0.0.1:[http.port]/bbolt，可以直接察看数据库保存的内容
6. 在浏览器中打开http://127.0.0.1:[http.port]/l，可以直接察看本程序的日志，如果看不到，请调整配置文件中的相应目录配置
7. 在浏览器中打开http://127.0.0.1:[http.port]/s，可以直接察看sdk程序的日志，如果看不到，请调整配置文件中的相应目录配置
8. 在浏览器中打开http://127.0.0.1:[http.port]/ns，可以直接察看ns程序的日志，如果看不到，请调整配置文件中的相应目录配置
9. 在浏览器中打开http://127.0.0.1:[http.port]/ol，可以直接察看onlineupdate程序的日志，如果看不到，请调整配置文件中的相应目录配置
10. 在浏览器中打开http://127.0.0.1:[http.port]/rd，可以触发未下载完成的下载进行断点续传
11. 在浏览器中打开http://127.0.0.1:[http.port]/cf， 可以查看配置文件的内容
12. 在浏览器中打开http://127.0.0.1:[http.port]/ij，可以触发更新检测
13. 在浏览器中打开http://127.0.0.1:[http.port]/cdi，可以触发清除下载和提醒记录

**常用流程**

注意，下面的流程环节中不包含那些不需要设备端介入的部分

- 第一次设置
    - wifi设置：
        - 前端发wifi状态指令获取wifi状态，如果是已连接状态则跳过设置(除非用户要变更设置)，否则继续；
        - 前端发wifi列表指令获取wifi列表；
        - 用户选择其中1个输入密码由前端发送连接指定wifi指令
        - 设备端返回wifi状态，如果状态是connected，则继续，否则提示用户重新选择输入；
    - 设备授权：
        - 前端发status指令获取设备端状态，是待设置中(waitBinding)状态才继续，如果是waitWifiSetting则要跳到wifi设置去
        - 前端发门店指令、绑定门店
        - 设备端检查授权(如果没下载，则自动下载，下载完进行授权校验)并返回设备状态，如果还是待设置中(waitBinding)状态，则需要提醒用户联系客服或重试，如果设备处于free状态则表示第一设置成功。进度条（下载license和校验分别发状态，下载时要防止重复请求下载）,异常时则会返回abnormal状态;注意，下载成功时同时给前端返回该品牌的所有门店列表
- wifi设置修改：同第一次设置中的wifi设置
    - 注意，设备端会定时扫描wifi的网络状态，如果不是已连接状态会实时返回给前端
- 扫描：
    - 前端发status指令获取设备端状态，free状态才可以继续，否则提示用户
    - 前端发扫描指令
    - 设备端执行扫描并实时返回状态，前端根据返回的状态实时更新界面(这个状态进度需要单独定)
    - 设备端计算结束时，返回数据的计算结果，前端根据返回的结果显示界面内容(这个状态进度需要单独定)；设备端自动上传扫描结果；(扫描完成会自动复位)
- 标定：
    - 前端发status指令获取设备端状态，free状态才可以继续，否则提示用户
    - 前端发标定的new指令, step是左脚
    - 设备端执行左脚标定，返回状态，成功才继续，否则提示用户
    - 前端发标定的new指令, step是右脚
    - 设备端执行右脚标定，返回状态，成功才继续，否则提示用户
    - 前端发标定的new指令, step是compute
    - 设备端执行计算，返回状态，成功才继续，否则提示用户
- 数据管理：
    - 列表：
        - 前端发列表指令
        - 设备端返回数据列表
    - 操作：
        - 前端发各种Action指令
        - 设备端返回指定数据结果对象，如果状态是deleted则从界面上清除

# 通讯格式约定

## wifi相关

### wifi操作指令
**场景**

由前端程序发起给设备端，一般是用户初始化或修改wifi时触发

**扫描wifi列表**

***场景***

由前端程序给设备端，当用户操作时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

```json
{
    "topic": "equipment/wifi/list",  //required
    "padId": "", //required
    "data": {}
}
```

**wifi状态查询**

***场景***

由前端程序给设备端，当用户进入时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

```json
{
    "topic": "equipment/wifi/qst",  //required
    "padId": "", //required
    "data": {}
}
```

**返回wifi列表**

***场景***

由设备端程序返回给前端，当收到前端指令时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

不管成功与否都会返回这个结果，如果失败或是无可用wifi，则count为0，list为空数组
```json
{
    "topic": "equipment/wifi/result", //required
    "padId": "", //optional
    "data": { //required
        "count": 12, // required 附近wifi列表数量
        "list":[{ //required
            "ssid":"XXX", //wifi名称
            "rssi":"-50", //信号强度
            "isCurrent": false, //是否当前已连接的
            "isOurAp": false //是否当前自身创建的ap
    }]
}}
```

**连接指定wifi**

***场景***

由前端程序给设备端，当用户操作时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

不管原来是否有连接，都替换，结果返回status
```json
{
    "topic": "equipment/wifi/connect", //required
    "padId": "", //required
    "data": {//required
        "ssid": "XXX", // required 指定的wifi名称
        "pwd":"XXX" // required wifi密码
    }
}
```

**断开wifi**

***场景***

由前端程序给设备端，当用户操作时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

不管原来是否有连接，都执行断开，结果返回status
```json
{
    "topic": "equipment/wifi/disconnect", //required
    "padId": "", //required
    "data": {}
}
```

**返回wifi状态**

***场景***

由设备端程序主动推送给前端，当状态变化时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

```json
{
    "topic": "equipment/wifi/status", //required
    "padId": "", //optional
    "data": {//required
        "status": "unconnected",//required 未连接状态
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        }
    }
}
status还可以有以下的值：
    "status": "connected" //已连接
    "status": "noInternet" //已连接无网络
```

## 设备相关
### 设备状态实时通知
**场景**

由设备端程序主动推送给前端，当状态变化时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

**notify**
```json
{
    "topic": "equipment/scan/status", //required
    "padId": "", //optional
    "data": { //required
        "status": "unready",//设备未就绪
        "currentPad": "xxx",//当前占用设备的padId
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        }
    }
}
status还可以有以下的值：
    "status": "waitBinding" //待设置中，设备没有绑定门店，都是这个状态
    "status": "duringDownLicense" //待设置中，设备没有可用授权文件，都是这个状态
    "status": "licenseChecking" //待设置中，设备没有可用授权文件，都是这个状态
    "status": "waitLicense" //待下载授权中，设备没有可用授权文件但有网络时，都是这个状态
    "status": "waitWifiSetting" //待wifi设置中，设备没有可用wifi连接而又需要网络时，都是这个状态
    "status": "init" //设备初始化中
    "status": "free" //设备就绪
    "status": "debug" //设备处于调试状态中
    "status": "booking" //设备占用中，只有对应的padid才能Reset或scan
    "status": "calibrating" //标定中
    "status": "scanning" //扫描中
    "status": "computing" //计算中
    "status": "abnormal" //异常中，需要提醒用户联系技术支持
```

### 设备操作指令
**场景**

由前端程序发起给设备端，一般是用户操作时触发

**扫描**

***场景***

由前端程序发起给设备端，一般是用户操作时触发，注意，如果Device_id这类在用户第一次设置过程中缺少的信息存在，前端会收到abnormal不正常的状态

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/scan/new", //required
    "padId": "", //required
    "data": {//required
        "sex": 0, // required 1表示男，0表示女
        "requestId": "" // required 用于万一无法及时收到时可以在后面列表中找到
    }
}
```

**扫描指令执行结果**

***场景***

由设备端程序发起给前端，用于返回给指定的pad创建的新scanid，如果scanid为空，则表示本次扫描指令执行失败，需要重置

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/scan/result",
    "padId": "",
    "scanId": "xxx"
}
```

**标定**

***场景***

由前端程序发起给设备端，一般是用户操作时触发

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/calibration/new", //required
    "padId": "", //required
    "data": {//required
        "step": "left" // required 扫左脚
    }
}
step还可以有以下的值：
    "step": "right" // 扫右脚
    "step": "compute" // 左右脚模式的计算
    "step": "c1" // 标准物标定的第1个位置
    "step": "c2" // 标准物标定的第2个位置
    "step": "c3" // 标准物标定的第3个位置
    "step": "c4" // 标准物标定的第4个位置
    "step": "c5" // 标准物标定的第5个位置
    "step": "c6" // 标准物标定的第6个位置
    "step": "c7" // 标准物标定的第7个位置
    "step": "c8" // 标准物标定的第8个位置
    "step": "8compute" // 标准物标定的计算
```

**标定结果**

***场景***

由设备端程序发起给前端，一般是用户操作时触发

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/calibration/result", //required
    "padId": "", //required
    "data": {//required
        "status": "success",//设备未就绪
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        },
        "step": "left" // required 扫左脚
    }
}
```

**门店所属品牌信息**

***场景***

由前端发起给设备端程序

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/store/brand", //required
    "padId": "", //required
}
```

**门店所属品牌信息返回**

***场景***

由设备端发起给前端程序

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/store/brandresult", //required
    "padId": "", //required
    "data": {//required
        "status": "success",//设备未就绪
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        },
        "logo": "XXX", // 本地的服务器路径
        "sourceLogo": "XXX", // 场景logo，本地的服务器路径
        "bigLogo": "XXX", // 首页logo，本地的服务器路径
        "smallLogo": "XXX", // 小logo，本地的服务器路径
        "reportTitle": "XXX", // 标题
        "reportSubTitle": "XXX", // 副标题
        "footerContent": "XXX", // 页脚内容
        "storeName": "XXX", // required
        "brandName": "XXX" // required
    }
}
```

**门店列表**

***场景***

由前端发起给设备端程序，一般是用户进行激活操作时触发

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/store/list", //required
    "padId": "", //required
    "data": {//required
        "province": "XXX", // required
        "city": "XXX", // required
        "region": "XXX", // required
        "page": 1, 
        "pageSize": 1, 
        "environment": 1
    }
}
```

**门店列表返回**

***场景***

由设备端发起给前端程序，一般是用户进行激活操作时触发

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/store/listresult", //required
    "padId": "", //required
    "data": {//required
        "status": "success",//设备未就绪
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        },
        "count":100,
        "pageSize":10,
        "page":1,
        "list":[{
            "name":"storeName", 
            "number":"storeNumber"
        }]
    }
}
```

**门店获取**

***场景***

由前端发起给设备端程序，一般是用户进行激活操作时触发

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/store/get", //required
    "padId": "", //required
    "data": {//required
        "number": "XXX", // required
        "environment": 1
    }
}
```

**门店信息返回**

***场景***

由设备端发起给前端程序，一般是用户进行激活操作时触发

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/store/getresult", //required
    "padId": "", //required
    "data": {//required
        "status": "success",//设备未就绪
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        },
        "name":"storeName", 
        "number":"storeNumber"
    }
}
```

**门店绑定**

***场景***

由前端发起给设备端，一般是用户进行激活操作时触发

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/store/bind", //required
    "padId": "", //required
    "data": {//required
        "storeId": "xxx", // required 门店编号
        "storeName": "xxx" // required 门店名称
    }
}
```

**门店解除绑定**

***场景***

由前端发起给设备端，一般是用户进行激活操作时触发

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/store/unbind", //required
    "padId": "", //required
}
```

**门店解除/绑定结果**

***场景***

由设备端程序主动推送给前端，当有绑定或解除结果时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

**notify**
```json
{
    "topic": "equipment/store/result", //required
    "padId": "", //optional
    "data": { //required
        "status": "success",//设备未就绪
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        }
    }
}
status还可以有以下的值：
    "status": "fail" //失败
```

**其它操作**

***场景***

由前端程序发起给设备端，一般是用户操作时触发

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/scan/action", //required
    "padId": "", //required
    "data": {//required
        "action": "reset" // required 复位，扫描或标定退出也发这个指令
    }
}
action还可以有以下的值：
    "action": "open" // 打开，设备将开启
    "action": "book" // 预占，只有padid相符的才能发scan指令，也只有padid相符的才能发reset指令恢复
    "action": "status" // 触发设备端推送设备状态
    "action": "license" // 触发设备端重新拿license并且让用户进行绑定
    "action": "debug" // 触发设备端进入debug模式
```

## 数据相关
### 数据操作指令
**场景**

由前端程序发起给设备端，一般是用户操作时触发

**列表**

***场景***

由前端程序发起给设备端，一般是用户操作时触发

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "files/scan/list", //required
    "padId": "", //required
    "data": {
        "page":1, // 当前页，不传默认为1
        "pageSize":10 // 每页数量，不传默认为10
    }
}
该指令将由数据状态通知返回结果
```

**扫描用户信息更新**

***场景***

由前端程序发起给设备端，一般是用户操作时触发，用于更新用户的扫描信息

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "files/scan/uinfo", //required
    "padId": "", //required
    "data": {
        "scanId":"xxx", // required
        "telephone": "xxx", 
        "member_num": "xxx", 
        "operator": "xxx", 
        "birthday": "xxx", 
        "name": "xxx"
    }
}
``` 

**扫描用户信息更新结果**

***场景***

由设备端程序主动推送给前端，当有更新结果时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

**notify**
```json
{
    "topic": "files/scan/uinforesult", //required
    "padId": "", //optional
    "data": { //required
        "status": "success",//设备未就绪
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        }
    }
}
status还可以有以下的值：
    "status": "fail" //失败
```

**其它操作**

***场景***

由前端程序发起给设备端，一般是用户操作时触发

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "files/scan/action", //required
    "padId": "", //required
    "data": {
        "action": "upload", // required 上传
        "scanId":["xxx"] // 当action不是list时必须提供
    }
}
action还可以有以下的值：
    "action": "status" // 数据状态查询
    "action": "statistics" // 数据统计查询
    "action": "delete" // 删除
``` 

### 数据状态通知
**场景**

由设备端程序发起给前端，一般是用户操作时触发或是数据状态发生变化时，前端收到这个消息后，根据scanId对界面上的同scanId进行更新显示或显示

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "files/scan/status", //required
    "padId": "", //optional
    "data": { //required
        "count":1, //required，无数据时为0
        "page":1, // 当前页，不传默认为1
        "pageSize":10, // 每页数量，不传默认为10
        "list":[{ //required，无数据时为空数组
            "scanId":"xxx",  
            "requestId":"xxx",  
            "createPadId":"xxx",  
            "updatePadId":"xxx",  
            "savePath":"xxx",  
            "scan__qr_tag":"xxx",
            "foot_features":[{
                "images" : "xxx",
                "text" : "xxx"
            }],
            "advise2":"xxx",
            "advise1":["xxx"],
            "userInfo":{
                "telephone": "xxx", 
                "member_num": "xxx", 
                "name": "xxx",
                "status":"init|complete|fail" // init表示尚未提交，complete表示提交到了远程
            },
            "sex":"0|1",                      //性别
            "createTime":"2018-10-10 22:00:01",     //创建时间
            "upateTime":"2018-10-10 22:00:01",     //更新时间
            "mini": { //低精度数据，有可能是空对象
                "status":"init|uploaded|fail",
                "path":"xxx",
                "saveName":"xxx",
                "ossUrl":"xxx",
                "lastUploadTime":"2018-10-10 22:00:01",  //最后上传时间
                "uploadNum":0,                     //上传次数
                "error": {//required
                    "code":0, // required 不同的code代表不同的意思
                    "message": {//required
                        "msg_cn":"xxx",
                        "msg_en":"xxx"
                    }
                }
            },
            "scan": { //高精度数据，有可能是空对象
                "status":"init|uploaded|fail",
                "path":"xxx",
                "saveName":"xxx",
                "ossUrl":"xxx",
                "lastUploadTime":"2018-10-10 22:00:01",  //最后上传时间
                "uploadNum":0,                     //上传次数
                "error": {//required
                    "code":0, // required 不同的code代表不同的意思
                    "message": {//required
                        "msg_cn":"xxx",
                        "msg_en":"xxx"
                    }
                }
            },
            "qrData":"XXX", // 这里为上报的数据url形成的png格式的[]byte
            "result":{//测量结果，有可能是空对象，调用孟焦的接口得到
                "fit_size_CN" : 0,
                "fit_size_EUR" : 0,
                "fit_size_UK" : 0,
                "fit_size_US" : 0,
                "lft_zugong" : 0,
                "rft_zugong" : 0,
                "lft_muwaifan" : 0,
                "rft_muwaifan" : 0,
                "lft_zuwaifan" : 0,
                "rft_zuwaifan" : 0,
                "l_r_zhixing" : 0,
                "zugong_descrp" : 0,
                "muwaifan_descrp" : 0,
                "zuwaifan_descrp" : 0,
                "zhixing_descrp" : 0,
                "lft_length":1.0,
                "lft_width":1.0,
                "lft_zhiwei":1.0,
                "lft_fuwei":1.0,
                "lft_douwei":1.0,
                "lft_jiaobeigaodu":1.0,
                "lft_muzhipose":1.0,   //拇趾外凸点部位
                "lft_xiaozhipose":1.0, //小趾外凸点部位
                "lft_diyizhizhipose":1.0, //第一跖趾部位
                "lft_qianjiaozhangpose":1.0, //前掌落地点部位
                "lft_diwuzhizhipose":1.0, //第五跖趾部位
                "lft_yaowopose":1.0,      //腰窝部位
                "lft_zhongxinpose":1.0, //踵心部位
                "lft_muzhilikuan":1.0,  //拇趾里宽
                "lft_xiaozhiwaikuan":1.0, //小趾外宽
                "lft_diyizhizhilikuan":1.0, //第一跖趾里宽
                "lft_diwuzhizhiwaikuan":1.0, //第五跖趾外宽
                "lft_zhizhizhikuan":1.0, //跖趾直宽（基宽）
                "lft_yaowowaikuan":1.0,//腰窝外宽
                "lft_zhongxinquankuan":1.0,//踵心全宽
                "lft_muzhigao":1.0,  //拇趾高
                "lft_zugonggao":1.0, //足弓高度
                "lft_hougengao":1.0, //后跟高
                "lft_houtudu":1.0,//后凸度
                "lft_houtugao":1.0,//后凸高
                "rlt_length":1.0,
                "rlt_width":1.0,
                "rlt_zhiwei":1.0,
                "rlt_fuwei":1.0,
                "rlt_douwei":1.0,
                "rlt_jiaobeigaodu":1.0,
                "rlt_muzhipose":1.0,   //拇趾外凸点部位
                "rlt_xiaozhipose":1.0, //小趾外凸点部位
                "rlt_diyizhizhipose":1.0, //第一跖趾部位
                "rlt_qianjiaozhangpose":1.0, //前掌落地点部位
                "rlt_diwuzhizhipose":1.0, //第五跖趾部位
                "rlt_yaowopose":1.0,      //腰窝部位
                "rlt_zhongxinpose":1.0, //踵心部位
                "rlt_muzhilikuan":1.0,  //拇趾里宽
                "rlt_xiaozhiwaikuan":1.0, //小趾外宽
                "rlt_diyizhizhilikuan":1.0, //第一跖趾里宽
                "rlt_diwuzhizhiwaikuan":1.0, //第五跖趾外宽
                "rlt_zhizhizhikuan":1.0, //跖趾直宽（基宽）
                "rlt_yaowowaikuan":1.0,//腰窝外宽
                "rlt_zhongxinquankuan":1.0,//踵心全宽
                "rlt_muzhigao":1.0,  //拇趾高
                "rlt_zugonggao":1.0, //足弓高度
                "rlt_hougengao":1.0, //后跟高
                "rlt_houtudu":1.0,//后凸度
                "rlt_houtugao":1.0,//后凸高
                "left_zgzhishu":1.0,//
                "right_zgzhishu":1.0,//
                "left_zwfdushu":1.0,//
                "right_zwfdushu":1.0,//
                "left_mwfdushu":1.0,//
                "right_mwfdushu":1.0,//
                "left_pangshouleixing":1.0,//
                "right_pangshouleixing":1.0,//
                "left_pangshoujiao":1.0,//
                "right_pangshoujiao":1.0//
            },
            "resultStatus":"init|complete|fail", //检测结果提交Public状态
            "resultPriStatus":"init|complete|fail", //private
            "status":"init|computing|uploading|enable|deleted|reset",            //存储状态 init 等待存储 computing 等待计算 uploading 等待计算 enable 可用 deleted 已删除 reset 已被重置
            "error": {//required
                "code":0, // required 不同的code代表不同的意思
                "message": {//required
                    "msg_cn":"xxx",
                    "msg_en":"xxx"
                }
            }
        }]
    }}
```

### 数据扫描结果通知
**场景**

由设备端程序发起给前端，一般是用户扫描操作完成时触发，前端收到这个消息后，根据padid和scanId对界面上的同scanId进行更新显示或显示

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "files/scan/result", //required
    "padId": "", //required
    "scanId": "", //required
    "data": { //required
        "scanId":"xxx",  
        "requestId":"xxx",  
        "createPadId":"xxx",  
        "updatePadId":"xxx",  
        "savePath":"xxx",  
        "scan__qr_tag":"xxx",
        "foot_features":[{
            "images" : "xxx",
            "text" : "xxx"
        }],
        "advise2":"xxx",
        "advise1":["xxx"],
        "userInfo":{
            "telephone": "xxx", 
            "member_num": "xxx", 
            "name": "xxx",
            "status":"init|complete|fail" // init表示尚未提交，complete表示提交到了远程
        },
        "sex":"0|1",                      //性别
        "createTime":"2018-10-10 22:00:01",     //创建时间
        "upateTime":"2018-10-10 22:00:01",     //更新时间
        "mini": { //低精度数据，有可能是空对象
            "status":"init|uploaded|fail",
            "path":"xxx",
            "saveName":"xxx",
            "ossUrl":"xxx",
            "lastUploadTime":"2018-10-10 22:00:01",  //最后上传时间
            "uploadNum":0,                     //上传次数
            "error": {//required
                "code":0, // required 不同的code代表不同的意思
                "message": {//required
                    "msg_cn":"xxx",
                    "msg_en":"xxx"
                }
            }
        },
        "scan": { //高精度数据，有可能是空对象
            "status":"init|uploaded|fail",
            "path":"xxx",
            "saveName":"xxx",
            "ossUrl":"xxx",
            "lastUploadTime":"2018-10-10 22:00:01",  //最后上传时间
            "uploadNum":0,                     //上传次数
            "error": {//required
                "code":0, // required 不同的code代表不同的意思
                "message": {//required
                    "msg_cn":"xxx",
                    "msg_en":"xxx"
                }
            }
        },
        "qrData":"XXX", // 这里为上报的数据url形成的png格式的[]byte
        "result":{//测量结果，有可能是空对象，调用孟焦的接口得到
            "fit_size_CN" : 0,
            "fit_size_EUR" : 0,
            "fit_size_UK" : 0,
            "fit_size_US" : 0,
            "lft_zugong" : 0,
            "rft_zugong" : 0,
            "lft_muwaifan" : 0,
            "rft_muwaifan" : 0,
            "lft_zuwaifan" : 0,
            "rft_zuwaifan" : 0,
            "l_r_zhixing" : 0,
            "zugong_descrp" : 0,
            "muwaifan_descrp" : 0,
            "zuwaifan_descrp" : 0,
            "zhixing_descrp" : 0,
            "lft_length":1.0,
            "lft_width":1.0,
            "lft_zhiwei":1.0,
            "lft_fuwei":1.0,
            "lft_douwei":1.0,
            "lft_jiaobeigaodu":1.0,
            "lft_muzhipose":1.0,   //拇趾外凸点部位
            "lft_xiaozhipose":1.0, //小趾外凸点部位
            "lft_diyizhizhipose":1.0, //第一跖趾部位
            "lft_qianjiaozhangpose":1.0, //前掌落地点部位
            "lft_diwuzhizhipose":1.0, //第五跖趾部位
            "lft_yaowopose":1.0,      //腰窝部位
            "lft_zhongxinpose":1.0, //踵心部位
            "lft_muzhilikuan":1.0,  //拇趾里宽
            "lft_xiaozhiwaikuan":1.0, //小趾外宽
            "lft_diyizhizhilikuan":1.0, //第一跖趾里宽
            "lft_diwuzhizhiwaikuan":1.0, //第五跖趾外宽
            "lft_zhizhizhikuan":1.0, //跖趾直宽（基宽）
            "lft_yaowowaikuan":1.0,//腰窝外宽
            "lft_zhongxinquankuan":1.0,//踵心全宽
            "lft_muzhigao":1.0,  //拇趾高
            "lft_zugonggao":1.0, //足弓高度
            "lft_hougengao":1.0, //后跟高
            "lft_houtudu":1.0,//后凸度
            "lft_houtugao":1.0,//后凸高
            "rlt_length":1.0,
            "rlt_width":1.0,
            "rlt_zhiwei":1.0,
            "rlt_fuwei":1.0,
            "rlt_douwei":1.0,
            "rlt_jiaobeigaodu":1.0,
            "rlt_muzhipose":1.0,   //拇趾外凸点部位
            "rlt_xiaozhipose":1.0, //小趾外凸点部位
            "rlt_diyizhizhipose":1.0, //第一跖趾部位
            "rlt_qianjiaozhangpose":1.0, //前掌落地点部位
            "rlt_diwuzhizhipose":1.0, //第五跖趾部位
            "rlt_yaowopose":1.0,      //腰窝部位
            "rlt_zhongxinpose":1.0, //踵心部位
            "rlt_muzhilikuan":1.0,  //拇趾里宽
            "rlt_xiaozhiwaikuan":1.0, //小趾外宽
            "rlt_diyizhizhilikuan":1.0, //第一跖趾里宽
            "rlt_diwuzhizhiwaikuan":1.0, //第五跖趾外宽
            "rlt_zhizhizhikuan":1.0, //跖趾直宽（基宽）
            "rlt_yaowowaikuan":1.0,//腰窝外宽
            "rlt_zhongxinquankuan":1.0,//踵心全宽
            "rlt_muzhigao":1.0,  //拇趾高
            "rlt_zugonggao":1.0, //足弓高度
            "rlt_hougengao":1.0, //后跟高
            "rlt_houtudu":1.0,//后凸度
            "rlt_houtugao":1.0,//后凸高
            "left_zgzhishu":1.0,//
            "right_zgzhishu":1.0,//
            "left_zwfdushu":1.0,//
            "right_zwfdushu":1.0,//
            "left_mwfdushu":1.0,//
            "right_mwfdushu":1.0,//
            "left_pangshouleixing":1.0,//
            "right_pangshouleixing":1.0,//
            "left_pangshoujiao":1.0,//
            "right_pangshoujiao":1.0//
        },
        "resultStatus":"init|complete|fail", //检测结果提交Public状态
        "resultPriStatus":"init|complete|fail", //private
        "status":"init|computing|uploading|enable|deleted|reset",            //存储状态 init 等待存储 computing 等待计算 uploading 等待计算 enable 可用 deleted 已删除 reset 已被重置
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        }
    }}
```

## 1.4需求相关

### 升级通知
**场景**

由设备端发给前端。ota升级，插入U盘时设备端检测到有比当前版本新的情况，或者是本程序检测到有新的在线版本，发消息给前端，用户确认是否升级。
protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "inform/upgradeInform", // required
    "padId": "", // empty
    "source":"ota", // ota/online
    "data": {
        "id": "xxxx", // uuid, 标识一次通知-响应，前端必须原样返回
        "info":{
            "adaptiveModel":"einscan-pro,einscan-plus", //适用的硬件型号
            "adaptiveModular":"", //适用的配件
            "file":"c:\down\aaa.exe", //下载文件的保存路径
            "lang":"", //语言
            "type":"", // install_package/patch 是安装包还是增量包
            "env":"", // release/beta 正式|测试
            "maxVersion":"", // 支持的最大版本
            "minVersion":"",// 支持的最低版本
            "os":"win", // 支持的操作系统
            "version":"2.7.0.6", // 版本
            "overwrite":"n", // 是否覆盖式安装，覆盖式安装一般是不通知前端的
            "versionCNLog":"xxx", // 中文变更日志
            "versionLog":"xxx" // 英文变更日志
        }
    }
}
``` 

### 升级响应
**场景**

前端发给设备端，响应是否升级
protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "inform/upgradeResponse", // required
    "padId": "", 
    "data": {
        "id": "xxxx",
        "source":"ota", // ota/online required
        "upgrade": true // 是否升级
    }
}
``` 

### 升级处理中消息
**场景**

设备端发给前端，表示已经开始升级
protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "inform/upgrading", // required
    "padId": "", 
    "data": {
        "id": "xxxx",
        "source":"ota", // ota/online required
    }
}
``` 

### 获取设备信息
**场景**

由前端发起给设备端，获取SSID、设备ID、主程序版本号、SDK版本号、固件版本号

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/deviceInfo", // required
    "padId": "", // required
    "data": {
    }
}
``` 

### 设备信息结果返回
**场景**

由设备端发起给前端，返回SSID、设备ID、主程序版本号、SDK版本号、固件版本号

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/deviceInfoResult", // required
    "padId": "", // empty
    "data": {
        "status": "success",//设备未就绪
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        },
        "modelName":"", //型号
        "sn":"", //硬件序列号
        "ssid":"", // 外网ssid
        "ap":"", // ap名称兼设备序列号
        "deviceId":"", //硬盘id
        "version":"", //主版本
        "algorighmVer":"", //算法版本
        "sdkVer":"", //扫描sdk版本
        "communityVer":"", //网络sdk版本
        "firmwareVer":"", //固件版本
        "frontVer":"", //前端版本
        "createOn":"",
        "prev":{ // 上一次启动的版本
            "version":"", //主版本
            "algorighmVer":"", //算法版本
            "sdkVer":"", //扫描sdk版本
            "communityVer":"", //网络sdk版本
            "firmwareVer":"", //固件版本
            "frontVer":"", //前端版本
            "createOn":"",
        }
    }
}
``` 

### 调试模式启用关闭
**场景**

由前端发起给本程序，当需要进入调试页面时，启用时设备状态变成debug，此状态只允许调试中的功能接口使用,且根据padId锁定.设备状态指令返回结果

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/debugEnable", // required
    "padId": "", // required
    "data": {
        "enable":true //true/false
    }
}
``` 

### U盘状态检测
**场景**

由前端发起给本程序

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/checkUDisk", // required
    "padId": "", // required
    "data": {
    }
}
``` 

### U盘状态检测结果
**场景**

由设备端发给前端，返回U盘连接状态

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/checkUDiskResult", // required
    "padId": "", // empty
    "data": {
        "status": "success",// success|fail
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        },
        "name":"xxx", //名称
        "size":3333, //尺寸
        "capibility": 444, //剩余容量
        "logSize":5555 //日志大小
    }
}
``` 

### 日志拷贝通知
**场景**

由前端发起给设备端，通知开始把日志拷贝到U盘

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/copyLog", // required
    "padId": "", // empty
    "data": {
    }
}
``` 

### 日志拷贝结果
**场景**

由设备端发起给前端，返回U盘拷贝结果

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/copyLogResult", // required
    "padId": "", // empty
    "data": {
        "status": "success",//
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        }
    }
}
``` 

### 上传日志
**场景**

由前端发起给本程序，上传本程序日志和设备日志到服务端

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/uploadLog", // required
    "padId": "", // required
    "data": {
    }
}
``` 

### 上传日志结果返回
**场景**

由前端发起给本程序，上传本程序日志和设备日志到服务端

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "equipment/uploadLogResult", // required
    "padId": "", // required
    "data": {
        "status": "success",//
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        }
    }
}
``` 


### 阿里模块发布相关的项目信息：
- 算法的账号： algorithmali@alibaba.com O9i8u7y6 自行修改密码
- 前端的账号： frontali@alibaba.com O9i8u7y6 自行修改密码
- https://git.shining3d.com/client/ali
- git项目中的.drone.yml不能删除
- 算法包压缩成zip包名称叫algorithm.zip，包解压后，所有东西是平级的：
    ```
    a.zip
        |_ a.dll
        |_ a....
    ```
- 前端所有内容压缩成zip包名称叫front.zip，包解压后，应该是如下的结构：
    ```
    b.zip
        |_ index.html
        |_ static
        |_ ...
    ```
- 版本的json格式：跟压缩包平级
    ```json
    {
        "version":"1.0.11",
        "changeLog": {
            "cn":"xxx",
            "en":"xxx"
        }
    }
    ```


### 数据有更新时的推送
**场景**

由设备端程序发起给前端，一般是数据由于提交服务器有结果时推送

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "files/scan/update", //required
    "padId": "", //required
    "scanId": "", //required
    "data": { //required
        "scanId":"xxx", 
        "requestId":"xxx",   
        "createPadId":"xxx",  
        "updatePadId":"xxx",  
        "savePath":"xxx",  
        "scan__qr_tag":"xxx",
        "foot_features":[{
            "images" : "xxx",
            "text" : "xxx"
        }],
        "advise2":"xxx",
        "advise1":["xxx"],
        "userInfo":{
            "telephone": "xxx", 
            "member_num": "xxx", 
            "name": "xxx",
            "status":"init|complete|fail" // init表示尚未提交，complete表示提交到了远程
        },
        "sex":"0|1",                      //性别
        "createTime":"2018-10-10 22:00:01",     //创建时间
        "upateTime":"2018-10-10 22:00:01",     //更新时间
        "mini": { //低精度数据，有可能是空对象
            "status":"init|uploaded|fail",
            "path":"xxx",
            "saveName":"xxx",
            "ossUrl":"xxx",
            "lastUploadTime":"2018-10-10 22:00:01",  //最后上传时间
            "uploadNum":0,                     //上传次数
            "error": {//required
                "code":0, // required 不同的code代表不同的意思
                "message": {//required
                    "msg_cn":"xxx",
                    "msg_en":"xxx"
                }
            }
        },
        "scan": { //高精度数据，有可能是空对象
            "status":"init|uploaded|fail",
            "path":"xxx",
            "saveName":"xxx",
            "ossUrl":"xxx",
            "lastUploadTime":"2018-10-10 22:00:01",  //最后上传时间
            "uploadNum":0,                     //上传次数
            "error": {//required
                "code":0, // required 不同的code代表不同的意思
                "message": {//required
                    "msg_cn":"xxx",
                    "msg_en":"xxx"
                }
            }
        },
        "qrData":"XXX", // 这里为上报的数据url形成的png格式的[]byte
        "result":{//测量结果，有可能是空对象，调用孟焦的接口得到
            "fit_size_CN" : 0,
            "fit_size_EUR" : 0,
            "fit_size_UK" : 0,
            "fit_size_US" : 0,
            "lft_zugong" : 0,
            "rft_zugong" : 0,
            "lft_muwaifan" : 0,
            "rft_muwaifan" : 0,
            "lft_zuwaifan" : 0,
            "rft_zuwaifan" : 0,
            "l_r_zhixing" : 0,
            "zugong_descrp" : 0,
            "muwaifan_descrp" : 0,
            "zuwaifan_descrp" : 0,
            "zhixing_descrp" : 0,
            "lft_length":1.0,
            "lft_width":1.0,
            "lft_zhiwei":1.0,
            "lft_fuwei":1.0,
            "lft_douwei":1.0,
            "lft_jiaobeigaodu":1.0,
            "lft_muzhipose":1.0,   //拇趾外凸点部位
            "lft_xiaozhipose":1.0, //小趾外凸点部位
            "lft_diyizhizhipose":1.0, //第一跖趾部位
            "lft_qianjiaozhangpose":1.0, //前掌落地点部位
            "lft_diwuzhizhipose":1.0, //第五跖趾部位
            "lft_yaowopose":1.0,      //腰窝部位
            "lft_zhongxinpose":1.0, //踵心部位
            "lft_muzhilikuan":1.0,  //拇趾里宽
            "lft_xiaozhiwaikuan":1.0, //小趾外宽
            "lft_diyizhizhilikuan":1.0, //第一跖趾里宽
            "lft_diwuzhizhiwaikuan":1.0, //第五跖趾外宽
            "lft_zhizhizhikuan":1.0, //跖趾直宽（基宽）
            "lft_yaowowaikuan":1.0,//腰窝外宽
            "lft_zhongxinquankuan":1.0,//踵心全宽
            "lft_muzhigao":1.0,  //拇趾高
            "lft_zugonggao":1.0, //足弓高度
            "lft_hougengao":1.0, //后跟高
            "lft_houtudu":1.0,//后凸度
            "lft_houtugao":1.0,//后凸高
            "rlt_length":1.0,
            "rlt_width":1.0,
            "rlt_zhiwei":1.0,
            "rlt_fuwei":1.0,
            "rlt_douwei":1.0,
            "rlt_jiaobeigaodu":1.0,
            "rlt_muzhipose":1.0,   //拇趾外凸点部位
            "rlt_xiaozhipose":1.0, //小趾外凸点部位
            "rlt_diyizhizhipose":1.0, //第一跖趾部位
            "rlt_qianjiaozhangpose":1.0, //前掌落地点部位
            "rlt_diwuzhizhipose":1.0, //第五跖趾部位
            "rlt_yaowopose":1.0,      //腰窝部位
            "rlt_zhongxinpose":1.0, //踵心部位
            "rlt_muzhilikuan":1.0,  //拇趾里宽
            "rlt_xiaozhiwaikuan":1.0, //小趾外宽
            "rlt_diyizhizhilikuan":1.0, //第一跖趾里宽
            "rlt_diwuzhizhiwaikuan":1.0, //第五跖趾外宽
            "rlt_zhizhizhikuan":1.0, //跖趾直宽（基宽）
            "rlt_yaowowaikuan":1.0,//腰窝外宽
            "rlt_zhongxinquankuan":1.0,//踵心全宽
            "rlt_muzhigao":1.0,  //拇趾高
            "rlt_zugonggao":1.0, //足弓高度
            "rlt_hougengao":1.0, //后跟高
            "rlt_houtudu":1.0,//后凸度
            "rlt_houtugao":1.0,//后凸高
            "left_zgzhishu":1.0,//
            "right_zgzhishu":1.0,//
            "left_zwfdushu":1.0,//
            "right_zwfdushu":1.0,//
            "left_mwfdushu":1.0,//
            "right_mwfdushu":1.0,//
            "left_pangshouleixing":1.0,//
            "right_pangshouleixing":1.0,//
            "left_pangshoujiao":1.0,//
            "right_pangshoujiao":1.0//
        },
        "resultStatus":"init|complete|fail", //检测结果提交Public状态
        "resultPriStatus":"init|complete|fail", //private
        "status":"init|computing|uploading|enable|deleted|reset",            //存储状态 init 等待存储 computing 等待计算 uploading 等待计算 enable 可用 deleted 已删除 reset 已被重置
        "error": {//required
            "code":0, // required 不同的code代表不同的意思
            "message": {//required
                "msg_cn":"xxx",
                "msg_en":"xxx"
            }
        }
    }}
```

### 数据状态统计定时推送
**场景**

由设备端程序发起给前端

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |
```json
{
    "topic": "files/scan/statistics", //required
    "padId": "", //required
    "data": { //required
        "total":10, //所有数据
        "totalUncomplete":0, //未完成上传的数据
        "totalUserUncomplete":0, //未完成上传的用户数据
        "totalUserFail":0, //未完成上传的用户失败数据
        "totalJsonUncomplete":0, //未完成上传的json数据
        "totalJsonFail":0, //未完成上传的json失败数据
        "totalJsonPriUncomplete":0, //未完成上传的json私有数据
        "totalJsonPriFail":0, //未完成上传的json私有失败数据
        "totalCloudUncomplete":0, //未完成上传的点云数据
        "totalCloudFail":0, //未完成上传的点云失败数据
        "totalMiniUncomplete":0, //未完成上传的低精度数据
        "totalMiniFail":0, //未完成上传的低精度失败数据
        "totalScanUncomplete":0, //未完成上传的高精度数据
        "totalScanFail":0 //未完成上传的高精度失败数据
    }}
```

### 1.5.1接口

**设备信息更新接口**

***场景***

由前端程序给设备端，当用户需要更新二维码前缀、Logo等设备相关的远程信息时，收到后从远程服务器再重新取，取到后保存并通过equipment/store/brandresult发前端

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

```json
{
    "topic": "equipment/info/update",  //required
    "padId": "", //required
    "data": {}
}
```

**根据requestId查询扫描结果**

***场景***

由前端程序给设备端，当需要调用时，设备端返回files/scan/result

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

```json
{
    "topic": "files/scan/request",  //required
    "padId": "", //required
    "data": {
        "requestId":"xxx"
    }
}
```

**服务端连接通畅状态查询**

***场景***

由前端程序给设备端，当需要调用时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

```json
{
    "topic": "equipment/net/qst",  //required
    "padId": "", //required
    "data": {}
}
```

**返回服务端连接通畅状态**

***场景***

由设备端程序返回给前端，当收到前端指令或是自动检测到时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

```json
{
    "topic": "equipment/net/result", //required
    "padId": "", //optional
    "data":  true //true表示通畅， false表示不通
}}
```

**提醒前端设备信息与当前门店、品牌不相符**

***场景***

由设备端程序返回给前端，当收到前端指令或是自动检测到时

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /aliscan| notify | 1.0.0 |

```json
{
    "topic": "equipment/brand/error",
    "padId": "", //optional
    "data": 22001 // data的值为22001、22003、22005、20001、20005、20007、23001等服务端的错误码
}}
```

## 异常码


### 以下为先临异常码
异常码|	异常描述| 需要管理员处理异常
---|---|-|
**0**	|**非异常，无需关注**
**1**	|**未知异常**               |**Y**
**1000**	|**硬件异常**
100001	|设备异常               |**Y**
100002	|激活远程异常               |**Y**
**1002**	| **扫描标定异常** 
100201	|投光失败               |**Y**
100202	|采图失败               |**Y**
100203	|点云生成异常
100204	|计算失败(标定中发生)
100205  |点数异常

**6000**	| **wifi异常**
600001	|无权限               |**Y**
600002	|连接超时               |**Y**
600003	|其它未知异常              |**Y**
600004	|密码错误
**6001**	| **本地数据异常**
600101	|本地数据存储异常               |**Y**
600102	|template.json 保存错误               |**Y**
600103	|授权失败              |**Y**
600104	|数据上报网络不通
**7001**	| **u盘及日志相关异常**
700101	|u盘内存不足
700102	|u盘中途拔出
700103	|异常错误
700104	|无可处理日志

### 以下为原异常码，请阿里的同学确认是否与算法返回的错误码匹配

异常码|	异常描述| 需要管理员处理异常
---|---|-|
**2000**	| **3D模型构建异常**
200001	|3D模型生成失败                            |**Y**  
**3000**	| **数据存储异常**
300001	|3D 高精度模型上传失败                       |**Y**     
300002	|3D 低精度模型上传失败                       |**Y**   
300003	|脚型解析json数据上传失败                    |**Y**  
300004	|扫描预览图上传失败                          |**Y**  
300010  | 上传网络不通                                
300011  | 上传OSS接口故障   
300021  | 上传高精度模型间隔时间太短                             
**4000**	| **配置文件异常**
400001	|配置文件写入异常                            |**Y**  
400002	|配置文件不存在                              |**Y**
400010	|globalref_output.txt 不存在，需要重新标定   |**Y**
400011	|plane.txt 生成失败                          |**Y**
**5000**	| **尺码异常**
500001	|尺码计算错误     
**8000**	| **参数错误**
800000  | 参数错误 
800001	|性别错误