# Global Quantum + AI Challenge 2026 — Cleveland Clinic Enterprise Challenge Statement

> Official reference document. Source: `docs/Cleveland-Clinic-Challenge-Statement-vF.pdf` (10 pages, A4, created 2026-04-17).
> This file is a faithful, complete restatement of the challenge statement. Anything marked _[note]_ is our annotation, not source text.

---

## 1. Challenge Title

**Unlocking undruggable targets: quantum simulation of allosteric signal propagation**

---

## 2. Executive Summary

- Over **85% of disease-causing proteins are currently considered undruggable**. They lack deep, obvious active sites where traditional small-molecule drugs can bind.
- For these intractable targets, **the only viable therapeutic strategy is allostery**: identifying hidden **distal regulatory pockets on the protein surface** [1,2] that, when bound, **transmit a signal to shut down the active site from a distance** [3–6].
- Unlocking allosteric targeting would revolutionize drug discovery, enabling therapeutic intervention for historically intractable diseases driving **cancer, heart disease**, and many other therapeutic areas. For the global healthcare industry this unlocks a **new paradigm of drug design**, offering hope to patients with currently untreatable conditions.
- **Detecting these hidden communication channels classically is computationally prohibitive.** It requires **months of Molecular Dynamics (MD) simulations** to observe the rare fluctuations that transmit signals across a protein structure. Current approximations are **often too linear** to capture the complex, **non-linear dynamics** of biological signal propagation, leaving vast areas of the proteome unexplored [7–9].
- **Quantum computers offer a unique advantage** in simulating **non-local correlations and interference effects**, which are analogous to how biological signals propagate through a complex protein network [10,11].
- **The ask:** hypothesize and demonstrate that **quantum information propagation can identify allosteric pathways more accurately or more efficiently than classical diffusive models**.
- **Deliverable in one sentence:** develop a **quantum algorithm approach that takes a protein structure as input and identifies potential allosteric sites** based on structural fluctuations or via **dynamic connectivity to an active site**.

---

## 3. Industrial and Operational Context

### The bottleneck being addressed

This challenge targets a critical bottleneck at the **very beginning of the pharmaceutical R&D value chain: the target identification and validation phase.**

### Eroom's Law

The industry faces the productivity problem described as **Eroom's Law** [12] (Figure 1 in the PDF, p.3): the **inflation-adjusted cost of developing a new drug has historically doubled approximately every nine years** since the 1950s. A primary driver of this inefficiency is the **high attrition rate of clinical candidates that fail because they targeted the wrong mechanism, or because the target protein is simply undruggable** (i.e., poor target validation).

### The current (classical) workflow and where it fails

1. Medicinal chemists and structural biologists identify a target protein directly implicated in the pathogenesis of a specific disease.
2. High-resolution structures are retrieved from the **Protein Data Bank (PDB)** [13] — obtained via **X-ray crystallography, NMR, or Cryo-EM**.
3. These models serve as a base for **structure-based drug design**, where **classical docking software scans for deep, hydrophobic pockets** suitable for small-molecule binding [14].
4. **Failure mode:** if the protein's active site is **too flat, featureless, involved in Protein–Protein Interfaces (PPIs), or solvent-exposed** — which is the case for the **majority of the human proteome** — traditional approaches fail. The target is **deprioritized and categorized as "undruggable"**, leaving vast areas of potentially high-value intellectual property and therapeutic benefit unexplored.
5. Even when a target is selected, the next step is often **high-throughput screening** (millions of compounds physically tested). This is **prohibitively expensive and inefficient if performed blindly**, without knowing where on the protein surface to target.

### The proposed solution's place in the value chain

Insert a **quantum-enabled "allosteric scanner" directly upstream of the more expensive classical screening steps.**

Operationalized within a computational biology unit, this tool would:

- **Ingest static PDB structures of "failed" targets**, and
- **Output a dynamic probability map of cryptic/allosteric binding sites.**

