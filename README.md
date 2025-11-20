# DesktopPet-playground
> 一个用 Python 和 PySide6 制作的桌宠程序，目前为单文件版本，用于练手和实验  
> A desktop pet program made with Python and PySide6, single-file version for practice and experimentation.

---

## 项目简介 / Project Overview

这个项目实现了一个可以在桌面自由移动的桌宠：
- 支持不同状态的动画（idle / walk）  
- 鼠标拖动  
- 随机行为（自动走动或坐下）  
- 点击切换状态  
- 桌宠保持在最上层，不会被其他窗口遮挡  

This project implements a desktop pet that can freely move on your screen:
- Supports multiple animation states (idle / walk)  
- Can be dragged with the mouse  
- Random behavior (walk or sit automatically)  
- Click to switch states  
- Pet stays on top and won’t be hidden by other windows  

当前版本为单 Python 文件，方便快速实验。  
This version is a single Python file for easy experimentation.

---

## 运行环境 / Requirements

- Python 3.8+  
- PySide6  
- macOS 系统（桌面层效果针对 macOS）  

Install dependencies:

```bash
pip install PySide6 pyobjc
````

> macOS 用户推荐先安装 pyobjc 来支持桌面层功能；Windows 用户可以暂时忽略。
> macOS users should install pyobjc to support desktop-level features; Windows users can ignore for now.

---

## 使用方法 / How to Run

1. 下载或克隆仓库 / Clone the repository：

```bash
git clone https://github.com/你的用户名/DesktopPet-playground.git
cd DesktopPet-playground
```

2. 运行程序 / Run the program：

```bash
python main.py
```

3. 桌宠会出现在屏幕中央：

   * 左键拖动移动桌宠 / Drag with left mouse button
   * 右键切换状态（走/坐） / Right-click to switch state (walk/sit)
   * 鼠标覆盖时可以暂停移动 / Mouse hover can pause movement

---

## 文件说明 / File Structure

* `main.py` ：项目入口，创建桌宠窗口和启动程序 / Entry point, creates pet window and runs program
* `assets/` ：存放桌宠动画图片（idle / walk 等） / Folder for pet animation images (idle / walk, etc.)

---

## 后续计划 / Future Plans

* 支持多只桌宠同时存在 / Support multiple pets at the same time
* 增加不同桌宠的互动行为 / Add different interactions for different pets
* 多状态、多动作动画 / More states and animations
* 配置文件化创建桌宠 / Create pets via configuration file

---

## 注意 / Note

目前桌宠仅在 macOS 上实现桌面层效果，Windows 上桌宠仍然会在普通窗口上方显示。
Currently, the desktop-layer effect works only on macOS. On Windows, the pet will appear above normal windows.

