# content-maker

## Install dependencies

```sh
pip3 install -r requirements.txt
```

## Run script

```sh
python3 main.py convert -i <input-file-path> -s <execution-step> -o <output-folder> -k <OPEN_AI_API_KEY>
```


```sh
python3 main.py convert -i input.txt -s 3 -o ../output -k <OPEN_AI_API_KEY>
```
> example usages starting from step 3


```sh
python3 main.py convert -i input.wav -o ../output -k <OPEN_AI_API_KEY>
```
> example usages starting from step 0


## Arguments

| Arg | Default |  Description |
| --- | --- | --- |
| -i | - | Path to input file |
| -s | 0 | Step from which to start the process. It is important to provide the correct input for the next step. |
| -o | - | Path to output folder |
| -k | -| OpenAI API Key |


## Result
In Output folder you will have the following files (depending on the execution step):

| File                              | Description                       |
| --------------------------------- | --------------------------------- |
| input.wav                         | Converted audio file      |
| audio_transcriber_result.txt      | Result of the transcribed audio |
| transcription_analyzer_result.txt | Analysis of the text      |
| script_generator_result.txt       | Result for the script       |
| image_describer_result.txt        | Image generation prompts        |
