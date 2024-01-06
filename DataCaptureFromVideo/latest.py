import moviepy.editor as mp
import librosa
import numpy as np
import csv

# Convert video to audio
def convert_video_to_audio(video_path, audio_path):
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec='mp3')

# Frequency analysis
def analyze_frequency(audio_file, min_freq, max_freq):
    y, sr = librosa.load(audio_file)
    onset_envelope = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_envelope)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    stft = librosa.stft(y)
    power_spectrogram = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

    freq_bins = np.fft.fftfreq(len(power_spectrogram), d=1/sr)

    results = []

    for onset_time in onset_times:
        onset_frame = librosa.time_to_frames(onset_time, sr=sr)
        freq_content = power_spectrogram[:, onset_frame]

        valid_freq_indices = np.where((freq_bins >= min_freq) & (freq_bins <= max_freq))[0]

        if len(valid_freq_indices) > 0:
            max_freq_bin = valid_freq_indices[np.argmax(freq_content[valid_freq_indices])]
            max_freq_hz = freq_bins[max_freq_bin]

            results.append([onset_time, max_freq_hz])

    return results

# Save results to CSV
def save_to_csv(results, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Timestamp', 'Frequency (Hz)'])
        csv_writer.writerows(results)

# Example usage
video_path = 'D:/Computer-vision-in-brick-kiln/videos/Rec1.avi'
audio_path = 'D:/Computer-vision-in-brick-kiln/audios/R1.mp3'
csv_path = 'D:/Computer-vision-in-brick-kiln/CSVFiles/results.csv'

convert_video_to_audio(video_path, audio_path)

# Frequency analysis on the converted audio
min_freq = 2500  
max_freq = 4000 
results = analyze_frequency(audio_path, min_freq, max_freq)

# Save results to CSV
save_to_csv(results, csv_path)
