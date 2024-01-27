# Import the necessary libraries
import whisper

from src.steps.base_step import BaseStep

class AudioTranscriber(BaseStep):
    def __init__(self, *args):
        super().__init__('audio_transcriber', *args)
        self.model = whisper.load_model("base")
    
    def execute(self, wav_path: str):
        self.log('2 - Starting audio transcription...')
        response = self.model.transcribe(wav_path, fp16=False)
        result_path = self.get_path('audio_transcriber_result.txt')
        self.save_result(result_path, response['text'])

        self.log(f'2 - Audio transcription complete - Result is saved to: {result_path}')
        # Transcribe the audio file
        return response['text']
    