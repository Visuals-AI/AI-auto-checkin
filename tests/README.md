# 单元测试

------

| 测试用例 | 测试场景 | 执行命令 | 测试条件 | 
|:---:|:---|:---|:---|
| ADB 测试 | ADB 命令 | `python ./tests/test_adb.py -p [unlock_password]` | 需用调试模式连接手机 |
| 摄像头测试 | 人脸方框检测 | `python ./tests/test_camera.py -d` | 需要摄像头 |
| 摄像头测试 | 人脸网格检测 | `python ./tests/test_camera.py -m` | 需要摄像头 |
| 视频测试 | 人脸方框检测 | `python ./tests/test_video.py -d` | 无 |
| 视频测试 | 人脸网格检测 | `python ./tests/test_video.py -m` | 无 |
| 人脸检测 | 网格检测 | `python ./tests/test_mesh.py -c` | 无 |
| 人脸检测 | 五官检测 | `python ./tests/test_detection.py -c` | 无 |
| 人脸对齐 | 人脸对齐 | `python ./tests/test_alignment.py -c` | 需要生成标准脸数据，作为仿射变换参照系 |
| 人脸比对 | 特征值比较 | `python ./tests/test_compare.py -c` | 需要录入预设人脸，作为特征匹配的比对基准 |
