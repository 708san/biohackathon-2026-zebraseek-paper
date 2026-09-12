"""Draw a conceptual study figure, without changing any empirical result figure.

No patient example, new algorithm or simulated result is encoded in this figure.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

OUT = Path(__file__).resolve().parents[1] / 'paper' / 'figures'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'svg.fonttype': 'none', 'savefig.facecolor': 'white'})
NAVY, TEAL, PURPLE = '#263451', '#008D9D', '#7851A9'
GREY, LINE, ORANGE = '#566478', '#AAB4C0', '#BE6632'
fig, ax = plt.subplots(figsize=(10.2, 7.2))
ax.set(xlim=(0, 10.2), ylim=(0, 7.2)); ax.axis('off')

def text(x, y, s, size=12, color=NAVY, weight='normal', ha='left', va='center'):
    return ax.text(x, y, s, fontsize=size, color=color, weight=weight,
                   ha=ha, va=va, linespacing=1.3)

def box(x, y, w, h, edge=LINE, face='white', dash='solid'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.025,rounding_size=0.08',
                 linewidth=1.3, edgecolor=edge, facecolor=face, linestyle=dash))

def arrow(start, end, color=GREY, dashed=False):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=13,
                 lw=1.4, color=color, linestyle='--' if dashed else '-'))

text(.15, 6.94, 'Complementary evidence must survive shortlist formation', 16, weight='bold')
text(.15, 6.54, 'Study concept: distinguish retrieval opportunities from integration losses', 11.5, GREY)
# The three columns describe tasks, not independent modalities or a new algorithm.
for x, n, label in [(.2, '1', 'Evidence inputs'), (3.64, '2', 'Candidate pool'), (7.17, '3', 'Final differential')]:
    ax.add_patch(plt.Circle((x+.12, 5.95), .17, color=NAVY))
    text(x+.12, 5.95, n, 10, 'white', 'bold', 'center')
    text(x+.42, 5.95, label, 12.4, weight='bold')

for y, label, desc, col in [(4.98, 'Clinical findings', 'HPO and context', '#0072B2'),
                             (3.94, 'Facial phenotype', 'Facial similarity', ORANGE),
                             (2.90, 'Disease knowledge', 'Reference resources', '#997044')]:
    box(.2, y-.37, 2.75, .84, col, '#F8FAFC')
    ax.plot([.36,.36],[y-.19,y+.28],color=col,lw=3,solid_capstyle='round')
    text(.53, y+.12, label, 12.0, weight='bold')
    text(.53, y-.17, desc, 10.7, GREY)
arrow((3.02,4.08),(3.52,4.08),TEAL)

box(3.63,2.55,2.78,2.95,TEAL,'#F2F9FA')
text(5.02,5.14,'Shared and distinct\nretrieval routes',11.3,TEAL,'bold','center')
box(3.88,4.15,2.28,.58,TEAL)
text(5.02,4.44,'Shared candidates',12,ha='center')
box(3.88,3.34,2.28,.58,TEAL)
text(5.02,3.63,'Source-specific\ncandidates',11.3,ha='center')
text(5.02,2.87,'Source ranks and scores',10.5,GREY,ha='center')
arrow((6.47,4.08),(7.03,4.08),PURPLE)
text(6.76,4.66,'Rank /\ncheck',10.3,PURPLE,ha='center')
box(7.15,2.55,2.83,2.95,PURPLE,'#F7F4FB')
text(8.56,5.14,'Five ranked diseases',12,PURPLE,'bold','center')
for y,w in [(4.51,1.82),(4.21,1.6),(3.91,1.43),(3.61,1.23),(3.31,1.05)]:
    ax.plot([7.57,7.57+w],[y,y],lw=6,color='#B6A0D1',solid_capstyle='round')
text(8.56,2.87,'Explanatory text\nfor clinical review',10.5,GREY,ha='center')
# Two evaluative questions, with different failure locations.
for x, heading, desc, col in [(.2,'QUESTION 1  /  AVAILABILITY','Did any component retrieve\nthe recorded diagnosis?',TEAL),
                              (5.37,'QUESTION 2  /  RETENTION','If retrieved, did it remain\nin the final top five?',PURPLE)]:
    box(x,.64,4.6,1.32,col,'white')
    text(x+.22,1.66,heading,11.7,col,'bold')
    text(x+.22,1.15,desc,12.5)
arrow((4.02,2.49),(3.79,2.03),TEAL,True)
arrow((7.46,2.49),(7.15,2.03),PURPLE,True)
text(.2,.23,'A useful candidate can lack cross-tool agreement; agreement is not independent evidence.',11.4,GREY)
fig.savefig(OUT/'concept_candidate_retention.png',dpi=320,bbox_inches='tight',pad_inches=.13)
fig.savefig(OUT/'concept_candidate_retention.svg',bbox_inches='tight',pad_inches=.13,
            metadata={'Date':None,'Creator':'ZebraSeek conceptual figure script'})
plt.close(fig)