This output serves as a **strategic roadmap for medicinal chemists**, letting them focus library design on specific protein-surface regions that are **mechanistically connected to disease function**.

**The paradigm shift:** from **static pocket detection** → to **quantum-enabled dynamic signal mapping**.

**Claimed impact:** potential to **rescue thousands of high-value biological targets**, drastically **reduce the cost of physical screening**, and ultimately **lower the clinical attrition rate** by **validating the mechanism of action before a screening campaign or drug synthesis**.

---

## 4. Challenge Objective

### 4.1 Primary Objective _(the single most important objective)_

**Maximize the predictive accuracy of the quantum algorithm in identifying experimentally validated allosteric sites.**

Requirements:

- Participants **must build a quantum circuit that simulates signal propagation through the protein structure**.
- The circuit must output a **ranking of residues based on their dynamic connectivity** — in most cases, connectivity **to an active site**.
- **Success is defined by** the algorithm's ability to assign **statistically significantly higher scores to known distal regulatory residues** compared to:
  - **random background residues**, and
  - **non-functional surface pockets**.
- **Participants are free to hypothesize and define the specific quantum metric** that serves as the proxy for this biological signal.

### 4.2 Secondary Objectives _(for real-world deployability)_

| Objective                                | Requirement                                                                                                                                                                                                                                                           |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Noise resilience**                     | Algorithms must be **robust against noise inherent in current quantum processors**, demonstrating **stability of the signal-propagation metric despite gate errors and limited coherence times**.                                                                     |
| **Scalability / coarse-graining**        | Many relevant protein targets **exceed the qubit capacity of current devices if mapped 1-to-1**. Participants should **demonstrate a method for coarse-graining the protein structure** and **prove that this compression retains the essential topological signal**. |
| **Interpretability / low entry barrier** | Lower the entry level so **medicinal chemists can leverage quantum algorithms without extensive training**.                                                                                                                                                           |
| **Actionable output**                    | Prioritize **3D visualization of the quantum connectivity maps**, plus **clear logic linking the chosen quantum metric to the biological phenomenon**.                                                                                                                |
| **Classical comparison**                 | **Comparison to classical analogs, where relevant, should be analyzed.**                                                                                                                                                                                              |

---

## 5. Problem Definition

### Inputs

Structural data for a set of **benchmark proteins obtained from the RCSB Protein Data Bank**.

### Required Outputs (all three)

1. **The Connectivity Matrix** — an **N × N matrix** where entry **(i, j)** represents the **calculated quantum connectivity strength between residue i and residue j**.
2. **The Hit List** — a **ranked list of the top 5 predicted allosteric sites (residue indices) for each target protein**.
3. **Methodological Report** — a **brief explanation of the quantum metric chosen and why it serves as a proxy for biological signal transmission**.

### Constraints

1. **Hardware:** Solutions may leverage **gate-based quantum, quantum-inspired, or hybrid** approaches — **provided the proposal demonstrates a credible path to execution on near-term or fault-tolerant quantum hardware**.
2. **Circuit Depth:** Proposals **must demonstrate awareness of coherence time limitations**. **Deep, unoptimized circuits that cannot run on near-term hardware will be penalized.**
3. **No Classical MD:** The solution **cannot rely on classical MD trajectories as inputs**. The goal is to **predict the dynamics _ab initio_ from topology**.
4. **Provided infrastructure:** Participants will have access to **AWS Braket** and **Classiq** services, provided as part of the challenge infrastructure **at no cost**.

### Scope and Assumptions

- **Included:** the **catalytic domains** of the proteins.
- **Excluded:** **solvents (water molecules), co-factors, and complex post-translational modifications** — _unless modeled as simple nodes_.
- **Assumption:** the **elastic network hypothesis** [8,15,16] — i.e., **the topology of the contact network is the primary driver of signal propagation**, allowing us to **abstract away specific atomic force fields**.

---

## 6. Data and Resources

