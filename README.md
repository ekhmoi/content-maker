# content-maker

```sh
pip3 install -r requirements.txt
```


```sh
python3 main.py convert -i <input-file-path> -o <output-folder> -k <OPEN_AI_API_KEY>
```


```sh
python3 main.py convert -i test-3.wav -o ../output -k <OPEN_AI_API_KEY>
```



In Output folder you will have
- input.wav
- audio_transcriber_result.txt
- transcription_analyzer_result.txt
- script_generator_result.txt
- image_describer_result.txt
- image_generator_result.txt