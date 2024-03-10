from flask import Flask
from flask import request
from flask import Response, json
import os


# 解决跨域问题
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
# route()装饰器来告诉Flask触发函数的URL

rules = {}  # 以字典形式存储规则

"""
读取规则库文件中规则，并存放在rules字典中
    - 字典的键：前提
    - 字典的值：结论 
"""


def readRules(filePath):
    global rules
    for line in open(filePath, mode='r', encoding='utf-8'):
        line = line.replace('if', '').strip()
        temp = line.split(' then ')
        premise = temp[0]
        conclusion = temp[1]
        rules[premise] = conclusion


"""
2. 推理机用这些事实(即：facts变量)，依次与知识库中的规则的前提匹配
    - 注意：匹配成功的规则可能不止一条，进行冲突消解（本代码没有这个功能）
    - 代码很简单，没有对综合数据库进行设置
3. 若某规则的前提全被事实满足，则规则可以得到运用
4. 规则的结论部分作为新的事实存储
5. 用更新过的事实再与其它规则的前提匹配，直到不再有可匹配的规则为止
"""


def matchRules(facts):
    # 循环匹配
    isEnd = False
    result = []
    temp_rules = rules.copy()

    def loop():
        global rules
        print("match", rules)
        nonlocal facts, isEnd, result, temp_rules
        rules_copy = temp_rules.copy()
        i = 0
        for premise in temp_rules:
            flag = True
            # print(premise+ ':' + temp_rules[premise])
            pre = premise.split(' and ')
            for p in pre:
                if p in facts:
                    pass
                else:
                    flag = False
            if (flag):
                print('该动物：' + premise + ' -> ' + temp_rules[premise])
                result.append(premise + ' -> ' + temp_rules[premise])
                for p in pre:
                    facts = facts.replace(p, ' ')
                facts = facts + temp_rules[premise]
                rules_copy.pop(premise)
            else:
                i += 1
        if i == len(rules_copy):
            isEnd = True
        temp_rules = rules_copy

    # 是否推导出最终结论
    while (not isEnd):
        loop()
    isEnd = False
    return result

# 返回所有的规则(前提和结论)
@app.route('/getrules', methods=['POST', 'GET'])
def getrules():
    global rules
    strRules = []
    strResult = []
    for premise in rules:
        strRules.append(premise.split(' and '))
        strResult.append(rules[premise])
    # 以json形式返回数据
    return Response(json.dumps({'rules': strRules, 'result': strResult}), content_type='application/json')


# 增加规则(前提,结论和结论类型)
@app.route('/add', methods=['POST', 'GET'])
def add():
    # 得到传递过来的参数
    data1 = request.get_json(silent=True)
    newRules = data1['newrules']
    newResult = data1['newresult']


    global rules

    premise = newRules.replace(",", " and ").replace("，", " and ")
    rules[premise] = newResult
    print("add", newRules, newResult)
    print("add", premise, newResult)

    # 添加成功返回200
    return Response(json.dumps({'code': 200}), content_type='application/json')


# 分析得到结论
@app.route('/test', methods=['POST', 'GET'])
def test():
    # 动物产生式识别系统
    str1 = request.get_json(silent=True)


    facts = " and ".join(str1['msg'])
    print("test", str1, facts)
    r = matchRules(facts)
    return Response(json.dumps({'code': 200, 'result': r}), content_type='application/json')

# 通过文件增加规则(前提,结论和结论类型)
@app.route('/addfile', methods=['POST', 'GET'])
def addfile():
    # 保存文件
    f = request.files['file']
    if f is None:
        return "";
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, 'uploads', f.filename)
    f.save(upload_path)
    print("addfile", upload_path)
    # 读取文件
    readRules(upload_path)

    # 删除文件
    os.remove(upload_path)
    return Response(json.dumps({'code': 200}), content_type='application/json')

# 删除规则
@app.route('/delrow', methods=['POST', 'GET'])
def delrow():
    global rules
    data1 = request.get_json(silent=True)
    del_rules = data1['rules']

    print("delrow", del_rules)

    key = " and ".join(del_rules['name'])
    result = rules.pop(key)

    if result is None:
        return Response(json.dumps({'code': 500}), content_type='application/json')
    else:
        return Response(json.dumps({'code': 200}), content_type='application/json')

if __name__ == '__main__':
    app.run()
