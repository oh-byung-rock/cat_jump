def replace_file(file_path, old_word, new_word):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()  # 파일 읽기

    content = content.replace(old_word, new_word)  # 문자열 변환

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)  # 변경된 내용 저장

# 단어 replace 실행
# 방법 : 터미널에서 'python replace.py' 실행
file_path = 'final2.py'  # 수정할 파일 경로
replace_file(file_path, 'screen_width', 'configure.screen_width')
replace_file(file_path, 'screen_height', 'configure.screen_height')