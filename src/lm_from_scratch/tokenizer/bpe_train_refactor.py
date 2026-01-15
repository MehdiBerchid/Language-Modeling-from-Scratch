import regex as re
from typing import Iterator,Optional



PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+'"""


def raw_text_loader(raw_path:str,cha_numbre: Optional[int]) -> str:
    with open(file=raw_path,encoding= "UTF-8") as file:
        return file.read(cha_numbre)

def Split_Special_tokens(raw_text:str, special_tokens: list[str]) -> list[str]:
    if not special_tokens:
        return [raw_text]
    patt = "|".join(re.escape(tok) for tok in special_tokens)
    chucks = [chunk for chunk in re.split(patt, raw_text) if chunk != ""]
    return chucks

def Split_text_words(raw_text:str,pat = PAT)-> Iterator[str]:
    for m in re.finditer(pattern=pat,string=raw_text):
        yield m.group(0)

def Unique_Words_Count(chunks: Iterator[str]) -> dict[str:int]:
    Word_Counts = {}
    for word in chunks:
        Word_Counts[word] = Word_Counts.get(word,0) + 1
    return Word_Counts



def Optimized_Count_pairs(unique_pre_tokens: dict[str:int]):
    Tokens_Count = {}
    Pair_index = {}
    words = []
    for wid, t in (unique_pre_tokens.keys()):
        e = [bytes([x]) for x in t.encode('utf-8')]
        words.append(e)
        for i in range(len(e)-1):
            pair = (e[i], e[i+1])
            Pair_index.setdefault(pair, []).append((wid, i))
            Tokens_Count[pair] = Tokens_Count.get(pair, 0) + unique_pre_tokens[t]


    return Tokens_Count,Pair_index,words

    






            
         
















