import csv, statistics as S, os, json
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(f"{D}/results/runs.csv")))
def final_words(r):
    for l in open(f"{D}/{r['raw_jsonl']}"):
        d=json.loads(l) if l.strip() else {}
        if d.get("type")=="result": return len(str(d.get("result","")).split())
    return 0
arms=["none","short619","agents25","bloated"]; size={"none":0}
for a in arms[1:]: size[a]=os.path.getsize(f"{D}/scripts/claude_md/{a}.md")
out=[]
for a in arms:
    rs=[r for r in rows if r["cond"]==a]
    out.append(dict(variant=a, claude_md_bytes=size[a], n=len(rs), passed=sum(r["passed"]=="True" for r in rs),
        total_tokens_mean=round(S.mean(int(r["total_tokens"]) for r in rs)), first_prompt_mean=round(S.mean(int(r["first_call_input"])+int(r["first_call_cache_creation"])+int(r["first_call_cache_read"]) for r in rs)),
        output_mean=round(S.mean(int(r["output_tokens"]) for r in rs),1), final_reply_words_mean=round(S.mean(final_words(r) for r in rs),1),
        turns_mean=round(S.mean(int(r["num_turns"]) for r in rs),2), est_cost_mean=round(S.mean(float(r["est_cost_usd"]) for r in rs),4),
        wall_mean=round(S.mean(float(r["wall_s"]) for r in rs),1)))
base=out[0]
for o in out:
    o["output_vs_none_pct"]=round(100*(o["output_mean"]/base["output_mean"]-1),1); o["cost_vs_none_pct"]=round(100*(o["est_cost_mean"]/base["est_cost_mean"]-1),1)
w=csv.DictWriter(open(f"{D}/results/summary.csv","w"),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for o in out: print(o)
fig,ax=plt.subplots(1,3,figsize=(14,4.4)); names=[f"{o['variant']}\n({o['claude_md_bytes']} B)" for o in out]; col=["#999","#d17b4a","#5aa36b","#4a7bd1"]
for i,(k,t) in enumerate((("output_mean","output tokens/task"),("final_reply_words_mean","words in final reply"),("est_cost_mean","API-equiv. est. $ / task"))):
    v=[o[k] for o in out]; ax[i].bar(names,v,color=col); ax[i].set_title(t)
    for j,x in enumerate(v): ax[i].text(j,x,f"{x:.3f}" if k=="est_cost_mean" else f"{x:.0f}",ha="center",va="bottom",fontsize=8)
plt.suptitle("#004/#009 CLAUDE.md variants, 5 tasks each (all 20 passed)",fontsize=11); plt.tight_layout(); plt.savefig(f"{D}/results/chart.png",dpi=110)
