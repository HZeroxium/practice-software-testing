from pydub import AudioSegment
import math  # Thêm dòng này


def increase_volume(input_file: str, output_file: str, multiplier: float):
    """
    Tăng âm lượng file .wav theo hệ số multiplier.
    """
    # Đọc file âm thanh
    audio = AudioSegment.from_wav(input_file)

    # Tính số dB cần tăng
    if multiplier <= 0:
        raise ValueError("Multiplier must be > 0.")

    gain_db = 10 * math.log10(multiplier)  # Sửa chỗ này

    # Tăng âm lượng
    louder_audio = audio + gain_db

    # Ghi ra file mới
    louder_audio.export(output_file, format="wav")
    print(f"✅ File đã được tăng âm lượng ({gain_db:.2f} dB): {output_file}")


def convert_wav_to_mp3(input_wav: str, output_mp3: str, bitrate: str = "192k"):
    """
    Chuyển đổi file WAV sang MP3.

    Args:
        input_wav (str): Đường dẫn file .wav đầu vào
        output_mp3 (str): Đường dẫn file .mp3 đầu ra
        bitrate (str): Tùy chọn bitrate (ví dụ: "128k", "192k", "320k")
    """
    audio = AudioSegment.from_wav(input_wav)
    audio.export(output_mp3, format="mp3", bitrate=bitrate)
    print(f"🎵 Đã chuyển {input_wav} sang {output_mp3} với bitrate {bitrate}")


# Gọi thử
# increase_volume("input.wav", "output_louder.wav", multiplier=10.0)
convert_wav_to_mp3("output_louder.wav", "output_louder.mp3", bitrate="192k")
