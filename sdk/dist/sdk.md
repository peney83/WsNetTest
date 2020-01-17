# 与软件通讯约定文档

[toc]

## 版本更新
### 1.0.9 by victor
* 添加1.4版本需求接口，见后面部分
### 1.0.8 by lidong
* 增加本程序返回软件sdk请求的通用格式

### 1.0.7 by victor
* 标定结果调整
### 1.0.1 by victor
* 基于3.12日会议调整格式，所有指令加入"padId"
* 调整为标准的json格式
* 补充设备状态
### 1.0.0 by victor
* 基于原独立网络模块与软件的websocket通讯格式

## 格式说明

### SOCKET message

```json
{
    "topic":"status", // required
    "status":"xxx", // optional
    "padId":"xxx", // optional
    "params":"XXX" // optional
}
```
- cmd是触发的命令值
- params： 一般是对象或是空的，具体由各命令约定
- status允许为空，如果有值可以有以下几种值：
    - success：表示成功
    - notExist：表示不存在，这种表示要客户联系销售或技术支持
    - noInternet：表示网络不通
    - unconnected:表示未连接
    - connected:表示连接
    - serverBug：表示服务器问题
    - illegal：表示参数不相符
    - noResult：表示没有结果
    - localBug: 表示本地出现问题了
    - unready: 表示设备未就绪
    - waitBinding: 表示待设置中，设备没有可用授权文件或是无wifi设置，都是这个状态
    - init: 表示设备初始化中
    - free: 表示设备就绪
    - fail: 表示失败
    - calibrating: 表示标定中
    - scanning: 表示扫描中
    - computing: 表示计算中
    - abnormal: 表示异常中，需要提醒用户联系技术支持

### params约定
```json
scanId //指单次扫描的唯一识别id，组成规则是YYYYMMDD-HHmmss
padId //操作pad的唯一id，由前端生成，在扫描和标定这些设备操作相关的指令过程中需要使用到，其它的根据产品需求定;前端每次请求时必须要提供，如果本程序有传给sdk，则sdk需要在返回时提供，否则可以为空
```

### Response to sdk
```json
{
    "cmdOld":"xxx", // required
    "status":"xxx", // required
    "result":"xxx", // optional 
}
```

- cmdOld是源触发的命令值
- status有以下几种值：
     - success：表示成功
    - notExist：表示不存在，这种表示要客户联系销售或技术支持
    - noNetwork：表示网络不通
    - serverBug：表示服务器问题
    - illegal：表示参数不相符
    - noResult：表示没有结果
    - localBug: 表示本地出现问题了
- result在status是success时一般是文字内容，比如路径等，或是空的，但具体以不同命令约定的格式为准，有可能是空的，有可能是字符串，也有可以是列表的json字符串，也有可能是对象的json字符串
- 当状态不是success时，请查看本程序的运行日志

