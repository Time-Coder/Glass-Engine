# Assimpy -- 为 Glass Engine 提供 3D 模型加载功能

**Assimpy** 为 **Glass Engine** 的子项目，是 Assimp 项目的 Python 绑定，为 Glass Engine 提供 3D 模型加载功能。
仅提供 ``load(file_name:str, flags:int)->Model`` 函数用于加载模型。其优势在于：

* 使用 assimp 加载模型后，不做任何的中间类型拷贝，直接将原生内存 buffer 暴露给 python
* 支持内置纹理加载

你可以在任意需要加载 3D 模型的时候使用 **Assimpy**，并在其源码中找见加载上来的模型结构，
但不建议你这么做。因为其初衷是为 **Glass Engine** 提供 3D 模型的加载功能，
因此不过多介绍 **Assimpy** 的用法，欢迎访问 **Glass Engine** 项目：

* 文档：<https://glass-engine-doc.readthedocs.io/zh/latest/>
* Github 项目主页：<https://github.com/Time-Coder/Glass-Engine>
* Gitee 项目主页：<https://gitee.com/time-coder/Glass-Engine>
* PyPI 索引：<https://pypi.org/project/glass-engine/>

**Glass Engine** 中的模型加载功能用法请参考：

<https://glass-engine-doc.readthedocs.io/zh/latest/model/model.html>