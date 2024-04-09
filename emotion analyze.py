import librosa
import numpy as np
from transformers import pipeline
# 加载情感分析模型
sentiment_analysis = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")def analyze_emotion_and_intonation(audio, text):
# 分析文本情感和语调
def analyze_emotion_and_intonation(audio, text):
    # 文本情感分析
    text_results = sentiment_analysis(text)
    text_emotion = 'neutral'  # 设置默认情感为中立
    if text_results[0]['label'] == 'POSITIVE':
        text_emotion = 'positive'
    elif text_results[0]['label'] == 'NEGATIVE':
        text_emotion = 'negative'

    # 语音语调分析
    audio_data = np.frombuffer(audio.get_wav_data(), dtype=np.int16)
    y, sr = librosa.load(io.BytesIO(audio.get_wav_data()), sr=None)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_mean = np.mean(pitches[pitches > 0])
    intensity_mean = np.mean(librosa.amplitude_to_db(np.abs(librosa.stft(y))))

    # 综合情感和语调分析
    if pitch_mean > 150 and intensity_mean > -20:  # 示例条件，可根据实际情况调整
        final_emotion = 'positive'
    elif pitch_mean < 100 and intensity_mean < -40:
        final_emotion = 'negative'
    else:
        final_emotion = text_emotion

    emotion_label.config(text=f"Emotion: {final_emotion} (Text: {text_emotion}, Pitch: {pitch_mean:.2f} Hz, Intensity: {intensity_mean:.2f} dB)")  # 更新情感标签
    messagebox.showinfo("Emotion Detected", f"The emotion of the text is: {final_emotion} (Text: {text_emotion}, Pitch: {pitch_mean:.2f} Hz, Intensity: {intensity_mean:.2f} dB)")
    return final_emotion, {'pitch': pitch_mean, 'intensity': intensity_mean}