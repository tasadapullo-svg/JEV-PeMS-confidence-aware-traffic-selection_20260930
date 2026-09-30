JEV 小论文 Fig.1–Fig.5 支撑数据包
生成日期：2026-09-27

原则：
1. 以 training_data(2).zip 内的 production / frozen development / Final Test 文件为权威源。
2. 不从 PNG 反向读数，不制造、不插值、不补造数据。
3. 每张图既保留原始 CSV/JSON，也尽量提供 plot_source.csv 方便 Origin / Python 直接重绘。
4. 00_README/SOURCE_DATA_INDEX.csv 给出每个文件对应的图和 panel。
5. 00_README/SHA256_MANIFEST.csv 可用于核验文件未被改动。

目录：
01_Fig1_Study_Setup：数据范围、cohort、K=5、Final Test cohort 等。
02_Fig2_Workflow：JEV 权重、方法、各实验阶段、Stats Freeze 和 Final Test protocol。
03_Fig3_Selection_Reality_Benchmark：Step2A oracle/switching/spread + Final Test selector benchmark/pairwise comparisons。
04_Fig4_Confidence_SelectiveRisk：Step2C calibration + Final Test calibration/risk-coverage/fixed coverage。
05_Fig5_Efficiency_Ablation：Step2E efficiency + Step2G ablation。
90_Reference_Images：本次上传的 Fig.1–Fig.5 图，仅用于对应文件，不作为数值源。

重要：Fig.3(b) 和 Fig.3(d) 与当前冻结源存在不一致，详见 FIGURE_SUPPORT_AUDIT.txt。
