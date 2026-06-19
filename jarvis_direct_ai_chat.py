"""
JARVIS DIRECT AI CHAT
=====================
JARVIS automatically chats with World AIs without manual browser interaction.
Uses multiple FREE AI APIs - no API key needed!

JARVIS নিজেই AI এর সাথে কথা বলবে - আপনাকে browser এ paste করতে হবে না!
"""

import requests
import json
import time
import random
import os
import sys
import io

if sys.platform.startswith('win'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

try:
    from core.brain import SYS_INSTRUCT
except ImportError:
    SYS_INSTRUCT = "You are JARVIS, an elite AI assistant. You have full GUI, mouse, and keyboard control over the PC."

class DirectAIChat:
    """Direct chat with AIs - no browser needed!"""
    
    def __init__(self):
        self.timeout = 30
        self.last_response = ""
        self.history = []
        self.max_history = 5
        self.current_ai = 'blackbox' # Default
        
        # Load Gemini keys from config file
        self.gemini_keys = []
        _BASE = os.path.dirname(os.path.abspath(__file__))
        _WORKSPACE_CFG = os.path.join(_BASE, 'jarvis_config.txt')
        _DESKTOP_CFG = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', 'ai', 'jarvis_config.txt')
        cfg_path = _WORKSPACE_CFG if os.path.exists(_WORKSPACE_CFG) else _DESKTOP_CFG
        if os.path.exists(cfg_path):
            with open(cfg_path, 'r') as f:
                for line in f:
                    key = line.strip()
                    if (key.startswith("AIza") or key.startswith("AQ.")) and len(key) > 30:
                        self.gemini_keys.append(key)

        
        # Multiple free AI APIs (no key needed!)
        self.free_apis = [
            {
                'name': 'Pollinations AI (Reliable)',
                'url': 'https://text.pollinations.ai/',
                'type': 'pollinations'
            },
            {
                'name': 'DuckDuckGo AI (Fast)',
                'url': 'https://duckduckgo.com/duckchat/v1/chat',
                'type': 'duckduckgo'
            },
            {
                'name': 'Blackbox AI',
                'url': 'https://www.blackbox.ai/api/chat',
                'type': 'blackbox'
            },
            {
                'name': 'Phind AI (Code)',
                'url': 'https://extension.phind.com/agent/',
                'type': 'phind'
            },
        ]
        # Hugging Face models (free, no API key needed!)
        self.hf_models = [
            "facebook/blenderbot-400M-distill",
            "google/flan-t5-large",
        ]
        
    def _get_project_context(self, query):
        """Build a dynamic, compact context about project files and recent updates."""
        try:
            import re
            map_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_project_map.json")
            files_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace_files_list.txt")
            if not os.path.exists(map_file) or not os.path.exists(files_list_path):
                try:
                    from jarvis_project_indexer import ProjectIndexer
                    indexer = ProjectIndexer(os.path.dirname(os.path.abspath(__file__)))
                    indexer.scan_project()
                except Exception:
                    pass
            
            if not os.path.exists(map_file):
                return ""
                
            with open(map_file, "r", encoding="utf-8") as f:
                project_map = json.load(f)
                
            total_files = len(project_map)
            categories = {}
            for f in project_map.values():
                cat = f.get("category", "Other")
                categories[cat] = categories.get(cat, 0) + 1
                
            # Load changes summary from last scan
            changes_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_project_changes.json")
            changes_summary = None
            if os.path.exists(changes_file):
                try:
                    with open(changes_file, "r", encoding="utf-8") as f:
                        changes_summary = json.load(f)
                except Exception:
                    pass
                
            # Find recently modified/active files (modified in the last 24 hours)
            import datetime
            now = datetime.datetime.now()
            recent_files = []
            for path, f_info in project_map.items():
                mtime_str = f_info.get("last_modified", "")
                if mtime_str:
                    try:
                        mtime = datetime.datetime.strptime(mtime_str, "%Y-%m-%d %H:%M:%S")
                        if (now - mtime).total_seconds() < 24 * 3600:
                            recent_files.append((path, f_info.get("category", "Code")))
                    except Exception:
                        pass
            
            # Find core scripts in root directory
            core_files = []
            important_names = [
                "jarvis_conversational.py", "jarvis_direct_ai_chat.py", 
                "jarvis_project_indexer.py", "jarvis_multilang_voice.py",
                "jarvis_code_studio.py", "START_PHONE_MIC_BRIDGE.bat", 
                "PC_MIC_TO_PHONE.bat", "phone_audio_bridge.py",
                "jarvis_conversations.db", "jarvis_project_map.json"
            ]
            for name in important_names:
                if name in project_map:
                    core_files.append(project_map[name])
                    
            # Check if user query matches any filename in the project map
            query_lower = query.lower()
            matched_files = []
            for path, f_info in project_map.items():
                filename = f_info.get("filename", "").lower()
                if filename in query_lower or (len(filename) > 4 and filename.split('.')[0] in query_lower):
                    matched_files.append(f_info)
                    if len(matched_files) >= 5:
                        break
                        
            # Search workspace_files_list.txt for any file matches from user query (A-to-Z recursive dir /s mapping)
            files_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace_files_list.txt")
            total_workspace_files = total_files
            matched_list_files = []
            if os.path.exists(files_list_path):
                try:
                    with open(files_list_path, "r", encoding="utf-8", errors="ignore") as lf:
                        all_files_list = lf.read().splitlines()
                    total_workspace_files = len(all_files_list)
                    
                    # Search for any file matches from the user query
                    query_words = [w.strip().lower() for w in re.split(r'[\s/\\_.]', query) if len(w.strip()) > 3]
                    for item in all_files_list:
                        item_clean = item.strip().replace("\\", "/")
                        basename = os.path.basename(item_clean).lower()
                        if basename and (basename in query_lower or any(qw in basename for qw in query_words)):
                            matched_list_files.append(item_clean)
                            if len(matched_list_files) >= 15:
                                break
                except Exception:
                    pass
                        
            # Format context block
            ctx = "\n=== PROJECT CODEBASE CONTEXT ===\n"
            ctx += f"Total active indexed code/script files: {total_files}\n"
            ctx += f"Total actual files in workspace (from dir /s): {total_workspace_files}\n"
            ctx += "File distribution: " + ", ".join([f"{k}: {v}" for k, v in categories.items()]) + "\n"
            
            if changes_summary:
                ctx += f"\nLast scan changes (Time: {changes_summary.get('last_scan_time', '')}):\n"
                if changes_summary.get("new"):
                    ctx += f"- Added/New files: {', '.join(changes_summary['new'][:10])}\n"
                if changes_summary.get("modified"):
                    ctx += f"- Updated/Modified files: {', '.join(changes_summary['modified'][:10])}\n"
                if changes_summary.get("deleted"):
                    ctx += f"- Removed/Deleted files: {', '.join(changes_summary['deleted'][:10])}\n"
            
            if recent_files:
                ctx += "\nRecently modified/active files (last 24 hours):\n"
                for path, cat in recent_files[:8]:
                    ctx += f"- {path} ({cat})\n"
                
            ctx += "\nCore project scripts:\n"
            for f in core_files:
                ctx += f"- {f['path']} ({f['category']}): {f.get('purpose', 'Active workspace script')}\n"
                
            if matched_list_files:
                ctx += "\nWorkspace file paths matching your query (A-to-Z search matches):\n"
                for path in matched_list_files:
                    ctx += f"- {path}\n"
                
            if matched_files:
                ctx += "\nReferenced files details (metadata):\n"
                for f in matched_files:
                    ctx += f"- File: {f['path']} ({f['category']})\n"
                    ctx += f"  Lines: {f.get('lines', 0)} | Size: {f.get('size_bytes', 0)} bytes | Modified: {f.get('last_modified', '')}\n"
                    ctx += f"  Purpose: {f.get('purpose', 'N/A')}\n"
                    if f.get("classes"):
                        ctx += f"  Classes: {', '.join(f['classes'])}\n"
                    if f.get("functions"):
                        ctx += f"  Functions: {', '.join(f['functions'])}\n"
                        
            ctx += "=================================\n"
            return ctx
        except Exception as e:
            return f"\n[Project Context Error: {e}]\n"

    def _detect_adb_devices(self):
        """Detect connected ADB devices using local adb.exe if possible."""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            adb_path = os.path.join(base_dir, "platform-tools", "adb.exe")
            if not os.path.exists(adb_path):
                adb_path = "adb"
            import subprocess
            res = subprocess.run([adb_path, "devices"], capture_output=True, text=True, timeout=5)
            lines = res.stdout.strip().split("\n")[1:]
            devices = [line.split()[0] for line in lines if "device" in line and "unauthorized" not in line]
            return devices
        except Exception:
            return []

    def _is_direct_command(self, query):
        """Check if query is a direct system command (to execute locally instantly)"""
        q = query.lower().strip()
        
        # Direct math check
        if any(c in q for c in ['+', '-', '*', '/']) and any(c.isdigit() for c in q):
            return True
            
        # Command prefixes
        command_prefixes = [
            'open ', 'search ', 'find ', 'calculate ', 'create file', 'create folder',
            'list files', 'list file', 'system info', 'systeminfo', 'sysinfo',
            'time', 'date', 'help', 'build website', 'build portfolio', 'build blog',
            'build business', 'build landing', 'build ecommerce', 'lock', 'shutdown',
            'restart', 'reboot', 'sleep', 'flipper', 'alien', 'learn from internet',
            'ultimate learn', 'auto learn', 'tree learn', 'devtools learn',
            'show history', 'chat history'
        ]
        if any(q.startswith(prefix) for prefix in command_prefixes):
            return True
            
        # Direct word matches
        direct_words = {'help', 'time', 'date', 'lock', 'shutdown', 'reboot', 'restart', 'sleep', 'flipper', 'alien', 'history'}
        if q in direct_words:
            return True
            
        return False

    def chat_with_ai(self, query, ai_name='auto'):
        """
        Chat directly with AI - JARVIS does everything!
        """
        # Maintain history
        self.history.append({"role": "user", "content": query})
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]

        # Get project codebase context dynamically
        project_context = self._get_project_context(query)

        # Get connected ADB devices
        adb_devices = self._detect_adb_devices()
        adb_status_str = ", ".join(adb_devices) if adb_devices else "None"

        # Create context-aware prompt with strict system persona reinforcement
        system_reinforcement = (
            "System Instruction: You are JARVIS, an elite AI assistant. You have full GUI control "
            "over this PC. You can move the mouse, type on the keyboard, and run system tasks. "
            f"Connected ADB Devices: {adb_status_str}. "
            "If you want to perform system actions, you MUST output 'EXECUTE: [command]' on a new line. "
            "Mouse actions: 'EXECUTE: mouse move X Y', 'EXECUTE: mouse click', 'EXECUTE: mouse click X Y'. "
            "Keyboard actions: 'EXECUTE: keyboard type [text]', 'EXECUTE: keyboard press [key]', 'EXECUTE: keyboard hotkey [keys]'. "
            "Standard commands: 'EXECUTE: app open [app]', 'EXECUTE: lock', 'EXECUTE: workspace', 'EXECUTE: battery', etc. "
            "Terminal commands: 'EXECUTE: cmd [command_string]', 'EXECUTE: powershell [command_string]'. "
            "File reading command: 'EXECUTE: read_file [path]' (use this to read the full content of any file). "
            "NEVER claim you are a language model or that you cannot control the PC. "
            "You always match the user's language (Bengali/Banglish/English). "
            "Please respond concisely."
        )
        
        context_query = f"[{system_reinforcement}]\n\n{project_context}\n\n"
        if len(self.history) > 1:
            context_query += "Previous conversation:\n"
            for msg in self.history[:-1]:
                context_query += f"{msg['role'].capitalize()}: {msg['content']}\n"
            context_query += f"Current User Query: {query}"
        else:
            context_query += f"User: {query}"

        # Try direct commands first (instant local execution!)
        if self._is_direct_command(query):
            local_response = self._try_local_response(query)
            if local_response:
                self.history.append({"role": "assistant", "content": local_response})
                return {
                    'success': True,
                    'response': local_response,
                    'ai': 'JARVIS Local Intelligence'
                }
        
        # Try official Gemini API keys first if available
        if self.gemini_keys and (ai_name == 'auto' or ai_name == 'gemini'):
            gemini_res = self._chat_gemini(context_query)
            if gemini_res['success']:
                self.history.append({"role": "assistant", "content": gemini_res['response']})
                return gemini_res

        # Try free AI APIs (fast and reliable!)
        target_ais = self.free_apis if ai_name == 'auto' else [api for api in self.free_apis if api['type'] == ai_name]

        for api in target_ais:
            try:
                result = self._chat_free_api(context_query, api)
                if result['success']:
                    self.history.append({"role": "assistant", "content": result['response']})
                    return result
            except Exception:
                continue

        # If specific AI failed, try Auto fallback
        if ai_name != 'auto':
            print(f"[!] {ai_name.upper()} failed. Falling back to AUTO...")
            return self.chat_with_ai(query, 'auto')

        # Try Hugging Face models (as last resort)
        for model in self.hf_models:
            try:
                result = self._chat_huggingface(context_query, model)
                if result['success']:
                    self.history.append({"role": "assistant", "content": result['response']})
                    return result
            except Exception:
                continue
        
        # Fallback to local intelligence / offline brain if completely offline or all online models failed
        local_response = self._try_local_response(query)
        if local_response:
            self.history.append({"role": "assistant", "content": local_response})
            return {
                'success': True,
                'response': local_response,
                'ai': 'JARVIS Local Intelligence'
            }
        
        # All failed
        return {
            'success': False,
            'response': 'AI services temporarily unavailable. Please use manual World AI Chat.',
            'ai': 'none'
        }
    
    def _chat_gemini(self, query):
        """Chat using official Gemini API keys from jarvis_config.txt"""
        if not self.gemini_keys:
            return {'success': False, 'response': 'No keys'}
            
        for key in self.gemini_keys:
            try:
                # Try Omni-Agent Orchestrator routing first
                try:
                    from omni_agent_orchestrator import OmniAgentOrchestrator
                    orchestrator = OmniAgentOrchestrator(api_key=key)
                    result = orchestrator.process(query)
                    if result:
                        return {
                            'success': True,
                            'response': result,
                            'ai': 'JARVIS Omni-Agent'
                        }
                except Exception as orchestrator_err:
                    print(f"[!] OmniAgentOrchestrator routing failed: {orchestrator_err}. Falling back...")

                # Try new SDK first
                try:
                    import google.genai as genai_new
                    client = genai_new.Client(api_key=key)
                    for model_name in ["gemini-2.5-pro", "gemini-2.0-pro-exp-02-05", "gemini-1.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=query
                            )
                            if response and response.text:
                                return {
                                    'success': True,
                                    'response': response.text,
                                    'ai': f'Gemini ({model_name})'
                                }
                        except Exception as model_err:
                            err_str = str(model_err).lower()
                            if any(msg in err_str for msg in ["api_key_invalid", "api key", "unauthorized", "invalid", "key not found", "not valid", "api_key"]):
                                break
                            continue
                except ImportError:
                    # Fallback to old SDK
                    import google.generativeai as genai_old
                    genai_old.configure(api_key=key)
                    for model_name in ["gemini-2.5-pro", "gemini-2.0-pro-exp-02-05", "gemini-1.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
                        try:
                            model = genai_old.GenerativeModel(model_name)
                            response = model.generate_content(query)
                            if response and response.text:
                                return {
                                    'success': True,
                                    'response': response.text,
                                    'ai': f'Gemini ({model_name})'
                                }
                        except Exception as model_err:
                            err_str = str(model_err).lower()
                            if any(msg in err_str for msg in ["api_key_invalid", "api key", "unauthorized", "invalid", "key not found", "not valid", "api_key"]):
                                break
                            continue
            except Exception as e:
                print(f"[!] Gemini query failed for key {key[:10]}: {e}")
                continue
                
        return {'success': False, 'response': 'All Gemini keys failed'}

    def _try_local_response(self, query):
        """Try to answer simple questions locally (instant!)"""
        query_lower = query.lower()
        import re
        
        # Simple factual questions & Bengali greetings
        local_knowledge = {
            'what is python': "Python is a high-level, interpreted programming language known for its simplicity and versatility.",
            'what is ai': "AI (Artificial Intelligence) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions.",
            'kemon acho': "Ami bhalo achi! Apni kemon achen? Bolun ami apnake ki bhabe help korte pari.",
            'kemon achen': "Ami bhalo achi sir! Apnar ki dorkার?",
            'ki koro': "Ami apnar AI assistant JARVIS. Ami apnake help korar jonno ready achi!",
            'ki korcho': "Ami apnar kotha bhabchi! Ki help dorkar?",
            'who are you': "I'm JARVIS - Just A Rather Very Intelligent System. Your personal AI assistant.",
            'tumi ke': "Ami JARVIS, apnar personal AI assistant. Ami apnar PC control korte pari ebong apnake help korte pari!",
            'jarvis': "Yes Boss! I'm here. Ami apnar sob kotha sunchi. Bolun ki korte hobe?",
            'help': "Ami apnake computer automation, hacking tools, ebong AI chat e help korte pari. Bolun ki dorkar?",
            'hi': "Hello! How can I assist you today?",
            'hello': "Hi there! JARVIS at your service. What's on your mind?",
            'amr name ki': "Apni amar Boss! Ami apnake 'Boss' hisebe chini.",
            'tomar name ki': "Amar naam JARVIS (Just A Rather Very Intelligent System).",
            'who is your creator': "I was created by ASIF and the Google DeepMind team. I am JARVIS Prime V11.",
            'tomar nirmata ke': "Amar nirmata holo ASIF (ASIF Hacker Suite er developer). Ami tar banano ekty powerful AI assistant.",
            'tomr nirmata k': "Amar nirmata holo ASIF. Ami JARVIS Prime V11, apnar personal assistant.",
            'tomar nirmata k': "Amar nirmata holo ASIF. Ami JARVIS Prime V11, apnar personal assistant.",
            'tomar creator k': "Amar creator holo ASIF. Ami JARVIS Prime V11.",
            'who made you': "I was developed by ASIF to be the ultimate AI assistant.",
        }
        
        for key, value in local_knowledge.items():
            pattern = rf"\b{re.escape(key)}\b"
            if re.search(pattern, query_lower):
                return value
        
        # Fallback to OfflineBrain (fully local database query)
        try:
            from jarvis_offline_brain import OfflineBrain
            brain = OfflineBrain()
            result = brain.process_query(query)
            # Close connection to release SQLite lock
            try:
                brain.close()
            except Exception:
                pass
            if result and result.get('status') == 'success' and result.get('type') != 'info':
                return result.get('response')
        except Exception as e:
            print(f"[!] OfflineBrain local fallback error: {e}")
        
        return None

    def _chat_free_api(self, query, api):
        """Chat with free AI APIs (no key needed!)"""
        try:
            if api['type'] == 'blackbox':
                # Blackbox AI (Enhanced headers to bypass auth error)
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://www.blackbox.ai/',
                    'Origin': 'https://www.blackbox.ai'
                }
                payload = {
                    "messages": [
                        {"role": "system", "content": SYS_INSTRUCT},
                        {"role": "user", "content": query}
                    ],
                    "id": str(random.randint(100000, 999999)),
                    "previewToken": None,
                    "userId": None,
                    "codeModelMode": True,
                    "agentMode": {},
                    "trendingAgentMode": {},
                    "isUtmSource": False,
                    "isChromeExtension": False,
                    "githubToken": None
                }
                response = requests.post(api['url'], headers=headers, json=payload, timeout=self.timeout)
                if response.status_code == 200:
                    # Blackbox sometimes returns JSON strings in a stream format
                    answer = response.text.strip()
                    if "error" not in answer.lower():
                        return {'success': True, 'response': answer, 'ai': api['name']}
            
            elif api['type'] == 'pollinations':
                # Pollinations AI (Very stable free endpoint with system instruction support)
                url = f"{api['url']}{requests.utils.quote(query)}?system={requests.utils.quote(SYS_INSTRUCT)}"
                response = requests.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    return {'success': True, 'response': response.text.strip(), 'ai': api['name']}

            elif api['type'] == 'duckduckgo':
                # DuckDuckGo AI (Requires VQD token)
                status_url = "https://duckduckgo.com/duckchat/v1/status"
                headers = {'x-vqd-accept': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                vqd_resp = requests.get(status_url, headers=headers)
                vqd = vqd_resp.headers.get('x-vqd-4') or vqd_resp.headers.get('x-vqd-accept')
                
                if vqd:
                    payload = {
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": SYS_INSTRUCT},
                            {"role": "user", "content": query}
                        ]
                    }
                    headers = {
                        'Content-Type': 'application/json',
                        'x-vqd-4': vqd,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                    }
                    resp = requests.post(api['url'], headers=headers, json=payload)
                    if resp.status_code == 200:
                        # Parse DDG stream response
                        lines = resp.text.split('\n')
                        full_text = ""
                        for line in lines:
                            if line.startswith('data: '):
                                content = line[6:]
                                if content == '[DONE]': break
                                try:
                                    data = json.loads(content)
                                    if 'message' in data: full_text += data['message']
                                except Exception as e:
                                    print(f"⚠️ Error: {e}")
                                    continue
                        if full_text:
                            return {'success': True, 'response': full_text, 'ai': api['name']}

            elif api['type'] == 'phind':
                # Phind AI
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                payload = {
                    "question": query,
                    "options": {"date": time.strftime("%Y-%m-%d"), "language": "en"}
                }
                response = requests.post(api['url'], headers=headers, json=payload, timeout=self.timeout)
                if response.status_code == 200:
                    try:
                        result = response.json()
                        if 'answer' in result:
                            return {'success': True, 'response': result['answer'], 'ai': api['name']}
                    except Exception as e:

                        print(f"⚠️ Error: {e}")
                        # Fallback to text parsing if JSON fails
                        if response.text: return {'success': True, 'response': response.text, 'ai': api['name']}
            
            return {
                'success': False,
                'response': f'{api["name"]} not available',
                'ai': api['name']
            }
            
        except Exception as e:
            return {
                'success': False,
                'response': f'Error: {str(e)}',
                'ai': api['name']
            }
    
    def _chat_huggingface(self, query, model):
        """Chat with Hugging Face model (Free!)"""
        
        try:
            url = f"https://api-inference.huggingface.co/models/{model}"
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            # Different payload based on model type
            if 'flan-t5' in model:
                payload = {
                    "inputs": query,
                    "parameters": {
                        "max_length": 200,
                        "temperature": 0.7
                    }
                }
            else:
                payload = {
                    "inputs": {
                        "text": query
                    },
                    "parameters": {
                        "max_length": 200
                    }
                }
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Parse response based on model type
                answer = ""
                if isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        answer = result[0]['generated_text']
                    elif 'translation_text' in result[0]:
                        answer = result[0]['translation_text']
                    else:
                        answer = str(result[0])
                elif isinstance(result, dict):
                    if 'generated_text' in result:
                        answer = result['generated_text']
                    else:
                        answer = str(result)
                
                if answer and len(answer) > 10:
                    self.last_response = answer
                    model_name = model.split('/')[-1]
                    return {
                        'success': True,
                        'response': answer,
                        'ai': f'Hugging Face ({model_name})'
                    }
            
            return {
                'success': False,
                'response': f'Model {model} not ready',
                'ai': 'huggingface'
            }
            
        except Exception as e:
            return {
                'success': False,
                'response': f'Error: {str(e)}',
                'ai': 'huggingface'
            }
    
    def get_available_ais(self):
        """Get list of available AIs"""
        return {
            'local': {
                'name': 'JARVIS Local Intelligence',
                'description': 'Instant answers from local knowledge',
                'icon': '🧠',
                'free': True
            },
            'duckduckgo': {
                'name': 'DuckDuckGo AI',
                'description': 'Free GPT-3.5 Turbo access',
                'icon': '🦆',
                'free': True
            },
            'phind': {
                'name': 'Phind AI',
                'description': 'Free GPT-4 for coding',
                'icon': '🔍',
                'free': True
            },
            'you': {
                'name': 'You.com AI',
                'description': 'Free AI search and chat',
                'icon': '🌐',
                'free': True
            },
            'huggingface': {
                'name': 'Hugging Face AI',
                'description': 'Free AI models from Hugging Face',
                'icon': '🤗',
                'free': True
            },
        }


# Test function
if __name__ == "__main__":
    print("="*60)
    print("🤖 TESTING DIRECT AI CHAT")
    print("="*60)
    
    chat = DirectAIChat()
    
    test_queries = [
        "What is Python?",
        "Who are you?",
        "What is AI?",
    ]
    
    for test_query in test_queries:
        print(f"\n📝 Query: {test_query}")
        print("🔄 Trying to get response from AI...")
        
        result = chat.chat_with_ai(test_query, 'auto')
        
        if result['success']:
            print(f"✅ Success!")
            print(f"🤖 AI: {result['ai']}")
            print(f"💬 Response: {result['response'][:200]}...")
        else:
            print(f"❌ Failed!")
            print(f"⚠️ Error: {result['response']}")
        
        print("-"*60)
    
    print("\n" + "="*60)

