# Python code to convert video to audio
import moviepy.editor as mp

# Insert Local Video File Path 
clip = mp.VideoFileClip(r"D:/Computer-vision-in-brick-kiln/videos/Rec1.avi")

# Insert Local Audio File Path
clip.audio.write_audiofile(r"D:/Computer-vision-in-brick-kiln/audios/R1.mp3")

def detect_metal_sound(audio_file, start_time):
    y, sr = librosa.load(audio_file, sr=None)
    metal_sound_indices = np.where((y >= 1000) & (y <= 3000))[0]
    metal_sound_times = librosa.samples_to_time(metal_sound_indices, sr=sr)
    metal_sound_times += start_time
    return metal_sound_times

