def componentImport(name):
    res = ""
    with open("./components/zw_"+name+".html","r") as f:
        res = f.read()
    return res