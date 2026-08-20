# Experiment registry

Newest last. One line each: date · slug · target · method · headline metric · verdict.

| Date | Experiment | Target | Method | Headline | Verdict |
|---|---|---|---|---|---|
| — | *(none yet — Phase 1 baselines go here first)* | | | | |

## Benchmark characterisation (not method runs)

Structural numbers are pinned by `docs/benchmark/frozen.json` (`uv run allo benchmark verify`);
statistical ones by `uv run allo benchmark stats` (seed 0). Rows citing literature are not
repo-derived and say so.

| Date | Quantity | Target | Value | Note |
|---|---|---|---|---|
| 2026-08-20 | ligand-transplant clash | KRAS `4OBE`←`6OIM` | 0.75 Å, 14/41 atoms | pocket genuinely cryptic |
| 2026-08-20 | ligand-transplant clash | KRAS `4LDJ`←`6OIM` | 0.69 Å, 18/41 atoms | corrected apo, also cryptic |
| 2026-08-20 | ligand-transplant clash | BCR-ABL1 `1OPL`←`5MO4` | 2.60 Å, 0/31 atoms | pocket pre-formed, not cryptic |
| 2026-08-20 | ligand-transplant clash | BCR-ABL1 `2G2H`←`5MO4` | 1.95 Å, 2/31 atoms | myristate-free apo, still pre-formed |
| 2026-08-20 | ligand-transplant clash | myosin `9GZ3`←`9GZ2` | 2.63 Å, 0/20 atoms | pocket pre-formed |
| 2026-08-20 | apo↔holo Cα RMSD | BCR-ABL1 `1OPL`/`5MO4` | 1.00 Å core (409 res), 0.50 Å pocket | pocket is pre-formed — a difficulty axis, not a defect (ADR 0007) |
| 2026-08-20 | apo↔holo Cα RMSD | KRAS `4OBE`/`6OIM` | 1.07 Å core (145 res), 2.61 Å pocket, 8.9 Å max | change is local and large |
| 2026-08-20 | P(≥1 hit in top-5), random, scoreable labels, **candidate set** | KRAS / ABL1 / myosin Site 1 (corrected tier) | **0.440 / 0.302 / 0.081** | hypergeometric; the bar a top-5 list must clear. Supersedes the 0.394/0.292/0.076 row computed over the whole node set — ADR 0011 removed the propagation source and registered functional sites from the negatives too |
| 2026-08-20 | MDE AUC, 80 % power, α=0.05, scoreable sets | KRAS / ABL1 / myosin Site 1 (corrected) | 0.690 / 0.675 / 0.709 | rank-sum, residues assumed independent — an upper bound on evidence. `allo benchmark stats` |
| 2026-08-20 | MDE AUC, one effective patch | KRAS / ABL1 / myosin | **no solution below 1.0** | once spatial autocorrelation is admitted, no single target can carry the claim. `allo benchmark stats` |
| 2026-08-20 | apo heteroatom inventory | 8 distinct apo entries across 11 scoreable arms | **0 of 8** globally ligand-free | site-apo is the only reading under which this benchmark has apo members |
| 2026-08-20 | apo ligand → labels | BCR-ABL1 `1OPL` MYR+P16 | 3.29 Å, 16/20 contacted | mandated apo is holo at the predicted site; quantifies the recorded defect |
| 2026-08-20 | apo ligand → labels, strict-C5 scope | BCR-ABL1 `bcr_abl1_trimmed` | 3.47 Å, 13/17 contacted | same `1OPL` bytes, UniProt-derived 261–512 node range; trimming does not repair site occupancy |
| 2026-08-20 | apo ligand → labels | KRAS `4OBE`/`4LDJ` GDP·Mg | 5.35 / 5.14 Å, 0 contacted | passes clause (ii); nucleotide is active-site, not S-IIP |
| 2026-08-20 | scoreable-label prevalence, **candidate set** | KRAS / ABL1 / myosin Site 1 (corrected tier) | **10.8 % / 6.9 % / 1.6 %** | 6.7× span drives the AUC-PR decision. Was 9.4/6.6/1.6 % over the node set (ADR 0011) |
| 2026-08-20 | matched-pair core RMSD, IHM arm | myosin `9YRG`/`9YR7` vs replaced `8ACT`/`9GZ1` | **0.88 Å over 900 res, 100 % identity** vs 11.78 Å | what a matched pair looks like; the 11.78 Å is how the mismatch was caught |
| 2026-08-20 | AUC-ROC vs AUC-PR at fixed signal (d=0.8, seed 0) | candidate-set prevalence 10.8 / 6.9 / 1.6 % | ROC 0.714/0.713/0.716; PR 0.290/0.208/0.076 | target-specific deterministic streams; adding an arm cannot move existing baselines. `allo benchmark stats` |
| 2026-08-20 | AUC-PR lost by a connectivity method to the old scoring universe | identical signal (d=1.2, 400 draws), active site as negatives vs. excluded | **-62 % / -47 % / -61 %** (KRAS / ABL1 corrected / myosin S1 corrected) | the measurement behind ADR 0011. ROC moves 0.799→0.679 on KRAS; PR is where the damage is |
| 2026-08-20 | residues excluded from scoring per arm | propagation source + per-protein functional-site registry | 11–51 of 169–912 nodes (**13.6 %** of N on KRAS) | `excluded_from_scoring` in `frozen.json`; candidate set is 146–861. ADR 0015 now freezes the registry explicitly, so adding an arm cannot move another arm's universe |
| 2026-08-20 | CryptoSite AUC, full model | literature reference | 0.83 | SVM, 3 features incl. MD pocket score (doi 10.1016/j.jmb.2016.01.029, full text) |
| 2026-08-20 | CryptoSite AUC, **MD-free** variant | literature reference | **0.74** | reference for the **cryptic-site** task, not ours. The in-domain bar is APOP (GNM, no MD, no training): 88.5 % top-3 self-reported, 15 % at Jaccard>0.5 after AlloBench's UniRef50 dedup |
| 2026-08-20 | CryptoSite AUC, best single MD feature vs 30 crystal features | literature reference | 0.73 vs 0.74 | one dynamics feature ≈ thirty static ones; the premise our method rests on |
| 2026-08-20 | covalent-ligand check (`_struct_conn`) | KRAS `6OIM` MOV | covale to Cys12, 1.805 Å | Binding MOAD would exclude the pair; deviation declared in benchmark README §1 |
| 2026-08-20 | pocket-lining RMSD vs CryptoBench 2 Å cryptic floor | all 11 scoreable arms | KRAS 2.61/2.62; ABL1 **0.50** mandated, 2.38 corrected, 2.28 sensitivity, **0.37 trimmed**; myosin 1.10/1.79/0.46/1.90/0.46 | a **difficulty** descriptor, not a pass/fail (ADR 0007) — the threshold is CryptoBench's cryptic-site entry criterion, quoted as a yardstick. The two 1OPL views show the occupied site already in the bound conformation |
| 2026-08-20 | prior classical prediction of the S-IIP | KRAS | Grant 2011 pocket p2 (61–65, 90–99) covers **6 of 16 scoreable labels**, Jaccard 0.24 | 120 ns MD + FTMap, 2 years before Ostrem. The S-IIP is not an open problem; sets the novelty bar (doi 10.1371/journal.pone.0025711) |
| 2026-08-20 | ligand fit to density (RCSB validation) | `6OIM`/`5MO4`/`8QYR` | RSCC 0.908 / 0.946 / 0.915 | cryo-EM arms (`9GZ2`, `9GZ1`) carry no deposited ligand-fit score at all |
| 2026-08-20 | crystal-packing enrichment at the pocket | `4OBE` vs rest of chain | 48 % vs 40 %, OR 1.37, **p = 0.33** | confound tested, not significant; crypticity verdict survives (`4LDJ`, less packed, clashes more) |
| 2026-08-20 | apo↔holo sequence identity; mutations inside labels | all 11 scoreable arms | 97.6–100 %; exactly one in-label difference, `GLY12->CYS` on `kras_g12c_mandated` | the wrong-genotype defect is now a pinned number, not a paragraph |
| 2026-08-20 | CTQW centrality on residue networks, prior art | literature | "consistently strong agreement with classical eigenvector centrality" | JACS 2026, doi 10.1021/jacs.6c08053 — the quantum bar, and what it does not do (no active-site conditioning, no apo/holo scoring) |
| 2026-08-20 | label-set invariance to alternate conformations | all 11 scoreable arms | **identical on 11/11** | pockets re-derived from the primary conformer alone; 4 holos carry altlocs. `test_label_sets_do_not_depend_on_a_minor_conformer` under `make verify` |
| 2026-08-20 | resolution span, corrected + sensitivity entries | frozen inputs | **1.15–3.40 Å** (lowest X-ray `8QYP` 2.759 Å) | corrects a stated 1.15–3.7 Å; the draft X-ray ≤2.5 Å ceiling would have deleted a corrected arm. ADR 0009 |
| 2026-08-20 | `srx` heavy-chain extent | myosin `9YRG`:A | 912 residues, span **4–943 native MYH7**, 0 chimeric | GCN4/EGFP not modelled in the heavy chain; the frozen residue set needs no trimming |
| 2026-08-20 | apo cofactor → **scoreable** labels | KRAS `4OBE`/`4LDJ`; myosin Site 2 `8QYP` | 4.57 / 4.58 / 4.58 Å, **0 contacted** | over the full label set these read 2.78/2.79/2.47 Å with 5/5/3 contacted — every contacted residue is itself an active-site residue. The two `1OPL` views fail clause (iii): 3.29 Å, 16/20 whole-chain; 3.47 Å, 13/17 trimmed |
| 2026-08-20 | `1OPL` RSRZ outliers | BCR-ABL1 mandated apo | **6.5 %** | wwPDB validation `percent-RSRZ-outliers`; corrects a stated 22 %, which was a percentile read as a percentage. Resolution 3.42 Å and R-free 0.315 are exact |
| 2026-08-20 | strict-C5 node-set sensitivity | `1OPL` whole chain vs same-byte trim | **451 vs 252** nodes; P(≥1) **0.208 vs 0.309** | explicit UniProtKB 2026_02 range isolates construct extent from crystal choice. ADR 0010 |
| 2026-08-20 | transplant shell sensitivity | all frozen arms | `transplant_min_distance` moves ≤ 0.4 Å over shells 12/16/20/25 Å and global | the three difficulty classes never reorder; the 20 Å shell and 2.5 Å clash constants are descriptive, not load-bearing |
| 2026-08-20 | **Zheng 2023 site 1 → frozen mavacamten labels** | myosin Site 1 | **3 of 5** on `8QYP` (120, 710, 711), E=0.11, **P(≥3)=0.0001**; 2 of 5 on `9GZ3`, P=0.0022 | ESSA residues 120/121/688/693/694 (Dicty) carried onto MYH7 119/120/705/710/711 by 1MMA↔MYH7 alignment, 673 residues at 52 % identity. **Refutes the Site-1 blind claim**, using the challenge's own reference [1] |
| 2026-08-20 | arms in the primary benchmark that are blind | all 12 manifest arms (11 scoreable) | **0** | was recorded as 1 (myosin Site 1) until the Zheng re-read. ASBench absence is checkable; ASD-proper and CASBench absence are not, and are no longer asserted |
| 2026-08-20 | orthosteric-state classification | all 11 scoreable arms | SO4 and DMS recorded as additives; x-ray Site 1 remains VO4→BEF unmatched; omecamtiv and Site 2 are matched | only manifest-vocabulary components contacting mapped active residues decide state; effectors are separate |
| 2026-08-20 | pair-audit re-run | all 11 scoreable arms | KRAS coupling minima **1.32/1.31 Å**; core-frame scoreable medians **1.53/1.21 Å** | replaces stale 3.37/3.43 Å and 1.88/1.63 Å values; embedded script enumerates `sorted(frozen)` |
| 2026-08-20 | null type-I acceptance criterion | 1,000 independent replicates at α=0.05 | **37–64 rejections; [0.037, 0.064]** | central equal-tailed 95 % Binomial(1000, 0.05) prediction interval; replaces ad hoc [0.02, 0.08] |
| 2026-08-20 | exact frozen structure corpus | 17 unique benchmark entries | **22,712,256 bytes raw; 5,465,227 deterministic-gzip bytes** | all 15 pinned entries are byte-identical to their wwPDB versioned artifacts; all 17 are retained offline under partitioned `structures/apo` and `structures/holo` (ADR 0014) |
