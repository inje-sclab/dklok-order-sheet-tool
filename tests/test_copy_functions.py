"""
엑셀 복사 기능의 핵심 로직만 테스트 (PyQt 위젯 없이)
"""

def format_table_for_excel(data, headers=None, include_header=True):
    """테이블 데이터를 엑셀 호환 형식으로 변환하는 함수"""
    result = []
    
    # 헤더 추가
    if include_header and headers:
        result.append("\t".join(headers))
    
    # 데이터 행 추가
    for row in data:
        # 특수 문자 처리
        formatted_row = []
        for cell in row:
            cell_text = str(cell).replace('\n', ' ').replace('\r', ' ')
            formatted_row.append(cell_text)
        result.append("\t".join(formatted_row))
    
    return "\n".join(result)


def test_excel_format_with_header():
    """헤더 포함 엑셀 형식 테스트"""
    data = [
        ["DMCA-4N-SA", "22"],
        ["DMCA-8N-SA", "7"],
        ["DMCA-12N-SA", "15"]
    ]
    headers = ["품번", "수량"]
    
    result = format_table_for_excel(data, headers, include_header=True)
    lines = result.split('\n')
    
    assert lines[0] == "품번\t수량"
    assert lines[1] == "DMCA-4N-SA\t22"
    assert lines[2] == "DMCA-8N-SA\t7"
    assert lines[3] == "DMCA-12N-SA\t15"
    assert len(lines) == 4


def test_excel_format_without_header():
    """헤더 없이 엑셀 형식 테스트"""
    data = [
        ["DMCA-4N-SA", "22"],
        ["DMCA-8N-SA", "7"],
        ["DMCA-12N-SA", "15"]
    ]
    
    result = format_table_for_excel(data, include_header=False)
    lines = result.split('\n')
    
    assert lines[0] == "DMCA-4N-SA\t22"
    assert lines[1] == "DMCA-8N-SA\t7"
    assert lines[2] == "DMCA-12N-SA\t15"
    assert len(lines) == 3


def test_special_character_handling():
    """특수 문자 처리 테스트"""
    data = [
        ["TEST\nPART", "10\r"],
        ["NORMAL-PART", "5"]
    ]
    
    result = format_table_for_excel(data, include_header=False)
    lines = result.split('\n')
    
    # 줄바꿈과 캐리지 리턴이 공백으로 변환되어야 함
    assert lines[0] == "TEST PART\t10 "
    assert lines[1] == "NORMAL-PART\t5"


def test_empty_data():
    """빈 데이터 테스트"""
    data = []
    headers = ["품번", "수량"]
    
    result = format_table_for_excel(data, headers, include_header=True)
    assert result == "품번\t수량"
    
    result = format_table_for_excel(data, include_header=False)
    assert result == ""


if __name__ == "__main__":
    test_excel_format_with_header()
    test_excel_format_without_header() 
    test_special_character_handling()
    test_empty_data()
    print("모든 테스트 통과! ✅")