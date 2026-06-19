"""
JARVIS Multi-Brain System
Supports multiple AI backends simultaneously:
  - Gemini (primary, via core/brain.py)
  - OpenAI GPT-4o (fallback)
  - Ollama (local offline LLM)
  - Hugging Face Inference API (free tier)
  - Cohere (free tier)
Each brain can be queried independently or in parallel (consensus mode).
"""
import os
import json
import time
import threading
import urllib.request
import urllib.error
from typing import Optional

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── OLLAMA (local offline brain) ─────────────────────────────────────────────
def ask_ollama(prompt: str, model: str = "llama3", host: str = "http://localhost:11434") -> Optional[str]:
    """Query a local Ollama instance (offline capable)."""
    try:
        data = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
        req = urllib.request.Request(
            f"{host}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            return result.get("response", "").strip()
    except Exception as e:
        return None


def list_ollama_models(host: str = "http://localhost:11434") -> list[str]:
    """List available Ollama models."""
    try:
        with urllib.request.urlopen(f"{host}/api/tags", timeout=5) as r:
            data = json.loads(r.read())
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


# ── HUGGING FACE (free inference API) ────────────────────────────────────────
def ask_huggingface(prompt: str, model: str = "mistralai/Mistral-7B-Instruct-v0.2",
                    hf_token: str = "") -> Optional[str]:
    """Query Hugging Face Inference API (free tier, no key needed for some models)."""
    try:
        url = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Content-Type": "application/json"}
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"
        data = json.dumps({"inputs": prompt, "parameters": {"max_new_tokens": 512}}).encode()
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            if isinstance(result, list) and result:
                return result[0].get("generated_text", "").replace(prompt, "").strip()
            return str(result)
    except Exception as e:
        return None


# ── COHERE (free tier) ────────────────────────────────────────────────────────
def ask_cohere(prompt: str, cohere_key: str = "") -> Optional[str]:
    """Query Cohere API (free tier available)."""
    if not cohere_key:
        return None
    try:
        data = json.dumps({
            "model": "command-r",
            "message": prompt,
            "max_tokens": 500,
        }).encode()
        req = urllib.request.Request(
            "https://api.cohere.com/v1/chat",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {cohere_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            result = json.loads(r.read())
            return result.get("text", "").strip()
    except Exception:
        return None


# ── GROQ (free tier, very fast) ───────────────────────────────────────────────
def ask_groq(prompt: str, groq_key: str = "", model: str = "llama3-8b-8192") -> Optional[str]:
    """Query Groq API (free tier, extremely fast inference)."""
    if not groq_key:
        return None
    try:
        data = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
        }).encode()
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {groq_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            result = json.loads(r.read())
            return result["choices"][0]["message"]["content"].strip()
    except Exception:
        return None


# ── MULTI-BRAIN ORCHESTRATOR ──────────────────────────────────────────────────
class MultiBrain:
    """
    Orchestrates multiple AI backends.
    Priority order: Gemini → Groq → Ollama → HuggingFace → Cohere → OpenAI
    """

    def __init__(self, gemini_brain=None):
        self.gemini = gemini_brain
        self.ollama_model = "llama3"
        self.ollama_host  = "http://localhost:11434"
        self.hf_token     = self._load_key("HF_TOKEN")
        self.cohere_key   = self._load_key("COHERE_KEY")
        self.groq_key     = self._load_key("GROQ_KEY")
        self.active_brain = "gemini"
        self._status: dict[str, str] = {}

    def _load_key(self, name: str) -> str:
        """Load extra API keys from jarvis_config.txt comments or env."""
        val = os.environ.get(name, "")
        if val:
            return val
        cfg = os.path.join(_BASE, "jarvis_config.txt")
        if os.path.exists(cfg):
            with open(cfg) as f:
                for line in f:
                    if line.strip().startswith(f"#{name}="):
                        return line.strip().split("=", 1)[1]
        return ""

    def save_extra_key(self, name: str, value: str):
        """Save an extra key to jarvis_config.txt as a comment line."""
        cfg = os.path.join(_BASE, "jarvis_config.txt")
        lines = []
        if os.path.exists(cfg):
            with open(cfg) as f:
                lines = f.readlines()
        # Remove old entry
        lines = [l for l in lines if not l.strip().startswith(f"#{name}=")]
        lines.append(f"#{name}={value}\n")
        with open(cfg, "w") as f:
            f.writelines(lines)
        setattr(self, name.lower(), value)

    def think(self, query: str, history_str: str = "", prefer: str = "auto") -> str:
        """
        Route query to best available brain.
        prefer: "auto" | "gemini" | "ollama" | "groq" | "huggingface" | "cohere"
        """
        brains_to_try = self._build_priority(prefer)

        for brain_name in brains_to_try:
            result = self._try_brain(brain_name, query, history_str)
            if result:
                self.active_brain = brain_name
                self._status[brain_name] = "OK"
                return f"[{brain_name.upper()}] {result}"
            else:
                self._status[brain_name] = "FAIL"

        # AUTO-FIX: Try offline brain as last resort
        try:
            from jarvis_offline_brain import OfflineBrain
            offline_brain = OfflineBrain()
            result = offline_brain.process_query(query)
            offline_brain.close()  # Close connection to release database lock
            if result and result.get('status') == 'success':
                self.active_brain = "offline"
                self._status["offline"] = "OK"
                return f"[OFFLINE BRAIN] {result.get('response', 'Processing...')}"
        except Exception:
            print("⚠️ Error occurred but was silently ignored")

        return "QUOTA_EXCEEDED_USE_OFFLINE"

    def _build_priority(self, prefer: str) -> list[str]:
        order = ["gemini", "groq", "ollama", "huggingface", "cohere"]
        if prefer != "auto" and prefer in order:
            order.remove(prefer)
            order.insert(0, prefer)
        return order

    def _try_brain(self, name: str, query: str, history: str) -> Optional[str]:
        prompt = f"{history}\nUser: {query}" if history else query
        try:
            if name == "gemini":
                if self.gemini and self.gemini.is_connected:
                    return self.gemini.think(query, history)
            elif name == "ollama":
                return ask_ollama(prompt, self.ollama_model, self.ollama_host)
            elif name == "groq":
                return ask_groq(prompt, self.groq_key)
            elif name == "huggingface":
                return ask_huggingface(prompt, hf_token=self.hf_token)
            elif name == "cohere":
                return ask_cohere(prompt, self.cohere_key)
        except Exception:
            print("⚠️ Error occurred but was silently ignored")
        return None

    def status(self) -> str:
        lines = ["--- MULTI-BRAIN STATUS ---"]
        checks = {
            "gemini":      "ONLINE" if (self.gemini and self.gemini.is_connected) else "OFFLINE",
            "groq":        "KEY SET" if self.groq_key else "NO KEY",
            "ollama":      "AVAILABLE" if list_ollama_models(self.ollama_host) else "OFFLINE",
            "huggingface": "KEY SET" if self.hf_token else "FREE TIER",
            "cohere":      "KEY SET" if self.cohere_key else "NO KEY",
        }
        for name, st in checks.items():
            active = " << ACTIVE" if name == self.active_brain else ""
            lines.append(f"  {name.upper():15} {st}{active}")
        return "\n".join(lines)

    def parallel_think(self, query: str) -> str:
        """Query all available brains in parallel and return all responses."""
        results = {}
        threads = []

        def _query(name):
            r = self._try_brain(name, query, "")
            if r:
                results[name] = r

        for name in ["gemini", "groq", "ollama"]:
            t = threading.Thread(target=_query, args=(name,), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join(timeout=15)

        if not results:
            return "No brains responded."

        lines = ["--- PARALLEL BRAIN RESPONSES ---"]
        for name, resp in results.items():
            lines.append(f"\n[{name.upper()}]:\n{resp[:300]}")
        return "\n".join(lines)
