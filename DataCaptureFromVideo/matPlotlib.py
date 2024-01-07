import librosa
import numpy as np
import matplotlib.pyplot as plt

# Load the audio file
file_path = 'D:/Computer-vision-in-brick-kiln/audios/R1.mp3'
y, sr = librosa.load(file_path)

# Compute the onset strength
onset_envelope = librosa.onset.onset_strength(y=y, sr=sr)

# Use the onset envelope to detect onsets
onset_frames = librosa.onset.onset_detect(onset_envelope=onset_envelope)

# Convert onset frames to timestamps
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

# Compute the short-time Fourier transform (STFT) once
stft = librosa.stft(y)
# Convert the STFT to a power spectrogram
power_spectrogram = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

# Define the frequency range of interest
min_freq = 3000
max_freq = 4000

# Set a threshold for amplitude
amplitude_threshold = -60  # Adjust this threshold as needed

# Visualize the power spectrogram
plt.figure(figsize=(12, 8))
librosa.display.specshow(power_spectrogram, sr=sr, x_axis='time', y_axis='hz')
plt.colorbar(format='%+2.0f dB')
plt.title('Power Spectrogram')
plt.show()

# Iterate through onset times and filter by frequency range
for onset_time in onset_times:
    # Find the frequency bin corresponding to the onset time
    onset_frame = librosa.time_to_frames(onset_time, sr=sr)
    # Extract the frequency content around the onset frame
    freq_content = power_spectrogram[:, onset_frame]

    # Calculate min_freq and max_freq bin indices
    min_freq_bin = int(min_freq * len(power_spectrogram[0]) / (sr / 2))
    max_freq_bin = int(max_freq * len(power_spectrogram[0]) / (sr / 2))

    # Ensure valid frequency range indices
    min_freq_bin = max(0, min(min_freq_bin, len(freq_content) - 1))
    max_freq_bin = min(len(freq_content), max_freq_bin)

    print(f"At timestamp {onset_time:.2f} seconds:")
    print(f"  min_freq_bin: {min_freq_bin}, max_freq_bin: {max_freq_bin}")

    # Print information about frequency content
    print(f"  Frequency content: {freq_content}")

    # Find the frequency with the maximum amplitude within the specified range and above the threshold
    if min_freq_bin < max_freq_bin:
        valid_freq_content = freq_content[min_freq_bin:max_freq_bin]
        valid_freq_indices = np.where(valid_freq_content > amplitude_threshold)[0]

        if len(valid_freq_indices) > 0:
            max_freq_index = np.argmax(valid_freq_content[valid_freq_indices])
            max_freq_hz = (max_freq_index + min_freq_bin + valid_freq_indices[0]) * (sr / 2) / len(
                power_spectrogram[0])

            # Check if the frequency is within the specified range
            if min_freq <= max_freq_hz <= max_freq:
                print(f"  Dominant frequency: {max_freq_hz:.2f} Hz")
            else:
                print(f"  No valid frequency found in the specified range")
        else:
            print(f"  No valid frequency above the amplitude threshold")
    else:
        print(f"  Invalid frequency range")
    print()
