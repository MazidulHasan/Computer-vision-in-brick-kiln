import moviepy.editor as mp
import librosa
import numpy as np

# Convert video to audio
def convert_video_to_audio(video_path, audio_path):
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec='mp3')

# Analyze audio for the given frequency range
def detect_metal_sound(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    metal_sound_indices = np.where((y >= 1000) & (y <= 3000))[0]
    metal_sound_times = librosa.samples_to_time(metal_sound_indices, sr=sr)
    return metal_sound_times

# Example usage
video_path = 'D:/Computer-vision-in-brick-kiln/videos/Rec1.avi'
audio_path = 'D:/Computer-vision-in-brick-kiln/audios/R1.mp3'

convert_video_to_audio(video_path, audio_path)
metal_sound_times = detect_metal_sound(audio_path)

print("Metal Sound Instances:")
for time in metal_sound_times:
    print(f"{time:.2f} seconds")