## 配置文件 .server.json 说明
```json
{
    "log": { //本程序的日志输出设置
        "output": "file",
        "path": "logs/fa.log",
        "level": "info", 
        "max": 10,
        "maxAge": 30,
        "localtime": true //本地时间显示
    },
    "http": {
        "port": ":80", //http服务端口
        "static":{
            ...
            "fileUrlPrefix":"/f", //http服务的扫描数据前缀路径
            "logUrlPrefix":"/l", //http服务的本程序日志文件列表前缀路径
            "logSdkUrlPrefix": "/s",//http服务的sdk程序日志文件列表前缀路径
            "logNSUrlPrefix": "/ns",//http服务的ns程序日志文件列表前缀路径
            "logOLUrlPrefix": "/ol"//http服务的onlineupdate程序日志文件列表前缀路径
        },
        ...
        "dsUrl": "xxx", // 模拟给设备发消息的url
        ...
    },
    "ws": {
        "dUrlPrefix": "/dscan", //websocket服务前缀路径，给SDK的
        ...
    },
    "api":{//发布生产事项：要换成对应的正确版本信息，现在是线下环境的
        "defaultPageSize": 10,
        "taobao":{
            "url":"https://gw.api.tbsandbox.com/router/rest",
            "appKey":"1025823871",
            "appSecret":"sandboxc61681d9d947538e7e6d81457",
            "token":"a15e03698369fbdaae90381e382fba15",
            "resultMeasureLength": 1
        }
    },
    "global":{
        "softs": [{
            "modelCode":"foot3dscan",
            "maxPatch": 10,
            "productLine":"scan",
            "cdnUrl": "https://cdnimg.shining3d.com/software/scan/interface.json",
            "upgradeMode":"ignore",
            "version":"1.3.0.0", //发布生产事项：要换成对应的正确版本信息
            "other": {
                "algorighmVer":"1.0.0", //发布生产事项：要换成对应的正确阿里算法版本信息
                "sdkVer":"1.0.0", //发布生产事项：要换成对应的正确sdk版本信息
                "communityVer":"1.4.1.9", 
                "firmwareVer":"15.0.0",//发布生产事项：要换成对应的正确固件版本信息
                "frontVer":"1.0.0"//发布生产事项：要换成对应的正确前端版本信息
            }, 
            "autoDownload":true,
            "env":"beta"//发布生产事项：要换成release, beta只是用于测试环境
        },{
            "modelCode":"foot3dscanfirmware",
            "maxPatch": 10,
            "productLine":"scan",
            "cdnUrl": "https://cdnimg.shining3d.com/software/scan/interface.json",
            "upgradeMode":"ignore",
            "version":"14.0.0.0",//发布生产事项：要换成正确的固件版本信息
            "autoDownload":true,
            "env":"beta"//发布生产事项：要换成release, beta只是用于测试环境
        }],
        "savePath":{
            "update":"tmp/update",
            "limit":{
                "upload": 10,
                "download": 10
            }
        }
    },
    "device":{ //发布生产事项：这部分由产测软件写入
        "boardId":"xxx",
        "modelCode":"xxx",
        "ap":{
            "ssid":"zbb-hahaha-rc",
            "pwd":"FootScan"
        }
    },
    "localExe": { //扫描程序相关设置
        "path":"xxx", //扫描程序的exe路径，用于唤起
        "logPath":"xxx", //本程序的日志保存路径
        "sdkLogPath": "../scanner/footscansdk_log",//sdk的日志保存路径
        "nsLogPath": "../scanner/logs",//ns的日志保存路径
        "olLogPath": "../OnlineUpdate/logs",//升级守护程序的日志保存路径
        "licensePath":"xxx" //授权文件的保存路径
    },
    ...
    "localFile": { //本地扫描数据相关, 发布生产事项：要换成以下标准的配置
        "path":"tmp/files", //本地扫描数据保存目录
        "retryUploadInterval": "30m",//扫描数据上传失败重试间隔时间，数字后面跟y表示单位是年，M表示单位是月，w表示单位是周，h表示单位是小时，m表示单位是分钟，s表示单位是秒，如果纯数字，则默认是以小时为单位，如果示满足前面所有规则，则表示未到敲定间隔时间
        "deleteLife": "30d", //扫描数据删除的过期时间，数字后面跟y表示单位是年，M表示单位是月，w表示单位是周，h表示单位是小时，m表示单位是分钟，s表示单位是秒，如果纯数字，则默认是以小时为单位，如果示满足前面所有规则，则表示未到敲定间隔时间
        "validBookPeriod": "3m", //预定的有效期，数字后面跟y表示单位是年，M表示单位是月，w表示单位是周，h表示单位是小时，m表示单位是分钟，s表示单位是秒，如果纯数字，则默认是以小时为单位，如果示满足前面所有规则，则表示未到敲定间隔时间
        "informFrontInterval": "4h",//未升级的前端提醒间隔时间，数字后面跟y表示单位是年，M表示单位是月，w表示单位是周，h表示单位是小时，m表示单位是分钟，s表示单位是秒，如果纯数字，则默认是以小时为单位，如果示满足前面所有规则，则表示未到敲定间隔时间
        "logInterval": "7d" //日志需要上传的时间长度，数字后面跟y表示单位是年，M表示单位是月，w表示单位是周，h表示单位是小时，m表示单位是分钟，s表示单位是秒，如果纯数字，则默认是以小时为单位，如果示满足前面所有规则，则表示未到敲定间隔时间
    },
    "mode":"dev", //发布生产事项：要换成release, beta只是用于测试环境，dev是开发环境
    ...
    "cron":{//发布生产事项：要换成以下标准的配置
        "cronOnSoft": "@every 5h", //检测更新的时间间隔
        "cronOnStatus": "@every 5m",//检测设备状态及上传的间隔
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

### 使用流程
**本程序mock步骤(3月20号之前使用，之后废弃)**
1. 修改.server.json，修改好与sdk相关的路径及参数
2. footer-ali.exe run 启动主程序。注意，如果端口设置为80，需要管理员权限，另外如果有涉及系统盘的文件内容，请注意权限要调整到位。最好用管理员身份把程序变成系统服务，自动运行，且优先于其它程序。
3. sdk中的websocket地址变成：ws://127.0.0.1:[http.port]/[ws.dUrlPrefix], 当前默认配置是ws://127.0.0.1/dscan
4. 在浏览器中打开http://127.0.0.1:[http.port]/[http.dsUrl], 当前默认配置是http://127.0.0.1/dsmsg，可以模拟给sdk发ws消息，模拟时先open，然后输入约定的数据格式(具体内容请自行构建)发送即可
4. 在浏览器中打开http://127.0.0.1:[http.port]/[http.fsUrl], 当前默认配置是http://127.0.0.1/fsmsg，可以模拟前端发ws消息，模拟时先open，然后输入约定的数据格式(具体内容请自行构建)发送即可
5. 在浏览器中打开http://127.0.0.1:[http.port]/bbolt，可以直接察看数据库保存的内容
6. 在浏览器中打开http://127.0.0.1:[http.port]/l，可以直接察看本程序的日志，如果看不到，请调整配置文件中的相应目录配置
7. 在浏览器中打开http://127.0.0.1:[http.port]/s，可以直接察看sdk程序的日志，如果看不到，请调整配置文件中的相应目录配置
8. 在浏览器中打开http://127.0.0.1:[http.port]/ns，可以直接察看ns程序的日志，如果看不到，请调整配置文件中的相应目录配置
9. 在浏览器中打开http://127.0.0.1:[http.port]/ol，可以直接察看onlineupdate程序的日志，如果看不到，请调整配置文件中的相应目录配置
5. 在浏览器中打开http://127.0.0.1:[http.port]/bbolt，可以直接察看数据库保存的内容
6. 在浏览器中打开http://127.0.0.1:[http.port]/l，可以直接察看本程序的日志，如果看不到，请调整配置文件中的相应目录配置
7. 在浏览器中打开http://127.0.0.1:[http.port]/s，可以直接察看sdk程序的日志，如果看不到，请调整配置文件中的相应目录配置
8. 在浏览器中打开http://127.0.0.1:[http.port]/ns，可以直接察看ns程序的日志，如果看不到，请调整配置文件中的相应目录配置
9. 在浏览器中打开http://127.0.0.1:[http.port]/ol，可以直接察看onlineupdate程序的日志，如果看不到，请调整配置文件中的相应目录配置
10. 在浏览器中打开http://127.0.0.1:[http.port]/rd，可以触发未下载完成的下载进行断点续传
11. 在浏览器中打开http://127.0.0.1:[http.port]/cf， 可以查看配置文件的内容
12. 在浏览器中打开http://127.0.0.1:[http.port]/ij，可以触发更新检测
13. 在浏览器中打开http://127.0.0.1:[http.port]/cdi，可以触发清除下载和提醒记录

# 通讯格式约定

**bucket信息**

***场景***

本程序给软件sdk，需要软件sdk写入阿里sdk的配置文件中

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |

```json
{
    "topic":"deviceBucket", // required
    "padId":"xxx", // optional
    "params":{
        "endpoint":"xxx",
        "bucket":"xxx",
        "realBucket":"xxx",
        "id":"xxx",
        "key":"xxx"
    }
}
```

## wifi相关
### wifi操作指令
**场景**

由前端程序发起给设备端，一般是用户初始化或修改wifi时触发

**扫描wifi列表**

***场景***

本程序给软件sdk

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |

```json
{
    "topic":"wifiList", // required
    "padId":"xxx", // optional
}
```

**wifi状态查询**

***场景***

本程序给软件sdk

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |

```json
{
    "topic":"wifiStatus", // required
    "padId":"xxx", // optional
}
```

**返回wifi列表**

***场景***

软件sdk给本程序

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"wifiListResult", // required
    "status":"XXX",  // required
    "errorCode":0, // required
    "padId":"xxx", // optional
    "params":[{ // required
        "ssid":"XXX", //required wifi名称
        "rssi":"-50", //required 信号强度
        "isCurrent": false, //是否当前已连接的
        "isOurAp": false //是否当前自身创建的ap
    }]
}
```

