from src.steps.base_step import BaseStep

class AudioTranscriber(BaseStep):
    def __init__(self, *args):
        super().__init__('AudioTranscriber', *args)
    
    def execute(self, wav_path: str):
        self.log('2 - Starting audio transcription...')
        response = self.openai.audio.transcriptions.create(
            file=open(wav_path, 'rb'),
            model="whisper-1"
        )
        result_path = self.get_path('audio_transcriber_result.txt')
        self.save_result(result_path, response.text)

        self.log(f'2 - Audio transcription complete - Result is saved to: {result_path}')

        return response.text
    