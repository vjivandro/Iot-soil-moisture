import ujson
import os
from lib.utils import Logger

class LocalStorage:
    def __init__(self, filename="data.json", max_entries=100):
        self.filename = filename
        self.max_entries = max_entries
        self.logger = Logger()
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        try:
            with open(self.filename, "r") as f:
                pass
        except:
            with open(self.filename, "w") as f:
                ujson.dump([], f)
                
    def save_data(self, data):
        try:
            with open(self.filename, "r") as f:
                existing_data = ujson.load(f)
                
            data["synced"] = False
            data["id"] = len(existing_data) + 1
            existing_data.append(data)
            
            # Batasi jumlah data yang disimpan
            if len(existing_data) > self.max_entries:
                existing_data = existing_data[-self.max_entries:]
                
            with open(self.filename, "w") as f:
                ujson.dump(existing_data, f)
                
            return True
        except Exception as e:
            self.logger.error("Failed to save data:", e)
            return False
            
    def get_unsynced_data(self):
        try:
            with open(self.filename, "r") as f:
                all_data = ujson.load(f)
                
            return [d for d in all_data if not d.get("synced", False)]
        except Exception as e:
            self.logger.error("Failed to get unsynced data:", e)
            return []
            
    def mark_as_synced(self, data_id):
        try:
            with open(self.filename, "r") as f:
                all_data = ujson.load(f)
                
            for d in all_data:
                if d["id"] == data_id:
                    d["synced"] = True
                    break
                    
            with open(self.filename, "w") as f:
                ujson.dump(all_data, f)
                
            return True
        except Exception as e:
            self.logger.error("Failed to mark data as synced:", e)
            return False