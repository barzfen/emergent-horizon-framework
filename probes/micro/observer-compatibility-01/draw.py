from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
from math import sin,cos,pi
import json
ROOT=Path(__file__).parent
r=json.loads((ROOT/'results.json').read_text())['first_probability_counterexamples'][0]
im=Image.new('RGB',(1500,1060),'#f3f5fa');d=ImageDraw.Draw(im)
def font(n,bold=False):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf',n)
def txt(x,y,t,n=26,fill='#24324b',bold=False,anchor=None):d.text((x,y),t,font=font(n,bold),fill=fill,anchor=anchor)
txt(65,40,'SAME COUNTS. DIFFERENT NEXT-STEP ODDS.',38,bold=True)
txt(65,100,'MICRO • no isolated bits • uniform choice among allowed growth events',23)
d.rounded_rectangle((65,150,1435,230),18,fill='#e1e9f8')
txt(750,190,'Both rings: 9 bits  |  5 zeros  |  4 ones',29,bold=True,anchor='mm')
for x,s,label,b,p,total in [(395,r['state_a'],'RING A',2,5,11),(1105,r['state_b'],'RING B',4,6,13)]:
    d.rounded_rectangle((x-330,260,x+330,805),25,fill='white',outline='#d7dfea',width=2)
    txt(x,293,label,25,bold=True,anchor='mm')
    pts=[(x+140*sin(2*pi*i/9),475-140*cos(2*pi*i/9)) for i in range(9)]
    for i,a in enumerate(pts):d.line([a,pts[(i+1)%9]],fill='#aebcd0',width=4)
    for (px,py),bit in zip(pts,s):
        d.ellipse((px-27,py-27,px+27,py+27),fill=('#2866ac' if bit=='0' else '#ffc260'))
        txt(px,py,bit,25,fill=('white' if bit=='0' else '#4a310b'),bold=True,anchor='mm')
    txt(x,475,f'{b} blocks',25,bold=True,anchor='mm')
    txt(x,665,f'{total} allowed growth events',24,anchor='mm')
    txt(x,716,f'P(next bit is 1) = {p}/{total}',28,bold=True,anchor='mm')
    txt(x,763,f'{100*p/total:.2f}%',28,fill='#2866ac',bold=True,anchor='mm')
d.rounded_rectangle((65,835,1435,990),20,fill='#24324b')
txt(750,875,'Counting colours alone misses the block structure.',29,fill='white',bold=True,anchor='mm')
txt(750,923,'Keeping the block count gives a consistent next-step rule in this model.',24,fill='#dbe6f7',anchor='mm')
txt(65,1018,'Exact difference: 1/143. Both rings can add either bit; the probabilities differ.',21)
im.save(ROOT/'observer_comparison.png')
