import json
from typing import Any, Dict
from datetime import datetime

class SharedMemory:
    """Persistent memory shared across all agents"""
    
    def __init__(self, storage_path: str = './memory.json'):
        self.storage_path = storage_path
        self.memory = self._load()
    
    def store(self, key: str, value: Any):
        """Store data in shared memory"""
        self.memory[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat(),
            'type': type(value).__name__
        }
        self._persist()
        print(f"✅ Stored: {key}")
    
    def get(self, key: str, default=None) -> Any:
        """Retrieve data from shared memory"""
        if key in self.memory:
            return self.memory[key]['value']
        return default
    
    def _load(self) -> Dict:
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _persist(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.memory, f, indent=2, default=str)