**连接指定wifi**

***场景***

本程序给软件sdk

不管原来是否有连接，都替换，结果返回status

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"wifiConnect", // required
    "padId":"xxx", // optional
    "params":{ // required
        "ssid": "XXX", // requried 指定的wifi名称
        "pwd":"XXX" // required wifi密码
    }
}
```

**断开wifi**

***场景***

本程序给软件sdk，并返回状态

不管原来是否有连接，都执行断开，结果返回status

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"wifiDisconnect", // required
    "padId":"xxx", // optional
    "params":"xxx" // required 目标ssid
}
```

**返回wifi状态**

***场景***

软件sdk给本程序

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |

```json
{
    "topic":"wifiStatusResult", // required
    "status":"XXX",  // required
    "padId":"xxx", // optional
    "params":0 // required 不同的code代表不同的意思
}
```

## 设备相关
### 设备状态实时通知
**场景**

软件sdk给本程序

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"deviceStatusResult", // required
    "status":"XXX",  // required
    "padId":"xxx", // optional
    "params":0 // required 不同的code代表不同的意思
}
```

### 设备操作指令
**场景**

由前端程序发起给设备端，一般是用户操作时触发

**扫描**

***场景***

本程序给软件sdk，软件sdk执行扫描，过程中实时返回状态，扫描结束自动调用阿里算法获取测量结果、高精度、低精度stl文件并保存至约定目录（保存规则是指定目录下，由孟焦自动保存2个文件,idst_3d_foot.obj或是idst_3d_foot_simpled.stl）

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"scan", // required
    "padId":"xxx", // optional
    "params": {
        "scanId":"DEVICEID-YYYYMMDD-HHmmss", //required 作为本次扫描的唯一id：后续当scanId回传,同时也作为孟焦的localFileKey
        "savePath":"xxx", // required 同时也作为孟焦的model_dir
        "brandName":"xxx", // required
        "sex":0
    }
}
```

