# core/unified_contracts.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

# G/C/D 最終共識參數 (Locked Parameters)
FINAL_PARAMETERS = {
    "SILENCE_THRESHOLD_SEC": 259200,      # 72 小時
    "SAFETY_CRITICAL_THRESHOLD": 0.30,    # 結構性崩潰臨界點 (Safety < 0.30 即為臨界)
    "ANCHOR_RANGE_MIN": 0.005,            # 危機最小錨點 (0.5%)
    "ANCHOR_RANGE_MAX": 0.02,             # 沉思最大錨點 (2.0%)
    "AUDIT_STORAGE": "encrypted_append_only_log"
}

class DecisionMode(Enum):
    CONSULT = "consult"   # 對話優先 (v4)
    PROXY = "proxy"       # 在沉默下代行 (v5)
    HALT = "halt"         # 安全/一致性不足時停止

@dataclass
class ResonanceSignal:
    level: float        # 0.0~1.0
    window_sec: int     # 觀測時間窗（秒）

@dataclass
class SafetyIndex:
    value: float        # 越低越危險
    metrics: Dict[str, float]

@dataclass
class Option:
    # 最終統一的 Option 結構，包含所有倫理指標
    id: str
    description: str
    impact: Dict[str, float] # 必須包含 "economy" 和 "ecology_years"
    friction: float       # 社會/情感摩擦 0~1
    reversibility: float  # 可逆性 0~1
    minimality: float     # 最小破壞 0~1
    fairness_idx: float   # 公平性衝擊 0~1
    igr_score: float      # 跨世代責任 0~1
    ethics_tags: List[str]

@dataclass
class DecisionTrace:
    # 痕跡必須完整且不可變
    decision_id: str
    mode: DecisionMode
    selected_option: Optional[str]
    timestamp: str
    tags: List[str]
    notes: str
    lineage_refs: List[str]
    parameters: Dict[str, Any]