- Protein structures are sourced from the **public RCSB PDB (rcsb.org)**.
- Participants are **encouraged to use open-source frameworks (like Qiskit [17]) to ensure reproducibility**.
- Validation design: the challenge uses **specific targets that were historically considered undruggable until a specific allosteric pocket was characterized**.
- **Critical rule:** participants must use the **unbound (apo) structure as input** and **blind-predict the location of the allosteric pocket** known to exist in the **drug-bound (holo) validation structure**.

### Table 1 — Validation Targets

| Target (Disease Area)           | Protein Class   | Challenge Objective                                                                            | Input Structure (apo) | Validation Structure (holo) |
| ------------------------------- | --------------- | ---------------------------------------------------------------------------------------------- | --------------------- | --------------------------- |
| **KRAS G12C** (Oncology)        | GTPase          | Identify the **cryptic "Switch-II" pocket** locked by **Sotorasib (AMG 510)** [18,19]          | **4OBE**              | **6OIM**                    |
| **BCR-ABL1** (Oncology)         | Tyrosine Kinase | Identify the **distal "Myristoyl" pocket** used by **Asciminib** to bypass resistance [20,21]  | **1OPL**              | **5MO4**                    |
| **Cardiac Myosin** (Cardiology) | Motor Protein   | Identify the **mechanical site where Mavacamten stabilizes the "super-relaxed state"** [22,23] | **5TBY**              | **6C1H** _[note] the organisers permit `9GZ2` in place of this entry (reply of 2026-09-02). See `docs/benchmark/review/00-official-reply.md`, which outranks this file where the two disagree, and ADR 0031._ |

_Table 1 caption (verbatim intent): List of targets used to score the predictive accuracy of the quantum algorithms. For each target, the unbound (apo) PDB structure serves as the input, and the drug-bound (holo) PDB structure serves as the ground truth for validating the predicted allosteric site._

### Stretch Target — c-Myc

- Beyond the validation set, participants are **invited to apply their algorithm to c-Myc** — **PDB 1NKP (cMyc/Max heterodimer)** — a transcription factor **dysregulated in >50% of cancers** [24].
- It is **widely considered undruggable** due to its **disordered nature and lack of FDA-approved allosteric inhibitors**.
- **Evaluation for c-Myc:** results will be **evaluated based on consensus across winning teams and theoretical docking viability** (no ground-truth structure exists).

### Submission set

- **c-Myc and the three targets in Table 1 constitute the MINIMUM set required for submission.**
- Participants are **highly encouraged to test robustness on additional targets of their choice** to demonstrate **generalizability and scalability**.
- For additional targets, refer to the **Allosteric Database (ASD)** [25] to select other proteins with known allosteric sites.

---

## 7. Success Criteria & Evaluation — Consolidated

_[note] The PDF does not contain a separate numbered scoring rubric section; the evaluation basis is distributed across §4 and §6. Consolidated here for reference._

**Primary (dominant) criterion**

- Statistically significant enrichment: known **distal regulatory residues score higher** than **random background residues** AND **non-functional surface pockets**.
- Blind prediction on **apo input**, scored against the **holo ground truth** for KRAS G12C, BCR-ABL1, Cardiac Myosin.
- Top-5 ranked hit list per target is the scored artifact.

**Secondary criteria**

- Noise resilience (metric stable under gate errors / limited coherence).
- Coarse-graining method + proof that compression retains the essential topological signal.
- Interpretability and low training barrier for medicinal chemists.
- 3D visualization of quantum connectivity maps.
- Clear logical link: quantum metric → biological phenomenon.
- Analysis vs. classical analogs where relevant.
- Generalizability/scalability shown on extra targets (ASD).

**Explicit penalties / disqualifiers**

- Deep, unoptimized circuits with no near-term hardware viability → **penalized**.
- Use of classical MD trajectories as input → **violates constraint #3**.
- No credible path to near-term or fault-tolerant quantum hardware → violates constraint #1.

