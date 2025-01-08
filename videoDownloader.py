import yt_dlp
import subprocess
import os

def download_youtube_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mkv',  # Geçici olarak MKV formatında birleştir
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            video_ext = info_dict.get('ext', None)
            input_file = f"{video_title}.{video_ext}"
            output_file = f"{video_title}.mp4"

            # FFmpeg ile H.264 ve AAC codec'lerine dönüştür
            subprocess.run([
                'ffmpeg', '-i', input_file, '-c:v', 'libx264', '-c:a', 'aac',
                '-strict', 'experimental', '-b:a', '192k', output_file
            ])

            # MKV dosyasını sil
            os.remove(input_file)

            print("Video başarıyla indirildi, dönüştürüldü ve MKV dosyası silindi.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Kullanıcıdan YouTube videosunun URL'sini al
video_url = input("Lütfen indirmek istediğiniz YouTube videosunun URL'sini girin: ")
download_youtube_video(video_url) 