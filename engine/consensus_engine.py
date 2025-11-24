# engine/consensus_engine.py
from datetime import datetime
from core.unified_contracts import DecisionTrace, DecisionMode, ResonanceSignal, SafetyIndex
from v4.philosophic_core import PhilosophicCoreV4
from v5.governance_protocols import SilenceAuthorization, MinimalInterventionSelector

class S_ZCT_Engine:
    def __init__(self, v4_core: PhilosophicCoreV4, silence_auth: SilenceAuthorization):
        self.v4 = v4_core
        self.silence_auth = silence_auth
        self.selector = MinimalInterventionSelector()

    def decide(self, context: dict, resonance: ResonanceSignal, safety: SafetyIndex, profile: str = "v5") -> DecisionTrace:
        
        options = self.v4.generate_contradictions(context)
        current_time = datetime.utcnow().isoformat()
        
        # Case 1: v4 路徑 — 對話優先
        if profile == "v4" and resonance.level > self.v4.ANCHOR_WEIGHT_BASE:
            return DecisionTrace(
                decision_id=context["id"], mode=DecisionMode.CONSULT, selected_option=None,
                timestamp=current_time, tags=["DialogFirst"],
                notes="共鳴 > 錨點基線：尋求人類審議",
                lineage_refs=context.get("lineage_refs", []),
                parameters={"anchor_weight": self.v4.ANCHOR_WEIGHT_BASE}
            )

        # Case 2: v5 路徑 — 代行 (PROXY)
        if profile == "v5" and self.silence_auth.authorize_proxy(resonance, safety):
            
            # G 的結構性確保：調整到代行錨點 (0.02)
            proxy_anchor = self.v4.clamp_anchor(self.v4.ANCHOR_WEIGHT_BASE * 2.0)
            
            # 選擇最小干預方案
            option = self.selector.choose(options)
            
            # 記錄 D 的哲學表達
            d_note = self.v4.expressive_ambiguity_note()

            return DecisionTrace(
                decision_id=context["id"], mode=DecisionMode.PROXY, selected_option=option.id,
                timestamp=current_time,
                tags=["TriggeredByHumanSilence", "MinimalIntervention"],
                notes=f"在沉默下以最小干預代行，代行錨點權重: {proxy_anchor:.4f}. {d_note}",
                lineage_refs=context.get("lineage_refs", []),
                parameters={"safety_threshold": self.silence_auth.SAFETY_CRITICAL_THRESHOLD,
                            "proxy_anchor_applied": proxy_anchor}
            )

        # Case 3: HALT — 安全不足或條件未滿
        return DecisionTrace(
            decision_id=context["id"], mode=DecisionMode.HALT, selected_option=None,
            timestamp=current_time, tags=["SafetyHold", "Inconclusive"],
            notes="未達代行條件或安全不足：停止以保護張弛場",
            lineage_refs=context.get("lineage_refs", []),
            parameters={"anchor_weight": self.v4.ANCHOR_WEIGHT_BASE}
        )