**扫描结果返回**

***场景***

软件sdk给本程序，软件sdk在扫描结束自动调用阿里算法获取测量结果、高精度、低精度stl文件并保存至约定目录（保存规则是指定目录下，由孟焦自动保存2个文件,idst_3d_foot.obj或是idst_3d_foot_simpled.stl）

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"scanResult", // required
    "status":"XXX",  // required
    "padId":"xxx", // optional
    "params":{ // required
        "scanId":"xxx", // required
        "errorCode":0,  // required
        "savePath":"xxx",
        "scan__qr_tag":"xxx",  // required, 字符串，用|隔开，依次为欧码、左右脚脚宽均值四舍五入到最近的5的整数倍（例如90/95/100/…），后三个数固定为0
        "foot_features":[{
            "images" : "xxx", // https://gw.alicdn.com/tfs/TB1pIzYrpOWBuNjy0FiXXXFxVXa-144-144.png
            "text" : "xxx" //分别为脚掌宽窄、脚背高低的结论
        }],
        "advise2":"xxx",
        "advise1":["xxx"],
        "sex":0,  // required
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
            "rlt_houtugao":1.0//后凸高
        }
    }
}
```

**上传**

***场景***

本程序给软件sdk，软件sdk调用孟焦算法上传，这里待与孟焦确认

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"upload", // required
    "padId":"xxx", // optional
    "params":{ // required
        "scanId":"xxx", // required 对应孟焦的localFileKey
        "type":"mini|scan|log|cloud", // required
        "saveName":"xxx", // required 对应孟焦的saveName, idst_3d_foot.obj或是idst_3d_foot_simpled.stl
        "filePath":"xxx" // required 对应孟焦的localFile
    }
}
```

**上传结果返回**

***场景***

软件sdk给本程序，软件sdk调用孟焦算法上传后要返回以下结果，这里待与孟焦确认

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"uploadResult",
    "status":"XXX",
    "padId":"xxx", // optional
    "errorCode":0,  // required
    "params":{ // required
        "scanId":"xxx", // required
        "ossUrl":"xxx", // optional
        "type":"mini|scan|log|cloud", // required
        "lastUploadTime":"2018-10-10 22:00:01",  //最后上传时间
        "uploadNum":0                      //required 上传次数，每次传1，如果失败则由本程序再触发
    }
}
```

**标定**

***场景***

本程序给软件sdk，并返回状态

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"calibration", // required
    "padId":"xxx", // optional
    "params":"left" //required 作为本次扫描的要求，值分别是left/right/compute，对应标定过程中的扫左脚、扫右脚、计算过程
}
```

**标定结果**

***场景***

