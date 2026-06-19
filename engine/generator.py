"""
JARVIS Generator Engine [UPGRADED]
Handles: Text, Image, Audio, Video, 3D Model, File generation
Uses: Gemini (text), Pollinations AI (image/video/3D - free, no key needed),
      edge-tts (audio), wave PCM synth (music/chiptune), local file creation
"""
import os
import time
import math
import struct
import wave
import urllib.request
import urllib.parse

DESKTOP = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
GEN_DIR = os.path.join(DESKTOP, "jarvis_generated")


def _ensure_gen_dir():
    os.makedirs(GEN_DIR, exist_ok=True)
    return GEN_DIR


# ── TEXT GENERATION ──────────────────────────────────────────────────────────
def generate_text(prompt: str, brain=None) -> str:
    """Generate text/code/story using JARVIS brain."""
    if brain and brain.is_connected:
        result = brain.think(f"Generate the following (respond with content only, no extra commentary):\n{prompt}")
        ts = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(_ensure_gen_dir(), f"text_{ts}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(result)
        return f"[TEXT GENERATED]\nSaved: {path}\n\nPreview:\n{result[:500]}..."
    return "[ERROR] Brain offline. Cannot generate text."


# ── IMAGE GENERATION ─────────────────────────────────────────────────────────
def generate_image(prompt: str, width: int = 1024, height: int = 1024, style: str = "none") -> str:
    """Generate image using Pollinations AI with style support."""
    try:
        style_prefix = ""
        style = style.lower().strip()
        if style == "cyberpunk":
            style_prefix = "Cyberpunk style neon glow, digital art, high tech: "
        elif style == "anime":
            style_prefix = "Anime illustration style, vibrant colors, clean lines: "
        elif style == "cinematic":
            style_prefix = "Cinematic 8k photo, dramatic lighting, highly detailed: "
        elif style == "sketch":
            style_prefix = "Hand-drawn pencil sketch, black and white, artistic: "
        elif style == "3d-render":
            style_prefix = "3D digital model render, Blender style, realistic textures, glossy: "
        elif style == "fantasy":
            style_prefix = "Mystical fantasy painting, magical, colorful, oil on canvas: "
        elif style == "pixel-art":
            style_prefix = "Retro 8-bit pixel art style, game asset: "

        full_prompt = style_prefix + prompt
        encoded = urllib.parse.quote(full_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&nologo=true"
        
        ts = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(_ensure_gen_dir(), f"image_{ts}.jpg")
        urllib.request.urlretrieve(url, path)
        return f"[IMAGE GENERATED]\nStyle: {style.upper()}\nPrompt: {prompt}\nSaved: {path}"
    except Exception as e:
        return f"[IMAGE ERROR] {e}"


# ── AUDIO GENERATION ─────────────────────────────────────────────────────────
def generate_audio(text: str, lang: str = "en") -> str:
    """Generate audio speech using edge-tts or fallback to local files."""
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(_ensure_gen_dir(), f"audio_{ts}.mp3")
    try:
        import asyncio
        import edge_tts
        voice = "en-US-AriaNeural" if lang == "en" else "bn-BD-NabanitaNeural"
        async def _save():
            comm = edge_tts.Communicate(text, voice=voice)
            await comm.save(path)
        asyncio.run(_save())
        return f"[AUDIO GENERATED]\nText: {text[:60]}...\nSaved: {path}"
    except Exception as e:
        # Fallback to offline gTTS if possible
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=lang)
            tts.save(path)
            return f"[AUDIO GENERATED (gTTS Fallback)]\nSaved: {path}"
        except Exception as e2:
            return f"[AUDIO ERROR] Cloud: {e} | Fallback: {e2}"


# ── MUSIC CHIPTUNE SYNTHESIZER ───────────────────────────────────────────────
def generate_music_chiptune(prompt: str = "retro") -> str:
    """Synthesize retro WAV chiptune music from scratch (no dependencies)."""
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(_ensure_gen_dir(), f"music_{ts}.wav")
    try:
        sample_rate = 22050
        with wave.open(path, 'wb') as wav:
            wav.setnchannels(1) # Mono
            wav.setsampwidth(2) # 16-bit
            wav.setframerate(sample_rate)
            
            # Simple chord/melody arpeggio progression based on prompt keywords
            if "sad" in prompt.lower():
                # A minor progression
                progression = [220.00, 261.63, 329.63, 440.00, 392.00, 329.63, 261.63, 196.00]
            elif "hype" in prompt.lower() or "fast" in prompt.lower():
                # Fast techno scale
                progression = [293.66, 349.23, 440.00, 587.33, 523.25, 440.00, 349.23, 293.66] * 2
            else:
                # C major arpeggio
                progression = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 261.63, 196.00]

            duration_per_note = 0.25 if ("hype" in prompt.lower()) else 0.4
            
            for note in progression:
                num_samples = int(duration_per_note * sample_rate)
                for i in range(num_samples):
                    t = i / sample_rate
                    # Chiptune square/triangle hybrid sound
                    val = math.sin(2 * math.pi * note * t)
                    if val > 0: val = 0.5
                    else: val = -0.5
                    
                    # Sub-bass component
                    val_bass = math.sin(2 * math.pi * (note / 2) * t) * 0.3
                    
                    # Envelope (decay)
                    env = 1.0 - (i / num_samples)
                    sample = int((val + val_bass) * 0.3 * env * 32767)
                    
                    data = struct.pack('<h', max(-32768, min(32767, sample)))
                    wav.writeframesraw(data)
                    
        return f"[MUSIC SYNTHESIZED]\nMelody: {prompt}\nSaved: {path}"
    except Exception as e:
        return f"[MUSIC ERROR] {e}"


