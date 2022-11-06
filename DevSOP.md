# 开发者手册

------

本项目的人脸识别依赖 Mediapipe 和 dlib



adb：连接华为手机 https://cto.eguidedog.net/node/609
adb 无线： https://blog.csdn.net/ai_qh77/article/details/123383801
adb： error: device unauthorized. https://stackoverflow.com/questions/23081263/adb-android-device-unauthorized
adb 指令： https://www.cnblogs.com/botoo/p/9655798.html?share_token=bc2d44e1-e6d5-40fd-9890-7c6b8eebc8ed
 
*#*#2846579#*#*



```shell
# 进入 shell (可以不进入)
adb shell

# 唤醒屏幕
adb shell input keyevent 224

# 滑动调出密码输入
adb shell input swipe 300 1000 300 500

# 输入锁屏密码
adb shell input text <password>

# 返回首页
adb shell input keyevent 3

# 查找 GT 包名
adb shell dumpsys window w | grep "geniustalk"
# com.dji.geniustalk/com.dji.geniustalk.ui.main.HomeActivity

# 调起 GT (不支持， GT 设置了 android:exported="false" 禁止外部调用)
adb shell am start com.dji.geniustalk/com.dji.geniustalk.ui.main.HomeActivity

# 微信是可以的
adb shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI

# 点击屏幕坐标逐步打开 (座标可以截屏再通过画图工具查看)
# 点开分类
adb shell input tap 411 1387

# 点开 GT
adb shell input tap 800 706

# 选择应用
adb shell input tap 543 2051

# 点击打卡
adb shell input tap 896 849
```





mac install dlib
https://blog.csdn.net/Robin_Pi/article/details/119909829




利用机器学习进行人脸468点的3D坐标检测，并生成3D模型 https://www.toutiao.com/article/6913754944206258696/?app=news_article&timestamp=1666621808&use_new_style=1&req_id=202210242230080102121621361C58653B&group_id=6913754944206258696&wxshare_count=1&tt_from=weixin&utm_source=weixin&utm_medium=toutiao_android&utm_campaign=client_share&share_token=2903d457-7d99-47f1-bce3-1787abde8660&source=m_redirect&wid=1666629121540

https://blog.csdn.net/u012505617/article/details/89191158


定时任务： https://cloud.tencent.com/developer/article/1887717
欧氏距离等： https://blog.csdn.net/Kevin_cc98/article/details/73742037
人脸相似度比对： https://cloud.tencent.com/developer/article/1775752
人脸相似度计算： https://blog.csdn.net/u014657795/article/details/85850891?share_token=e5d5a8d7-ebd4-4c43-9285-f9afbff9aade
mediapipe 官方文档 https://google.github.io/mediapipe/solutions/face_mesh
                    https://steam.oxxostudio.tw/category/python/ai/ai-mediapipe-face-mesh.html

以图搜图 https://cloud.tencent.com/developer/article/1487432

mediapipe的坐标已经归一化，需要乘以宽高得到初始坐标 https://blog.csdn.net/qq_64605223/article/details/125606507

入门 https://www.stubbornhuang.com/1490/

归一化 相似度 https://blog.csdn.net/xsdxs/article/details/49857591
            https://zhuanlan.zhihu.com/p/158199835?utm_id=0


L2抑制 https://blog.csdn.net/u010725283/article/details/79212762

- 《[人脸三维关键点检测 + 颜值打分](https://www.bilibili.com/video/BV1ei4y1d7zA/?is_story_h5=false&p=4&share_from=ugc&share_medium=android&share_plat=android&share_session_id=0b5ebe12-cde7-48e8-a079-fd406805866a&share_source=WEIXIN&share_tag=s_i&timestamp=1666659516&unique_k=NommQi6)》
468 个特征点编号 https://blog.csdn.net/weixin_52465909/article/details/122183670

框取人脸 https://blog.csdn.net/weixin_43229348/article/details/120524852
使用opencv在视频上添加文字和标记框 https://blog.csdn.net/weixin_30852419/article/details/97603572


https://www.jianshu.com/p/6ed3e26b4ebc?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation


dlib 人脸对齐 https://www.bilibili.com/video/BV1J94y1D7f2/?is_story_h5=false&p=1&share_from=ugc&share_medium=android&share_plat=android&share_session_id=21a0f014-ad8d-419f-b92f-852823a4d623&5种最著名的人脸识别算法和关键特征介绍 share_source=WEIXIN&share_tag=s_i&timestamp=1667087907&unique_k=d1j29L6
https://blog.csdn.net/tsingsee/article/details/121514932?share_token=8012fabd-4bcb-4d28-abff-823a195e8eaf

定时任务：https://www.cnblogs.com/leffss/p/11912364.html

5种最著名的人脸识别算法和关键特征介绍 https://blog.csdn.net/tsingsee/article/details/121514932?share_token=8012fabd-4bcb-4d28-abff-823a195e8eaf


https://blog.csdn.net/weixin_52465909/article/details/122183670