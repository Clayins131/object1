import speech_recognition as sr
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
