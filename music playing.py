import pygame
import os
# 初始化 pygame
pygame.mixer.init()
# 指定音乐文件夹路径
music_folder = 'C:\\Users\\clays\\Desktop\\music'
# 音乐库字典
music_library = {
    'positive': ['celestial.wav'],
    'neutral': ['under no flag.wav'],
    'negative': ['I like me better.wav', 'I aint worries.wav']
}
# 录制音频并返回识别的文本，并根据情感播放音乐
def record_audio_and_play_music():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 1 minute...")
        progress_bar['value'] = 0
        root.update()
        audio = None
        try:
            # Start a thread to update the progress bar
            def update_progress():
                for i in range(60):
                    time.sleep(1)
                    progress_bar['value'] += 100 / 60
                    root.update()

            threading.Thread(target=update_progress).start()

            audio = recognizer.listen(source, timeout=10, phrase_time_limit=60)
        except sr.WaitTimeoutError:
            messagebox.showerror("Error", "Listening timed out.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        if audio:
            try:
                text = recognizer.recognize_google(audio, language='zh-CN')
                print(f"Recognized text: {text}")
                emotion, intonation_features = analyze_emotion_and_intonation(audio, text)
                play_music(emotion)
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")
            except http.client.IncompleteRead as e:  # 修改异常类型
                messagebox.showerror("Error", f"Incomplete read error: {e}")
# 播放音乐的函数
def play_music(emotion, index=0):
    global current_emotion, current_index, current_song_length
    current_emotion = emotion
    current_index = index
    if emotion in music_library:
        song = music_library[emotion][index]
        music_path = os.path.join(music_folder, song)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
        current_song_label.config(text=f"Playing {emotion} music: {song}")
        plot_waveform(music_path)
        current_song_length = pygame.mixer.Sound(music_path).get_length() * 1000  # 获取歌曲长度（毫秒）
        update_progress()  # 更新进度条和时间

