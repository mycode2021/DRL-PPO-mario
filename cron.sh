#!/bin/bash

eval $(date +'%H %M'|awk '{printf "H=%s\nM=%s\n",$1,$2}')
[ "$(egrep '.*train.sh.*' /etc/crontab)" != "" ] && \
sed -i "s/.*train.sh.*/$[($M+30)%60] $[(($M+30)/60+$H)%24] \* \* \* root \/root\/DRL-PPO-mario\/train\.sh/g" /etc/crontab || \
echo "$[($M+30)%60] $[(($M+30)/60+$H)%24] * * * root /root/DRL-PPO-mario/train.sh" >> /etc/crontab
rm -rf log records tensorboard utils/__pycache__ nohup.out score
reboot
