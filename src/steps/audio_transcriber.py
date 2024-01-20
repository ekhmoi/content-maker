from src.steps.base_step import BaseStep

class AudioTranscriber(BaseStep):
    def __init__(self, openai):
        super().__init__(openai, 'AudioTranscriber')
    
    def execute(self, wav_path: str):
        self.log('Starting audio transcription...')
        response = self.openai.audio.transcriptions.create(
            file=open(wav_path, 'rb'),
            model="whisper-1"
        )
        self.save_result(wav_path.rsplit('.', 1)[0] + '.wav' + '-transcription.txt', response.text)

        self.log('Audio transcription complete. Result is saved to' + wav_path.rsplit('.', 1)[0] + '.wav' + '-transcription.txt')
        return response.text
    