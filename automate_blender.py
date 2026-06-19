import os
import sys
import subprocess
import shutil

BLENDER_SCRIPT = os.path.join(os.path.dirname(__file__), 'BLENDER_FIX_ALL_FACE_PROBLEMS.py')
DEFAULT_BLENDER_PATHS = [
    r'C:\Program Files\Blender Foundation\Blender\blender.exe',
    r'C:\Program Files (x86)\Blender Foundation\Blender\blender.exe',
]


def find_blender_executable():
    for path in DEFAULT_BLENDER_PATHS:
        if os.path.exists(path):
            return path

    blender_path = shutil.which('blender')
    if blender_path:
        return blender_path

    env_path = os.environ.get('BLENDER_PATH')
    if env_path and os.path.exists(env_path):
        return env_path

    return None


def run_blender_script(blender_exe, script_path):
    print(f'[*] Launching Blender: {blender_exe}')
    print(f'[*] Running script: {script_path}')

    result = subprocess.run([
        blender_exe,
        '--background',
        '--python',
        script_path,
    ], capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print('=== Blender STDERR ===')
        print(result.stderr)

    return result.returncode


def main():
    if not os.path.exists(BLENDER_SCRIPT):
        print(f'ERROR: Blender script not found: {BLENDER_SCRIPT}')
        sys.exit(1)

    blender_exe = find_blender_executable()
    if not blender_exe:
        print('ERROR: Blender executable not found.')
        print('Please install Blender or set BLENDER_PATH to the blender.exe location.')
        sys.exit(1)

    exit_code = run_blender_script(blender_exe, BLENDER_SCRIPT)
    if exit_code == 0:
        print('\n✅ Blender automation completed successfully.')
    else:
        print(f'\nERROR: Blender exited with code {exit_code}.')
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
