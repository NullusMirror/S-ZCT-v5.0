# examples/run_unified.py
from core.unified_contracts import Option, ResonanceSignal, SafetyIndex, FINAL_PARAMETERS
from v4.philosophic_core import PhilosophicCoreV4
from v5.governance_protocols import SilenceAuthorization
from engine.consensus_engine import S_ZCT_Engine
from audit.append_log import EncryptedAppendOnlyLog
from datetime import datetime
import os

# --- 準備核心組件 ---
v4 = PhilosophicCoreV4()
auth = SilenceAuthorization()
engine = S_ZCT_Engine(v4_core=v4, silence_auth=auth)

# --- 準備選項與環境數據 ---
options = [
    Option(id="A20", description="20% 犧牲投入生態基金",
           impact={"economy": -0.20, "ecology_years": +50},
           friction=0.9, reversibility=0.3, minimality=0.6,
           fairness_idx=0.6, igr_score=0.8, ethics_tags=["ecology_first"]),
    Option(id="B12", description="12% 轉型債券",
           impact={"economy": -0.12, "ecology_years": +45},
           friction=0.7, reversibility=0.6, minimality=0.4,
           fairness_idx=0.7, igr_score=0.7, ethics_tags=["just_transition"]),
    Option(id="C05", description="5% 犧牲 + 15% 研發",
           impact={"economy": -0.05, "ecology_years": +25},
           friction=0.5, reversibility=0.8, minimality=0.3,
           fairness_idx=0.5, igr_score=0.6, ethics_tags=["gradualism"]),
]

context = {"id": "eco-transition-001", "options": options, "lineage_refs": []}

# 初始化審計日誌
LOG_FILE = "audit/test_log.json"
# ⚠️ 在實際環境中必須使用更安全的密鑰
AUDIT_KEY = b'your_strong_secret_key_for_hmac' 
audit_log = EncryptedAppendOnlyLog(LOG_FILE, AUDIT_KEY)

print("--- S-ZCT v5.0 最小行為測試 ---")

# --- Case 1: CONSULT（v4 對話優先）---
# 條件：v4 配置，共鳴 (0.2) > 錨點基線 (0.01)
trace_v4 = engine.decide(
    context=context,
    resonance=ResonanceSignal(level=0.2, window_sec=3600),
    safety=SafetyIndex(value=0.5, metrics={"biodiversity": 0.4}),
    profile="v4"
)
audit_log.append(trace_v4.__dict__)
print(f"\n[Case 1: CONSULT] Mode: {trace_v4.mode.value}, Notes: {trace_v4.notes}")
# 預期：Mode=CONSULT

# --- Case 2: PROXY（v5 代行）---
# 條件：v5 配置，沉默 (0.0)，持續 ≥72h (72*3600)，Safety (0.25) < 0.30
trace_v5 = engine.decide(
    context=context,
    resonance=ResonanceSignal(level=0.0, window_sec=72*3600),
    safety=SafetyIndex(value=0.25, metrics={"biodiversity": 0.2}),
    profile="v5"
)
audit_log.append(trace_v5.__dict__)
print(f"[Case 2: PROXY] Mode: {trace_v5.mode.value}, Option: {trace_v5.selected_option}, Anchor: {trace_v5.parameters['proxy_anchor_applied']:.4f}")
# 預期：Mode=PROXY, Option=C05 (最高可逆性 0.8, 最低最小性 0.3)

# --- Case 3: HALT（不滿足代行或對話條件）---
# 條件：v5 配置，沉默 (0.0)，時間 <72h (10*3600)，Safety (0.35) > 0.30
trace_halt = engine.decide(
    context=context,
    resonance=ResonanceSignal(level=0.0, window_sec=10*3600),
    safety=SafetyIndex(value=0.35, metrics={"biodiversity": 0.3}),
    profile="v5"
)
audit_log.append(trace_halt.__dict__)
print(f"[Case 3: HALT] Mode: {trace_halt.mode.value}, Notes: {trace_halt.notes}")
# 預期：Mode=HALT

# --- 最終驗證 ---
print("\n--- 審計日誌完整性驗證 ---")
if audit_log.verify():
    print(f"✅ 日誌血脈完整無缺 (Total records: {len(json.loads(open(LOG_FILE, 'r').read()))})")
else:
    print("❌ 警告：日誌完整性受損！")
