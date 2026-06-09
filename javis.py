import os
import csv
import time
import datetime
import wave
import pyaudio
import speech_recognition as sr

class Javis:
    def __init__(self):
        self.record_dir = 'records'
        self._prepare_directory()

    def _prepare_directory(self):
        if not os.path.exists(self.record_dir):
            try:
                os.makedirs(self.record_dir)
            except Exception as e:
                print(f'오류: 폴더 생성에 실패했습니다. ({e})')

    def record_audio(self, record_seconds=10):
        """마이크로 음성을 녹음하여 wav 파일로 저장합니다."""
        chunk = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 44100
        
        p = pyaudio.PyAudio()
        
        try:
            print(f'\n=== 🎙️ 마이크 녹음을 시작합니다 ({record_seconds}초) ===')
            stream = p.open(format=audio_format,
                            channels=channels,
                            rate=rate,
                            input=True,
                            frames_per_buffer=chunk)
                            
            frames = []
            
            for _ in range(0, int(rate / chunk * record_seconds)):
                data = stream.read(chunk)
                frames.append(data)
                
            print('=== 🛑 녹음이 완료되었습니다 ===')
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            print(f'오류: 마이크 접근 중 문제가 발생했습니다. ({e})')
            p.terminate()
            return
            
        p.terminate()
        
        now = datetime.datetime.now()
        filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
        filepath = os.path.join(self.record_dir, filename)
        
        try:
            wf = wave.open(filepath, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(audio_format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            print(f'[저장 성공] 파일명: {filename}')
        except Exception as e:
            print(f'오류: 오디오 파일을 저장하는 중 문제가 발생했습니다. ({e})')

    def convert_stt_to_csv(self):
        """[수행과제] records 폴더의 wav 파일들을 STT로 변환하여 CSV로 저장합니다."""
        recognizer = sr.Recognizer()
        
        try:
            files = os.listdir(self.record_dir)
            wav_files = [f for f in files if f.endswith('.wav')]
        except Exception as e:
            print(f'오류: 디렉토리를 읽을 수 없습니다. ({e})')
            return
            
        if not wav_files:
            print('안내: 변환할 wav 파일이 없습니다.')
            return
            
        for wav_file in wav_files:
            csv_file = wav_file.replace('.wav', '.csv')
            wav_path = os.path.join(self.record_dir, wav_file)
            csv_path = os.path.join(self.record_dir, csv_file)
            
            # 이미 변환된 CSV가 있다면 중복 변환을 피하기 위해 건너뜁니다.
            if os.path.exists(csv_path):
                continue
                
            print(f'\n📝 STT 변환 중... ({wav_file})')
            results = []
            
            try:
                # 시간 기록을 위해 전체 오디오의 길이를 구합니다.
                with sr.AudioFile(wav_path) as source:
                    duration = int(source.DURATION)
                    
                # 10초 단위로 오디오를 잘라서 인식합니다.
                for i in range(0, duration, 10):
                    with sr.AudioFile(wav_path) as source:
                        audio = recognizer.record(source, offset=i, duration=10)
                        
                    try:
                        text = recognizer.recognize_google(audio, language='ko-KR')
                        time_str = f'{i // 60:02d}:{i % 60:02d}'
                        results.append([time_str, text])
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError:
                        print('오류: 구글 STT 서버에 접근할 수 없습니다.')
                        break
                        
            except Exception as e:
                print(f'오류: 파일 처리 중 문제가 발생했습니다. ({e})')
                continue
                
            # 시간과 텍스트를 CSV 파일로 저장합니다.
            if results:
                try:
                    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['시간', '인식된 텍스트'])
                        writer.writerows(results)
                    print(f'[변환 성공] 파일명: {csv_file}')
                except Exception as e:
                    print(f'오류: CSV 파일을 저장할 수 없습니다. ({e})')
            else:
                print(f'안내: {wav_file} 에서 인식된 음성이 없습니다.')

    def find_files_by_date(self, start_date, end_date):
        print(f'\n=== 📅 검색 기간: {start_date} ~ {end_date} ===')
        try:
            files = os.listdir(self.record_dir)
            wav_files = [f for f in files if f.endswith('.wav')]
            
            found = False
            for f in wav_files:
                file_date = f.split('-')[0]
                if start_date <= file_date <= end_date:
                    print(f'- 발견된 파일: {f}')
                    found = True
                    
            if not found:
                print('해당 기간에 녹음된 파일이 없습니다.')
        except Exception as e:
            print(f'오류: 파일을 검색하는 중 문제가 발생했습니다. ({e})')

    def search_keyword_in_csv(self, keyword):
        """[보너스 과제] 저장된 CSV 파일 안에서 특정 키워드를 찾습니다."""
        print(f'\n=== 🔍 키워드 검색: \'{keyword}\' ===')
        try:
            files = os.listdir(self.record_dir)
            csv_files = [f for f in files if f.endswith('.csv')]
            
            found = False
            for csv_file in csv_files:
                csv_path = os.path.join(self.record_dir, csv_file)
                
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)
                    
                    for row in reader:
                        if len(row) == 2:
                            time_str, text = row
                            if keyword in text:
                                print(f'[{csv_file}] {time_str} - {text}')
                                found = True
                                
            if not found:
                print('일치하는 키워드가 없습니다.')
        except Exception as e:
            print(f'오류: 키워드 검색 중 문제가 발생했습니다. ({e})')


def main():
    javis = Javis()
    
    while True:
        print('\n' + '='*40)
        print('🤖 JAVIS - 화성 기지 음성 기록 시스템')
        print('='*40)
        print('1. 음성 기록 시작 (10초 녹음)')
        print('2. 미변환 녹음 파일 STT 해독 (CSV 저장)')
        print('3. 날짜로 기록 찾기')
        print('4. 키워드로 기록 내용 검색')
        print('5. 시스템 종료')
        print('='*40)
        
        choice = input('원하는 기능의 번호를 입력하세요: ')
        
        if choice == '1':
            javis.record_audio(record_seconds=10)
        elif choice == '2':
            javis.convert_stt_to_csv()
        elif choice == '3':
            start = input('시작 날짜를 입력하세요 (예: 20260501): ')
            end = input('종료 날짜를 입력하세요 (예: 20260531): ')
            javis.find_files_by_date(start, end)
        elif choice == '4':
            keyword = input('검색할 키워드를 입력하세요: ')
            javis.search_keyword_in_csv(keyword)
        elif choice == '5':
            print('시스템을 종료합니다. 행운을 빕니다, 박사님.')
            break
        else:
            print('잘못된 입력입니다. 다시 선택해주세요.')

if __name__ == '__main__':
    main()