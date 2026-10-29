# Craftsman-Motor-Vehicle-Maintenance-CBT

자동차정비기능사 필기 학습용 CBT. React + TypeScript + Vite 정적 앱이며 로그인·서버·유료 API가 없다.

## 구현

- 실전 60문항/60분 학습용 모의시험: 고유 문항 추출, family 분산, 답안 변경·번호 이동·북마크, 절대 종료시각, 자동 제출·중복 제출 방지, 결과·전체 해설·오답 복습.
- 랜덤 문제풀이: 통합과목 선택, 순회 중복 방지, 즉시 채점, 연속 정답, 이어하기, 오답노트·북마크·통계.
- 두 모드 답안 선택 후 Space 이동. 미응답·길게 누름·IME·수정키·폼·메뉴·대화상자 보호, 마지막 문항 자동 제출 없음.
- 문제은행 JSON/CSV 양식·가져오기, ID/본문/보기 재배열 중복 제거, 검증 대기, 근거 입력 후 로컬 승인, 검색·페이지·내보내기.
- 자동차정비 고유 localStorage 키 `motor-vehicle-maintenance-cbt:v1`. 최근 응답 5,000개·시험 30회, 진행 상태·개인 등록·오답·북마크 저장. 손상 원본 보존과 저장 실패 경고, JSON 백업·확인 후 초기화. 백업 복원 UI는 제공하지 않는다.
- 학습 기준/연도 선택 메뉴 및 상단 상시 면책 배너 없음. 비공식 표시는 사이드바·푸터, 상세 한계는 문제은행과 문서.
- 모바일 메뉴 독립 스크롤·100dvh/100vh·flex 높이 보존·배경 스크롤 전파 억제. 작은 화면·가로·확대 글자에서 휠·터치 입력 회귀 검사.

## 표준과 재사용

최신 main에서 읽은 스킬: `YunSangYeong/electrician-cbt` 커밋 `76b990b8720adfa85c22a0a8f699b17094aa357b`, 표준 **v1.4.0**.
스킬 전체와 references를 `.agents/skills/cbt-site-standard/`로 복사했고 AGENTS.md로 연결했다. 기존 AGENTS.md는 없었다.
앱은 지정된 `b9a682ccff1b460334b78d5bfad9375b7ec4fbb6`의 App/model/styles/설정/테스트/workflow를 실제 재사용했다. 전기 문제 데이터는 복사하지 않았다. 원본 MIT 고지를 유지했다. 원본 저장소를 수정·푸시·재배포하지 않았다.

## 시험 규칙 확인 상태

**최신 공식 규칙 직접 대조 미완료.** Q-Net 시도 URL과 실제 403 오류는 [문항 검토 기록](docs/question-review.md)에 있다. 종목 코드·공식 과목명·시간·배점·과락 조건의 일치도 확인되지 않았다.
현재 `src/qualification.json`의 설정은 학습용 가정: 자동차정비 통합과목, 60문항·60분·4지선다·동일 배점 총 100점·60점 이상 합격·과락 없음·미응답 오답. 점수 표시 소수 첫째 자리 반올림과 합격 판정 원값을 구별한다.
단원별 균등 출제를 공식 규칙으로 주장하지 않는다. 실제 차량 정비는 제조사 최신 매뉴얼과 안전절차를 따른다.

## 실제 문제 수와 한계

|분류|실제 수|
|---|---:|
|자체 제작 개념 원고|100|
|자체 제작 숫자 조건 변형|900 (15 family × 60)|
|원문 기출 / 복원|0 / 0|
|중복 제거 후 내부 검토 등록 합계|1,000|
|목표 대비 수량 부족|0|
|검증 대기 기본 문항 / 개인 등록 포함 수|0 / 0|

분야별: 엔진 332, 섀시 267, 전기전자 325, 안전 76. 공식 과목별 분포가 아닌 학습 은행 구성이다.
100개 개념 원고와 15개 계산 family로 구성되며 1,000개의 독립 개념이나 기출을 뜻하지 않는다.
`reviewed`는 AI 일반 지식 기반 내부 개념·해설 검토와 별도 수치 테스트 범위다. 공식 출제기준 대조와 외부 전문가 검수는 미완료이며, 수량 충족을 전체 정확성 인증으로 해석하지 않는다.
확인하지 않은 출처·연도·회차는 만들지 않았다. 모든 year/session은 null. sourceUrl은 작성 기록이고 외부 정답 증빙이 아니다. 자체 작성 문항/양식 CC BY 4.0, 재사용 앱 MIT. [자세한 출처·권리·검토 범위](docs/question-review.md).

## 로컬 개발

