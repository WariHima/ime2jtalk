import re
from pathlib import Path

import jaconv
from tqdm import tqdm

line_list = Path("./dmime-tdmelodic_ipa.csv").read_text(encoding="utf-8")
line_list = line_list.split("\n")

KOMOJI_PATTERN = re.compile("[ァィゥェォッャュョ]")
DOWN_PATTERN = re.compile(".+\[.+\].+")
komoji_list = ["ァ","ィ","ゥ","ェ","ォ""ッ","ャ","ュ","ョ"]
kana_list = ["ア","イ","ウ","エ","オ","ツ","ヤ","ユ","ヨ"]
out_list = []

for line in tqdm(line_list):

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

        #最初アクセント核の時頭高型に
        if len(acc) != 1 and acc[1] == "]":
            out = f"1/{mora}"

        #下降する場合
        else:
            
            if DOWN_PATTERN.fullmatch(acc):

                down_acc_position2 = acc.find("]") -1

                if down_acc_position2 < len(yomi) and KOMOJI_PATTERN.match(yomi[down_acc_position2]): 
                    acc2 = down_acc_position2 -1
                else: 
                    acc2 = down_acc_position2

                out = f"{acc2}/{mora}"
        
            else:
                out = f"0/{mora}"

        kanji = line[0]

        out_line = line[:10] + [kanji, yomi, yomi, out, "*", line[12]] 
        #print(out_line)

        out_list.append( ",".join(out_line) )
    
Path("./dmime.csv").write_text("\n".join(out_list) , encoding="utf-8")  