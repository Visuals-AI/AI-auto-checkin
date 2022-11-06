# AI-auto-checkin

> AI 自动考勤

------

## 0x00 运行环境

![](https://img.shields.io/badge/Windows-x64-brightgreen.svg) ![](https://img.shields.io/badge/Mac-x64-brightgreen.svg) ![](https://img.shields.io/badge/Linux-x64-brightgreen.svg)

![](https://img.shields.io/badge/Python-3.8-red.svg)


## 0x10 项目说明

相信很多人都有上下班忘记考勤签到的问题，此项目就是为了解决这个问题。

只要在 PC 运行此程序，即可通过 PC 摄像头进行 AI 人脸识别；只要 AI 判定是本人，就能够用 ADB 触发手机上的考勤程序进行自动打卡。

> 使用 ADB 能支持大部分 Android 的考勤程序


## 0x20 程序原理

```mermaid
sequenceDiagram
    participant 人脸识别服务
    participant 定时打卡脚本
    participant ADB
    participant 考勤手机
    人脸识别服务->>人脸识别服务: 用摄像头采集<br/>【我】的面部特征
    Note right of 人脸识别服务: 正脸 & 侧脸
    ADB->>考勤手机: 连接
    Note left of 考勤手机: 有线
    定时打卡脚本->>定时打卡脚本: 检查打卡时间
    Note right of 定时打卡脚本: 触发打卡脚本
    loop 自动打卡
        定时打卡脚本->>人脸识别服务: 激活摄像头画面
        人脸识别服务->>定时打卡脚本: 识别【我】是否在画面内
        定时打卡脚本->>ADB: 调用 ADB 指令
        ADB->>考勤手机: 解锁屏幕
        ADB->>考勤手机: 启动考勤程序
        ADB->>考勤手机: 模拟按键打卡
        ADB->>考勤手机: 锁屏
        考勤手机->>定时打卡脚本: 记录打卡时间
    end
```

> 理论上不需要人脸识别也能使用，但安全性会大大降低，毕竟万一不在工位时、手机被 ADB 解锁了 ...


## 0x30 硬件接线

| 硬件 | 要求 | 用途 |
|:---:|:---|:---|
| PC 摄像头 | 内置/外设均可 | 用于 AI 人脸识别，作为触发解锁手机考勤的安全条件 |
| 手机支架 | 可充电、支持数据传输 | 用于接收 ADB 指令 |

> 如果你的考勤程序不需要进一步做人脸识别（如钉钉等），可以把手机支架换成数据线


![](./imgs/01.jpg)



## 0x40 实机演示

TODO


## 0x50 使用步骤

### 0x51 预操作：设置标准脸 

标准脸，即用于人脸识别过程中、对齐五官坐标的脸，是类似参考系一般的存在。

因为摄像头在拍摄的时候，我们的脸不可能每次都刚好完全在同一个 **角度/位置/距离**，如果不对齐两张脸直接进行比对，就会导致即使是同一人都没法识别出来。

这时就需要一张标准脸，把我们拍摄的所有人脸，都 **旋转/平移/缩放** 到和标准脸一样的 **角度/位置/距离**，就能在确保一定误差范围内识别人脸。

此项目对设置标准脸的方法做了一定的封装，具体设置的方法如下：

1. 网上任意找一张人脸，最好相对规正的正脸，如 [吴彦祖-正脸.png](./face/00_standard/吴彦祖-正脸.png)
2. 用 PhotoShop 将其裁剪加工，做成五官在画面正中的 `N x M` 的头像（N、M 可以为任意值，建议 `N = M`，如 `512 x 512`）
3. 修改 [settings.xml](./conf/settings.yml) 中的 `mediapipe.standard_face` 值为 `N x M`
4. 执行命令 `python ./presrc/gen_standard.py`
5. 根据提示选择第 2 步加工后的头像照片
6. 如无异常，即成功生成标准脸数据到 [`data/standard`](./data/standard/) 目录下，如 [`512 x 512`](./data/standard//512x512)
7. 标准脸只需要设置一次即可，当设置有多个时，以 [settings.xml](./conf/settings.yml) 的 `mediapipe.standard_face` 设置值为准

> 此项目已预生成了一张**标准正脸**数据，如果使用场景需要**标准侧脸**，建议重新设置


### 0x52 预操作：建库

1. 执行命令 `python ./presrc/gen_pdm.py`
2. 如无异常即创建 sqlite3 成功

> 数据库只需要创建一次，主要用于存储【你】的人脸特征值


### 0x53 预操作：录入【你】的人脸特征

