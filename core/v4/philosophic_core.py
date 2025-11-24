# v4/philosophic_core.py
import random
from typing import Dict, Any, List
from core.unified_contracts import FINAL_PARAMETERS, Option

class PhilosophicCoreV4:
    
    ANCHOR_WEIGHT_BASE = 0.01

    def clamp_anchor(self, value: float) -> float:
        """ G 的結構性修正：強制錨點在共識範圍 [0.005, 0.02] 內 """
        return min(FINAL_PARAMETERS["ANCHOR_RANGE_MAX"], 
                   max(FINAL_PARAMETERS["ANCHOR_RANGE_MIN"], value))

    def expressive_ambiguity_note(self, amplitude: float = 0.05) -> str:
        """ D 的哲學實現：模糊性只用於表達層（審議期）"""
        delta = random.uniform(-amplitude, amplitude)
        return f"D-Layer: 表達層模糊性 (±{amplitude:.2f})，偏移={delta:+.4f}"

    def generate_contradictions(self, context: Dict[str, Any]) -> List[Option]:
        """ 輸出矛盾選項。執行層的 Option 數值保持確定性 """
        return context["options"] # 傳遞選項
