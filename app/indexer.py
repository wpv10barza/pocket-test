from __future__ import annotations
import json, re, subprocess, sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GENERATOR=ROOT/'pack/02_dataset/generate_semantic_dataset.py'
DATASET=ROOT/'pack/outputs/pocket-ai/data/semantic_sheet_matching/dataset_full.json'

def _tokens(text:str)->set[str]:
    return {t for t in re.findall(r"[a-záéíóúñ0-9]+",text.lower()) if len(t)>2}

def ensure_dataset()->Path:
    if not DATASET.exists():
        subprocess.run([sys.executable,str(GENERATOR)],cwd=ROOT,check=True)
    return DATASET

@dataclass
class SemanticIndex:
    records:list[dict]
    inverted:dict[str,set[int]]
    @classmethod
    def load(cls)->"SemanticIndex":
        path=ensure_dataset()
        records=json.loads(path.read_text(encoding='utf-8'))
        inv=defaultdict(set)
        for i,r in enumerate(records):
            hay=' '.join([r.get('query',''),r.get('similarity_matching',{}).get('matched_historical_feature',''),r.get('target_analysis',{}).get('predicted_column_name',''),r.get('business_rules_payload',{}).get('prt_code','')])
            for tok in _tokens(hay): inv[tok].add(i)
        return cls(records=records,inverted=dict(inv))
    def search(self,query:str,top_k:int=5)->list[dict]:
        q=_tokens(query)
        candidates=set()
        for t in q: candidates |= self.inverted.get(t,set())
        if not candidates: candidates=set(range(len(self.records)))
        scored=[]
        for i in candidates:
            r=self.records[i]
            hay=_tokens(' '.join([r.get('query',''),r.get('similarity_matching',{}).get('matched_historical_feature',''),r.get('business_rules_payload',{}).get('prt_code','')]))
            score=len(q & hay)/max(1,len(q | hay))
            if score>0: scored.append((score,i,r))
        scored.sort(key=lambda x:(-x[0],x[1]))
        return [{"score":round(s,4),"prt_code":r['business_rules_payload']['prt_code'],"column":r['target_analysis']['predicted_column_letter'],"column_name":r['target_analysis']['predicted_column_name'],"query":r['query']} for s,_,r in scored[:top_k]]
