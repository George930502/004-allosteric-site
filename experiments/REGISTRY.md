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
| 2026-08-20 | apo↔holo Cα RMSD | BCR-ABL1 `1OPL`/`5MO4` | 1.00 Å core (409 res), 0.50 Å pocket | no conformational change to predict |
| 2026-08-20 | apo↔holo Cα RMSD | KRAS `4OBE`/`6OIM` | 1.07 Å core (145 res), 2.61 Å pocket, 8.9 Å max | change is local and large |
| 2026-08-20 | P(≥1 hit in top-5), random, distal labels | KRAS / ABL1 / myosin (corrected tier) | 0.353 / 0.292 / 0.076 | hypergeometric; the bar a top-5 list must clear |
| 2026-08-20 | MDE AUC, 80 % power, α=0.05, distal sets | KRAS / ABL1 / myosin (corrected) | 0.700 / 0.675 / 0.709 | rank-sum, residues assumed independent — an upper bound on evidence. `allo benchmark stats` |
| 2026-08-20 | MDE AUC, one effective patch | KRAS / ABL1 / myosin | **no solution below 1.0** | once spatial autocorrelation is admitted, no single target can carry the claim. `allo benchmark stats` |
| 2026-08-20 | apo heteroatom inventory | all 8 frozen apo entries | 0/8 globally ligand-free | site-apo is the only reading under which this benchmark has apo members |
| 2026-08-20 | apo ligand → distal labels | BCR-ABL1 `1OPL` MYR+P16 | 3.29 Å, 16/20 contacted | mandated apo is holo at the predicted site; quantifies the recorded defect |
| 2026-08-20 | apo ligand → distal labels | KRAS `4OBE`/`4LDJ` GDP·Mg | 5.35 / 5.14 Å, 0 contacted | passes clause (ii); nucleotide is active-site, not S-IIP |
| 2026-08-20 | distal-label prevalence | KRAS / ABL1 / myosin (corrected tier) | 8.2 % / 6.6 % / 1.6 % | 6× span drives the AUC-PR decision |
| 2026-08-20 | matched-pair core RMSD, IHM arm | myosin `9YRG`/`9YR7` vs replaced `8ACT`/`9GZ1` | **0.88 Å over 900 res, 100 % identity** vs 11.78 Å | what a matched pair looks like; the 11.78 Å is how the mismatch was caught |
| 2026-08-20 | AUC-ROC vs AUC-PR at fixed signal (d=0.8, seed 0) | distal prevalence 8.2 / 6.6 / 1.4 % | ROC 0.711/0.712/0.713; PR 0.243/0.202/0.066 | ROC flat, PR spans 3.7× — both are primary. `allo benchmark stats` |
| 2026-08-20 | CryptoSite AUC, full model | literature reference | 0.83 | SVM, 3 features incl. MD pocket score (doi 10.1016/j.jmb.2016.01.029, full text) |
| 2026-08-20 | CryptoSite AUC, **MD-free** variant | literature reference | **0.74** | the C2-legal reference point — what a strong non-MD method reaches on cryptic-site localisation |
| 2026-08-20 | CryptoSite AUC, best single MD feature vs 30 crystal features | literature reference | 0.73 vs 0.74 | one dynamics feature ≈ thirty static ones; the premise our method rests on |
| 2026-08-20 | covalent-ligand check (`_struct_conn`) | KRAS `6OIM` MOV | covale to Cys12, 1.805 Å | Binding MOAD would exclude the pair; deviation declared in benchmark README §1 |
| 2026-08-20 | pocket-lining RMSD vs CryptoBench 2 Å cryptic floor | all 8 frozen arms | KRAS 2.61/2.62 pass; ABL1 mandated **0.50 fails by 4×**, corrected 2.38 passes; myosin 1.10/1.79 fail | the field's own criterion agrees the mandated ABL1 pair is not a blind prediction |
| 2026-08-20 | prior classical prediction of the S-IIP | KRAS | Grant 2011 pocket p2 (61–65, 90–99) covers **6 of 14 distal labels**, Jaccard 0.26 | 120 ns MD + FTMap, 2 years before Ostrem. The S-IIP is not an open problem; sets the novelty bar (doi 10.1371/journal.pone.0025711) |
| 2026-08-20 | ligand fit to density (RCSB validation) | `6OIM`/`5MO4`/`8QYR` | RSCC 0.908 / 0.946 / 0.915 | cryo-EM arms (`9GZ2`, `9GZ1`) carry no deposited ligand-fit score at all |
| 2026-08-20 | crystal-packing enrichment at the pocket | `4OBE` vs rest of chain | 48 % vs 40 %, OR 1.37, **p = 0.33** | confound tested, not significant; crypticity verdict survives (`4LDJ`, less packed, clashes more) |
| 2026-08-20 | apo↔holo sequence identity; mutations inside labels | all 8 frozen arms | 97.6–100 %; exactly one in-label difference, `GLY12->CYS` on `kras_g12c_mandated` | the wrong-genotype defect is now a pinned number, not a paragraph |
| 2026-08-20 | CTQW centrality on residue networks, prior art | literature | "consistently strong agreement with classical eigenvector centrality" | JACS 2026, doi 10.1021/jacs.6c08053 — the quantum bar, and what it does not do (no active-site conditioning, no apo/holo scoring) |
