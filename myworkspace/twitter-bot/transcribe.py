#!/usr/bin/env python3
import whisper
import sys

model = whisper.load_model("base")
audio_file = sys.argv[1] if len(sys.argv) > 1 else "scripts/2026-02-01/voiceover.mp3"
result = model.transcribe(audio_file, language="zh")

output_file = audio_file.replace(".mp3", "_transcription.txt")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(result["text"])

print(f"✓ Transcription saved to: {output_file}")
print(f"\n{result['text']}")