**c-Myc (stretch)** — judged by **consensus across winning teams** and **theoretical docking viability**.

---

## 8. Final Target — What We Must Ship

1. A **quantum (or quantum-inspired/hybrid) algorithm** that takes an **apo PDB structure** → builds a **residue contact/elastic network** → **simulates quantum signal propagation** → scores residues by **dynamic connectivity to the active site**.
2. Per target (4 minimum: KRAS G12C 4OBE, BCR-ABL1 1OPL, Cardiac Myosin 5TBY, c-Myc 1NKP):
   - N × N **connectivity matrix**
   - **Top-5 ranked allosteric residue hit list**
3. A **methodological report** justifying the quantum metric as a biological-signal proxy.
4. Supporting evidence: statistical enrichment vs. random/decoy residues, noise-resilience study, coarse-graining validation, 3D visualizations, classical-baseline comparison, near-term hardware feasibility (circuit depth) analysis.

---

## 9. Quick Constraint Checklist

- [ ] Input = **apo structure only**; holo used **only** for scoring
- [ ] **No classical MD trajectories** as input — dynamics predicted _ab initio_ from topology
- [ ] Catalytic domains only; no water/co-factors/PTMs (unless simple nodes)
- [ ] Elastic network hypothesis assumed (topology drives propagation)
- [ ] Circuit depth aware / near-term hardware viable
- [ ] Credible quantum hardware execution path (gate-based, quantum-inspired, or hybrid all allowed)
- [ ] Uses AWS Braket and/or Classiq (free challenge infrastructure)
- [ ] Open-source frameworks (e.g. Qiskit) for reproducibility
- [ ] All 3 output artifacts produced per target
- [ ] Minimum 4 targets covered

---

## 10. References (verbatim from §7 of the PDF)

