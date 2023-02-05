# LightScreenShot

使用Python写的学习型和实用性截图软件，正在更新

计划功能：

1.✅全屏截图

2.✅矩形截图

3.✅录制GIF

4.✅录制视频（❌录制声音）

5.❌指定窗口录制（待考虑）

6.✅快捷键

7.✅图形化界面设置

8.❌加水印

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
前四项功能已实现，增加了使用pystray制作的系统托盘功能。去掉了grab.py，将其主要功能函数删减并与main.pyw合并

运用多线程，但是python多线程不能很好地利用多核处理器（GIL惹得），录制屏幕视频时不能录制GIF

## 1.2 beta
新增UI.py，包括一些控件。
基本完善了功能，但是快捷键有问题，不能图形化设置，请手动修改settings.json

## 1.3 beta
更改了为了修复快捷键bug修改了快捷键，目前快捷键没有问题。录屏和录制屏幕GIF可以同时进行，功能更完善。改UI.py为Widgets.py，退出是新增对话框询问是否确定要退出，防止点错

## 使用第三方库
PIL，pynput，sounddevice，pyopencv2，pystray

![image](https://user-images.githubusercontent.com/111341725/216746287-4bcb13e2-35b3-41a1-8cdb-37c12c5dd198.png)
![2023-02-04_11_35_06](https://user-images.githubusercontent.com/111341725/216746291-e864d00e-c81d-4886-8f88-55fdeb60aae5.gif)
