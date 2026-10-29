"""Deterministic automotive original bank. No third-party question text.
Concept manuscript: concepts.tsv. Numeric variants: 15 families × 60.
Use Decimal half-up; independent JS tests invert equations and parse all options.
"""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import json, csv, hashlib
ROOT=Path(__file__).resolve().parents[1]
D=lambda x:Decimal(str(x))
def rounded(x):return float(D(x).quantize(D('0.01'),rounding=ROUND_HALF_UP))
def fmt(x):return f'{x:g}'
bank=[]
url='https://github.com/YunSangYeong/Craftsman-Motor-Vehicle-Maintenance-CBT/blob/main/docs/question-review.md'
def add(id,topic,text,choices,explanation,**kw):
 shift=len(bank)%4
 choices=choices[shift:]+choices[:shift]
 q=dict(id=id,subject='자동차정비',topic=topic,question=text,choices=choices,answer=(4-shift)%4+1,explanation=explanation,difficulty='하',year=None,session=None,type='original',sourceUrl=url,verificationStatus='reviewed',reviewNote='AI 일반 지식 기반 자체 작성. 정답·오답·해설 내부 검토. 공식 출제기준 대조 및 외부 전문가 검수 미완료.',version='main',rights='프로젝트 자체 제작 · CC BY 4.0; 제3자 기출을 복제하지 않음',**kw)
 bank.append(q)
for i,line in enumerate((ROOT/'scripts/concepts.tsv').read_text().splitlines(),1):
 topic,text,correct,a,b,c,explanation=line.split('|')
 add(f'CAR-C-{i:03}',topic,text,[correct,a,b,c],explanation)
