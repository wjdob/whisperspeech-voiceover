# whisperspeech-voiceover
Automated Text-to-Speech Conversion Script using WhisperSpeech

# Text-to-Speech Conversion Script with WhisperSpeech

## Overview
This Python script automates the process of converting text files into audio files using the WhisperSpeech text-to-speech model. It scans the current directory and an optional `input` folder for `.txt` files, processes each file to create corresponding audio files, and saves the output in a designated `speech_output` folder.
Optionally, user can simply enter the text to be converted into speech when prompted.
The original purpose of this project was to automate the generation of voiceovers for use in educational materials and learning resources.

## Features
- **Directory Scanning**: Automatically scans the current directory and an optional `input` folder for `.txt` files to convert.
- **Custom Speech Parameters**: Prompts for language prefix and CPS (characters per second) to customize the speech rate and style.
- **Seamless Audio**: Splits long texts into chunks that end at sentence boundaries, ensuring smooth transitions and a natural flow.
- **Automatic Pauses Between Chunks**: Adds customizable silent gaps between chunks for better listening continuity.
- **Automated Output Management**: Generates separate audio files for each text file in the `speech_output` folder.

## Requirements
- **Python 3.7+**
- **WhisperSpeech**: Install via `pip install whisperspeech`
- **pydub**: For handling audio file creation. Install via `pip install pydub`
- **FFmpeg**: Required by `pydub` for exporting `.wav` files. [Install FFmpeg](https://ffmpeg.org/download.html) and add it to your system PATH.
- **CUDA**: A GPU with CUDA, and CUDA libraries and dev toolkit installed. Generating speech is resource-intensive. When using CUDA, a 30 second long speech generation takes about 10-15 minutes using GTX 1660 Ti.

## Usage
1. **Run the Script**: Execute the script by running:
   ```bash
   python generate_voiceovers.py

2. **Input Prompts**: The script will prompt you to:

    Specify whether to scan directories (main directory and input folder) for .txt files.
    ```bash
    Would you like to scan the current directory and 'input' folder for text files? (yes/no): yes
    Found 8 text file(s).
    ```
    Enter the language prefix (e.g., en for English, pl for Polish).
    ```bash
    Enter the language prefix (e.g., 'en' for English, 'pl' for Polish): en
    ```
    Enter the CPS (characters per second) to control the speech rate.
    ```bash
    Enter the CPS (characters per second) value (e.g., 15): 15
    ```

4. **Output**: The script will generate .wav audio files in the speech_output folder, with filenames based on the original text filenames. The output filenames will have "_speech" appended at the end of the filename.

### Limitations
WhisperSpeech currently supports only 30-second-long chunks. When multiple chunks are combined, the speech may not always sound fully continuous or maintain consistent tone and pitch.

Some possible workarounds include:
- Logically separate voiceover text inputs into distinct topics or sections, each under 30 seconds long.
- Increase the silence gap between chunks, or consider randomizing the gap to create a more natural pause.

## License
This project is licensed under the MIT License.

## Acknowledgments
**WhisperSpeech**: For the text-to-speech model.\
**pydub and FFmpeg**: For audio file handling and export.\
**User BBC-Esq**: For solving the challenge of outputting Whisperspeech audio to a .wav file - [Github original post](https://github.com/collabora/WhisperSpeech/issues/67#issuecomment-1917716701)
