# 주문서 OCR 처리 도구

OpenAI GPT-4o-mini를 활용하여 주문서 이미지/PDF에서 품번과 수량 정보를 자동으로 추출하는 도구입니다.

## 기능

- **다양한 파일 형식 지원**: PDF, JPG, PNG 등
- **자동 품목 추출**: 표 형태의 데이터에서 품번과 수량을 정확히 추출
- **GUI 및 CLI 모드**: 사용 환경에 맞는 인터페이스 선택
- **개발 모드**: API 키 없이도 개발 및 테스트 가능
- **결과 내보내기**: JSON 형태로 결과 저장, 클립보드 복사 기능

## 설치

### 필수 요구사항
- Python 3.12+
- uv (패키지 관리자)

### 의존성 설치
```bash
uv sync
```

### PDF 처리를 위한 추가 설치 (권장)
```bash
pip install PyMuPDF
```

## 사용법

### GUI 모드 (기본)
```bash
python main.py
```

### CLI 모드
```bash
python main.py --cli [파일경로]
```

## 프로젝트 구조

```
dklok_order_sheet_tool/
├── src/
│   ├── core/           # 핵심 비즈니스 로직
│   │   ├── ocr_service.py      # OCR 서비스 (실제/모킹)
│   │   └── document_processor.py  # 문서 처리 메인 로직
│   ├── gui/            # GUI 컴포넌트
│   │   ├── main_window.py      # 메인 윈도우
│   │   ├── widgets.py          # 커스텀 위젯들
│   │   └── styles.py           # UI 스타일
│   ├── models/         # 데이터 모델
│   │   ├── order_item.py       # 주문 항목 모델
│   │   └── document.py         # 문서 모델
│   ├── config/         # 설정 관리
│   │   └── settings.py         # 앱 설정
│   └── utils/          # 유틸리티
│       ├── file_utils.py       # 파일 처리 유틸
│       └── pdf_converter.py    # PDF 변환 유틸
├── tests/              # 테스트 코드
├── data/               # 샘플 데이터
├── docs/               # 문서
├── main_new.py         # 새로운 메인 진입점
├── main.py             # 기존 메인 파일 (레거시)
└── test.py             # 테스트 파일 (레거시)
```

## 설정

### API 키 설정
1. GUI 모드에서 `설정` 메뉴 클릭
2. OpenAI API 키 입력
3. 모델명 설정 (기본: gpt-4o-mini)

### 개발 모드
API 키 없이 개발하려면 설정에서 "개발 모드" 체크박스를 활성화


### 모킹 시스템
- API 키가 없거나 개발 모드일 때 자동으로 모킹 데이터 사용
- 실제 API 호출 없이 기능 테스트 가능

## 개발

### 새로운 기능 추가
1. 적절한 모듈에 기능 구현
2. 모킹 데이터 추가 (필요한 경우)
3. 테스트 코드 작성
4. GUI에 기능 연동

### 테스트 실행
```bash
python -m pytest tests/
```

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.