# LightScreenShot

使用Python写的学习型和实用性截图软件，正在更新

计划功能：

1.✅全屏截图

2.✅矩形截图

3.❌录制GIF

4.❌录制视频

5.❌指定窗口录制（待考虑）

更新日志如下
## 0.1
使用wxpython做界面
## 0.2
改用tkinter做全局界面

5.设置（✅保存模式：储存到指定位置或储存到剪切板；✅储存位置：目录；❌录屏模式：录制内部声音或麦克风声音或不录制声音，录制质量等）
在settings.json文件中，目前仅能手动修改

## 1.0 alpha

计划功能：

1.✅全屏截图

2.✅矩形截图

3.✅录制GIF（理论上可以，还不完善）

4.✅录制视频

5.❌指定窗口录制（待考虑）

6.❌设置

## 1.1 beta
前四项功能已实现，增加了使用pystray制作的系统托盘功能

运用多线程，但是python多线程不能很好地利用多核处理器（GIL惹得），录制屏幕视频时不能录制GIF

## 1.2 beta
基本完善了功能，但是快捷键有问题，不能图形化设置，请手动修改settings.json

使用第三方库：PIL，pynput，sounddevic
e，pyopencv2，pystray

![image](https://user-images.githubusercontent.com/111341725/216746287-4bcb13e2-35b3-41a1-8cdb-37c12c5dd198.png)
![2023-02-04_11_35_06](https://user-images.githubusercontent.com/111341725/216746291-e864d00e-c81d-4886-8f88-55fdeb60aae5.gif)
https://user-images.githubusercontent.com/111341725/216746310-950ba1b9-3621-4834-a460-8b14dcad5308.mp4

