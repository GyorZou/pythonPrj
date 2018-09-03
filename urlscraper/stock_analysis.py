from  company import  Company
import  re
def analysis_company(comp):
    pass



def analysis_news(lis):
    # 消息数量
    #
    #
    #
    if not lis:
        return 0
    count = len(lis)
    result = 1
    must_words = ["修订稿", "上市", "借壳","业绩"]
    positive_words = ["收购", "提振", "盈利", "增"]
    negative_words = ["减持", "停牌", "负面", "下滑", "亏","跌"]

    total = positive_words + negative_words
    reg = ""
    c = len(total)
    index = 0
    for w in total:
        reg += w
        index += 1
        if index != c:
            reg += "|"
    reg = r"\w*(%s\w*)" % reg
    reg = re.compile(reg)

    reg2 = ""
    c = len(must_words)
    index = 0
    for w in must_words:
        reg2 += w
        index += 1
        if index != c:
            reg2 += "|"
    reg2 = r"\w*(%s\w*)" % reg2
    reg2 = re.compile(reg2)

    for new in lis:
        # 判断是否包含must字词，每个50分
        title = new.title
        if reg.match(title):
            result += 10
        title = new.title

        if reg2.match(title):
            result += 50

        # 判断是否包含关键字词，每个10分

    return result * count
