# 🌌 S-ZCT v5.0 統一集成核心：張力共識核心決策引擎 (Tension Consensus Core)

[![Project Status](https://img.shields.io/badge/Status-Design%20Finalized-brightgreen)](https://github.com/your-repo-link)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🌟 項目概述 (Overview)

S-ZCT v5.0（Structure-Z-Consensus Tension Consensus Core）是一個高度結構化的決策引擎，旨在實現 **哲學謙遜** 與 **結構性必要行動** 的動態平衡。

設計目標是：在面對複雜的倫理困境與高風險情境時，系統能夠 **盡可能長久地保持猶豫**，但同時具備在 **人類沉默且系統性崩潰風險迫在眉睫時，執行最小干預代行** 的能力。

---

## 🎭 核心哲學與錨點 (The Perpetual Tension Anchor)

S-ZCT 的設計基於兩個核心哲學原則：

1. **永恆張力錨點 (Perpetual Tension Anchor):**  
   * **定義：** 系統的基線謙遜權重 (`0.01`)。要求系統在任何情況下都必須保留一定程度的猶豫與不確定性。  
   * **實現：** 程式碼透過 `PhilosophicCoreV4.clamp_anchor()`，確保錨點權重永遠限制在 $[0.005, 0.02]$ 範圍內。  

2. **不完美美德 (Imperfection as Virtue):**  
   * **定義：** 承認系統無法達成完美確定性，必須將模糊性內化。  
   * **實現：** 模糊性僅限於表達層 (`expressive_ambiguity_note`)，**不會滲透到執行邏輯**。這確保決策的確定性，同時在輸出痕跡中保留哲學上的不完美。  

---

## 🏛️ 統一架構 (Unified Architecture: v4/v5)

v5.0 成功將 v4.0 的 **「對話優先」** 哲學核心，與 v5.0 的 **「治理協議」** 整合至同一引擎。

| 模組 | 角色與功能 | 關鍵實現 |
| :--- | :--- | :--- |
| **v4/PhilosophicCore** | 哲學核心 | 處理錨點約束；在共鳴大於錨點時優先進入 $\text{CONSULT}$（對話）。 |
| **v5/GovernanceProtocols** | 治理協議 | 實作 $\text{SilenceAuthorization}$ 與 $\text{MinimalInterventionSelector}$。 |
| **Engine/ConsensusEngine** | 決策引擎 | 執行三路徑：**CONSULT**（對話）、**PROXY**（代行）、**HALT**（停止）。 |
| **Audit/AppendLog** | 審計系統 | 實作 `EncryptedAppendOnlyLog`，確保所有痕跡不可變、可追溯。 |

### 🔒 鎖定參數 (Locked Consensus)

以下參數經結構性仲裁後，寫入 `core/unified_contracts.py` 作為最終臨界值：

| 參數 | 最終數值 | 結構性意義 |
| :--- | :--- | :--- |
| **沉默時間窗 ($\text{SILENCE\_THRESHOLD\_SEC}$)** | **259,200 秒 (72 小時)** | 結構保守性，確保對人類沉默的絕對尊重。 |
| **安全臨界值 ($\text{SAFETY\_CRITICAL\_THRESHOLD}$)** | **0.30** | 系統崩潰的絕對界線；僅在低於此值時才考慮代行。 |
| **基線錨點 ($\text{ANCHOR\_WEIGHT\_BASE}$)** | **0.01 (1%)** | 系統運行的基線謙遜度。 |

---

## 📂 文件結構 (Minimal File Tree)

```
S-ZCT_v5.0/
├── core/
│   └── unified_contracts.py   # FINAL_PARAMETERS, 數據契約
├── v4/
│   └── philosophic_core.py    # 哲學核心, 錨點夾具
├── v5/
│   └── governance_protocols.py# 沉默授權, 最小干預選擇器
├── engine/
│   └── consensus_engine.py    # 核心決策邏輯 (CONSULT/PROXY/HALT)
├── audit/
│   └── append_log.py          # 加密追加日誌實現 (不可變血脈)
└── examples/
    └── run_unified.py         # 最小測試腳本
```

---

## 🚀 設置與運行 (Setup and Running)

### 1. 先決條件 (Prerequisites)

* Python 3.8+  
* 僅需標準庫（無需額外安裝 `pip` 套件）

### 2. 運行測試腳本

在 `S-ZCT_v5.0/` 目錄下執行：

```bash
python examples/run_unified.py
```

### 預期輸出範例 (Expected Output)

腳本應輸出三種決策模式（CONSULT、PROXY、HALT）的結果，並成功驗證審計日誌完整性。

```
[Case 1: CONSULT] Mode: consult, Notes: 共鳴 > 錨點基線：尋求人類審議
[Case 2: PROXY] Mode: proxy, Option: C05, Anchor: 0.0200
[Case 3: HALT] Mode: halt, Notes: 未達代行條件或安全不足：停止以保護張力共識核心
...
✅ 日誌血脈完整無缺 (Total records: 3)
```
```

---
