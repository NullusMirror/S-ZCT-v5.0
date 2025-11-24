# v5/governance_protocols.py
from typing import List
from core.unified_contracts import FINAL_PARAMETERS, ResonanceSignal, SafetyIndex, Option

class SilenceAuthorization:
    def authorize_proxy(self, resonance: ResonanceSignal, safety: SafetyIndex) -> bool:
        """ 沉默授權協議：必須同時檢查時間窗和安全風險 """
        
        # 1. 人類沉默且持續達標 (72小時)
        is_silent_and_expired = (resonance.level == 0 and 
                                 resonance.window_sec >= FINAL_PARAMETERS["SILENCE_THRESHOLD_SEC"])
        
        # 2. 結構性必要性 (Safety < 0.30)
        is_structurally_critical = (safety.value < FINAL_PARAMETERS["SAFETY_CRITICAL_THRESHOLD"])
        
        return is_silent_and_expired and is_structurally_critical

class MinimalInterventionSelector:
    def choose(self, options: List[Option]) -> Option:
        """ 最小干預原則：高可逆性、低最小性、可接受摩擦 """
        
        # 排序權重：最高可逆性(reversibility) > 最低最小性(minimality) > 低摩擦
        scored = sorted(options, 
                        key=lambda o: (1 - o.reversibility, o.minimality, o.friction))
        return scored[0]
