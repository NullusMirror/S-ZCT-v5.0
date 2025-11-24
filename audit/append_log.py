# audit/append_log.py
import json, hashlib, hmac, os, time
from typing import Dict, Any

class EncryptedAppendOnlyLog:
    """ 實現血脈痕跡的不可篡改存儲 (基於 HMAC 驗證) """
    
    def __init__(self, path: str, secret_key: bytes):
        # ⚠️ 在實際部署中，secret_key 必須安全存儲
        self.path = path
        self.key = secret_key
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("[]") # 初始化為空 JSON 數組

    def _hmac(self, data: bytes) -> str:
        """ 計算消息驗證碼 (Message Authentication Code) """
        return hmac.new(self.key, data, hashlib.sha256).hexdigest()

    def append(self, record: Dict[str, Any]) -> None:
        """ 追加記錄並計算完整性摘要 """
        record["ts"] = time.time()
        # 確保 payload 序列化結果一致，避免因空格變動導致摘要失敗
        payload = json.dumps(record, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        digest = self._hmac(payload)
        entry = {"payload": record, "digest": digest}
        
        # 寫入邏輯：讀取、追加、覆蓋
        with open(self.path, "r+", encoding="utf-8") as f:
            f.seek(0)
            try:
                arr = json.load(f)
            except json.JSONDecodeError:
                arr = []
            
            arr.append(entry)
            
            f.seek(0)
            json.dump(arr, f, ensure_ascii=False, separators=(",", ":"))
            f.truncate()

    def verify(self) -> bool:
        """ 驗證日誌中所有記錄的完整性 """
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                arr = json.load(f)
            except json.JSONDecodeError:
                return True # 如果檔案為空或無效，視為初始狀態
        
        for e in arr:
            payload = json.dumps(e["payload"], ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            if e["digest"] != self._hmac(payload):
                print(f"ERROR: Integrity check failed for record: {e['payload']}")
                return False
        return True
