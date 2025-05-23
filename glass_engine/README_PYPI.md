# Glass Engine -- 相当易用的 Python 3D 渲染引擎

![glass engine logo](https://gitee.com/time-coder/Glass-Engine/raw/main/glass_engine/images/glass_engine_logo256.png)

**Glass Engine** 是一个相当易用的 Python 实时 3D 渲染引擎，完全免费开源。使用 **Glass Engine** 你可以轻松地在你的 Python 界面程序中嵌入可交互的 3D 画面。

首先，使用以下命令即可完成对 **Glass Engine** 的安装：

```
pip install glass-engine
```

如果你是中国区用户，则可以使用以下命令以加速安装过程：

```
pip install glass-engine -i https://mirrors.aliyun.com/pypi/simple
```

若发生安装错误，请参考 [Glass Engine 的安装教程](https://glass-engine-doc.readthedocs.io/zh/latest/installation/installation.html) 进行解决。

接下来，让我们通过一个简单例子来直观感受一下 **Glass Engine** 的使用过程：

```python
from glass_engine import *
from glass_engine.Geometries import * # 导入所有的基本几何体

scene, camera, light, floor = SceneRoam() # 创建基本场景

sphere = Sphere() # 创建一个球体模型
sphere.position.z = 1 # 设置球体位置
scene.add(sphere) # 将球体添加到场景中

camera.screen.show() # 相机显示屏显示渲染结果
```

上述代码首先使用 ``SceneRoam`` 创建出一个基本场景，包括了相机、光源、地板，然后往场景中添加了一个球体模型，最后将相机观察到的视口显示出来。

可以看出，使用 **Glass Engine** 创建 3D 场景无需自定义任何类和任何函数，仅通过对象创建、方法调用的顺序程序结构就可完成场景的构建和显示，由此体现出 **Glass Engine** 高度的易用性，这也是 **Glass Engine** 相比于其他同类 3D 引擎的优势所在。

运行上述程序，你将得到下图所示结果：

![glass engine simple scene](https://gitee.com/time-coder/Glass-Engine/raw/main/glass_engine/images/start.png)

你可以通过鼠标右键拖动以旋转视角，还可通过键盘按键 <kbd>W</kbd> <kbd>A</kbd> <kbd>S</kbd> <kbd>D</kbd> <kbd>E</kbd> <kbd>C</kbd> 来在场景中漫游：

* <kbd>A</kbd> 向左移动，<kbd>D</kbd> 向右移动
* <kbd>W</kbd> 向前移动，<kbd>S</kbd> 向后移动
* <kbd>E</kbd> 向上移动，<kbd>C</kbd> 向下移动

怎么样，是不是很简单、直观、易用？如果你感兴趣的话，就让我们开始接下来的 3D 渲染之旅吧！

* [Github 项目主页](https://github.com/Time-Coder/Glass-Engine)
* [Gitee 项目主页](https://gitee.com/time-coder/Glass-Engine)
* [文档](https://glass-engine-doc.readthedocs.io/zh/latest/)

## Release notes

### version 0.1.61

* 升级 tree-sitter 为现代版
* 优化预处理调用时机，减少调用次数

### version 0.1.57

* 兼容 Python 3.13

### version 0.1.54

* 修复 bug [#4](https://github.com/Time-Coder/Glass-Engine/issues/4): "view_pos.y" is used before being initialized
* 修复 bug [#5](https://github.com/Time-Coder/Glass-Engine/issues/5): ShaderToy 动态纹理文件不存在
* 修复 bug [#6](https://github.com/Time-Coder/Glass-Engine/issues/6): ImportError: cannot import name 'Self' from 'typing'
* 修复 bug [#7](https://github.com/Time-Coder/Glass-Engine/issues/7): #version directive error

### temp version 0.1.52

* 添加深度树摇尝试修复 bug #3
* 临时版本，代码结构有待优化

### version 0.1.51

* 修复相机挂载到有缩放的节点位置不对的 bug
* 将所有屏幕四边形绘制取消依赖顶点和索引
* 去除不必要的 FBO

### version 0.1.39

* 兼容 Linux
* 支持 PyInstaller 无配置打包

### version 0.1.36

* 修复纹理数超过硬件限制问题

### version 0.1.35

* 修改 PyPI 主页文档

### version 0.1.34

* 删除对 OpenEXR 的依赖，使用 opencv 读取 exr

### version 0.1.33

* 修复打包错误

### version 0.1.31

* 将 OpenGL 封装模块分离出来并单独打包为 [python-glass](https://pypi.org/project/python-glass/)
* 将模型加载模块分离出来并单独打包为 [assimpy](https://pypi.org/project/assimpy/)
* 模型加载支持内置纹理
* 添加对 metallic-roughness map 的支持

### version 0.1.30

* 兼容了 AMD 显卡
* 修复仅有天空盒不显示 bug
* 优化 shader 逻辑
* 改进 Qt API 选择逻辑

### version 0.1.29

* 修改动态加载新功能代码 bug

### version 0.1.28

* 修改 pcpp 冲突 bug

### version 0.1.27

* 禁用滚轮
* 修改 Python 3.7 f-string bug

### version 0.1.26

* 添加 treeshake 功能，自动删除 glsl 无用函数
* 添加功能自动剪裁功能，没有用到的功能不参与 glsl 编译

### version 0.1.25

* 添加 minifyc 进一步减小 glsl 代码体积，避免 OSError: 0x000000010 bug

### version 0.1.24

* 修复 OSError: 0x000000010 bug
* 修复 dynamic_env_map 开启再关闭失效 bug
* 修复 cast_shadows 开启再关闭失效 bug
* 修复 16bits 灰度图像加载错误 bug

### version 0.1.23

* 修复后处理 bug
* 修复半透明 bug

### version 0.1.22

* 支持了 Python 3.12