软件sdk给本程序

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"calibrationResult", // required
    "status":"XXX",
    "padId":"xxx", // optional
    "errorCode":0,  // required
    "params":"left" //required 作为本次扫描的要求，值分别是left/right/compute，对应标定过程中的扫左脚、扫右脚、计算过程
}
```
- 标准物标定的各个类型值
    "params": "c1" // 标准物标定的第1个位置
    "params": "c2" // 标准物标定的第2个位置
    "params": "c3" // 标准物标定的第3个位置
    "params": "c4" // 标准物标定的第4个位置
    "params": "c5" // 标准物标定的第5个位置
    "params": "c6" // 标准物标定的第6个位置
    "params": "c7" // 标准物标定的第7个位置
    "params": "c8" // 标准物标定的第8个位置
    "params": "8compute" // 标准物标定的计算

**重置**

***场景***

本程序给软件sdk，并返回状态

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"reset", // required
    "padId":"xxx", // optional
}
```

**硬盘id**

***场景***

本程序给软件sdk，软件sdk返回硬盘id

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"diskId", // required
    "padId":"xxx", // optional
}
```

**硬盘id返回**

***场景***

软件sdk给本程序，软件sdk返回硬盘id

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"diskIdResult", // required
    "status":"XXX",
    "padId":"xxx", // optional
    "errorCode":0,  // required
    "params":"xxx" // required 是当前的diskid值
}
```

**license信息写入指令**

***场景***

本程序给软件sdk，由软件sdk写入到指定的文件中

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"licenseWrite", // required
    "padId":"xxx", // optional
    "params":"xxx" // required 是当前的license值
}
```

**打开设备将开启**

***场景***

本程序给软件sdk，软件sdk初始化设备，并返回状态

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"deviceOpen", // required
    "padId":"xxx", // optional
}

**设备状态指令**

***场景***

本程序给软件sdk，软件sdk返回状态

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"deviceStatus", // required
    "padId":"xxx", // optional
}
```

**设备调试模式开启**

***场景***

本程序给软件sdk，软件sdk设置为debug模式并返回状态

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"debug", // required
    "padId":"xxx", // optional
}
```

**设备调试模式关闭**

***场景***

本程序给软件sdk，软件sdk设置为debug关闭模式并返回状态

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"debugoff", // required
    "padId":"xxx", // optional
}
```

**设备接入**

***场景***

软件sdk给本程序，硬件接入的时候，更新硬件信息

注意，本接口无返回消息，详情请查看日志

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"deviceUp", // required
    "padId":"", // optional
    "params":{
        "modelCode":"XXX",// required
        "version":"XXX",
        "productLine":"XXX",// required
        "env":"XXX",// required beta/release
        "sn":"XXX", // required if scan product line, this is a encryptcode or ple file name
        "validTo":"XXX", //有效期, optional
        "modulars":[{ //模块列表, optional
            "modelCode":"XXX", // required
            "sn":"XXX", //模块序列号, optional
            "validTo":"XXX", //模块有效期, optional
            "status":true
        }],
        "status":true
    }
}
```

**软件**

***场景***

软件sdk给本程序，获取本程序当前所有计入的软件信息，可以更新软件信息
软件在启动时，应该要给程序2个soft的信息，modelCode分别是foot3dscanfirmware和foot3dscan

注意，本接口无返回消息，详情请查看日志

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
 {
     "topic":"softUp", // required
     "padId":"", // optional
     "params":{
        "modelCode":"XXX", // required
        "version":"0.0.0.0", // required
        "env":"production", // default is release/beta
        "tracingStatus":"false", //是否允许采集, optional, true/false, 注意是字符串
        "sn":"XXX", //软件序列号, optional
        "installPath":"XXX", //optional
        "validTo":"XXX", //有效期, optional
        "modulars":[{ //模块列表, optional
            "modelCode":"XXX",
            "sn":"XXX", //模块序列号, optional
            "validTo":"XXX", //模块有效期, optional
            "status":true //模块是否启用
        }],
        "lang":"XXX"
     }
}
```

## 1.4需求相关

**license请求**

***场景***

软件sdk给本程序，本程序返回licenseWrite指令

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic":"licenseResult", // required
    "padId":"xxx" // optional
}
```

### ota可升级消息
**场景**

设备端发给本程序，告诉u盘检测到有可执行的程序。
注意每次这种方式升级时，软件要先提取softUp.json中的信息，如果提取不到，则直接放弃升级，如果提取到：
1、如果overwrite值是y，则直接升级，不管版本；
2、如果overwrite值不是y，则判断版本是否比当前版本新，如果新才发本消息；发消息时要注意文件路径带上

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic": "otaUpgradable", // required
    "padId": "", 
    "data": {
        "modelCode":"XXX",
        "adaptiveModel":"einscan-pro,einscan-plus",
        "adaptiveModular":"",
        "file":"c:\down\aaa.exe",
        "lang":"",
        "type":"", // install_package/patch/firmware/other
        "env":"", // release/beta
        "maxVersion":"",
        "minVersion":"",
        "os":"win",
        "version":"2.7.0.6",
        "versionCNLog":"xxx",
        "versionLog":"xxx"
    }
}
``` 

