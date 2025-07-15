
from elevenlabs import Voice, VoiceSettings
from elevenlabs import save
from elevenlabs.client import ElevenLabs

import var.config as config

# Создаем клиент с использованием нового API
client = ElevenLabs(api_key=config.elevenlabs_api_key)

# audio_filename = "audio.mp3"

# Получение всех доступных голосов
def get_all_voices():
    voices_response = client.voices.get_all()
    voices_list = getattr(voices_response, 'voices', [])
    return voices_list
    #return [{'name': [voice.name](http://voice.name/), 'id': voice.voice_id} for voice in voices_response.voices]

# Генерация аудиофайла из текста и голоса
def generate_audio_file(text, voice_id, filename="output.mp3", output_format="mp3_44100_128"):
    audio_response = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        output_format=output_format
    )
    with open(filename, "wb") as f:
        for chunk in audio_response:
            f.write(chunk)
    return filename
    # audio = client.generate(
    #    text=text,
    #    voice=Voice(
    #        voice_id=voice_id,
    #        settings=VoiceSettings(stability=0.75, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
    #    ),
    #    model="eleven_multilingual_v2"
    #
    # save(audio_response, filename)