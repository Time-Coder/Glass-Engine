# Glass Engine -- 相当易用的 Python 3D 渲染引擎

![glass engine logo](https://gitee.com/time-coder/Glass-Engine/raw/main/glass_engine/images/glass_engine_logo256.png)

**Glass Engine** 是一个相当易用的 Python 实时 3D 渲染引擎，完全免费开源。使用 **Glass Engine** 你可以轻松地在你的 Python 界面程序中嵌入可交互的 3D 画面。

首先，使用以下命令即可完成对 **Glass Engine** 的安装：

```
pip install glass-engine
```

如果你是中国区用户，则可以使用以下命令以加速安装过程：

```
pip install glass-engine -i https://pypi.tuna.tsinghua.edu.cn/simple
```

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

并可通过鼠标滚轮来缩放场景。

怎么样，是不是很简单、直观、易用？如果你感兴趣的话，就让我们开始接下来的 3D 渲染之旅吧！

* Github 项目主页：<https://github.com/Time-Coder/Glass-Engine>
* Gitee 项目主页：<https://gitee.com/time-coder/Glass-Engine>
* 文档：<https://glass-engine-doc.readthedocs.io/zh/latest/>

## 说明
* 若发生 PyOpenGL-accelerate 安装失败的情况，请到 [github](https://github.com/Time-Coder/Glass-Engine/tree/main/PyOpenGL-accelerate) 或 [gitee](https://gitee.com/time-coder/Glass-Engine/tree/main/PyOpenGL-accelerate) 手动下载 PyOpenGL-accelerate for Python 3.12 的 wheel 包并使用 pip install 安装；
* 若发生 moderngl 安装失败的情况，请到 [github](https://github.com/Time-Coder/Glass-Engine/tree/main/moderngl) 或 [gitee](https://gitee.com/time-coder/Glass-Engine/tree/main/moderngl) 手动下载 moderngl for Python 3.12 的 wheel 包并使用 pip install 安装。

## Release note

* version 0.1.26:
    * 添加 treeshake 功能，自动删除 glsl 无用函数
    * 添加功能自动剪裁功能，没有用到的功能不参与 glsl 编译

* version 0.1.25:
    * 添加 minifyc 进一步减小 glsl 代码体积，避免 OSError: 0x000000010 bug

* version 0.1.24:
    * 修复 OSError: 0x000000010 bug
    * 解决 dynamic_env_map 开启再关闭失效 bug
    * 解决 cast_shadows 开启再关闭失效 bug

* version 0.1.23:
    * 修复后处理 bug
    * 修复半透明 bug

* version 0.1.22:
    * 支持了 Python 3.12
