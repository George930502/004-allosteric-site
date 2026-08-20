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
| 2026-08-20 | P(≥1 hit in top-5), random, scoreable labels, **candidate set** | KRAS / ABL1 / myosin Site 1 (corrected tier) | **0.440 / 0.302 / 0.078** | hypergeometric; the bar a top-5 list must clear. Supersedes the 0.394/0.292/0.076 row computed over the whole node set — ADR 0011 removed the propagation source and sibling sites from the negatives too |
| 2026-08-20 | MDE AUC, 80 % power, α=0.05, scoreable sets | KRAS / ABL1 / myosin Site 1 (corrected) | 0.690 / 0.675 / 0.709 | rank-sum, residues assumed independent — an upper bound on evidence. `allo benchmark stats` |
| 2026-08-20 | MDE AUC, one effective patch | KRAS / ABL1 / myosin | **no solution below 1.0** | once spatial autocorrelation is admitted, no single target can carry the claim. `allo benchmark stats` |
| 2026-08-20 | apo heteroatom inventory | 8 distinct apo entries across 10 arms | **0 of 8** globally ligand-free | site-apo is the only reading under which this benchmark has apo members |
| 2026-08-20 | apo ligand → labels | BCR-ABL1 `1OPL` MYR+P16 | 3.29 Å, 16/20 contacted | mandated apo is holo at the predicted site; quantifies the recorded defect |
| 2026-08-20 | apo ligand → labels | KRAS `4OBE`/`4LDJ` GDP·Mg | 5.35 / 5.14 Å, 0 contacted | passes clause (ii); nucleotide is active-site, not S-IIP |
| 2026-08-20 | scoreable-label prevalence, **candidate set** | KRAS / ABL1 / myosin Site 1 (corrected tier) | **10.8 % / 6.9 % / 1.6 %** | 6.7× span drives the AUC-PR decision. Was 9.4/6.6/1.6 % over the node set (ADR 0011) |
| 2026-08-20 | matched-pair core RMSD, IHM arm | myosin `9YRG`/`9YR7` vs replaced `8ACT`/`9GZ1` | **0.88 Å over 900 res, 100 % identity** vs 11.78 Å | what a matched pair looks like; the 11.78 Å is how the mismatch was caught |
| 2026-08-20 | AUC-ROC vs AUC-PR at fixed signal (d=0.8, seed 0) | candidate-set prevalence 10.8 / 6.9 / 1.6 % | ROC 0.716/0.713/0.716; PR 0.292/0.208/0.077 | ROC flat, PR spans 3.8× — both are primary. `allo benchmark stats` |
| 2026-08-20 | AUC-PR lost by a connectivity method to the old scoring universe | identical signal (d=1.2, 400 draws), active site as negatives vs. excluded | **-62 % / -47 % / -61 %** (KRAS / ABL1 corrected / myosin S1 corrected) | the measurement behind ADR 0011. ROC moves 0.799→0.679 on KRAS; PR is where the damage is |
| 2026-08-20 | residues excluded from scoring per arm | propagation source, + sibling site on the 3 `8QYP` arms | 11–47 of 169–912 nodes (**13.6 %** of N on KRAS) | `excluded_from_scoring` in `frozen.json`; candidate set is 146–886 |
| 2026-08-20 | CryptoSite AUC, full model | literature reference | 0.83 | SVM, 3 features incl. MD pocket score (doi 10.1016/j.jmb.2016.01.029, full text) |
| 2026-08-20 | CryptoSite AUC, **MD-free** variant | literature reference | **0.74** | reference for the **cryptic-site** task, not ours. The in-domain bar is APOP (GNM, no MD, no training): 88.5 % top-3 self-reported, 15 % at Jaccard>0.5 after AlloBench's UniRef50 dedup |
| 2026-08-20 | CryptoSite AUC, best single MD feature vs 30 crystal features | literature reference | 0.73 vs 0.74 | one dynamics feature ≈ thirty static ones; the premise our method rests on |
| 2026-08-20 | covalent-ligand check (`_struct_conn`) | KRAS `6OIM` MOV | covale to Cys12, 1.805 Å | Binding MOAD would exclude the pair; deviation declared in benchmark README §1 |
| 2026-08-20 | pocket-lining RMSD vs CryptoBench 2 Å cryptic floor | all 10 frozen arms | KRAS 2.61/2.62; ABL1 **0.50** mandated, 2.38 corrected, 2.28 sensitivity; myosin 1.10/1.79/0.46/1.90/0.46 | a **difficulty** descriptor, not a pass/fail (ADR 0007) — the threshold is CryptoBench's cryptic-site entry criterion, quoted as a yardstick. What the mandated ABL1 0.50 Å says is that its apo is already in the bound conformation, which is the ligand-occupancy defect restated |
| 2026-08-20 | prior classical prediction of the S-IIP | KRAS | Grant 2011 pocket p2 (61–65, 90–99) covers **6 of 14 distal labels**, Jaccard 0.26 | 120 ns MD + FTMap, 2 years before Ostrem. The S-IIP is not an open problem; sets the novelty bar (doi 10.1371/journal.pone.0025711) |
| 2026-08-20 | ligand fit to density (RCSB validation) | `6OIM`/`5MO4`/`8QYR` | RSCC 0.908 / 0.946 / 0.915 | cryo-EM arms (`9GZ2`, `9GZ1`) carry no deposited ligand-fit score at all |
| 2026-08-20 | crystal-packing enrichment at the pocket | `4OBE` vs rest of chain | 48 % vs 40 %, OR 1.37, **p = 0.33** | confound tested, not significant; crypticity verdict survives (`4LDJ`, less packed, clashes more) |
| 2026-08-20 | apo↔holo sequence identity; mutations inside labels | all 10 frozen arms | 97.6–100 %; exactly one in-label difference, `GLY12->CYS` on `kras_g12c_mandated` | the wrong-genotype defect is now a pinned number, not a paragraph |
| 2026-08-20 | CTQW centrality on residue networks, prior art | literature | "consistently strong agreement with classical eigenvector centrality" | JACS 2026, doi 10.1021/jacs.6c08053 — the quantum bar, and what it does not do (no active-site conditioning, no apo/holo scoring) |
| 2026-08-20 | label-set invariance to alternate conformations | all 10 frozen arms | **identical on 10/10** | pockets re-derived from the primary conformer alone; 4 holos carry altlocs. Now `test_label_sets_do_not_depend_on_a_minor_conformer` under `make verify` |
| 2026-08-20 | resolution span, corrected + sensitivity entries | frozen inputs | **1.15–3.40 Å** (lowest X-ray `8QYP` 2.759 Å) | corrects a stated 1.15–3.7 Å; the draft X-ray ≤2.5 Å ceiling would have deleted a corrected arm. ADR 0009 |
| 2026-08-20 | `srx` heavy-chain extent | myosin `9YRG`:A | 912 residues, span **4–943 native MYH7**, 0 chimeric | GCN4/EGFP not modelled in the heavy chain; the frozen residue set needs no trimming |
| 2026-08-20 | apo cofactor → **scoreable** labels | KRAS `4OBE`/`4LDJ`; myosin Site 2 `8QYP` | 4.57 / 4.58 / 4.58 Å, **0 contacted** | over the full label set these read 2.78/2.79/2.47 Å with 5/5/3 contacted — every contacted residue is itself an active-site residue. Clause (iii) turns on the scoreable column; only `1OPL` fails it (3.29 Å, 16 of 20) |
| 2026-08-20 | `1OPL` RSRZ outliers | BCR-ABL1 mandated apo | **6.5 %** | wwPDB validation `percent-RSRZ-outliers`; corrects a stated 22 %, which was a percentile read as a percentage. Resolution 3.42 Å and R-free 0.315 are exact |
| 2026-08-20 | non-catalytic residues in the mandated ABL1 node set | `1OPL` vs `2G2H` | **451 vs 272** (~179 extra: SH3+SH2+linker) | most of the mandated arm's harder baseline (P(≥1) 0.204 vs 0.292) is construct extent, not the myristate defect. ADR 0010 |
| 2026-08-20 | transplant shell sensitivity | all frozen arms | `transplant_min_distance` moves ≤ 0.4 Å over shells 12/16/20/25 Å and global | the three difficulty classes never reorder; the 20 Å shell and 2.5 Å clash constants are descriptive, not load-bearing |
| 2026-08-20 | **Zheng 2023 site 1 → frozen mavacamten labels** | myosin Site 1 | **3 of 5** on `8QYP` (120, 710, 711), E=0.11, **P(≥3)=0.0001**; 2 of 5 on `9GZ3`, P=0.0022 | ESSA residues 120/121/688/693/694 (Dicty) carried onto MYH7 119/120/705/710/711 by 1MMA↔MYH7 alignment, 673 residues at 52 % identity. **Refutes the Site-1 blind claim**, using the challenge's own reference [1] |
| 2026-08-20 | arms in the primary benchmark that are blind | all 11 | **0** | was recorded as 1 (myosin Site 1) until the Zheng re-read. ASBench absence is checkable; ASD-proper and CASBench absence are not, and are no longer asserted |
