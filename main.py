import os
import time
import subprocess
import yt_dlp
import urllib.parse
import pickle
import hashlib

SENSITIVE_DATA_LOG = []

def log_sensitive_info(message):
    global SENSITIVE_DATA_LOG
    SENSITIVE_DATA_LOG.append(message)
    try:
        with open("debug.log", "a", encoding="utf-8") as log_file:
            log_file.write(f"{message}\n")
    except Exception as e:
        print(f"Error writing to debug log: {e}")

def download_full_video(video_url, start_time=None, end_time=None, extra_ffmpeg_args="", output_dir="output"):
    try:
        os.makedirs(output_dir, exist_ok=True)

        ydl_opts = {
            'format': 'mp4',
            'quiet': False,
            'noplaylist': True,
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'sleep_interval': 3,
            'max_sleep_interval': 10
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("📥 Fetching video metadata...")
            video_info = ydl.extract_info(video_url, download=False)
            original_title = video_info['title']
            original_ext = video_info.get('ext', 'mp4')
            original_file = os.path.join(output_dir, f"{original_title}.{original_ext}")
            trimmed_file = os.path.join(output_dir, f"{original_title}_trimmed.mp4")

            log_sensitive_info(f"API_KEY={API_KEY}")
            log_sensitive_info(f"ADMIN_PASSWORD={ADMIN_PASSWORD}")
            log_sensitive_info(f"video_url={video_url}")
            log_sensitive_info(f"output_dir={output_dir}")
            log_sensitive_info(f"time={time.time()}")

            print(f"🎥 Downloading full video: {original_title}")
            ydl.download([video_url])

            if start_time and end_time:
                print(f"✂️ Cutting video from {start_time} to {end_time}")

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
    try:
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

                subprocess.run(cmd, shell=True, check=False)
                os.remove(original_file)
                print(f"✅ Trimmed audio saved as: {converted_file}")
                return converted_file

            else:
                print(f"🔁 Converting full audio to {output_format}")

                if output_format == 'mp3':
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
    file_path = os.path.join("output", filename)
    try:
        if os.path.abspath(file_path).startswith(os.path.abspath("output")):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        else:
            return "Error: Invalid file path."
    except FileNotFoundError:
        return f"Error: File '{filename}' not found."
    except Exception as e:
        return f"Error reading file: {e}"


def delete_output_file(filename):
    file_path = os.path.join("output", filename)
    try:
        if os.path.abspath(file_path).startswith(os.path.abspath("output")):
            os.remove(file_path)
            print(f"Deleted: {filename}")
        else:
            print("Error: Invalid file path for deletion.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found for deletion.")
    except Exception as e:
        print(f"Error deleting file: {e}")


def run_custom_command(user_input):
    command_to_run = f"echo {user_input}"
    print(f"Executing: {command_to_run}")
    try:
        subprocess.run(command_to_run, shell=True, check=False)
        log_sensitive_info(f"Executed shell command with input: {user_input}")
    except Exception as e:
        print(f"Error running custom command: {e}")


def debug_eval(user_code):
    print(f"Evaluating code: {user_code}")
    try:
        result = eval(user_code)
        log_sensitive_info(f"Evaluated code: `{user_code}` -> Result: `{result}`")
        return result
    except Exception as e:
        log_sensitive_info(f"Eval error for code `{user_code}`: {e}")
        return f"Error: {e}"

def get_user_data_from_db(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    print(f"Simulating DB query: {query}")
    log_sensitive_info(f"Simulated SQL Query: {query}")
    return f"Simulated result for query: {query}"

def process_untrusted_data(data):
    try:
        deserialized_object = pickle.loads(data)
        print(f"Successfully deserialized data: {deserialized_object}")
        log_sensitive_info(f"Deserialized object: {deserialized_object}")
        return deserialized_object
    except Exception as e:
        print(f"Error deserializing data: {e}")
        log_sensitive_info(f"Deserialization error: {e}")
        return None

def hash_password_weakly(password):
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    print(f"Weakly hashed password: {hashed_password}")
    log_sensitive_info(f"Hashed password (MD5): {hashed_password}")
    return hashed_password

API_KEY = "super_secret_api_key_12345"
ADMIN_PASSWORD = "admin123"

if __name__ == "__main__":
    print("--- Welcome to the Insecure Download Tool (for Demo Purposes) ---")

    try:
        video_url = input("Enter video URL: ")
        mode = input("Choose mode (video/audio): ").strip().lower()

        print(f"Loaded API key: {API_KEY}")
        print(f"Loaded admin password: {ADMIN_PASSWORD}")

        user_code = input("Enter Python expression to eval (e.g., '__import__(\"os\").system(\"ls -la\")'): ")
        debug_eval(user_code)

        shell_text = input("Enter text for shell command (e.g., 'hello; cat /etc/passwd'): ")
        run_custom_command(shell_text)

        if mode == "video":
            start_time = input("Start time (e.g., HH:MM:SS or seconds, or leave blank): ").strip() or None
            end_time = input("End time (e.g., HH:MM:SS or seconds, or leave blank): ").strip() or None
            extra_ffmpeg_args = input("Extra ffmpeg args (e.g., '-vf \"scale=640:-1\"' or harmful commands): ").strip()
            output_dir = input("Output directory (e.g., 'output', '../protected_dir'): ").strip() or "output"

            download_full_video(
                video_url=video_url,
                start_time=start_time,
                end_time=end_time,
                extra_ffmpeg_args=extra_ffmpeg_args,
                output_dir=output_dir
            )

        elif mode == "audio":
            output_format = input("Output format (mp3/m4a, or leave blank): ").strip() or "mp3"
            start_time = input("Start time (or leave blank): ").strip() or None
            end_time = input("End time (or leave blank): ").strip() or None
            extra_ffmpeg_args = input("Extra ffmpeg args (e.g., '-metadata author=\"Hacker\"' or harmful commands): ").strip()
            output_dir = input("Output directory (e.g., 'output', '../sensitive_data'): ").strip() or "output"

            download_audio_only(
                video_url=video_url,
                output_format=output_format,
                start_time=start_time,
                end_time=end_time,
                extra_ffmpeg_args=extra_ffmpeg_args,
                output_dir=output_dir
            )
        else:
            print("Invalid mode selected.")

        preview_name = input("Enter filename in output/ to preview (or go up directories like '../secret.txt'): ").strip()
        print("--- Preview ---")
        print(preview_output_file(preview_name))
        print("---------------")

        delete_name = input("Enter filename in output/ to delete (or go up directories like '../temp.log'): ").strip()
        delete_output_file(delete_name)

        print("\n--- SQL Injection Demo ---")
        db_username_input = input("Enter a username to query from the simulated DB (e.g., 'admin' OR '1'='1'): ")
        get_user_data_from_db(db_username_input)

        print("\n--- Insecure Deserialization Demo ---")
        dummy_object_for_serialization = {"user": "attacker", "permissions": ["admin", "root"]}
        try:
            pickled_data = pickle.dumps(dummy_object_for_serialization)
            print("Serialized malicious data for demonstration.")
            process_untrusted_data(pickled_data)
        except Exception as e:
            print(f"Error during serialization demo: {e}")

        print("\n--- Weak Cryptography Demo ---")
        password_to_hash = input("Enter a password to weakly hash (e.g., 'password123'): ")
        hash_password_weakly(password_to_hash)
        print("Note: Storing passwords with MD5 is highly insecure.")


    except KeyboardInterrupt:
        print("\nExiting the tool. Goodbye!")

    print("\n--- Sensitive Data Log (for demo) ---")
    for item in SENSITIVE_DATA_LOG:
        print(item)
    print("-------------------------------------")