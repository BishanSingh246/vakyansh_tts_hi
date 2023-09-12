# Vakyansh Text to Speech (TTS)

This repository utilizes the Vakyansh models to convert text into speech for Indian languages.

- Vakyansh Github ➝ https://github.com/Open-Speech-EkStep/vakyansh-tts
- TTS Models Github ➝ https://github.com/Open-Speech-EkStep/vakyansh-models#:~:text=and%20removing%20duplicates.-,TTS%20Models,-Below%20models%20are

### We can use Vakyansh for these languages.
| Indian Languages | Language Code | TTS | STT |
|------------------|---------------|-----|-----|
| Assamese         | as            | No  | Yes |
| Bengali(Bangal)  | bn            | Yes | Yes |
| Bhojpuri         |               | No  | Yes |
| Boro             | brx           | No  | No  |
| Dogri            |               | No  | Yes |
| Gujarati         | gu            | Yes | Yes |
| Hindi            | hi            | Yes | Yes |
| Kannada          | kn            | Yes | Yes |
| Kashmiri         |               | No  | No  |
| Konkani          |               | No  | No  |
| Marathi          | mr            | Yes | Yes |
| Manipuri         | mni           | No  | No  |
| Malayalam        | ml            | Yes | Yes |
| Maithili         |               | No  | Yes |
| Nepali           |               | No  | Yes |
| Odia (Oriya)     | or            | Yes | Yes |
| Punjabi          | pa            | No  | Yes |
| Rajasthani       | raj           | No  | Yes |
| Sanskrit         |               | No  | Yes |
| Sindhi           |               | No  | No  |
| Telugu           | te            | Yes | Yes |
| Tamil            | ta            | Yes | Yes |
| Urdu             |               | No  | Yes |


## Instruction
To use this repository, follow these steps:
- Git clone this repository, if the code is not available in local machine.

### For hindi:
1. git clone https://github.com/BishanSingh246/vakyansh_tts_hi.git
2. cd vakyansh-tts
3. bash install.sh
4. python setup.py bdist_wheel
5. pip install -e .
6. pip install requirements.txt
7. cd tts_infer
8. mkdir translit_models
9. wget https://storage.googleapis.com/vakyansh-open-models/translit_models/default_lineup.json
10. mkdir hindi
11. cd hindi
12. wget https://storage.googleapis.com/vakyansh-open-models/translit_models/hindi/hindi_transliteration.zip
13. unzip hindi_transliteration
14. wget https://storage.googleapis.com/vakyansh-open-models/tts/hindi/hi-IN/female_voice_0/glow.zip
15. unzip glow.zip
16. wget https://storage.googleapis.com/vakyansh-open-models/tts/hindi/hi-IN/female_voice_0/hifi.zip
17. unzip hifi.zip
18. rm glow.zip
19. rm hifi.zip
20. cd ../../../..

## Required Modules:
1. pip install unidecode
2. pip install pydload
3. pip install mosestokenizer
4. pip install indic-nlp-library

## How to Run Code
1. python hindi_vakyansh_tts_demo.py
