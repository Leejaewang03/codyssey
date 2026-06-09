import os

def caesar_cipher_decode(target_text):
    # 보너스 과제: 텍스트 사전 (화성 기지에서 쓰일 법한 유력한 키워드들)
    dictionary = ['coffee', 'oxygen', 'mars', 'base', 'system', 'emergency', 'door', 'water', 'food', 'open']
    
    print('=== 카이사르 암호 해독을 시작합니다 ===')
    
    # 알파벳 개수(26개)만큼 반복하므로 1부터 25까지 Shift(자리수) 이동
    for shift in range(1, 26):
        decoded_chars = []
        
        for char in target_text:
            if 'a' <= char <= 'z':
                decoded_chars.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                decoded_chars.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                # 알파벳이 아닌 기호나 숫자는 그대로 둡니다.
                decoded_chars.append(char)
                
        decoded_text = ''.join(decoded_chars)
        print(f'[Shift {shift:02d}] {decoded_text}')
        
        # 보너스 과제 로직: 해독된 문장에 사전 속 단어가 포함되어 있는지 검사
        word_found = False
        for word in dictionary:
            if word in decoded_text.lower():
                print(f'\n*** [시스템 알림] 사전에 등록된 단어(\'{word}\')가 발견되었습니다! ***')
                print('- 의미 있는 문장으로 판단되어 자동 해독을 중지합니다.')
                word_found = True
                break
                
        if word_found:
            break

def main():
    # 1. 파일 읽기 및 예외 처리
    try:
        with open('password.txt', 'r', encoding='utf-8') as f:
            target_text = f.read().strip()
    except FileNotFoundError:
        print('오류: password.txt 파일을 찾을 수 없습니다.')
        return
    except Exception as e:
        print(f'오류: 파일을 읽는 중 문제가 발생했습니다: {e}')
        return
        
    if not target_text:
        print('경고: password.txt 파일이 비어 있습니다.')
        return
        
    # 2. 카이사르 암호 해독 함수 호출 (결과 출력 및 사전 매칭 시 자동 중단)
    caesar_cipher_decode(target_text)
    
    # 3. 눈으로 확인한 자리수 입력 및 결과 저장
    try:
        user_input = input('\n눈으로 식별된 올바른 암호의 자리수(Shift 번호)를 입력하세요: ')
        selected_shift = int(user_input)
        
        # 입력받은 자리수로 텍스트를 최종 복호화
        final_chars = []
        for char in target_text:
            if 'a' <= char <= 'z':
                final_chars.append(chr((ord(char) - ord('a') + selected_shift) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                final_chars.append(chr((ord(char) - ord('A') + selected_shift) % 26 + ord('A')))
            else:
                final_chars.append(char)
                
        final_text = ''.join(final_chars)
        
        # result.txt에 예외 처리를 포함하여 저장
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write(final_text)
            
        print(f'\n[성공] 해독된 암호 \'{final_text}\'가 result.txt에 저장되었습니다. 창고 문이 열립니다!')
        
    except ValueError:
        print('오류: 올바른 숫자를 입력하지 않아 프로그램을 종료합니다.')
    except Exception as e:
        print(f'오류: 파일을 저장하는 중 문제가 발생했습니다: {e}')

if __name__ == '__main__':
    main()