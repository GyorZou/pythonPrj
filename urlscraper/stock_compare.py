
#评分排序比较
def compare_rate(comp):
    return comp.rate

#价格排序比较
def compare_price(obj):
    return abs(float(obj.up.replace("%", "")))