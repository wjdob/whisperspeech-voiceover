import os
import re
from pydub import AudioSegment
import numpy as np
from whisperspeech.pipeline import Pipeline
import torch

# Ensure CUDA is available
if not torch.cuda.is_available():
    print("CUDA is not available. The process will use the CPU.")
else:
    print("CUDA is available. The process will use the GPU for faster performance.")

# Initialize the WhisperSpeech pipeline with specified models
pipe = Pipeline(
    t2s_ref='whisperspeech/whisperspeech:t2s-v1.95-small-8lang.model',
    s2a_ref='whisperspeech/whisperspeech:s2a-v1.95-medium-7lang.model'
)

# Function to chunk text into parts, ending at sentence boundaries
def chunk_text(text, max_length=300):
    # Split the text into sentences based on common sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Check if adding the next sentence exceeds the max length
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence + " "
        else:
            # Add the current chunk to the list and start a new chunk
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    # Append any remaining text as the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# Function to generate and save audio from text files with chunking for long inputs
def generate_and_save_audio_from_files(text_files, lang_prefix, cps):
    output_dir = os.path.join(os.getcwd(), 'speech_output')
    os.makedirs(output_dir, exist_ok=True)

    # Define a silent audio segment to be inserted between chunks (e.g., 500 milliseconds)
    gap_duration_ms = 500  # Duration of the gap in milliseconds
    silent_segment = AudioSegment.silent(duration=gap_duration_ms)

    for text_file in text_files:
        with open(text_file, 'r', encoding='utf-8') as file:
            user_input = file.read()

        # Split the input text into sentence-aware chunks
        text_chunks = chunk_text(user_input)
        input_filename = os.path.splitext(os.path.basename(text_file))[0]
        output_filename = os.path.join(output_dir, f"{input_filename}_speech.wav")

        print(f"Generating audio for '{text_file}' in {len(text_chunks)} chunks...")

        # Concatenate all audio segments
        combined_audio = AudioSegment.empty()

        for i, chunk in enumerate(text_chunks):
            print(f"Generating chunk {i + 1}/{len(text_chunks)}...")
            try:
                audio_tensor = pipe.generate(chunk, cps=cps, lang=lang_prefix)
                audio_np = (audio_tensor.cpu().numpy() * 32767).astype(np.int16)

                if len(audio_np.shape) == 1:
                    audio_np = np.expand_dims(audio_np, axis=0)
                else:
                    audio_np = audio_np.T

                # Convert to an AudioSegment
                audio_segment = AudioSegment(
                    audio_np.tobytes(),
                    frame_rate=24000,  # Adjust sample rate if needed
                    sample_width=2,
                    channels=1
                )

                # Append the audio segment
                combined_audio += audio_segment

                # Add the silent gap between chunks, except after the last chunk
                if i < len(text_chunks) - 1:
                    combined_audio += silent_segment

            except Exception as e:
                print(f"Error during audio generation for chunk {i + 1}: {e}")

        # Export combined audio to the output file
        combined_audio.export(output_filename, format='wav')
        print(f"Audio file generated: {output_filename}")

# Main function to run the script logic
def main():
    scan_choice = input("Would you like to scan the current directory and 'input' folder for text files? (yes/no): ").strip().lower()

    if scan_choice == 'yes':
        text_files = scan_for_text_files()
        if text_files:
            print(f"Found {len(text_files)} text file(s).")

            # Prompt for language and CPS
            lang_prefix = input("Enter the language prefix (e.g., 'en' for English, 'pl' for Polish): ")
            cps_value = input("Enter the CPS (characters per second) value (e.g., 15): ")

            # Convert CPS input to an integer
            try:
                cps = int(cps_value)
            except ValueError:
                print("Invalid CPS value. Please enter a number.")
                return

            # Generate and save audio for each text file
            generate_and_save_audio_from_files(text_files, lang_prefix, cps)
        else:
            print("No text files found in the current directory or 'input' folder.")
    else:
        print("Exiting program.")

# Function to scan for text files in the current directory and 'input' folder
def scan_for_text_files():
    text_files = []
    search_dirs = [os.getcwd(), os.path.join(os.getcwd(), 'input')]

    for directory in search_dirs:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                if file.endswith('.txt'):
                    full_path = os.path.join(directory, file)
                    text_files.append(full_path)

    return text_files

# Run the main function
if __name__ == "__main__":
    main()