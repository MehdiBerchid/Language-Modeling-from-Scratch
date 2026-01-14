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

def Split_text_words(raw_text:str,pat = PAT):
    for m in re.finditer(pattern=pat,string=raw_text):
        yield m.group(0)


def merge_tokens(toks:list[bytes],pair:tuple[bytes,bytes]):
    new_toks = []
    i=0
    while i< len(toks):
        if i + 1 < len(toks) and toks[i] == pair[0] and toks[i+1] == pair[1]:
            new_toks.append(toks[i]+toks[i+1])
            i = i+2
        else:
            new_toks.append(toks[i])
            i = i + 1
    return new_toks



def apply_merges(toks:list[bytes],merges:list[tuple[bytes,bytes]]):
    new_toks = toks
    for element in merges:
        new_toks = merge_tokens(new_toks,element)
    return new_toks





def count_pairs_with_merges(pre_tokens: Iterator[str], merges: list[tuple[bytes, bytes]]) -> dict[tuple[bytes, bytes], int]:
    Tokens_Count = {}
    for t in pre_tokens:
        e = [bytes([x]) for x in t.encode('utf-8')]
        e = apply_merges(e,merges)
        pairs = [(e[i],e[i+1]) for i in range(len(e)-1)]
        for element in pairs:
            Tokens_Count[element] = Tokens_Count.get(element,0) + 1
    return Tokens_Count
    



    
        
def Optimized_Count_pairs(pre_tokens: Iterator[str]):
    Tokens_Count = {}
    Pair_index = {}
    words = []
    for wid, t in enumerate(pre_tokens):
        e = [bytes([x]) for x in t.encode('utf-8')]
        words.append(e)
        for i in range(len(e)-1):
            pair = (e[i], e[i+1])
            Pair_index.setdefault(pair, []).append((wid, i))
            Tokens_Count[pair] = Tokens_Count.get(pair, 0) + 1


    return Tokens_Count,Pair_index,words

    






            
         
















