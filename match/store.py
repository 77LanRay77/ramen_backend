import os, json



def match_store(stores: list[str]) -> list[str]:

    BASE = os.path.dirname(__file__)  # 程式所在的資料夾
    path = os.path.join(BASE, 'data.r1.1.json')

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 在這裡可以使用 data 進行比對
    #print(type(data))

    tmp = []
    for info in range(5):

       tmp.append(data.get(stores[info]))
       #print(type(data.get(stores[info])))
    feedback = json.dumps(tmp, ensure_ascii=False, indent=4)
    return feedback


if __name__ == "__main__":

    a=["麵屋吉光","Yén itte 言って食処","浮生閣","拉麵 豚鷄魚","麵宮浦島"]
    print(match_store(a))