"""Reproduce aggregate study figures; this does not run diagnostic models.

Input counts are transcribed or reconstructed as recorded in aggregate_results.json.
Run from any directory: python scripts/make_figures.py
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'paper/data/aggregate_results.json').read_text())
OUT = ROOT / 'paper/figures'
OUT.mkdir(exist_ok=True)
N = DATA['n_cases']
TOOLS = DATA['component_order']
COLORS = ['#0072B2', '#997044', '#009E73', '#D55E00', '#8055B4']
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11,
                     'axes.spines.top':False, 'axes.spines.right':False,
                     'svg.fonttype':'none', 'savefig.facecolor':'white'})

# Check the scientific aggregates before rendering.
assert sum(p['count'] for p in DATA['success_overlap']) == 59
assert sum(p['count'] for p in DATA['failure_overlap']) == 15
for tool, record in DATA['recall'].items():
    counts = record['reconstructed_counts']
    assert counts == sorted(counts)
    assert [round(100*c/N,1) for c in counts] == record['percent']
for tool in TOOLS:
    count = sum(p['count'] for p in DATA['success_overlap'] + DATA['failure_overlap']
                if tool in p['components'])
    assert count == DATA['recall'][tool]['reconstructed_counts'][-1], (tool, count)
assert sum(p['count'] for p in DATA['success_overlap'] + DATA['failure_overlap'] if p['components']) == 66

def save(fig, stem):
    fig.savefig(OUT / f'{stem}.png', dpi=320, bbox_inches='tight', pad_inches=.12)
    fig.savefig(OUT / f'{stem}.svg', bbox_inches='tight', pad_inches=.12,
                metadata={'Date':None, 'Creator':'ZebraSeek manuscript figure script'})
    plt.close(fig)

def box(ax,x,y,w,h,label,color='#40566D',fill='#F5F7FA',fontsize=11):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.025',
                              edgecolor=color,facecolor=fill,linewidth=1.4))
    ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=fontsize,color='#192B3D',linespacing=1.35)

def arrow(ax,start,end,color='#607286'):
    ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=13,
                                linewidth=1.25,color=color))

# Figure 1. A diagram based on reported data flow, with no patient images.
fig,ax=plt.subplots(figsize=(10,5.6))
ax.set(xlim=(0,10),ylim=(0,5.6)); ax.axis('off')
for x,label in [(1.0,'Inputs'),(3.9,'Candidate generation'),(7.9,'Integration and output')]:
    ax.text(x,5.35,label,ha='center',weight='bold',fontsize=13)
ys=[4.05,2.95,1.85,.75]
inputs=['HPO findings','HPO findings','HPO findings\nand recorded sex','Facial image']
labels=['PubCaseFinder','SemanticSearch\nMondo descriptions','Direct LLM\nGPT-5.2','GestaltMatcher']
for i,(y,inp,lab) in enumerate(zip(ys,inputs,labels)):
    box(ax,.1,y,1.8,.75,inp,fontsize=11)
    box(ax,2.65,y,2.6,.75,lab,COLORS[i],fontsize=11)
    arrow(ax,(1.93,y+.375),(2.61,y+.375),COLORS[i])
    arrow(ax,(5.29,y+.375),(5.95,y+.375),COLORS[i])
    ax.text(5.6,y+.68,'Top 5',ha='center',fontsize=9)
ax.plot([6,6],[1.125,4.425],color='#607286',lw=1.3)
box(ax,6.55,3.9,3.25,.85,'Candidate ranking\nLLM (GPT-5.2)',COLORS[4])
arrow(ax,(6,4.325),(6.51,4.325))
box(ax,6.55,2.4,3.25,.95,'Candidate verification\nLLM + external literature',COLORS[4])
arrow(ax,(8.175,3.86),(8.175,3.39))
ax.text(8.175,2.13,'Including PubMed',ha='center',fontsize=10,color='#526372')
box(ax,6.55,.65,3.25,1.0,'Final top-five diseases\nand explanatory text',COLORS[4],fill='#F0EAF6')
arrow(ax,(8.175,2.0),(8.175,1.69))
ax.text(6.12,.35,'Up to 20 entries before overlap is resolved',ha='right',fontsize=10,color='#526372')
save(fig,'figure1_workflow')

# Figure 2. Every value retained, a clear legend, and an explicit denominator.
fig,ax=plt.subplots(figsize=(8.8,5.0))
x=np.arange(5); width=.155
for i,(tool,record) in enumerate(DATA['recall'].items()):
    positions=x+(i-2)*width
    bars=ax.bar(positions,record['percent'],width,color=COLORS[i],label=tool)
    ax.bar_label(bars,labels=[f'{p:.1f}' for p in record['percent']],padding=3,fontsize=8.8,rotation=90)
ax.set_xticks(x,[f'Top {k}' for k in range(1,6)])
ax.set_ylabel('Cases with the recorded diagnosis (%)')
ax.set_ylim(0,100); ax.set_yticks(range(0,101,20))
ax.set_axisbelow(True); ax.grid(axis='y',alpha=.2)
ax.legend(ncol=3,loc='upper center',bbox_to_anchor=(.5,1.24),frameon=False,fontsize=10)
ax.text(1,1.03,'74 cases / 19 diseases',ha='right',transform=ax.transAxes,fontsize=10)
fig.tight_layout(); save(fig,'figure2_recall')

# Figure 3. Exclusive intersections with conditional component totals.
patterns=DATA['success_overlap']
fig=plt.figure(figsize=(8.8,4.9))
gs=fig.add_gridspec(2,1,height_ratios=[2.0,1.35],hspace=.05,left=.26,right=.98,top=.90,bottom=.1)
ax=fig.add_subplot(gs[0]); mat=fig.add_subplot(gs[1],sharex=ax)
x=np.arange(len(patterns)); counts=[p['count'] for p in patterns]
ax.bar(x,counts,color='#25394C',width=.62)
for xx,c in zip(x,counts): ax.text(xx,c+.23,str(c),ha='center',fontsize=12)
ax.set_ylim(0,15); ax.set_yticks([0,5,10,15]); ax.set_ylabel('Cases',labelpad=10)
ax.tick_params(axis='x',bottom=False,labelbottom=False)
ax.spines['bottom'].set_visible(False)
mat.set_xlim(-.6,len(patterns)-.4); mat.set_ylim(3.5,-.5)
labels=[]
for row,tool in enumerate(TOOLS):
    count=sum(p['count'] for p in patterns if tool in p['components'])
    labels.append(f'{tool} ({count})')
    mat.axhspan(row-.45,row+.45,color='#F3F5F7' if row%2==0 else 'white',zorder=0)
for col,p in enumerate(patterns):
    rows=[TOOLS.index(t) for t in p['components']]
    if len(rows)>1: mat.plot([col,col],[min(rows),max(rows)],color='#25394C',lw=1.4,zorder=2)
    for row in range(4):
        mat.scatter(col,row,s=65,color=COLORS[row] if row in rows else '#D7DDE2',zorder=3)
mat.set_yticks(range(4),labels); mat.set_xticks([])
mat.tick_params(axis='y',length=0,pad=12)
for spine in mat.spines.values(): spine.set_visible(False)
fig.text(.52,.98,'Correct-candidate overlap in 59 ZebraSeek successes',ha='center',va='top',fontsize=13,weight='bold')
fig.text(.62,.025,'Filled circles identify an exclusive tool combination',ha='center',fontsize=10,color='#526372')
save(fig,'figure3_overlap')

# Figure 4. Failure counts; no case-level traces are inferred.
fig,ax=plt.subplots(figsize=(7.4,4.5))
labels=['No component','PubCaseFinder\nonly','GestaltMatcher\nonly']
counts=[p['count'] for p in DATA['failure_overlap']]
bars=ax.bar(np.arange(3),counts,width=.55,color=['#6A7885',COLORS[0],COLORS[3]])
ax.bar_label(bars,padding=5,fontsize=15,weight='bold')
ax.set_xticks(range(3),labels); ax.set_ylim(0,10); ax.set_yticks(range(0,11,2))
ax.set_ylabel('Cases'); ax.set_xlabel('Component top-five lists containing the recorded diagnosis',labelpad=12)
ax.set_axisbelow(True); ax.grid(axis='y',alpha=.2)
ax.text(.5,1.1,'Correct-candidate availability in 15 ZebraSeek failures',ha='center',transform=ax.transAxes,fontsize=12,weight='bold')
fig.tight_layout(); save(fig,'figure4_failures')
print('Aggregate consistency checks passed; wrote four PNG/SVG figure pairs.')