assert len(bank)==100
for kind in range(15):
 for i in range(60):
  # No random generator: fixed inputs, stable family/ID and choice rotation.
  a=D(20+i); b=D(2+i%7)
  if kind==0:
   a=D(60+i);b=D(50+i%10);v=[float(a),float(b),4];r=D('3.141592653589793')/4*a*a*b*4/1000;u='cm³';topic='엔진 · 배기량';text=f'보어 {a} mm, 행정 {b} mm인 4기통 엔진의 총 배기량은? π=3.141592653589793, 소수 둘째 자리까지 반올림한다.';eq=f'V=π/4×보어²×행정×기통수÷1000={r} cm³. mm³에서 cm³로 변환하므로 1000으로 나눈다.'
  elif kind==1:
   a=D(300+i*10);b=D(40+i%9);v=[float(a),float(b)];r=(a+b)/b;u='배';topic='엔진 · 압축비';text=f'한 실린더 행정체적 {a} cm³, 연소실 체적 {b} cm³일 때 기하학적 압축비는? 소수 둘째 자리까지 반올림한다.';eq=f'압축비=(행정체적+연소실 체적)/연소실 체적=({a}+{b})/{b}={r}. 압축 압력과 구별한다.'
  elif kind==2:
   a=D(800+i*40);v=[float(a)];r=a/2;u='rpm';topic='엔진 · 캠축';text=f'4행정 엔진 크랭크축이 {a} rpm이면 캠축 회전속도는?';eq=f'한 사이클은 크랭크축 2회전, 캠축 1회전이다. 캠축 속도={a}/2={r} rpm.'
  elif kind==3:
   a=D(10+i);b=D(20+i%8);v=[float(a),float(b)];r=a*b/100;u='N·m';topic='안전 · 체결 토크';text=f'볼트 축에 수직인 힘 {a} N을 축에서 {b} cm 떨어진 지점에 가했다. 토크는? 소수 둘째 자리까지 반올림한다.';eq=f'토크=힘×수직 거리={a}×({b}/100)={r} N·m. cm를 m로 변환한다. 실제 지정 체결 토크를 뜻하지 않는다.'
  elif kind==4:
   a=D(18+i);b=D(36+i%11);v=[float(a),float(b)];r=b/a;u='배';topic='섀시 · 기어비';text=f'구동기어 {a}개 이, 종동기어 {b}개 이인 한 쌍 기어의 감속비(입력속도/출력속도)는? 소수 둘째 자리까지 반올림한다.';eq=f'감속비=종동기어 잇수/구동기어 잇수={b}/{a}={r}. 값이 1보다 작으면 증속이다.'
  elif kind==5:
   a=D(1000+i*30);b=D(2+i%6);v=[float(a),float(b)];r=a/b;u='rpm';topic='섀시 · 출력속도';text=f'입력 {a} rpm, 감속비(입력/출력) {b}인 이상 기어의 출력속도는? 소수 둘째 자리까지 반올림한다.';eq=f'출력속도=입력속도/감속비={a}/{b}={r} rpm. 미끄럼이 없는 이상 조건이다.'
  elif kind==6:
   a=D(40+i);b=D(20+i%10);v=[float(a),float(b)];r=a/b;u='km/L';topic='엔진 · 연비';text=f'정확히 {b} L를 소비하여 {a} km를 주행했다. 거리/연료 기준 연비는? 소수 둘째 자리까지 반올림한다.';eq=f'연비=주행거리/소비 연료={a}/{b}={r} km/L. 도로·차량별 공인 연비를 뜻하지 않는다.'
  elif kind==7:
   a=D(60+i);v=[float(a)];r=a/ D('3.6');u='m/s';topic='섀시 · 속도 단위';text=f'자동차 속도 {a} km/h를 m/s로 바꾸면? 소수 둘째 자리까지 반올림한다.';eq=f'1 km=1000 m, 1 h=3600 s이므로 v={a}×1000/3600={r} m/s.'
  elif kind==8:
   a=D(100+i*5);b=D(2+i%9);v=[float(a),float(b)];r=a*b;u='N';topic='섀시 · 유압';text=f'제동계 피스톤에 게이지압 {a} kPa가 작용한다. 유효 면적이 {b}×10⁻³ m²이고 손실이 없을 때 힘은?';eq=f'F=pA=({a}×1000)×({b}×0.001)={r} N. 게이지압과 유효 면적을 사용한다.'
  elif kind==9:
   a=D(12);b=D(2)+D(i)/10;v=[float(a),float(b)];r=a/b;u='A';topic='전기전자 · 저항 부하';text=f'자동차의 이상 저항 부하 {b} Ω 양단에 {a} V가 걸린다. 전류는? 소수 둘째 자리까지 반올림한다.';eq=f'옴의 법칙 I=V/R={a}/{b}={r} A. 온도에 따른 저항 변화는 무시한다.'
  elif kind==10:
   a=D(12);b=D(1)+D(i)/10;v=[float(a),float(b)];r=a*b;u='W';topic='전기전자 · 전력';text=f'차량 직류 부하 양단 전압 {a} V, 전류 {b} A일 때 소비전력은? 소수 둘째 자리까지 반올림한다.';eq=f'직류 전력 P=VI={a}×{b}={r} W. 배선 손실 등은 별도로 고려하지 않는다.'
  elif kind==11:
   a=D(10+i);b=D('0.01')+D(i%10)/100;v=[float(a),float(b)];r=a*b;u='V';topic='전기전자 · 전압 강하';text=f'시동 회로 배선 구간 저항 {b} Ω에 {a} A가 흐른다. 구간 전압 강하는? 소수 둘째 자리까지 반올림한다.';eq=f'전압 강하 ΔV=IR={a}×{b}={r} V. 전체 배터리 전압과 해당 구간 전압 강하는 다르다.'
  elif kind==12:
   a=D(40+i);b=D(2+i%8);v=[float(a),float(b)];r=a/b;u='h';topic='전기전자 · 용량';text=f'사용 가능 용량 {a} Ah인 이상 배터리에서 일정 전류 {b} A를 공급한다. 이상적인 공급 시간은? 온도·방전율·손실·종지전압 영향 무시, 소수 둘째 자리까지 반올림한다.';eq=f'이상 시간 t=용량/전류={a}/{b}={r} h. 실제 배터리 사용 시간은 이 단순 비례식과 다를 수 있다.'
  elif kind==13:
   a=D(30+i);b=D(2+i%6);v=[float(a),float(b)];r=a*b;u='Wh';topic='전기전자 · 에너지';text=f'일정 소비전력 {a} W인 차량 부하를 {b} h 켜 두었다. 소비 전기에너지는?';eq=f'에너지 E=Pt={a}×{b}={r} Wh. W는 전력, Wh는 에너지 단위이다.'
  else:
   a=D(40+i);b=D(60+i%20);v=[float(a),float(b)];r=a*b/100;u='kW';topic='엔진 · 효율';text=f'기관 입력 동력 {a} kW, 축출력 기준 효율 {b}%일 때 축출력은? 소수 둘째 자리까지 반올림한다.';eq=f'출력=입력×효율={a}×({b}/100)={r} kW. 효율을 백분율에서 비율로 바꾼다.'
  result=rounded(r); vals=[result,rounded(D(str(result))*D('1.5')+1),rounded(D(str(result))*D('0.5')),rounded(D(str(result))*2+2)]
  assert len(set(vals))==4
  add(f'CAR-N-{kind+1:02}-{i+1:03}',topic,text,[f'{fmt(x)} {u}' for x in vals],eq+f' 최종값은 {fmt(result)} {u}이다. 자체 제작 계산 조건 변형이며 기출이 아니다.',family=f'CAR-F-{kind+1:02}',calculation=dict(kind=str(kind),values=v,result=result,unit=u,precision=2))
assert len(bank)==1000
fingerprints=[''.join((q['question']+'|'+ '|'.join(sorted(q['choices']))).split()) for q in bank]
assert len(set(fingerprints))==1000
out=ROOT/'src/data/questions.json';out.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
# A separately authored example avoids duplicating an already installed bank question.
example=dict(bank[0],id='IMPORT-CAR-001',question='등록 양식 예제: 시동 후 크랭킹 모터의 동력 연결을 해제해야 하는 이유는?',choices=['스타터 과회전 방지','연료탱크 용적 증가','냉매 증발 방지','차체 높이 고정'],answer=1,topic='전기전자',explanation='엔진이 자체 회전하면 스타터가 과속 구동될 수 있으므로 구동 연결을 해제한다. 실제 사용 전 근거와 권한을 검토한다.',verificationStatus='pending',reviewNote='등록 양식 예제 · 사용 전 검수 필요')
(ROOT/'public/templates/questions.json').write_text(json.dumps([example],ensure_ascii=False,indent=2)+'\n')
keys=[k for k in example if k!='choices']+['choice1','choice2','choice3','choice4']
with (ROOT/'public/templates/questions.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");w.writeheader();w.writerow({**{k:v for k,v in example.items() if k!='choices'},**{f'choice{i+1}':v for i,v in enumerate(example['choices'])}})
print('1000 original = 100 concepts + 900 numerical variants / 15 families. SHA256',hashlib.sha256(out.read_bytes()).hexdigest())
