import re, sys


with open(sys.argv[1]) as f:
    readlines = f.read()
    print("当前最多分数: %.2f分"%max([-10]+list(map(float, re.findall("Score: (.*?),", readlines)))))
    print("当前最多移动: %d步"%max([0]+list(map(int, re.findall("Step: (.*?),", readlines)))))
    print("当前最久耗时: %d分%d秒"%divmod(max([0]+list(map(lambda x:int(x[0])*60+int(x[1]), re.findall("Time: (.*?)m(.*?)s,", readlines)))), 60))
    print("当前通关次数: %d次"%sum([0]+list(map(bool, re.findall("Evaluation: (success?).", readlines)))))
