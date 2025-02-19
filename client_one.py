from streaming_app import StreamingApp


PORTS = {
    "server": 7777,
    "audio_receiver": 6666,
    "camera_stream": 9999,
    "screen_stream": 9999,
    "audio_stream": 8888
}


if __name__ == "__main__":
    app = StreamingApp(
        PORTS["server"], PORTS["audio_receiver"], PORTS["camera_stream"], PORTS["screen_stream"], PORTS["audio_stream"]
    )
    app.run()