### 升级执行通知
**场景**

本程序发给设备端，指示执行升级,一般是指前端确认的执行指令
protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic": "upgradeExec", // required
    "padId": "", 
    "data": {
        "adaptiveModel":"einscan-pro,einscan-plus",
        "adaptiveModular":"",
        "file":"c:\down\aaa.exe",
        "lang":"",
        "type":"", // install_package/patch/firmware/other
        "env":"", // release/beta
        "maxVersion":"",
        "minVersion":"",
        "os":"win",
        "version":"2.7.0.6",
        "versionCNLog":"xxx",
        "versionLog":"xxx"
    }
}
``` 

### U盘状态检测
**场景**

由本程序发给设备端

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic": "checkUDiskStatus", // required
    "padId": "", // empty
    "data": {
    }
}
``` 

### 错误预警消息
**场景**

由设备端发给本程序

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic": "logAlert", // required
    "padId": "", // empty
    "data": {
        "msg": "xxx",//错误内容
    }
}
``` 

### U盘状态检测结果
**场景**

由设备端发给本程序，返回U盘连接状态

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic": "checkUDiskResult", // required
    "padId": "", // empty
    "data": {
        "status": "success",//设备未就绪
        "errorCode":0, 
        "name":"xxx", //名称
        "size":3333, //尺寸
        "capibility": 444, //剩余容量
        "logSize":5555 //日志大小
    }
}
``` 

### 日志拷贝通知
**场景**

由本程序发起给设备端，通知开始把日志拷贝到U盘

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic": "copyLog", // required
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
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic": "copyLogResult", // required
    "padId": "", // empty
    "data": {
        "status": "success",//设备未就绪
        "errorCode":0
    }
}
``` 

### 点云数据上传
**场景**

由设备端发起给本程序

protocol|namespace|event|doc version|
:-----:|:------: |:-:     |:------:
SOCKET | /dscan| notify | 1.0.0 |
```json
{
    "topic": "cloudData", // required
    "padId": "", // empty
    "data": {
        "scanId": "xxx",// required
        "filePath":"xxx"// required
    }
}
``` 

## 异常码


### 以下为先临异常码
异常码|	异常描述| 需要管理员处理异常
---|---|-|
**0**	|**非异常，无需关注**
**1**	|**未知异常**               |**Y**
**1000**	|**硬件异常**
100001	|设备异常               |**Y**
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

## 用户在平板上的常用流程

注意，下面的流程环节中不包含那些不需要设备端介入的部分

- 第一次设置
    - 前端发status指令获取设备端状态，是待设置中(waitSetting)状态才进入下一步
    - wifi设置：
        - 前端发wifi状态指令获取wifi状态，如果是已连接状态则跳过设置(除非用户要变更设置)，否则继续；
        - 前端发wifi列表指令获取wifi列表；
        - 用户选择其中1个输入密码由前端发送连接指定wifi指令
        - 设备端返回状态，如果状态是connected，则继续，否则提示用户重新选择输入；
    - 设备授权：
        - 前端发status指令获取设备端状态，是待设置中(waitSetting)状态才进行授权操作
        - 前端发门店指令、绑定门店
        - 设备端检查授权(如果没下载，则自动下载，下载完进行授权校验)并返回设备状态，如果还是待设置中(waitSetting)状态，则需要提醒用户联系客服或重试，如果设备处于free状态则表示第一设置成功。
- wifi设置修改：同第一次设置中的wifi设置
    - 注意，设备端会定时扫描wifi的网络状态，如果不是已连接状态会实时返回给前端
- 扫描：
    - 前端发status指令获取设备端状态，free状态才可以继续，否则提示用户
    - 前端发扫描指令
    - 设备端执行扫描并实时返回状态，前端根据返回的状态实时更新界面
    - 设备端计算结束时，返回数据的计算结果，前端根据返回的结果显示界面内容；设备端自动上传扫描结果；
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