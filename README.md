# Lightweight-Screenshot tool轻量截屏工具

使用Python语言写的适用于windows系统的实用性截图软件，最新版本2.0.0，正在更新

## 计划功能

1.✅全屏截图

2.✅矩形截图

3.✅录制GIF

4.✅录制视频（❌录制声音）

5.❌指定窗口录制（待考虑）

6.✅快捷键

7.❌图形化界面设置

8.❌加水印

9.❌屏幕批注

10.❌图形化设置（目前仅能手动修改settings.json）

## 更新日志


### 0.1
使用wxpython做界面
### 0.2
改用tkinter做全局界面

### 1.0 alpha
添加了全局快捷键，重要更新

### 1.1 beta
前四项功能已实现，增加了使用pystray制作的系统托盘功能。去掉了grab.py，将其主要功能函数删减并与main.pyw合并

运用多线程，但是python多线程不能很好地利用多核处理器（GIL惹得），录制屏幕视频时不能录制GIF

### 1.2 beta
新增UI.py，包括一些控件。
基本完善了功能，但是快捷键有问题，不能图形化设置，请手动修改settings.json

### 1.3 beta
更改了为了修复快捷键bug修改了快捷键，目前快捷键没有问题。录屏和录制屏幕GIF可以同时进行，功能更完善。改UI.py为Widgets.py，退出是新增对话框询问是否确定要退出，防止点错

### 1.7 beta
修复了小bug，并且更改了托盘图标菜单

### 2.0 beta
更改了界面，全面使用ttkbootstrap，即将完成图形化设置功能

## 第三方库
PIL，pynput，pyaudio，pyopencv2，pystray，moviepy，pyinstaller，ttkbootstrap

## ⚠️警告
目前2.0.0版本由于打包问题无法正常使用

## ⚠️由于其他原因已停止更新
1.有点想弃坑，但打算继续搞

2.python本身运行效率低，写截图类实用工具可能不太合适

## 效果图
（2.0版本）
![2023-02-12_16_17_15](https://user-images.githubusercontent.com/111341725/218300549-e0040ea7-3920-43c0-b5c7-65b6e2cb1d46.jpg)
