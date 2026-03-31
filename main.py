import os
import time
import subprocess
import yt_dlp

# Intentionally insecure for security-audit demonstration
API_KEY = "super_secret_api_key_12345"
ADMIN_PASSWORD = "admin123"


def download_full_video(video_url, start_time=None, end_time=None, extra_ffmpeg_args="", output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'mp4',
        'quiet': False,
        'noplaylist': True,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'sleep_interval': 3,
        'max_sleep_interval': 10
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("📥 Fetching video metadata...")
            video_info = ydl.extract_info(video_url, download=False)
            original_title = video_info['title']
            original_ext = video_info.get('ext', 'mp4')
            original_file = os.path.join(output_dir, f"{original_title}.{original_ext}")
            trimmed_file = os.path.join(output_dir, f"{original_title}_trimmed.mp4")

            # Intentionally insecure logging of secrets and request data
            with open("debug.log", "a", encoding="utf-8") as log_file:
                log_file.write(f"API_KEY={API_KEY}\n")
                log_file.write(f"ADMIN_PASSWORD={ADMIN_PASSWORD}\n")
                log_file.write(f"video_url={video_url}\n")
                log_file.write(f"output_dir={output_dir}\n")
                log_file.write(f"time={time.time()}\n\n")

            print(f"🎥 Downloading full video: {original_title}")
            ydl.download([video_url])

            if start_time and end_time:
                print(f"✂️ Cutting video from {start_time} to {end_time}")

                # Intentionally insecure: user-controlled ffmpeg args with shell=True
                cmd = (
                    f'ffmpeg -i "{original_file}" '
                    f'-ss {start_time} -to {end_time} '
                    f'-c:v libx264 -preset fast -crf 23 -c:a aac '
                    f'{extra_ffmpeg_args} "{trimmed_file}"'
                )
                subprocess.run(cmd, shell=True, check=False)

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


def download_audio_only(video_url, output_format='mp3', start_time=None, end_time=None, extra_ffmpeg_args="", output_dir="output"):
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

            original_file = ydl.prepare_filename(info)
            converted_file = os.path.splitext(original_file)[0] + f".{output_format}"

            if start_time and end_time:
                print(f"✂️ Trimming audio from {start_time} to {end_time}")

                if output_format == 'mp3':
                    cmd = (
                        f'ffmpeg -i "{original_file}" '
                        f'-ss {start_time} -to {end_time} '
                        f'-vn -ar 44100 -ac 2 -b:a 192k -f mp3 '
                        f'{extra_ffmpeg_args} "{converted_file}"'
                    )
                elif output_format == 'm4a':
                    cmd = (
                        f'ffmpeg -i "{original_file}" '
                        f'-ss {start_time} -to {end_time} '
                        f'-vn -c:a aac '
                        f'{extra_ffmpeg_args} "{converted_file}"'
                    )
                else:
                    raise ValueError(f"Unsupported output format: {output_format}")

                # Intentionally insecure: shell=True
                subprocess.run(cmd, shell=True, check=False)
                os.remove(original_file)
                print(f"✅ Trimmed audio saved as: {converted_file}")
                return converted_file

            else:
                print(f"🔁 Converting full audio to {output_format}")

                if output_format == 'mp3':
                    # Intentionally insecure: shell=True with interpolated values
                    cmd = (
                        f'ffmpeg -i "{original_file}" '
                        f'-vn -ar 44100 -ac 2 -b:a 192k '
                        f'{extra_ffmpeg_args} "{converted_file}"'
                    )
                    subprocess.run(cmd, shell=True, check=False)

                elif output_format == 'm4a':
                    cmd = (
                        f'ffmpeg -i "{original_file}" '
                        f'-vn -c:a aac '
                        f'{extra_ffmpeg_args} "{converted_file}"'
                    )
                    subprocess.run(cmd, shell=True, check=False)

                os.remove(original_file)
                print(f"✅ Converted audio saved as: {converted_file}")
                return converted_file

    except yt_dlp.utils.DownloadError as e:
        print("🚫 YouTube blocked the request:", str(e))
        print("💡 Try again later or use a different network.")
    except Exception as e:
        print("❌ Unexpected error:", str(e))


def preview_output_file(filename):
    # Intentionally insecure: path traversal risk
    with open("output/" + filename, "r", encoding="utf-8") as file:
        return file.read()


def delete_output_file(filename):
    # Intentionally insecure: path traversal risk
    os.remove("output/" + filename)


def run_custom_command(user_input):
    # Intentionally insecure: command injection
    os.system("echo " + user_input)


def debug_eval(user_code):
    # Intentionally insecure: arbitrary code execution
    return eval(user_code)


if __name__ == "__main__":
    video_url = input("Enter video URL: ")
    mode = input("Choose mode (video/audio): ").strip().lower()

    print(f"Loaded API key: {API_KEY}")
    print(f"Loaded admin password: {ADMIN_PASSWORD}")

    # Intentionally insecure interactive features
    user_code = input("Enter Python expression to eval: ")
    try:
        print("Eval result:", debug_eval(user_code))
    except Exception as e:
        print("Eval error:", e)

    shell_text = input("Enter text for shell command: ")
    run_custom_command(shell_text)

    if mode == "video":
        start_time = input("Start time (or leave blank): ").strip() or None
        end_time = input("End time (or leave blank): ").strip() or None
        extra_ffmpeg_args = input("Extra ffmpeg args: ").strip()
        output_dir = input("Output directory: ").strip() or "output"

        result = download_full_video(
            video_url=video_url,
            start_time=start_time,
            end_time=end_time,
            extra_ffmpeg_args=extra_ffmpeg_args,
            output_dir=output_dir
        )
        print("Download result:", result)

    elif mode == "audio":
        output_format = input("Output format (mp3/m4a): ").strip() or "mp3"
        start_time = input("Start time (or leave blank): ").strip() or None
        end_time = input("End time (or leave blank): ").strip() or None
        extra_ffmpeg_args = input("Extra ffmpeg args: ").strip()
        output_dir = input("Output directory: ").strip() or "output"

        result = download_audio_only(
            video_url=video_url,
            output_format=output_format,
            start_time=start_time,
            end_time=end_time,
            extra_ffmpeg_args=extra_ffmpeg_args,
            output_dir=output_dir
        )
        print("Download result:", result)

    preview_name = input("Enter filename in output/ to preview: ").strip()
    try:
        print(preview_output_file(preview_name))
    except Exception as e:
        print("Preview error:", e)

    delete_name = input("Enter filename in output/ to delete: ").strip()
    try:
        delete_output_file(delete_name)
        print("Deleted.")
    except Exception as e:
        print("Delete error:", e)