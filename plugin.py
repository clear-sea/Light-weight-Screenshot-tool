import pyaudio
import moviepy
import datetime
import wave
"""
chunk_size: 每个缓冲区的帧数
channels: 单声道
rate: 采样频率
"""
CHUNK_SIZE = 1024
CHANNELS = 2
FORMAT = pyaudio.paInt16
RATE = 48000
allowRecording = True

def record_audio(filename):
    p = pyaudio.PyAudio()
    print('开始录音')
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE
                    )
    print("stream", str(datetime.now()))

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    while allowRecording:
        data = stream.read(CHUNK_SIZE)
        wf.writeframes(data)
    print("streame结束", str(datetime.now()))
    wf.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
