print("请输入URL:")
url = input()
print("请输入标题:")
title = input()

print("请输入标签,输入$结束:")
tags = []
while True:
    tag = input()
    if tag != "$":
        tags.append(tag)
    else:
        break

print(tags)
