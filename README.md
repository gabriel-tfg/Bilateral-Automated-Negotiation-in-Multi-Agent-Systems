# Bilateral Automated Negotiation in Multi-Agent Systems

## Overview

This project studies **bilateral automated negotiation** in Multi-Agent Systems through the implementation and evaluation of classical time-dependent concession strategies.

The objective is to analyse how different negotiation behaviours influence:

- Agreement Rate
- Negotiation Length
- Social Welfare

The work combines a theoretical review of automated negotiation with a large-scale experimental evaluation based on randomly generated negotiation domains.

---

## Negotiation Framework

The project considers:

- Bilateral negotiation
- Incomplete information
- Multi-issue domains
- Alternating Offers Protocol
- Additive utility functions

Each agent negotiates according to a predefined concession strategy and attempts to maximise its own utility while reaching an agreement before the deadline.

---

## Implemented Strategies

### Linear

Concedes at a constant rate during the negotiation.

\[
\alpha(t)=1-0.9t
\]

### Conceder

Concedes rapidly during the early stages.

\[
\alpha(t)=1-0.9t^{0.5}
\]

### Boulware

Maintains high demands and delays concessions until the end.

\[
\alpha(t)=1-0.9t^3
\]

---

## Experimental Setup

The experiments were performed using:

- 10,000 randomly generated negotiation domains
- 3 negotiation issues per domain
- 3–5 values per issue
- 12-round negotiation deadline
- Random additive utility functions
- 60,000 total negotiation sessions

Decision threshold:

\[
\tau(t)=\max\{\theta,\alpha(t)\}
\]

with:

\[
\theta=0.7
\]

---

## Evaluation Metrics

The following metrics were used:

### Agreement Rate

Percentage of negotiations that end successfully.

### Negotiation Length

Average number of rounds until termination.

### Social Welfare

Sum of the utilities obtained by both agents:

\[
SW = U_A + U_B
\]

---

## Main Results

| Strategy Pair | Agreement Rate (%) | Avg. Length | Avg. Welfare (%) |
|--------------|-------------------|------------|------------------|
| Boulware vs Boulware | 77.74 | 8.59 | 132.46 |
| Boulware vs Conceder | 82.57 | 6.12 | 144.47 |
| Boulware vs Linear | 81.68 | 6.79 | 142.54 |
| Conceder vs Conceder | 72.48 | 5.20 | 115.41 |
| Conceder vs Linear | 77.85 | 5.24 | 130.05 |
| Linear vs Linear | 77.96 | 5.75 | 130.55 |

Key findings:

- Mixed strategy interactions achieved the highest performance.
- Boulware vs Conceder produced the highest welfare and agreement rate.
- Conceder vs Conceder generated the lowest welfare.
- Boulware strategies resulted in longer negotiations.

---

## Project Structure

```text
.
├── agent.py
├── domain.py
├── session.py
├── strategies.py
├── tournament.py
├── utils.py
├── main.py
├── results/
└── Multi-Agent Systems Project.pdf
```

### File Description

- **agent.py** → Agent implementation.
- **domain.py** → Negotiation domain generation.
- **session.py** → Negotiation session logic.
- **strategies.py** → Negotiation strategies.
- **tournament.py** → Large-scale experimental execution.
- **utils.py** → Utility functions and helpers.
- **main.py** → Entry point of the project.

---

## Running the Project

Execute:

```bash
python main.py
```

Results and figures will be generated automatically inside the `results/` directory.

---

## Author

**Gabriel Losada Arias**

Master's Degree Project  
Multi-Agent Systems