Node 24.19.0 (`.node-version`), package engines >=22.12.0. 기존 체크아웃에서 작업하며 별도 worktree가 필요하지 않다.

```sh
cd /workspace/Craftsman-Motor-Vehicle-Maintenance-CBT
npm ci --cache /tmp/car-cbt-npm-cache --no-audit --no-fund
npm run dev
```

환경 기본 npm 캐시 경로에 쓰기 오류가 있어 현재 환경에서는 위 `/tmp` 캐시를 사용한다. TLS·패키지 integrity 검증은 유지한다.
라이브 프로세스는 새 작업에서 다시 시작해야 한다. dev/preview base는 `/Craftsman-Motor-Vehicle-Maintenance-CBT/`이다.

```sh
python3 scripts/generate_bank.py
npm test
npm run build
# 현재 환경의 Chromium 사용
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e
# 일반 개발기에서는 먼저 npx playwright install --with-deps chromium
```

JSON은 고정 ID·순서·보기 회전으로 재생성된다. 개념 원고와 생성 코드는 scripts에 있다. 생성과 검증 수식은 서로 다른 언어의 별도 구현이다.

## 실제 검증 결과

- `npm ci --cache /tmp/car-cbt-npm-cache --no-audit --no-fund`: 성공.
- `npm test`: **917 통과**, 계산 문항 900개의 별도 수치·단위·보기 검증 포함.
- `npm run test:e2e`: **26 통과 / 2 해당 없음 skip**. 데스크톱 프로젝트의 터치 전용 2건을 제외한 것이며 모바일 프로젝트에서는 두 터치 검사 모두 실행·통과했다.
- Chromium 데스크톱/Pixel 7 에뮬레이션: 실전 채점·수정·복원·만료·해설, 랜덤·오답·북마크·통계, JSON/CSV 등록·승인·중복·초기화, 저장 손상/실패, Space·포커스·경계 보호 검사.
- 390×480, 740×360: 실제 mouse wheel과 CDP touchStart/move/end로 하단 백업/초기화 → 상단 대시보드 왕복·클릭/탭 확인. 프로그램으로 scrollTop을 설정하지 않았다. 확대된 메뉴 글자 터치 검사 포함.
- PC 1440×1000와 모바일 390×844 전체 화면 캡처로 시각 확인. 실기기·Safari·Firefox 검사는 미실행.
- 프로덕션 타입 검사·Vite 빌드 성공. 단일 은행 번들이 커서 500kB chunk 경고가 있다(약 1.35MB, gzip 약149KB). 빌드 실패는 아니다.
- 개념 의미·차량 정비 적합성과 공식 규칙을 자동 테스트가 증명하지 않는다.

## GitHub·Pages 상태 (2026-10-30)

예정 흐름은 main push → validate(npm ci/단위/빌드/PC·모바일) → Pages deploy. PR은 검증만, 수동 실행은 자동 실행과 중복하지 않는다. Workflow는 `.github/workflows/pages.yml`에 준비했다.

**배포 사전 확인에서 첫 차단 발생, 재시도 없이 중단.**

- 대상 `git fetch origin main`: 성공. 원격 main은 초기 커밋 `848568ecd5233c59efd5d9a185124908fcb65d5c`와 같은 상태였다.
- `gh api repos/YunSangYeong/Craftsman-Motor-Vehicle-Maintenance-CBT --jq '{full_name,default_branch,permissions}'`: exit 1, `Get "https://api.github.com/repos/YunSangYeong/Craftsman-Motor-Vehicle-Maintenance-CBT": Forbidden`.
- 저장소 권한·Pages Source·배포 상태는 API 차단 때문에 확인하지 못했다. 인증 부재인지 HTTP 정책 거부인지 확정하지 않았다. 현재 네트워크 정책의 허용 호스트에는 `api.github.com`이 없다.
- main 푸시·워크플로 실행·재실행·우회 배포·배포 유발 추가 푸시 없음. CI/Pages를 성공했다고 주장하지 않는다. 구현은 로컬 work 브랜치 커밋에 보존한다.
- 사용자가 지금 확인할 첫 동작: 클라우드 환경 설정의 인터넷 허용 도메인에 `api.github.com` 추가. 이 설정만으로 GitHub 권한까지 확보됐다고 단정할 수 없다. 사용자 재개 지시 전 에이전트가 다시 시도하지 않는다.
- 예상 기본 주소: `https://YunSangYeong.github.io/Craftsman-Motor-Vehicle-Maintenance-CBT/`. 게시·접속·공개 화면 확인 모두 미실행. 기존 공개 사이트 유무도 미확인이다.

클라우드 환경 자체를 게시하거나 재게시하는 작업은 하지 않았다.
