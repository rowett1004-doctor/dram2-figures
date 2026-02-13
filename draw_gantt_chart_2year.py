"""
Generate 2-Year Gantt Chart (Project Roadmap) - ccRCC 단독 전략 (2026-02-13 수정)
BLCA 항목 제거, 논문 번호 업데이트 (①-⑦), 글씨 크기 확대
"""
import io, sys
if isinstance(sys.stdout, io.TextIOWrapper):
    pass
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

plt.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Malgun Gothic', 'Arial', 'DejaVu Sans'],
    'font.size': 14,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.2,
})

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

print("=== 2-Year Gantt Chart (ccRCC 단독 전략) ===")

fig, ax = plt.subplots(figsize=(28, 16))

# Phase colors
PHASE_COLORS = {
    'Phase 1': '#3498DB',   # Blue
    'Phase 2': '#27AE60',   # Green
    'Phase 3': '#E67E22',   # Orange
}

# Quarters: Q1-Q4 2026, Q1-Q4 2027
quarters = ['2026\nQ1', 'Q2', 'Q3', 'Q4', '2027\nQ1', 'Q2', 'Q3', 'Q4']
n_quarters = len(quarters)

# Tasks: (name, phase, start_q, duration_q)
# 논문 번호: ①②③④⑤⑥⑦ (BLCA ③ 제거 후 리넘버링)
tasks = [
    # Phase 1: In-Silico + Wet-Lab (Q1-Q3 2026)
    ('Paper ①② Draft + Submission', 'Phase 1', 0, 2.5),
    ('786-O shDRAM2 KD + WB', 'Phase 1', 0.5, 2),
    ('Ferroptosis Assay + LC3 Flux', 'Phase 1', 1, 2),
    ('Patent 2: DRAM2+PBRM1', 'Phase 1', 1.5, 1),
    # Phase 2: In-Vivo + IHC (Q4 2026 ~ Q2 2027)
    ('TMA IHC (n≥100) + Lunit Scope', 'Phase 2', 2.5, 2.5),
    ('Co-culture (CD8 T / M1 mac)', 'Phase 2', 3, 1.5),
    ('dbGaP Application', 'Phase 2', 3, 1),
    ('Xenograft + Rescue', 'Phase 2', 3.5, 2),
    ('Xenograft + anti-PD-1', 'Phase 2', 4.5, 2),
    ('Paper ③ (ccRCC IHC)', 'Phase 2', 4, 1.5),
    ('Paper ④ (ICI Response)', 'Phase 2', 5, 1.5),
    ('Paper ⑥ (Ferroptosis-Cisplatin)', 'Phase 2', 4.5, 2),
    # Phase 3: CDx Kit (Q3-Q4 2027)
    ('Exo-DRAM2 ELISA Dev', 'Phase 3', 6, 1.5),
    ('CDx Kit Prototype', 'Phase 3', 6.5, 1.5),
    ('Patent 1 PCT Filing', 'Phase 3', 7, 1),
    ('Paper ⑤ (Exo-DRAM2 LBx)', 'Phase 3', 6.5, 1.5),
]

n_tasks = len(tasks)

# Draw background grid
for i in range(n_quarters + 1):
    ax.axvline(x=i, color='#E0E0E0', linewidth=0.5, zorder=0)

for i in range(n_tasks + 1):
    ax.axhline(y=i, color='#F0F0F0', linewidth=0.3, zorder=0)

# Alternate row backgrounds
for i in range(n_tasks):
    if i % 2 == 0:
        ax.barh(i, n_quarters, left=0, height=1, color='#FAFAFA', edgecolor='none', zorder=0)

# Draw bars
bar_height = 0.7
for i, (name, phase, start, duration) in enumerate(tasks):
    y_pos = n_tasks - 1 - i
    color = PHASE_COLORS[phase]

    bar = FancyBboxPatch((start, y_pos - bar_height/2), duration, bar_height,
                          boxstyle="round,pad=0.06",
                          facecolor=color, edgecolor='white',
                          linewidth=1, alpha=0.88, zorder=3)
    ax.add_patch(bar)

    # Task name on bar — LARGER font
    fs = 15 if duration >= 2 else 13 if duration >= 1.5 else 11
    ax.text(start + duration/2, y_pos, name, ha='center', va='center',
            fontsize=fs, fontweight='bold', color='white', zorder=4)

# Phase labels on the left side
phase_labels = [
    ('Phase 1\nIn-Silico +\nWet-Lab', 'Phase 1', n_tasks - 4 + 0.5, n_tasks - 0.5),
    ('Phase 2\nIn-Vivo +\nIHC', 'Phase 2', n_tasks - 12 + 0.5, n_tasks - 4.5),
    ('Phase 3\nCDx Kit', 'Phase 3', 0.5, n_tasks - 12.5),
]

for label, phase, y_low, y_high in phase_labels:
    y_mid = (y_low + y_high) / 2
    color = PHASE_COLORS[phase]
    ax.annotate('', xy=(-0.6, y_high), xytext=(-0.6, y_low),
                arrowprops=dict(arrowstyle='-', color=color, lw=4))
    ax.text(-1.3, y_mid, label, ha='center', va='center',
            fontsize=16, fontweight='bold', color=color, rotation=0)

# Milestone diamonds
milestones = [
    (2.5, n_tasks - 1, 'MS-1\nPaper ①②\nSubmit'),
    (5, n_tasks - 5, 'MS-2\nTMA+Lunit\nDone'),
    (5.5, n_tasks - 10, 'MS-3\nPaper ③'),
    (6.5, n_tasks - 11, 'MS-4\nPaper ④'),
    (8, 1.5, 'MS-5\nCDx Kit\nPrototype'),
]

for mx, my, mlabel in milestones:
    ax.plot(mx, my, marker='D', markersize=12, color='#E74C3C',
            markeredgecolor='white', markeredgewidth=2, zorder=5)
    ax.text(mx, my + 0.7, mlabel, ha='center', va='bottom',
            fontsize=13, fontweight='bold', color='#C0392B', zorder=5,
            linespacing=1.1)

# Quarter labels at top
for i, q in enumerate(quarters):
    ax.text(i + 0.5, n_tasks + 0.5, q, ha='center', va='bottom',
            fontsize=17, fontweight='bold', color='#2C3E50')

# Title
ax.text(4, n_tasks + 2, 'DRAM2 Project 2-Year Roadmap (2026-2027)',
        fontsize=28, fontweight='bold', color='#2C3E50')
ax.text(4, n_tasks + 1.4, 'ccRCC-focused strategy — 6~7 papers + 4 patents + Exo-DRAM2 CDx Kit',
        fontsize=16, color='#666', style='italic')

# Phase legend at bottom
legend_elements = [mpatches.Patch(facecolor=c, label=p, edgecolor='white')
                   for p, c in PHASE_COLORS.items()]
legend_elements.append(plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#E74C3C',
                                   markersize=10, label='Milestone'))
ax.legend(handles=legend_elements, loc='lower right', fontsize=16,
          frameon=True, fancybox=True, ncol=4, bbox_to_anchor=(1.0, -0.06))

# Axis settings
ax.set_xlim(-2.2, n_quarters + 0.5)
ax.set_ylim(-1.2, n_tasks + 3)
ax.set_yticks([])
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
out_path = os.path.join(OUT_DIR, 'fig_gantt_chart_2year.png')
plt.savefig(out_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: {out_path}")

print("\n=== Done ===")
