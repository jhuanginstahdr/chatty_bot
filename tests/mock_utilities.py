from numpy import random, int16
from speech_recognition import AudioSource, AudioFile
from pydub import AudioSegment
from io import BytesIO

def mock_audio_file_as_source() -> AudioSource:

    # Sample audio data (replace this with your actual audio data)
    # For example, you might have a NumPy array from reading an audio file
    # This is a placeholder, replace with your actual audio data
    audio_data_numpy = random.randint(-32768, 32767, size=(44100,))  # Sample audio data for 1 second at 44100 Hz

    # Convert the NumPy array to bytes
    audio_bytes = audio_data_numpy.astype(int16).tobytes()

    # Create an AudioSegment from the bytes
    audio_segment = AudioSegment(
        audio_bytes,
        frame_rate=44100,  # Adjust frame rate as needed
        sample_width=2,  # Adjust sample width as needed
        channels=1  # Adjust number of channels as needed (1 for mono, 2 for stereo)
    )

    # Save the AudioSegment to a temporary file-like object (in-memory file)
    in_memory_file = BytesIO()
    audio_segment.export(in_memory_file, format="wav")
    in_memory_file.seek(0)  # Reset the file pointer to the beginning

    # Create an AudioFile object using the in-memory file
    return AudioFile(in_memory_file)