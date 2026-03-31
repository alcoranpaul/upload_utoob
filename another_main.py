import os
import time
import subprocess
import yt_dlp


def download_full_video(video_url, start_time=None, end_time=None):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'mp4',
        'quiet': False,
        'noplaylist': True,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'sleep_interval': 3,     # Be polite to servers
        'max_sleep_interval': 10
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("📥 Fetching video metadata...")
            video_info = ydl.extract_info(video_url, download=False)
            original_title = video_info['title']
            original_ext = video_info.get('ext', 'mp4')
            original_file = os.path.join(
                output_dir, f"{original_title}.{original_ext}")
            trimmed_file = os.path.join(
                output_dir, f"{original_title}_trimmed.mp4")

            print(f"🎥 Downloading full video: {original_title}")
            ydl.download([video_url])

            if start_time and end_time:
                print(f"✂️ Cutting video from {start_time} to {end_time}")
                cmd = [
                    'ffmpeg',
                    '-i', original_file,
                    '-ss', start_time,
                    '-to', end_time,
                    '-c:v', 'libx264',
                    '-preset', 'fast',
                    '-crf', '23',
                    '-c:a', 'aac',
                    '-strict', 'experimental',
                    trimmed_file
                ]
                subprocess.run(cmd, check=True)

                print(f"✅ Trimmed video saved as '{trimmed_file}'")
                return trimmed_file
            else:
                print(f"✅ Full video saved as '{original_file}'")
                return original_file

    except yt_dlp.utils.DownloadError as e:
        print("🚫 YouTube blocked the request:", str(e))
        print("💡 Try again later or use a different network.")
    except Exception as e:
        print("❌ Unexpected error:", str(e))


def download_audio_only(video_url, output_format='mp3', start_time=None, end_time=None):
    """
    Downloads only the audio from a video URL.
    """
    import os
    import subprocess
    import yt_dlp

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,
        'noplaylist': True,
        'restrictfilenames': True,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'sleep_interval': 3,
        'max_sleep_interval': 10
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("🎵 Downloading audio...")
            info = ydl.extract_info(video_url, download=True)

            # ✅ Get the actual filename after download
            original_file = ydl.prepare_filename(info)
            converted_file = os.path.splitext(
                original_file)[0] + f".{output_format}"

            if start_time and end_time:
                print(f"✂️ Trimming audio from {start_time} to {end_time}")
                if output_format == 'mp3':
                    cmd = [
                        'ffmpeg',
                        '-i', original_file,
                        '-ss', start_time,
                        '-to', end_time,
                        '-vn',
                        '-ar', '44100',
                        '-ac', '2',
                        '-b:a', '192k',
                        '-f', 'mp3',
                        converted_file
                    ]
                elif output_format == 'm4a':
                    cmd = [
                        'ffmpeg',
                        '-i', original_file,
                        '-ss', start_time,
                        '-to', end_time,
                        '-vn',
                        '-c:a', 'aac',
                        converted_file
                    ]
                else:
                    raise ValueError(
                        f"Unsupported output format: {output_format}")

                subprocess.run(cmd, check=True)
                os.remove(original_file)
                print(f"✅ Trimmed audio saved as: {converted_file}")
                return converted_file

            else:
                print(f"🔁 Converting full audio to {output_format}")
                if output_format == 'mp3':
                    subprocess.run([
                        'ffmpeg',
                        '-i', original_file,
                        '-vn',
                        '-ar', '44100',
                        '-ac', '2',
                        '-b:a', '192k',
                        converted_file
                    ], check=True)
                elif output_format == 'm4a':
                    subprocess.run([
                        'ffmpeg',
                        '-i', original_file,
                        '-vn',
                        '-c:a', 'aac',
                        converted_file
                    ], check=True)

                os.remove(original_file)
                print(f"✅ Converted audio saved as: {converted_file}")
                return converted_file

    except yt_dlp.utils.DownloadError as e:
        print("🚫 YouTube blocked the request:", str(e))
        print("💡 Try again later or use a different network.")
    except Exception as e:
        print("❌ Unexpected error:", str(e))


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=L4b-0HNOvyM&list=PLjccYdhdEbCioB6G5PBEX8eVb2i-i8q47&index=39"
    # start_time = "01:37:30"
    # end_time = "01:37:48"

    # print("🔗 Downloading and trimming video...")
    result = download_full_video(video_url)
