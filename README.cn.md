[English](./README.md) | 简体中文 

# 项目说明

基于PPO算法的超级马里奥改版版本通用游戏智能体。这个项目是从一个深度强化学习项目修改而来的，游戏端改为openAI的retro，
并对结构做了一定的改动，这个项目被创建用于验证游戏经验在不同马里奥改版间的泛化能力，如果你对此项目感兴趣可以尝试测试，
欢迎推荐好的建议和想法。

# 测试环境

## 1. 系统依赖库
如果你想可视化需要安装freeglut库用于渲染游戏画面，还有英伟达的CUDA(可选)，如下：
- **Ubuntu**
```bash
apt install -y freeglut3 freeglut3-dev
```
- **CentOS**
```bash
dnf install -y freeglut freeglut-devel
```

## 2. Python环境
你需要安装python3.7或者3.8和一些必要的模块，如下:
```bash
pip install gym-retro torch numpy opencv-python pyglet==1.5.0 tensorboard
```

## 3. 游戏ROM
项目已提供几个超级马里奥改版版本的ROM，请解压缩并移动到对应版本python的library库下site-packages/retro/data/stable目录中。

# 工具说明

## 1. 训练工具
**例如:**
```bash
python train.py --game HammarMarioBros-Nes --state Level1-1 --processes 6
```

## 2. 测试工具
**例如:**
```bash
python test.py --game HammarMarioBros-Nes --state Level1-1 --from_model HammarMarioBros/Level1-1.pass
```

## 3. 评估工具
**例如:**
```bash
python evaluate.py --game HammarMarioBros-Nes --state Level1-1 --from_dir 文件夹（训练产生的trained_models/2020-...）
```

###### :point_right: **提示: 参数--from_model和--from_dir的默认引用位置可以使用--loading_path参数临时指定。**

# 参考说明

:book: https://retro.readthedocs.io/en/latest.
