Glass -- 为 Glass Engine 提供 OpenGL 易用封装
================================================================

**Glass** 为 **Glass Engine** 的子项目，为 OpenGL Assistant 的缩写。
OpenGL 函数的底层接口的设计为了跨平台，牺牲了易用性。
为了使 OpenGL 的调用对 Python 用户更友好，封装了 **Glass** 库。
该库简化了大量 OpenGL 概念以及函数调用方法，几项重点简化包括：

- 支持从文件编译 Shader，支持在 Shader 中使用 ``include``，并将报错行号指向真实的 include 文件；
- ShaderProgram 自动采用增量编译策略，仅当文件和依赖改变时重新编译；
- 设置 Uniform/Uniform Block/Shader Storage Block 变量时，Python 对象可直接赋值给 Shader 中的对应结构变量；
- 提供 Vertices/Indices 类对顶点和索引进行管理，用户无需接触 VBO/VAO/EBO 等直接操作显存的概念；
- 变化的顶点和索引采用增量拷贝算法同步到显存，提高拷贝效率。

下面是一段不完整的代码展示了 glass 操作 OpenGL 的方法：

.. highlight:: python3

::

    from glass import *

    # 在一个合法的 OpenGL 上下文中：

    # 创建 shader 程序
    program = ShaderProgram()
    program.compile("path/to/vertex_shader.vs")
    program.compile("path/to/fragment_shader.fs")
    # 上述两个 compile 并不会每次运行都编译，仅首次以及 Shader 文件修改后才编译
    # shader 文件中可含有 #include 语法

    # 将 Python 变量 pyvar 直接赋值给 Shader 端的 Uniform 结构体变量 uniform_var
    # 只要 Python 变量中含有对应的属性
    program["uniform_var"] = pyvar

    # 纹理 uniform 变量可用如下方法赋值
    # 对用户隐藏纹理单元概念
    program["sampler_var"] = sampler2D("path/to/image.png")

    # 创建顶点数组
    vertices = Vertices() # 像 list 一样操作 vertices，只不过元素只能为 Vertex 类型

    # 添加顶点
    vertices.append(Vertex(position=glm.vec2(-0.5,-0.5), color=glm.vec3(1,0,0)))
    vertices.append(Vertex(position=glm.vec2(0.5,-0.5), color=glm.vec3(0,1,0)))
    vertices.append(Vertex(position=glm.vec2(0,0.5), color=glm.vec3(0,0,1)))
    # 构建顶点 Vertex 时，属性名可为任意值
    # 只要在 vertex shader 中的 layout 指定了该属性名并且类型匹配

    # 创建索引数组
    indices = Indices() # 像 list 一样操作 indices，只不过元素只能为 glm.uvec3 类型
    indices.append(glm.uvec3(0, 1, 2))

    # 绘制三角形
    program.draw_triangles(vertices=vertices, indices=indices)

    # vertices 和 indices 可在任意时刻动态修改内部元素，以及动态增加删除元素
    # 所有修改将在下次绘制时同步到显存

你可以在任意需要使用 OpenGL 的地方使用 **Glass**，
但其初衷是为 **Glass Engine** 提供 OpenGL 的封装，因此不过多介绍 **Glass** 的用法，欢迎访问 **Glass Engine** 项目：

- `文档 <https://glass-engine-doc.readthedocs.io/zh/latest/>`_
- `Github 项目主页 <https://github.com/Time-Coder/Glass-Engine>`_
- `Gitee 项目主页 <https://gitee.com/time-coder/Glass-Engine>`_
- `PyPI 索引 <https://pypi.org/project/glass-engine/>`_