# ── VIDEO GENERATION ─────────────────────────────────────────────────────────
def generate_video(prompt: str) -> str:
    """Generate video using Pollinations AI video endpoint."""
    try:
        encoded = urllib.parse.quote(prompt)
        url = f"https://video.pollinations.ai/prompt/{encoded}"
        ts = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(_ensure_gen_dir(), f"video_{ts}.mp4")
        urllib.request.urlretrieve(url, path)
        return f"[VIDEO GENERATED]\nPrompt: {prompt}\nSaved: {path}"
    except Exception as e:
        try:
            img_result = generate_image(prompt)
            return f"[VIDEO] Direct video failed ({e}). Generated image instead.\n{img_result}"
        except Exception as e2:
            return f"[VIDEO ERROR] {e} | Fallback: {e2}"


# ── PARAMETRIC 3D MODEL GENERATION ──────────────────────────────────────────
def generate_3d_model(prompt: str) -> str:
    """Generate a mathematical 3D model template in OBJ format."""
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(_ensure_gen_dir(), f"model_{ts}.obj")
    
    q = prompt.lower()
    
    if "sphere" in q or "ball" in q or "globe" in q:
        # UV Sphere Generation
        verts, faces = _generate_sphere_mesh(R=1.5, rings=16, sectors=16)
        mesh_name = "Sphere"
    elif "cylinder" in q or "pipe" in q:
        # Cylinder Generation
        verts, faces = _generate_cylinder_mesh(R=1.0, H=3.0, segments=16)
        mesh_name = "Cylinder"
    elif "cone" in q or "pyramid" in q:
        # Cone/Pyramid Generation
        verts, faces = _generate_cone_mesh(R=1.2, H=2.5, segments=16)
        mesh_name = "Cone/Pyramid"
    elif "rocket" in q or "spaceship" in q:
        # Composite Rocket Mesh
        verts, faces = _generate_rocket_mesh()
        mesh_name = "Spaceship Rocket"
    else:
        # Default Cube
        verts = [
            (-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),
            (-1,-1, 1),(1,-1, 1),(1,1, 1),(-1,1, 1),
        ]
        faces = [
            (1,2,3,4),(5,8,7,6),(1,5,6,2),
            (2,6,7,3),(3,7,8,4),(4,8,5,1),
        ]
        mesh_name = "Cube (Default)"
        
    try:
        with open(path, "w") as f:
            f.write(f"# JARVIS Parametric 3D Mesh\n# Name: {mesh_name}\n# Prompt: {prompt}\n\n")
            for v in verts:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            f.write("\n")
            for face in faces:
                f.write("f " + " ".join(str(idx) for idx in face) + "\n")
        return f"[3D MODEL GENERATED]\nMesh Type: {mesh_name}\nSaved: {path}"
    except Exception as e:
        return f"[3D MODEL ERROR] {e}"


def _generate_sphere_mesh(R=1.5, rings=16, sectors=16):
    verts = []
    faces = []
    for r in range(rings + 1):
        theta = r * math.pi / rings
        for s in range(sectors):
            phi = s * 2 * math.pi / sectors
            x = R * math.sin(theta) * math.cos(phi)
            y = R * math.cos(theta)
            z = R * math.sin(theta) * math.sin(phi)
            verts.append((x, y, z))
            
    for r in range(rings):
        for s in range(sectors):
            p0 = r * sectors + s + 1
            p1 = r * sectors + ((s + 1) % sectors) + 1
            p2 = (r + 1) * sectors + ((s + 1) % sectors) + 1
            p3 = (r + 1) * sectors + s + 1
            faces.append((p0, p1, p2, p3))
    return verts, faces


