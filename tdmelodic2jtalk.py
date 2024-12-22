import re
from pathlib import Path

import jaconv
from tqdm import tqdm

line_list = Path("./skk-station-tdmelodic_ipa.csv").read_text(encoding="utf-8")
line_list = line_list.split("\n")

KOMOJI_PATTERN = re.compile("[ァィゥェォッャュョ]")
DOWN_PATTERN = re.compile(".+\].+\].+")
komoji_list = ["ァ","ィ","ゥ","ェ","ォ""ッ","ャ","ュ","ョ"]
kana_list = ["ア","イ","ウ","エ","オ","ツ","ヤ","ユ","ヨ"]
out_list = []

UP_DOWN_PATTERN = re.compile(".+\[.+\].+")
DOWN_UP_PATTERN = re.compile(".+\].+\[].+")

for line in line_list:

    line = line.split(",")
    if len(line) == 13:
        acc = line[12]

        for i in kana_list:
            acc = acc.replace(i, "")
        
        yomi = jaconv.hira2kata(line[11])
        yomi_copy = yomi

        for i in komoji_list:
            yomi_copy = yomi_copy.replace(i, "")
        
        mora = acc.replace("[", "")
        mora = mora.replace("]", "")
        mora = len(mora)
        
        #上昇して下降しない場合平板型に
        if "[" in acc and "]" not in acc:
            out = f"0/{mora}"

        #アクセント核がない場合    
        elif "[" not in acc and "]" not in acc:
            # 平板型に設定
            out = f"0/{mora}"

        #下降だけする場合
        elif "]" in acc and "[" not in acc:
            
            if DOWN_PATTERN.fullmatch(acc):

                down_acc_position2 = acc.replace("]", "|", 1).find("]") -2
                 
                mora02 = mora - down_acc_position2  
                mora01 = mora - mora02 

                if KOMOJI_PATTERN.match(yomi[down_acc_position2]): 
                    acc = down_acc_position2 -1
                else: 
                    acc = down_acc_position2

        
                out = f"0/{acc}"
        
        #そうでない場合は平型
        else:
                out = f"0/{mora}"

        kanji = line[0]

        if "-" in out:
            out = f"{0}/{mora}"

        out_line = line[:10] + [kanji, yomi, yomi, out, "*", line[12]] 
        print(out_line)

        out_list.append( ",".join(out_line) )
    
Path("./skk-station-tdmelodic_ipa-jtalk.csv").write_text("\n".join(out_list) , encoding="utf-8")  