1. Zheng W. Predicting allosteric sites using fast conformational sampling as guided by coarse-grained normal modes. _J Chem Phys._ 2023;158: 124127. doi:10.1063/5.0141630
2. Koseki J, Motono C, Yanagisawa K, Kudo G, Yoshino R, Hirokawa T, et al. CrypToth: Cryptic Pocket Detection through Mixed-Solvent Molecular Dynamics Simulations-Based Topological Data Analysis. _J Chem Inf Model._ 2025;65: 5567–5575. doi:10.1021/acs.jcim.4c02111
3. Nussinov R, Tsai C-J. Allostery in disease and in drug discovery. _Cell._ 2013;153: 293–305. doi:10.1016/j.cell.2013.03.034
4. Motlagh HN, Wrabl JO, Li J, Hilser VJ. The ensemble nature of allostery. _Nature._ 2014;508: 331–339. doi:10.1038/nature13001
5. Changeux J-P, Edelstein SJ. Allosteric Mechanisms of Signal Transduction. _Science._ 2005. doi:10.1126/science.1108595
6. Tsai C-J, Nussinov R. A unified view of "how allostery works." _PLoS Comput Biol._ 2014;10: e1003394. doi:10.1371/journal.pcbi.1003394
7. Stock G, Hamm P. A non-equilibrium approach to allosteric communication. _Philos Trans R Soc Lond B Biol Sci._ 2018;373. doi:10.1098/rstb.2017.0187
8. Chennubhotla C, Bahar I. Signal propagation in proteins and relation to equilibrium fluctuations. _PLoS Comput Biol._ 2007;3: 1716–1726. doi:10.1371/journal.pcbi.0030172
9. Gunasekaran K, Ma B, Nussinov R. Is allostery an intrinsic property of all dynamic proteins? _Proteins._ 2004;57: 433–443. doi:10.1002/prot.20232
10. Mitarai K, Fujii K. Overhead for simulating a non-local channel with local channels by quasiprobability sampling. _Quantum._ 2021;5: 388. doi:10.22331/q-2021-01-28-388
11. Oh EK, Krogmeier TJ, Schlimgen AW, Head-Marsden K. Singular Value Decomposition Quantum Algorithm for Quantum Biology. _ACS Phys Chem Au._ 2024;4: 393–399. doi:10.1021/acsphyschemau.4c00018
12. Scannell JW, Blanckley A, Boldon H, Warrington B. Diagnosing the decline in pharmaceutical R&D efficiency. _Nat Rev Drug Discov._ 2012;11: 191–200. doi:10.1038/nrd3681
13. wwPDB consortium, Burley SK, Berman HM, Bhikadiya C, Bi C, Chen L, et al. Protein Data Bank: the single global archive for 3D macromolecular structure data. _Nucleic Acids Res._ 2018;47: D520–D528. doi:10.1093/nar/gky949
14. Lu S, Li S, Zhang J. Harnessing allostery: a novel approach to drug discovery. _Med Res Rev._ 2014;34: 1242–1285. doi:10.1002/med.21317
15. Das A, Gur M, Cheng MH, Jo S, Bahar I, Roux B. Exploring the conformational transitions of biomolecular systems using a simple two-state anisotropic network model. _PLoS Comput Biol._ 2014;10: e1003521. doi:10.1371/journal.pcbi.1003521
16. Erman B. The gaussian network model: precise prediction of residue fluctuations and application to binding problems. _Biophys J._ 2006;91: 3589–3599. doi:10.1529/biophysj.106.090803
17. Javadi-Abhari A, Treinish M, Krsulich K, Wood CJ, Lishman J, Gacon J, et al. Quantum computing with Qiskit. _arXiv [quant-ph]._ 2024. doi:10.48550/ARXIV.2405.08810
18. Ostrem JM, Peters U, Sos ML, Wells JA, Shokat KM. K-Ras(G12C) inhibitors allosterically control GTP affinity and effector interactions. _Nature._ 2013;503: 548–551. doi:10.1038/nature12796
19. Canon J, Rex K, Saiki AY, Mohr C, Cooke K, Bagal D, et al. The clinical KRAS(G12C) inhibitor AMG 510 drives anti-tumour immunity. _Nature._ 2019;575: 217–223. doi:10.1038/s41586-019-1694-1
20. Wylie AA, Schoepfer J, Jahnke W, Cowan-Jacob SW, Loo A, Furet P, et al. The allosteric inhibitor ABL001 enables dual targeting of BCR–ABL1. _Nature._ 2017;543: 733–737. doi:10.1038/nature21702
21. Schoepfer J, Jahnke W, Berellini G, Buonamici S, Cotesta S, Cowan-Jacob SW, et al. Discovery of Asciminib (ABL001), an Allosteric Inhibitor of the Tyrosine Kinase Activity of BCR-ABL1. _J Med Chem._ 2018. doi:10.1021/acs.jmedchem.8b01040
22. Green EM, Wakimoto H, Anderson RL, Evanchik MJ, Gorham JM, Harrison BC, et al. A small-molecule inhibitor of sarcomere contractility suppresses hypertrophic cardiomyopathy in mice. _Science._ 2016. doi:10.1126/science.aad3456
23. Anderson RL, Trivedi DV, Sarkar SS, Henze M, Ma W, Gong H, et al. Deciphering the super relaxed state of human β-cardiac myosin and the mode of action of mavacamten from myosin molecules to muscle fibers. _PNAS._ 2018;115: E8143–E8152. doi:10.1073/pnas.1809540115
24. Dang CV, Reddy EP, Shokat KM, Soucek L. Drugging the "undruggable" cancer targets. _Nat Rev Cancer._ 2017;17: 502–508. doi:10.1038/nrc.2017.36
25. Shen Q, Wang G, Li S, Liu X, Lu S, Chen Z, et al. ASD v3.0: unraveling allosteric regulation with structural mechanisms and biological networks. _Nucleic Acids Res._ 2016;44: D527–35. doi:10.1093/nar/gkv902
