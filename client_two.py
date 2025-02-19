from streaming_app import StreamingApp

PORTS = {
    "server": 9999,
    "audio_receiver": 8888,
    "camera_stream": 7777,
    "screen_stream": 7777,
    "audio_stream": 6666
}

if __name__ == "__main__":
    app = StreamingApp(
        PORTS["server"], PORTS["audio_receiver"], PORTS["camera_stream"], PORTS["screen_stream"], PORTS["audio_stream"]
    )
    app.run()