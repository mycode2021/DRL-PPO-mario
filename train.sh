#!/bin/bash

process=$(ps -ef|grep train.py|grep -v grep)

if [ "$process" != "" ]; then
echo "The train.py process is already running!"
exit 1
fi

export DISPLAY=:1

mkdir -p /root/DRL-PPO-mario/log

> /root/DRL-PPO-mario/log/evaluate.log

cd /root/DRL-PPO-mario

nohup python train.py --game SuperMarioBros-Nes --state Level1-1 --processes 6 &

if [ -e "log/evaluate.log" ]; then
gnome-terminal --geometry=100x10+0+400 -- bash -c "cd /root/DRL-PPO-mario; tail -f log/evaluate.log"
gnome-terminal --geometry=58x8+500+45 -- bash -c "cd /root/DRL-PPO-mario; watch -n 1 -d python score.py log/evaluate.log"
fi
