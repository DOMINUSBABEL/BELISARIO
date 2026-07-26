# -*- coding: utf-8 -*-
"""
BELISARIO AUDIOVISUAL QA AUDITOR (subagent_belisario_auditor)
Agente de Auditoría de Calidad Audiovisual y Re-renderizado Autónomo (BABYLON.IA)
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"

class AudiovisualQAAuditor:
    def __init__(self, target_dir=PROJECT_DIR):
        self.target_dir = target_dir
        self.min_short_size_bytes = 500 * 1024  # Min 500KB for Shorts
        self.min_essay_size_bytes = 2 * 1024 * 1024 # Min 2MB for Essays

    def log(self, msg, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [BELISARIO-AUDITOR] [{level}] {msg}")

    def inspect_media_properties(self, filepath):
        """Uses ffprobe to extract exact video/audio stream properties."""
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format", "-show_streams",
            filepath
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return json.loads(res.stdout)
        except Exception as e:
            self.log(f"ffprobe failed for {filepath}: {e}", level="ERROR")
            return None

    def audit_video_file(self, filename):
        filepath = os.path.join(self.target_dir, filename)
        self.log(f"Auditing deliverable: {filename}")
        
        if not os.path.exists(filepath):
            self.log(f"FAIL: File does not exist -> {filename}", level="ERROR")
            return False, "File Missing", 0

        file_size = os.path.getsize(filepath)
        is_short = "short" in filename.lower()
        min_size = self.min_short_size_bytes if is_short else self.min_essay_size_bytes

        if file_size < min_size:
            self.log(f"FAIL: Under-sized media file ({file_size} bytes < {min_size}) -> {filename}", level="WARNING")
            return False, "Corrupted/Undersized Render", 20

        props = self.inspect_media_properties(filepath)
        if not props:
            return False, "Invalid Container Structure", 0

        # Check Streams
        streams = props.get("streams", [])
        has_video = any(s.get("codec_type") == "video" for s in streams)
        has_audio = any(s.get("codec_type") == "audio" for s in streams)

        if not has_video or not has_audio:
            self.log(f"FAIL: Missing streams (video: {has_video}, audio: {has_audio}) -> {filename}", level="ERROR")
            return False, "Missing Audio or Video Stream", 30

        # Extract Resolution
        v_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
        width = v_stream.get("width", 0)
        height = v_stream.get("height", 0)

        # Check Aspect Ratio Standards
        if is_short and (width != 1080 or height != 1920):
            self.log(f"WARNING: Short resolution is {width}x{height}, expected 1080x1920 -> {filename}", level="WARNING")
            return False, "Non-standard Short Aspect Ratio", 60
        elif not is_short and (width != 1920 or height != 1080):
            self.log(f"WARNING: Essay resolution is {width}x{height}, expected 1920x1080 -> {filename}", level="WARNING")
            return False, "Non-standard Essay Aspect Ratio", 60

        duration = float(props.get("format", {}).get("duration", 0))
        self.log(f"PASS: {filename} [{width}x{height} | {duration:.1f}s | {file_size/1024/1024:.2f}MB] - Quality Score: 95/100")
        return True, "Passed High Quality Standard", 95

    def auto_remake_video(self, filename, reason):
        """Triggers KINESIO to automatically re-compile and remake low-quality or failed video deliverables."""
        self.log(f"AUTOMATIC REMAKE TRIGGERED for {filename}. Reason: {reason}", level="ACTION")
        
        # Invoke compile_all_campaigns using current Python executable
        cmd = [sys.executable, "compile_all_campaigns.py"]
        try:
            subprocess.run(cmd, cwd=self.target_dir, check=True)
            self.log(f"SUCCESS: Remake pipeline finished for {filename}")
            return True
        except Exception as e:
            self.log(f"ERROR: Failed to remake {filename}: {e}", level="ERROR")
            return False

    def run_full_audit(self):
        self.log("==================================================")
        self.log("  BELISARIO-AUDITOR: INICIANDO AUDITORÍA GLOBAL   ")
        self.log("==================================================")
        
        target_files = [f for f in os.listdir(self.target_dir) if f.endswith("_final.mp4")]
        if not target_files:
            self.log("No compiled video deliverables found for audit.", level="WARNING")
            return
            
        passed_count = 0
        remake_count = 0
        
        for fname in target_files:
            passed, reason, score = self.audit_video_file(fname)
            if passed:
                passed_count += 1
            else:
                remake_success = self.auto_remake_video(fname, reason)
                if remake_success:
                    remake_count += 1

        self.log("==================================================")
        self.log(f"AUDITORÍA FINALIZADA: {passed_count}/{len(target_files)} aprobados. {remake_count} re-hachados autónomamente.")
        self.log("==================================================")

def main():
    auditor = AudiovisualQAAuditor()
    auditor.run_full_audit()

if __name__ == "__main__":
    main()
