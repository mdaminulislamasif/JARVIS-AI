import os
import sys
import json
import hashlib
import re
from datetime import datetime

# UTF-8 encoding configuration for Windows terminal
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

class ProjectIndexer:
    def __init__(self, directory="."):
        self.directory = os.path.abspath(directory)
        self.map_file = os.path.join(self.directory, "jarvis_project_map.json")
        self.skip_dirs = {
            ".git", ".vscode", "__pycache__", ".pytest_cache", ".hypothesis", 
            "backups", "dist", "build", "jarvis_uploads", "cheng_bot", ".cheng_bot",
            "temp_blender", "platform-tools", "scrcpy", "vscode", "cache", "temp", "tmp",
            "jarvis_temp", "jarvis_downloads", "node_modules", "pytest_cache", "hypothesis"
        }
        self.skip_extensions = {".pyc", ".pyo", ".glb", ".png", ".ico", ".db", ".db-shm", ".db-wal", ".shared", ".tex", ".exe", ".dll", ".zip"}
        
    def get_file_hash(self, filepath):
        """Calculate SHA-256 hash of a file."""
        sha256 = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception:
            return ""

    def analyze_python_file(self, filepath):
        """Analyze python file imports, classes, functions, and purpose."""
        info = {
            "purpose": "General Python Script",
            "imports": [],
            "classes": [],
            "functions": []
        }
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            # Extract docstring for purpose
            docstring_match = re.match(r'^\s*"""(.*?)"""', content, re.DOTALL)
            if docstring_match:
                info["purpose"] = docstring_match.group(1).strip().split("\n")[0]
            elif docstring_match_single := re.match(r"^\s*'''(.*?)'''", content, re.DOTALL):
                info["purpose"] = docstring_match_single.group(1).strip().split("\n")[0]
                
            # Analyze line-by-line
            lines = content.splitlines()
            for line in lines:
                line_strip = line.strip()
                if line_strip.startswith("import ") or line_strip.startswith("from "):
                    info["imports"].append(line_strip)
                elif line_strip.startswith("class "):
                    class_name = line_strip.split("class ")[1].split("(")[0].split(":")[0].strip()
                    info["classes"].append(class_name)
                elif line_strip.startswith("def "):
                    func_name = line_strip.split("def ")[1].split("(")[0].strip()
                    if not func_name.startswith("_"):
                        info["functions"].append(func_name)
        except Exception:
            pass
        return info

    def scan_project(self):
        """Scan directory and build/update the project map."""
        # Load previous map if exists
        old_map = {}
        if os.path.exists(self.map_file):
            try:
                with open(self.map_file, "r", encoding="utf-8") as f:
                    old_map = json.load(f)
            except Exception:
                pass
                
        project_files = {}
        updates_detected = []
        new_files = []
        
        for root, dirs, files in os.walk(self.directory):
            # Prune directories to skip
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]
            
            for file in files:
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, self.directory).replace("\\", "/")
                
                _, ext = os.path.splitext(file)
                if ext in self.skip_extensions:
                    continue
                    
                # Collect basic metadata
                try:
                    stats = os.stat(filepath)
                    mtime = stats.st_mtime
                    size = stats.st_size
                    mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Count lines
                    line_count = 0
                    try:
                        with open(filepath, "rb") as lf:
                            line_count = sum(1 for _ in lf)
                    except Exception:
                        pass
                        
                    file_hash = self.get_file_hash(filepath)
                    
                    # File type categorization
                    category = "Document"
                    if ext == ".py":
                        category = "Python Code"
                    elif ext == ".bat":
                        category = "Batch CLI script"
                    elif ext == ".html":
                        category = "HTML Interface"
                    elif ext == ".css":
                        category = "CSS Stylesheet"
                    elif ext == ".js":
                        category = "Javascript Logic"
                        
                    # Check modifications
                    status = "unchanged"
                    if rel_path in old_map:
                        if old_map[rel_path].get("hash") != file_hash:
                            status = "modified"
                            updates_detected.append(rel_path)
                    else:
                        status = "new"
                        new_files.append(rel_path)
                        
                    file_info = {
                        "path": rel_path,
                        "filename": file,
                        "extension": ext,
                        "category": category,
                        "size_bytes": size,
                        "lines": line_count,
                        "last_modified": mtime_str,
                        "hash": file_hash,
                        "status": status,
                        "purpose": f"Local file in workspace ({category})"
                    }
                    
                    # Analyze python specifics
                    if ext == ".py":
                        py_info = self.analyze_python_file(filepath)
                        file_info.update(py_info)
                        
                    project_files[rel_path] = file_info
                except Exception:
                    continue
                    
        # Detect deleted files
        deleted_files = []
        for old_path in old_map:
            if old_path not in project_files:
                deleted_files.append(old_path)
                
        # Save map and changes summary
        summary = {
            "last_scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modified": updates_detected,
            "new": new_files,
            "deleted": deleted_files
        }
        
        summary_file = self.map_file.replace("jarvis_project_map.json", "jarvis_project_changes.json")
        try:
            with open(summary_file, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)
        except Exception:
            pass
            
        with open(self.map_file, "w", encoding="utf-8") as f:
            json.dump(project_files, f, indent=2)
            
        # Write workspace files list
        try:
            files_list_path = os.path.join(self.directory, "workspace_files_list.txt")
            with open(files_list_path, "w", encoding="utf-8") as lf:
                for rel_path in sorted(project_files.keys()):
                    lf.write(rel_path.replace("/", "\\") + "\n")
        except Exception:
            pass
            
        return {
            "files": project_files,
            "modified": updates_detected,
            "new": new_files,
            "deleted": deleted_files
        }

if __name__ == "__main__":
    indexer = ProjectIndexer()
    res = indexer.scan_project()
    print(f"✅ Project scan complete. Indexed {len(res['files'])} files.")
    if res["new"]:
        print(f"🆕 New files: {res['new']}")
    if res["modified"]:
        print(f"🔄 Modified files: {res['modified']}")
    if res["deleted"]:
        print(f"❌ Deleted files: {res['deleted']}")
