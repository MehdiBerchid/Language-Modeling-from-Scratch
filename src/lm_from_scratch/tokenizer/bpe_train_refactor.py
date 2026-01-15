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
    freqs = []
    for wid, t in enumerate(unique_pre_tokens.keys()):
        e = [bytes([x]) for x in t.encode('utf-8')]
        words.append(e)
        freqs.append(unique_pre_tokens[t])
        for i in range(len(e)-1):
            pair = (e[i], e[i+1])
            Pair_index.setdefault(pair, []).append((wid, i))
            Tokens_Count[pair] = Tokens_Count.get(pair, 0) + unique_pre_tokens[t]


    return Tokens_Count,Pair_index,words,freqs

    

def Up_Dating_Counts(Tokens_Counts,Pair_index,word,pair,freqs):
    merge = pair[0] + pair[1]
    occ_by_word = Pair_index[pair] 
    for (wid,id) in list(occ_by_word):
        element = word[wid]
        if (element[id],element[id+1]) == pair:
            if id> 0 and id< len(element)-2 :
                
                    right_merge = element[id-1]
                    left_merge = element[id+2]
                    Tokens_Counts[(right_merge,merge)] = Tokens_Counts.get((right_merge,merge),0) + freqs[wid]
                    Pair_index.setdefault((right_merge,merge),[]).append((wid,id-1))


                    Tokens_Counts[(merge,left_merge)] = Tokens_Counts.get((merge,left_merge),0) + freqs[wid]
                    Pair_index.setdefault((merge,left_merge),[]).append((wid,id))
                    
                    



                    #### NOW WE GONNA DECREASE RIGHT_MERGE,element(i) element, element,left_merge

                    rightpairs = (right_merge,element[id])
                    leftpairs = (element[id+1],left_merge)



                    Tokens_Counts[rightpairs] = Tokens_Counts.get(rightpairs,0) - freqs[wid]

                    Pair_index[rightpairs].remove((wid,id-1))
                
                    Tokens_Counts[leftpairs] = Tokens_Counts.get(leftpairs,0) - freqs[wid]

                    Pair_index[leftpairs].remove((wid,id+1))

                
            elif id == 0 :
                    left_merge = element[id+2]
                    leftpairs = (element[id+1],left_merge)
                    Tokens_Counts[(merge,left_merge)] = Tokens_Counts.get((merge,left_merge),0) + freqs[wid]
                    Pair_index.setdefault((merge,left_merge),[]).append((wid,id))
                    Tokens_Counts[leftpairs] = Tokens_Counts.get(leftpairs,0) - freqs[wid]
                    Pair_index[leftpairs].remove((wid,id+1))




            elif id == len(element)-2:
                    right_merge = element[id - 1]
                    rightpairs = (right_merge,element[id])
                    Tokens_Counts[(right_merge,merge)] = Tokens_Counts.get((right_merge,merge),0) + freqs[wid]
                    Pair_index.setdefault((right_merge,merge),[]).append((wid,id-1))
                    Tokens_Counts[rightpairs] = Tokens_Counts.get(rightpairs,0) - freqs[wid]
                    Pair_index[rightpairs].remove((wid,id-1))
    Tokens_Counts.pop(pair)
    Pair_index[pair].clear()





        








                
            

















        
            