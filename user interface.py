import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import time
import wave
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import http.client   
# 当前情感类别和曲目索引
current_emotion = None
current_index = 0
current_song_length = 0  # 当前歌曲长度（毫秒）

# 创建主窗口
root = tk.Tk()
root.title("Emotion-Based Music Player")

# 标签显示当前播放的曲目
current_song_label = tk.Label(root, text="No song is playing", font=("Helvetica", 12))
current_song_label.pack(pady=10)

# 进度条
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=10)

# 时间标签
time_label = tk.Label(root, text="00:00 / 00:00", font=("Helvetica", 12))
time_label.pack(pady=10)

# 情感标签
emotion_label = tk.Label(root, text="Emotion: None", font=("Helvetica", 12))
emotion_label.pack(pady=10)

# 按钮点击事件处理函数
def on_play_button_click():
    record_audio_and_play_music()

# 绘制波形图的画布
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# 格式化时间的函数（毫秒转换为分:秒）
def format_time(milliseconds):
    seconds = int((milliseconds / 1000) % 60)
    minutes = int((milliseconds / (1000 * 60)) % 60)
    return f"{minutes:02d}:{seconds:02d}"

# 上一曲和下一曲的函数
def previous_song():
    if current_emotion is not None:
        global current_index
        current_index = (current_index - 1) % len(music_library[current_emotion])
        play_music(current_emotion, current_index)

def next_song():
    if current_emotion is not None:
        global current_index
        current_index = (current_index + 1) % len(music_library[current_emotion])
        play_music(current_emotion, current_index)

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
                # 按钮点击事件处理函数
def on_play_button_click():
    record_audio_and_play_music()

# 绘制音频波形图的函数
def plot_waveform(music_path):
    try:
        with wave.open(music_path, 'rb') as wav_file:
            # 读取音频数据
            signal = wav_file.readframes(-1)
            signal = np.frombuffer(signal, dtype='int16')

            # 获取音频的帧率
            framerate = wav_file.getframerate()

            # 时间轴
            time = np.linspace(0, len(signal) / framerate, num=len(signal))

            # 绘制波形图
            ax.clear()
            ax.plot(time, signal)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude')
            ax.set_title('Audio Waveform')
            canvas.draw()
    except Exception as e:
        print(f"Error plotting waveform: {e}")
# 创建按钮
play_button = tk.Button(root, text="Record & Play", command=on_play_button_click, font=("Helvetica", 12))
play_button.pack(pady=10)

previous_button = tk.Button(root, text="<< Previous", command=previous_song, font=("Helvetica", 12))
previous_button.pack(side=tk.LEFT, padx=10)

next_button = tk.Button(root, text="Next >>", command=next_song, font=("Helvetica", 12))
next_button.pack(side=tk.RIGHT, padx=10)

# 处理情绪识别准确度反馈的函数
def handle_emotion_feedback(feedback):
    feedback_file = os.path.join(music_folder, 'emotion_feedback.txt')
    with open(feedback_file, 'a') as file:
        file.write(f'{feedback}\n')
    messagebox.showinfo("Feedback", "Thank you for your feedback on emotion recognition!")

# 处理歌曲标签正确度反馈的函数
def handle_song_feedback(feedback):
    feedback_file = os.path.join(music_folder, 'song_feedback.txt')
    with open(feedback_file, 'a') as file:
        file.write(f'{feedback}\n')
    messagebox.showinfo("Feedback", "Thank you for your feedback on song tagging!")

# 创建反馈按钮
emotion_correct_button = tk.Button(root, text="Emotion Correct", command=lambda: handle_emotion_feedback('correct'), font=("Helvetica", 12))
emotion_correct_button.pack(side=tk.LEFT, padx=10)

emotion_incorrect_button = tk.Button(root, text="Emotion Incorrect", command=lambda: handle_emotion_feedback('incorrect'), font=("Helvetica", 12))
emotion_incorrect_button.pack(side=tk.LEFT, padx=10)

song_correct_button = tk.Button(root, text="Song Tag Correct", command=lambda: handle_song_feedback('correct'), font=("Helvetica", 12))
song_correct_button.pack(side=tk.RIGHT, padx=10)

song_incorrect_button = tk.Button(root, text="Song Tag Incorrect", command=lambda: handle_song_feedback('incorrect'), font=("Helvetica", 12))
song_incorrect_button.pack(side=tk.RIGHT, padx=10)
