English | [简体中文](./README.cn.md)

# Description

Play modified versions of mario games based on PPO algorithm. This project is modified from a Super
Mario Bros deep reinforcement learning project. The project can be used for testing if you are
interested. Good ideas are welcome.

# Environment

## 1. System library
You need to install freeglut or NVIDIA CUDA(optional), as follows:
- **Ubuntu**
```bash
apt install -y freeglut3 freeglut3-dev
```
- **CentOS**
```bash
dnf install -y freeglut freeglut-devel
```

## 2. Python and Modules
You need to install python 3.7 or 3.8, and some necessary modules, as follows:
```bash
pip install gym-retro torch numpy opencv-python pyglet==1.5.0 tensorboard
```

## 3. Game ROM
The project has provided several modified versions of mario ROMs, please unzip and move them to the site-packages/retro/data/stable directory under the library of the python.

# Toolkit

## 1. Train
**For example:**
```bash
python train.py --game HammarMarioBros-Nes --state Level1-1 --processes 6
```

## 2. Test
**For example:**
```bash
python test.py --game HammarMarioBros-Nes --state Level1-1 --from_model HammarMarioBros/Level1-1.pass
```

## 3. Evaluate
**For example:**
```bash
python evaluate.py --game HammarMarioBros-Nes --state Level1-1 --from_dir Directory (like trained_models/2020-...)
```

###### :point_right: **Tips: The --from_model or --from_dir default reference location can be changed by --loading_path.**

# Reference

:book: https://retro.readthedocs.io/en/latest.
