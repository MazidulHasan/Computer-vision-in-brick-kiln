import librosa
import numpy as np

# Load the audio file
file_path = 'D:/Computer-vision-in-brick-kiln/audios/R1.mp3'
y, sr = librosa.load(file_path)

# Compute the onset strength
onset_envelope = librosa.onset.onset_strength(y=y, sr=sr)

# Print debug information
print("Length of onset envelope:", len(onset_envelope))

# Use the onset envelope to detect onsets
onset_frames = librosa.onset.onset_detect(onset_envelope=onset_envelope)

# Print debug information
print("Number of detected onsets:", len(onset_frames))

# Convert onset frames to timestamps
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

# Define the frequency range of interest
min_freq = 2500  # 1000Hz
max_freq = 3000  # 3000Hz

# Iterate through onset times and filter by frequency range
for onset_time in onset_times:
    # Compute the short-time Fourier transform (STFT)
    stft = librosa.stft(y)
    # Convert the STFT to a power spectrogram
    power_spectrogram = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
    # Find the frequency bin corresponding to the onset time
    onset_frame = librosa.time_to_frames(onset_time, sr=sr)
    # Extract the frequency content around the onset frame
    freq_content = power_spectrogram[:, onset_frame]
    # Find the frequency with the maximum amplitude
    max_freq_index = np.argmax(freq_content)
    max_freq_hz = max_freq_index * (sr / 2) / len(power_spectrogram)

    # Check if the frequency is within the specified range
    if min_freq <= max_freq_hz <= max_freq:
        print(f"At timestamp {onset_time:.2f} seconds, the dominant frequency is {max_freq_hz:.2f} Hz")