def _generate_cylinder_mesh(R=1.0, H=3.0, segments=16):
    verts = []
    faces = []
    # Bottom Circle
    for i in range(segments):
        theta = i * 2 * math.pi / segments
        verts.append((R * math.cos(theta), -H/2, R * math.sin(theta)))
    # Top Circle
    for i in range(segments):
        theta = i * 2 * math.pi / segments
        verts.append((R * math.cos(theta), H/2, R * math.sin(theta)))
        
    # Bottom cap
    faces.append([i + 1 for i in range(segments)][::-1])
    # Top cap
    faces.append([segments + i + 1 for i in range(segments)])
    # Side quads
    for i in range(segments):
        p0 = i + 1
        p1 = (i + 1) % segments + 1
        p2 = segments + ((i + 1) % segments) + 1
        p3 = segments + i + 1
        faces.append((p0, p1, p2, p3))
    return verts, faces


def _generate_cone_mesh(R=1.2, H=2.5, segments=16):
    verts = []
    faces = []
    # Base
    for i in range(segments):
        theta = i * 2 * math.pi / segments
        verts.append((R * math.cos(theta), -H/2, R * math.sin(theta)))
    # Apex
    verts.append((0.0, H/2, 0.0))
    
    # Base cap
    faces.append([i + 1 for i in range(segments)][::-1])
    # Sides
    apex_idx = segments + 1
    for i in range(segments):
        p0 = i + 1
        p1 = (i + 1) % segments + 1
        faces.append((p0, p1, apex_idx))
    return verts, faces


def _generate_rocket_mesh():
    verts = []
    faces = []
    segments = 12
    # Body cylinder radius, height
    R = 0.6
    H_body = 2.0
    
    # Cylinder Base Circle (y = -H_body/2 = -1)
    for i in range(segments):
        theta = i * 2 * math.pi / segments
        verts.append((R * math.cos(theta), -1.0, R * math.sin(theta)))
    # Cylinder Top Circle (y = 1)
    for i in range(segments):
        theta = i * 2 * math.pi / segments
        verts.append((R * math.cos(theta), 1.0, R * math.sin(theta)))
        
    # Cylindrical body faces
    for i in range(segments):
        p0 = i + 1
        p1 = (i + 1) % segments + 1
        p2 = segments + ((i + 1) % segments) + 1
        p3 = segments + i + 1
        faces.append((p0, p1, p2, p3))
        
    # Nose Cone Apex (y = 2.2)
    verts.append((0.0, 2.2, 0.0))
    apex_idx = len(verts)
    
    # Nose Cone faces
    for i in range(segments):
        p0 = segments + i + 1
        p1 = segments + ((i + 1) % segments) + 1
        faces.append((p0, p1, apex_idx))
        
    # Fins at base (4 fins pointing outwards)
    fin_angles = [0, math.pi/2, math.pi, 3*math.pi/2]
    for ang in fin_angles:
        # Base inner, Base outer, Top inner
        # We find index of closest circle vertices
        # To make it simpler, we just append fin vertices directly
        x_dir, z_dir = math.cos(ang), math.sin(ang)
        v0_idx = len(verts) + 1
        verts.append((R * x_dir, -1.0, R * z_dir))
        verts.append((R * 2.2 * x_dir, -1.2, R * 2.2 * z_dir))
        verts.append((R * x_dir, -0.2, R * z_dir))
        
        faces.append((v0_idx, v0_idx + 1, v0_idx + 2))
        
    return verts, faces


# ── FILE GENERATION ──────────────────────────────────────────────────────────
def generate_file(filename: str, content_prompt: str, brain=None) -> str:
    """Generate any file type with AI-generated content."""
    ts = time.strftime("%Y%m%d_%H%M%S")
    safe_name = filename.replace(" ", "_")
    path = os.path.join(_ensure_gen_dir(), safe_name)

    if brain and brain.is_connected:
        content = brain.think(
            f"Generate the complete content for a file named '{filename}'.\n"
            f"Requirements: {content_prompt}\n"
            f"Respond with ONLY the file content, no explanation."
        )
    else:
        content = f"# Generated by JARVIS\n# {content_prompt}\n# {time.strftime('%Y-%m-%d %H:%M:%S')}\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"[FILE GENERATED]\nName: {filename}\nSaved: {path}\nSize: {len(content)} chars"


# ── PHOTO GENERATION ──────────────────────────────────────────────────────────
def generate_photo(prompt: str, style: str = "realistic") -> str:
    """Generate a photo-realistic image."""
    return generate_image(prompt, width=1024, height=768, style="cinematic")


# ── OPEN GENERATED FILE ───────────────────────────────────────────────────────
def open_generated(filename: str) -> str:
    path = os.path.join(GEN_DIR, filename)
    if os.path.exists(path):
        os.startfile(path)
        return f"Opening: {path}"
    return f"File not found: {path}"


def list_generated() -> str:
    d = _ensure_gen_dir()
    files = sorted(os.listdir(d), reverse=True)[:20]
    if not files:
        return "No generated files yet."
    lines = [f"--- GENERATED FILES ({d}) ---"]
    for f in files:
        fp = os.path.join(d, f)
        size = os.path.getsize(fp)
        lines.append(f"  {f}  ({size} bytes)")
    return "\n".join(lines)
