# AI-auto-checkin

> AI 自动考勤

------

## 运行环境

![](https://img.shields.io/badge/Windows-x64-brightgreen.svg) ![](https://img.shields.io/badge/Mac-x64-brightgreen.svg) ![](https://img.shields.io/badge/Linux-x64-brightgreen.svg)

![](https://img.shields.io/badge/Python-3.8-red.svg)


## 项目说明

相信很多人都有上下班忘记考勤签到的问题，此项目就是为了解决这个问题。

只要在 PC 运行此程序，即可通过 PC 摄像头进行人脸识别；只要判定是本人，就能够触发手机上的考勤程序进行自动打卡。

> 只要能安装在 Android 的考勤程序都能使用


## 程序原理

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

## 硬件接线

硬件要求：

- PC 摄像头： 用于 AI 人脸识别，作为触发解锁手机考勤的安全条件
- 支持数据传输的可充电式手机支架： 用于接收 ADB 指令

> 如果你的考勤程序不需要进一步做人脸识别（如钉钉等），可以把手机支架换成数据线


![](./imgs/01.jpg)



## 实机演示

TODO


## 