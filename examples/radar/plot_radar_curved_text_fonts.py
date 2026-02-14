"""
====================================
Radar Charts with Curved Text Labels
====================================

This script is a curved-text focused variant of ``plot_radar.py``.
It creates multiple radar styles and switches fonts across examples so you can
visually inspect curved label placement, readability, and spacing.
"""

from pathlib import Path

import matplotlib.pyplot as plt

from mplsoccer import FontManager, Radar, grid


OUTPUT_DIR = Path(__file__).resolve().parent / "images" / "radar_curved_text_fonts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_plot(fig, filename):
    output_path = OUTPUT_DIR / f"{filename}.png"
    fig.savefig(
        output_path, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor()
    )
    return output_path


saved_paths = []

##############################################################################
# Setting the Radar boundaries
# ----------------------------

params = [
    "npxG",
    "Non-Penalty Goals",
    "xA",
    "Key Passes",
    "Through Balls",
    "Progressive Passes",
    "Shot-Creating Actions",
    "Goal-Creating Actions",
    "Dribbles Completed",
    "Pressure Regains",
    "Touches In Box",
    "Miscontrol",
]

low = [0.08, 0.0, 0.1, 1, 0.6, 4, 3, 0.3, 0.3, 2.0, 2, 0]
high = [0.37, 0.6, 0.6, 4, 1.2, 10, 8, 1.3, 1.5, 5.5, 5, 5]
lower_is_better = ["Miscontrol"]

radar = Radar(
    params,
    low,
    high,
    lower_is_better=lower_is_better,
    round_int=[False] * len(params),
    num_rings=4,
    ring_width=1,
    center_circle_radius=1,
)

##############################################################################
# Loading fonts
# -------------
# Using a spread of styles (serif, mono display, thin sans, slab)
# makes curved-text rendering differences easier to spot.

URL1 = (
    "https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/"
    "SourceSerifPro-Regular.ttf"
)
serif_regular = FontManager(URL1)

URL2 = (
    "https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/"
    "SourceSerifPro-ExtraLight.ttf"
)
serif_extra_light = FontManager(URL2)

URL3 = (
    "https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/"
    "RubikMonoOne-Regular.ttf"
)
rubik_regular = FontManager(URL3)

URL4 = "https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf"
roboto_thin = FontManager(URL4)

URL5 = (
    "https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/"
    "RobotoSlab%5Bwght%5D.ttf"
)
roboto_slab = FontManager(URL5)

##############################################################################
# Player values
# -------------

bruno_values = [0.22, 0.25, 0.30, 2.54, 0.43, 5.60, 4.34, 0.29, 0.69, 5.14, 4.97, 1.10]
bruyne_values = [0.25, 0.52, 0.37, 3.59, 0.41, 6.36, 5.68, 0.57, 1.23, 4.00, 4.54, 1.39]
eriksen_values = [
    0.13,
    0.10,
    0.35,
    3.08,
    0.29,
    6.23,
    5.08,
    0.43,
    0.67,
    3.07,
    1.34,
    1.06,
]

##############################################################################
# 1) Simple radar with curved labels (thin sans)
# -----------------------------------------------

fig, ax = radar.setup_axis()
radar.draw_circles(ax=ax, facecolor="#ffe4ec", edgecolor="#f36d85")
radar.draw_radar(
    bruno_values,
    ax=ax,
    kwargs_radar={"facecolor": "#df5a9c", "alpha": 0.8},
    kwargs_rings={"facecolor": "#7ad7f0", "alpha": 0.55},
)
radar.draw_range_labels(ax=ax, fontsize=13, fontproperties=roboto_thin.prop)
radar.draw_param_labels(
    ax=ax,
    fontsize=15,
    curved=True,
    fontproperties=roboto_thin.prop,
)
ax.set_title(
    "Simple Curved Labels | Roboto Thin",
    fontsize=16,
    fontproperties=roboto_slab.prop,
    pad=22,
)
saved_paths.append(save_plot(fig, "01_simple_curved_roboto_thin"))

##############################################################################
# 2) Single-player + spokes (serif, increased letter spacing)
# ------------------------------------------------------------

fig, ax = radar.setup_axis()
radar.draw_circles(ax=ax, facecolor="#fef6dc", edgecolor="#f3cc4e")
radar.draw_radar(
    bruyne_values,
    ax=ax,
    kwargs_radar={"facecolor": "#4d98ff", "alpha": 0.72},
    kwargs_rings={"facecolor": "#73d2de", "alpha": 0.65},
)
radar.spoke(ax=ax, color="#a49f8f", linestyle="--", lw=1.2, zorder=2)
radar.draw_range_labels(ax=ax, fontsize=13, fontproperties=serif_extra_light.prop)
radar.draw_param_labels(
    ax=ax,
    fontsize=15,
    curved=True,
    curved_letter_spacing=0.7,
    curved_align="center",
    fontproperties=serif_regular.prop,
)
ax.set_title(
    "Spokes + Curved Spacing | Source Serif Pro",
    fontsize=16,
    fontproperties=roboto_slab.prop,
    pad=22,
)
saved_paths.append(save_plot(fig, "02_spokes_serif_letter_spacing"))

##############################################################################
# 3) Two-player comparison (mono display labels)
# -----------------------------------------------

fig, ax = radar.setup_axis()
radar.draw_circles(ax=ax, facecolor="#f4f0ff", edgecolor="#9a88f2")
radar_output = radar.draw_radar_compare(
    bruno_values,
    bruyne_values,
    ax=ax,
    kwargs_radar={"facecolor": "#11b5e4", "alpha": 0.58},
    kwargs_compare={"facecolor": "#ff3366", "alpha": 0.56},
)
_, _, vertices_1, vertices_2 = radar_output
ax.scatter(
    vertices_1[:, 0],
    vertices_1[:, 1],
    c="#11b5e4",
    edgecolors="#2a2a2a",
    s=90,
    zorder=2,
)
ax.scatter(
    vertices_2[:, 0],
    vertices_2[:, 1],
    c="#ff3366",
    edgecolors="#2a2a2a",
    s=90,
    zorder=2,
)
radar.draw_range_labels(ax=ax, fontsize=11, fontproperties=roboto_thin.prop)
radar.draw_param_labels(
    ax=ax,
    fontsize=13,
    curved=True,
    curved_direction="auto",
    curved_align="center",
    fontproperties=rubik_regular.prop,
)
ax.set_title(
    "Comparison | Rubik Mono One",
    fontsize=16,
    fontproperties=roboto_slab.prop,
    pad=22,
)
saved_paths.append(save_plot(fig, "03_compare_rubik_mono"))

##############################################################################
# 4) Three-player comparison with title grid (mixed fonts)
# ---------------------------------------------------------

fig, axs = grid(
    figheight=14,
    grid_height=0.915,
    title_height=0.06,
    endnote_height=0.025,
    title_space=0,
    endnote_space=0,
    grid_key="radar",
    axis=False,
)

radar.setup_axis(ax=axs["radar"])
radar.draw_circles(ax=axs["radar"], facecolor="#f3f7ff", edgecolor="#6c8bd8")

radar_one, vertices_one = radar.draw_radar_solid(
    bruno_values,
    ax=axs["radar"],
    kwargs={"facecolor": "#f05d5e", "alpha": 0.55, "edgecolor": "#7f1d1d", "lw": 2.5},
)
radar_two, vertices_two = radar.draw_radar_solid(
    bruyne_values,
    ax=axs["radar"],
    kwargs={"facecolor": "#0fa3b1", "alpha": 0.55, "edgecolor": "#0d4e57", "lw": 2.5},
)
radar_three, vertices_three = radar.draw_radar_solid(
    eriksen_values,
    ax=axs["radar"],
    kwargs={"facecolor": "#8d6fd1", "alpha": 0.55, "edgecolor": "#40336b", "lw": 2.5},
)

axs["radar"].scatter(
    vertices_one[:, 0], vertices_one[:, 1], c="#f05d5e", edgecolors="#7f1d1d", s=110
)
axs["radar"].scatter(
    vertices_two[:, 0], vertices_two[:, 1], c="#0fa3b1", edgecolors="#0d4e57", s=110
)
axs["radar"].scatter(
    vertices_three[:, 0], vertices_three[:, 1], c="#8d6fd1", edgecolors="#40336b", s=110
)

radar.draw_range_labels(
    ax=axs["radar"], fontsize=19, fontproperties=serif_extra_light.prop
)
radar.draw_param_labels(
    ax=axs["radar"],
    fontsize=20,
    curved=True,
    curved_direction="auto",
    curved_radii="outward",
    fontproperties=serif_regular.prop,
)

axs["title"].text(
    0.01,
    0.60,
    "Curved Label Font Inspection",
    fontsize=25,
    fontproperties=roboto_slab.prop,
    ha="left",
    va="center",
)
axs["title"].text(
    0.01,
    0.20,
    "Three-player radar | Source Serif Pro labels",
    fontsize=18,
    fontproperties=roboto_thin.prop,
    ha="left",
    va="center",
    color="#35537a",
)
axs["endnote"].text(
    0.99,
    0.5,
    "Curved labels: curved=True, direction='auto', radii='outward'",
    fontsize=13,
    fontproperties=roboto_thin.prop,
    ha="right",
    va="center",
)
saved_paths.append(save_plot(fig, "04_three_player_grid_mixed_fonts"))

##############################################################################
# 5) Compact radar with wrapped labels (radii mode inspection)
# -------------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

compact_params = [
    "Chance Creation",
    "Off-ball Pressing",
    "Ball Carrying",
    "Final Third Entries",
    "Defensive Duels",
]
compact_radar = Radar(
    params=compact_params,
    min_range=[0, 0, 0, 0, 0],
    max_range=[5, 5, 5, 5, 5],
    round_int=[True, True, True, True, True],
    num_rings=5,
    center_circle_radius=1.5,
)
compact_values = [4, 5, 3, 4, 2]

for ax, radii_mode, title in zip(
    axes,
    ["outward", "center"],
    ["Wrapped lines: outward", "Wrapped lines: center"],
):
    compact_radar.setup_axis(ax=ax)
    compact_radar.draw_circles(ax=ax, facecolor="#f7efec", edgecolor="#d5a09a")
    compact_radar.draw_radar(
        compact_values,
        ax=ax,
        kwargs_radar={"facecolor": "#53a2be", "alpha": 0.78},
        kwargs_rings={"facecolor": "#f26ca7", "alpha": 0.40},
    )
    compact_radar.draw_range_labels(ax=ax, fontsize=12, fontproperties=roboto_thin.prop)
    compact_radar.draw_param_labels(
        ax=ax,
        wrap=12,
        fontsize=14,
        curved=True,
        curved_radii=radii_mode,
        curved_line_spacing=16,
        fontproperties=roboto_slab.prop,
    )
    ax.set_title(title, fontsize=15, fontproperties=serif_regular.prop, pad=15)

saved_paths.append(save_plot(fig, "05_wrapped_labels_radii_comparison"))

##############################################################################
# 6) Font comparison panel (matched to visual QA style)
# ------------------------------------------------------

qa_params = [
    "Pressures Applied",
    "Key Passes",
    "Shot-Creating Actions",
    "Expected Assists",
    "Through Balls",
    "Dribbles Completed",
    "Progressive Passes",
    "Touches In Box",
    "Interceptions",
    "Pressure Regains",
    "Carries Into Final Third",
    "Miscontrols",
]
qa_values = [0.86, 0.74, 0.79, 0.70, 0.58, 0.64, 0.92, 0.57, 0.60, 0.76, 0.68, 0.62]
qa_radar = Radar(
    qa_params,
    min_range=[0] * len(qa_params),
    max_range=[1] * len(qa_params),
    lower_is_better=["Miscontrols"],
    round_int=[False] * len(qa_params),
    num_rings=4,
    ring_width=1,
    center_circle_radius=1,
)

fig, axes = plt.subplots(1, 3, figsize=(20, 7), facecolor="#eef0f2")
fig.suptitle("Radar Curved Label Visual QA - Font Comparison", fontsize=24, y=0.98)

font_variants = [
    ("DejaVu Sans", "DejaVu Sans"),
    ("DejaVu Serif", "DejaVu Serif"),
    ("DejaVu Sans Mono", "DejaVu Sans Mono"),
]

for ax, (title, family) in zip(axes, font_variants):
    qa_radar.setup_axis(ax=ax, facecolor="None")
    qa_radar.draw_circles(ax=ax, facecolor="#edf0f3", edgecolor="#c7cfd8", lw=1.4)
    qa_radar.draw_radar(
        qa_values,
        ax=ax,
        kwargs_radar={
            "facecolor": "#9ecfcf",
            "edgecolor": "#86b8b9",
            "alpha": 0.62,
            "lw": 1.8,
        },
        kwargs_rings={"facecolor": "#d8eeef", "alpha": 0.30},
    )
    qa_radar.draw_range_labels(
        ax=ax,
        fontsize=7,
        color="#56687a",
        fontfamily=family,
    )
    qa_radar.draw_param_labels(
        ax=ax,
        fontsize=10,
        wrap=10,
        curved=True,
        curved_direction="auto",
        curved_align="center",
        color="#20354a",
        fontfamily=family,
    )
    ax.set_title(title, fontsize=24, pad=18, color="#20354a", fontfamily=family)

saved_paths.append(save_plot(fig, "06_font_comparison_panel"))

##############################################################################
# 7) Curved behavior variants panel (matched to visual QA style)
# ---------------------------------------------------------------

fig, axes = plt.subplots(3, 4, figsize=(24, 18), facecolor="#eef0f2")
fig.suptitle("Radar Curved Label Visual QA - Behavior Variants", fontsize=20, y=0.985)

variant_specs = [
    ("Straight labels (reference)", {"curved": False, "wrap": 14}),
    ("Curved default (auto)", {"curved": True, "wrap": 14}),
    ("Curved no wrap", {"curved": True, "wrap": None}),
    ("Curved wrap=10", {"curved": True, "wrap": 10}),
    ("Align start", {"curved": True, "wrap": 14, "curved_align": "start"}),
    ("Align center", {"curved": True, "wrap": 14, "curved_align": "center"}),
    ("Align end", {"curved": True, "wrap": 14, "curved_align": "end"}),
    (
        "Direction clockwise",
        {"curved": True, "wrap": 14, "curved_direction": "clockwise"},
    ),
    (
        "Direction counterclockwise",
        {"curved": True, "wrap": 14, "curved_direction": "counterclockwise"},
    ),
    ("Radii outward", {"curved": True, "wrap": 14, "curved_radii": "outward"}),
    ("Radii center", {"curved": True, "wrap": 14, "curved_radii": "center"}),
    (
        "Letter spacing +1.2",
        {"curved": True, "wrap": 14, "curved_letter_spacing": 1.2},
    ),
]

for ax, (title, param_kwargs) in zip(axes.flat, variant_specs):
    qa_radar.setup_axis(ax=ax, facecolor="None")
    qa_radar.draw_circles(ax=ax, facecolor="#edf0f3", edgecolor="#c7cfd8", lw=1.1)
    qa_radar.draw_radar(
        qa_values,
        ax=ax,
        kwargs_radar={
            "facecolor": "#9ecfcf",
            "edgecolor": "#86b8b9",
            "alpha": 0.62,
            "lw": 1.4,
        },
        kwargs_rings={"facecolor": "#d8eeef", "alpha": 0.30},
    )
    qa_radar.draw_range_labels(
        ax=ax, fontsize=6.5, color="#56687a", fontfamily="DejaVu Sans"
    )
    qa_radar.draw_param_labels(
        ax=ax,
        fontsize=9,
        color="#20354a",
        fontfamily="DejaVu Sans",
        **param_kwargs,
    )
    ax.set_title(title, fontsize=12, pad=10, color="#20354a")

saved_paths.append(save_plot(fig, "07_behavior_variants_panel"))

##############################################################################
# 8) Gallery parity: simple radar (original plot_radar.py styling)
# ---------------------------------------------------------------

fig, ax = radar.setup_axis(figsize=(7, 7))
radar.draw_circles(ax=ax, facecolor="#ffb2b2", edgecolor="#fc5f5f")
radar.draw_radar(
    bruno_values,
    ax=ax,
    kwargs_radar={"facecolor": "#aa65b2"},
    kwargs_rings={"facecolor": "#66d8ba"},
)
radar.draw_range_labels(ax=ax, fontsize=10, fontproperties=roboto_thin.prop)
radar.draw_param_labels(
    ax=ax, fontsize=10, curved=True, fontproperties=roboto_thin.prop
)
ax.set_title(
    "Gallery: Simple Radar (curved labels)",
    fontsize=16,
    fontproperties=roboto_slab.prop,
    pad=22,
)
saved_paths.append(save_plot(fig, "08_gallery_simple_radar"))

##############################################################################
# 9) Gallery parity: add spokes
# -----------------------------

fig, ax = radar.setup_axis(figsize=(7, 7))
radar.draw_circles(ax=ax, facecolor="#ffb2b2", edgecolor="#fc5f5f")
radar.draw_radar(
    bruno_values,
    ax=ax,
    kwargs_radar={"facecolor": "#aa65b2"},
    kwargs_rings={"facecolor": "#66d8ba"},
)
radar.draw_range_labels(ax=ax, fontsize=10, zorder=2.5, fontproperties=roboto_thin.prop)
radar.draw_param_labels(
    ax=ax, fontsize=10, curved=True, fontproperties=roboto_thin.prop
)
radar.spoke(ax=ax, color="#a6a4a1", linestyle="--", zorder=2)
ax.set_title(
    "Gallery: Spokes (curved labels)",
    fontsize=16,
    fontproperties=roboto_slab.prop,
    pad=22,
)
saved_paths.append(save_plot(fig, "09_gallery_spokes"))

##############################################################################
# 10) Gallery parity: simple comparison
# ------------------------------------

fig, ax = radar.setup_axis(figsize=(7, 7))
radar.draw_circles(ax=ax, facecolor="#ffb2b2", edgecolor="#fc5f5f")
radar.draw_radar_compare(
    bruno_values,
    bruyne_values,
    ax=ax,
    kwargs_radar={"facecolor": "#00f2c1", "alpha": 0.6},
    kwargs_compare={"facecolor": "#d80499", "alpha": 0.6},
)
radar.draw_range_labels(ax=ax, fontsize=10, fontproperties=roboto_thin.prop)
radar.draw_param_labels(
    ax=ax, fontsize=10, curved=True, fontproperties=roboto_thin.prop
)
ax.set_title(
    "Gallery: Compare Two Players (curved labels)",
    fontsize=16,
    fontproperties=roboto_slab.prop,
    pad=22,
)
saved_paths.append(save_plot(fig, "10_gallery_compare_two"))

##############################################################################
# 11) Gallery parity: compare three or more players
# ------------------------------------------------

fig, ax = radar.setup_axis(figsize=(7, 7))
radar.draw_circles(ax=ax, facecolor="#ffb2b2", edgecolor="#fc5f5f")

_, vertices1 = radar.draw_radar_solid(
    bruno_values,
    ax=ax,
    kwargs={"facecolor": "#aa65b2", "alpha": 0.6, "edgecolor": "#216352", "lw": 3},
)
_, vertices2 = radar.draw_radar_solid(
    bruyne_values,
    ax=ax,
    kwargs={"facecolor": "#66d8ba", "alpha": 0.6, "edgecolor": "#216352", "lw": 3},
)
_, vertices3 = radar.draw_radar_solid(
    eriksen_values,
    ax=ax,
    kwargs={"facecolor": "#697cd4", "alpha": 0.6, "edgecolor": "#222b54", "lw": 3},
)
ax.scatter(
    vertices1[:, 0], vertices1[:, 1], c="#aa65b2", edgecolors="#502a54", s=110, zorder=2
)
ax.scatter(
    vertices2[:, 0], vertices2[:, 1], c="#66d8ba", edgecolors="#216352", s=110, zorder=2
)
ax.scatter(
    vertices3[:, 0], vertices3[:, 1], c="#697cd4", edgecolors="#222b54", s=110, zorder=2
)

radar.draw_range_labels(ax=ax, fontsize=10, fontproperties=roboto_thin.prop)
radar.draw_param_labels(
    ax=ax, fontsize=10, curved=True, fontproperties=roboto_thin.prop
)
ax.set_title(
    "Gallery: Compare Three Players (curved labels)",
    fontsize=16,
    fontproperties=roboto_slab.prop,
    pad=22,
)
saved_paths.append(save_plot(fig, "11_gallery_compare_three"))

##############################################################################
# 12) Gallery parity: clean radar (no spokes; curved param labels)
# ---------------------------------------------------------------

fig, ax = radar.setup_axis(figsize=(7, 7))
radar.draw_circles(ax=ax, facecolor="#ffb2b2", edgecolor="#fc5f5f")
radar.draw_radar(
    bruno_values,
    ax=ax,
    kwargs_radar={"facecolor": "#aa65b2"},
    kwargs_rings={"facecolor": "#66d8ba"},
)
radar.draw_param_labels(
    ax=ax, fontsize=10, curved=True, fontproperties=roboto_thin.prop
)
ax.set_title(
    "Gallery: Clean Radar (curved labels)",
    fontsize=16,
    fontproperties=roboto_slab.prop,
    pad=22,
)
saved_paths.append(save_plot(fig, "12_gallery_clean_radar"))

##############################################################################
# 13) Gallery parity: title + endnote grid
# ---------------------------------------

fig, axs = grid(
    figheight=14,
    grid_height=0.915,
    title_height=0.06,
    endnote_height=0.025,
    title_space=0,
    endnote_space=0,
    grid_key="radar",
    axis=False,
)

radar.setup_axis(ax=axs["radar"])
radar.draw_circles(ax=axs["radar"], facecolor="#ffb2b2", edgecolor="#fc5f5f")
radar.draw_radar(
    bruno_values,
    ax=axs["radar"],
    kwargs_radar={"facecolor": "#aa65b2"},
    kwargs_rings={"facecolor": "#66d8ba"},
)
radar.draw_range_labels(ax=axs["radar"], fontsize=20, fontproperties=roboto_thin.prop)
radar.draw_param_labels(
    ax=axs["radar"], fontsize=20, curved=True, fontproperties=roboto_thin.prop
)

axs["endnote"].text(
    0.99,
    0.5,
    "Inspired By: StatsBomb / Rami Moghadam",
    fontsize=15,
    fontproperties=roboto_thin.prop,
    ha="right",
    va="center",
)
axs["title"].text(
    0.01,
    0.65,
    "Bruno Fernandes",
    fontsize=25,
    fontproperties=roboto_slab.prop,
    ha="left",
    va="center",
)
axs["title"].text(
    0.01,
    0.25,
    "Manchester United",
    fontsize=20,
    fontproperties=roboto_thin.prop,
    ha="left",
    va="center",
    color="#B6282F",
)
axs["title"].text(
    0.99,
    0.65,
    "Radar Chart",
    fontsize=25,
    fontproperties=roboto_slab.prop,
    ha="right",
    va="center",
)
axs["title"].text(
    0.99,
    0.25,
    "Midfielder",
    fontsize=20,
    fontproperties=roboto_thin.prop,
    ha="right",
    va="center",
    color="#B6282F",
)

saved_paths.append(save_plot(fig, "13_gallery_title_endnote"))

##############################################################################
# 14) Gallery parity: comparison radar with titles
# -----------------------------------------------

fig, axs = grid(
    figheight=14,
    grid_height=0.915,
    title_height=0.06,
    endnote_height=0.025,
    title_space=0,
    endnote_space=0,
    grid_key="radar",
    axis=False,
)

radar.setup_axis(ax=axs["radar"])
radar.draw_circles(ax=axs["radar"], facecolor="#ffb2b2", edgecolor="#fc5f5f")
radar_output = radar.draw_radar_compare(
    bruno_values,
    bruyne_values,
    ax=axs["radar"],
    kwargs_radar={"facecolor": "#00f2c1", "alpha": 0.6},
    kwargs_compare={"facecolor": "#d80499", "alpha": 0.6},
)
_, _, vertices1, vertices2 = radar_output
radar.draw_range_labels(ax=axs["radar"], fontsize=20, fontproperties=roboto_thin.prop)
radar.draw_param_labels(
    ax=axs["radar"], fontsize=20, curved=True, fontproperties=roboto_thin.prop
)
axs["radar"].scatter(
    vertices1[:, 0], vertices1[:, 1], c="#00f2c1", edgecolors="#6d6c6d", s=150, zorder=2
)
axs["radar"].scatter(
    vertices2[:, 0], vertices2[:, 1], c="#d80499", edgecolors="#6d6c6d", s=150, zorder=2
)

axs["endnote"].text(
    0.99,
    0.5,
    "Inspired By: StatsBomb / Rami Moghadam",
    fontsize=15,
    fontproperties=roboto_thin.prop,
    ha="right",
    va="center",
)
axs["title"].text(
    0.01,
    0.65,
    "Bruno Fernandes",
    fontsize=25,
    color="#01c49d",
    fontproperties=roboto_slab.prop,
    ha="left",
    va="center",
)
axs["title"].text(
    0.01,
    0.25,
    "Manchester United",
    fontsize=20,
    fontproperties=roboto_thin.prop,
    ha="left",
    va="center",
    color="#01c49d",
)
axs["title"].text(
    0.99,
    0.65,
    "Kevin De Bruyne",
    fontsize=25,
    fontproperties=roboto_slab.prop,
    ha="right",
    va="center",
    color="#d80499",
)
axs["title"].text(
    0.99,
    0.25,
    "Manchester City",
    fontsize=20,
    fontproperties=roboto_thin.prop,
    ha="right",
    va="center",
    color="#d80499",
)

saved_paths.append(save_plot(fig, "14_gallery_compare_titles"))

##############################################################################
# 15) Gallery parity: dark theme
# ------------------------------

fig, axs = grid(
    figheight=14,
    grid_height=0.915,
    title_height=0.06,
    endnote_height=0.025,
    title_space=0,
    endnote_space=0,
    grid_key="radar",
    axis=False,
)

radar.setup_axis(ax=axs["radar"], facecolor="None")
radar.draw_circles(ax=axs["radar"], facecolor="#28252c", edgecolor="#39353f", lw=1.5)
radar.draw_radar(
    bruno_values,
    ax=axs["radar"],
    kwargs_radar={"facecolor": "#d0667a"},
    kwargs_rings={"facecolor": "#1d537f"},
)
radar.draw_range_labels(
    ax=axs["radar"], fontsize=25, color="#fcfcfc", fontproperties=roboto_thin.prop
)
radar.draw_param_labels(
    ax=axs["radar"],
    fontsize=25,
    curved=True,
    color="#fcfcfc",
    fontproperties=roboto_thin.prop,
)

axs["endnote"].text(
    0.99,
    0.5,
    "Inspired By: StatsBomb / Rami Moghadam",
    fontsize=15,
    color="#fcfcfc",
    fontproperties=roboto_thin.prop,
    ha="right",
    va="center",
)
axs["title"].text(
    0.01,
    0.65,
    "Bruno Fernandes",
    fontsize=25,
    fontproperties=roboto_slab.prop,
    ha="left",
    va="center",
    color="#e4dded",
)
axs["title"].text(
    0.01,
    0.25,
    "Manchester United",
    fontsize=20,
    fontproperties=roboto_thin.prop,
    ha="left",
    va="center",
    color="#cc2a3f",
)
axs["title"].text(
    0.99,
    0.65,
    "Radar Chart",
    fontsize=25,
    fontproperties=roboto_slab.prop,
    ha="right",
    va="center",
    color="#e4dded",
)
axs["title"].text(
    0.99,
    0.25,
    "Midfielder",
    fontsize=20,
    fontproperties=roboto_thin.prop,
    ha="right",
    va="center",
    color="#cc2a3f",
)

fig.set_facecolor("#121212")
saved_paths.append(save_plot(fig, "15_gallery_dark_theme"))

##############################################################################
# 16) Gallery parity: Ben Eine theme
# ---------------------------------

fig, axs = grid(
    figheight=14,
    grid_height=0.915,
    title_height=0.06,
    endnote_height=0.025,
    title_space=0,
    endnote_space=0,
    grid_key="radar",
    axis=False,
)

radar.setup_axis(ax=axs["radar"], facecolor="None")
radar.draw_circles(
    ax=axs["radar"],
    facecolor="#5bc8ef",
    edgecolor="#b7ebff",
    linewidth=[0, 1, 2],
)
radar_output = radar.draw_radar(
    bruno_values,
    ax=axs["radar"],
    kwargs_radar={"facecolor": "#fa4554"},
    kwargs_rings={"facecolor": "#d298c4"},
)
_, _, vertices = radar_output
radar.draw_range_labels(
    ax=axs["radar"], fontsize=25, color="#f0f6f6", fontproperties=roboto_thin.prop
)
radar.draw_param_labels(
    ax=axs["radar"],
    fontsize=25,
    curved=True,
    color="#f0f6f6",
    fontproperties=roboto_thin.prop,
)
axs["radar"].scatter(
    vertices[:, 0],
    vertices[:, 1],
    c="#eeb743",
    edgecolors="#070707",
    marker="D",
    s=220,
    zorder=2,
)

axs["endnote"].text(
    0.99,
    0.5,
    "The theme is inspired by Ben Eine",
    fontsize=15,
    fontproperties=roboto_thin.prop,
    ha="right",
    va="center",
    color="#f0f6f6",
)
axs["title"].text(
    0.01,
    0.65,
    "Bruno Fernandes",
    fontsize=25,
    fontproperties=roboto_slab.prop,
    ha="left",
    va="center",
    color="#eeb743",
)
axs["title"].text(
    0.01,
    0.25,
    "Manchester United",
    fontsize=20,
    fontproperties=roboto_thin.prop,
    ha="left",
    va="center",
    color="#f0f6f6",
)
axs["title"].text(
    0.99,
    0.65,
    "Radar Chart",
    fontsize=25,
    fontproperties=roboto_slab.prop,
    ha="right",
    va="center",
    color="#eeb743",
)
axs["title"].text(
    0.99,
    0.25,
    "Midfielder",
    fontsize=20,
    fontproperties=roboto_thin.prop,
    ha="right",
    va="center",
    color="#f0f6f6",
)

fig.set_facecolor("#070707")
saved_paths.append(save_plot(fig, "16_gallery_ben_eine"))

##############################################################################
# 17) Gallery parity: Camille Walala theme
# ---------------------------------------

radar2 = Radar(
    params=["Speed", "Agility", "Strength", "Passing", "Dribbles"],
    min_range=[0, 0, 0, 0, 0],
    max_range=[5, 5, 5, 5, 5],
    round_int=[True, True, True, True, True],
    center_circle_radius=2,
    num_rings=5,
)

fig, axs = grid(
    figheight=14,
    grid_height=0.915,
    title_height=0.06,
    endnote_height=0.025,
    title_space=0,
    endnote_space=0,
    grid_key="radar",
    axis=False,
)

radar2.setup_axis(ax=axs["radar"], facecolor="None")
radar2.draw_circles(ax=axs["radar"], facecolor="#f77b83", edgecolor="#fe2837")
radar2.draw_radar(
    values=[5, 2, 4, 3, 1],
    ax=axs["radar"],
    kwargs_radar={"facecolor": "#f9c728", "hatch": ".", "alpha": 1},
    kwargs_rings={
        "facecolor": "#e6dedc",
        "edgecolor": "#1a1414",
        "hatch": "/",
        "alpha": 1,
    },
)
radar2.draw_radar(
    values=[5, 2, 4, 3, 1],
    ax=axs["radar"],
    kwargs_radar={"facecolor": "None", "edgecolor": "#646366"},
    kwargs_rings={"facecolor": "None"},
)
radar2.draw_range_labels(
    ax=axs["radar"], fontsize=25, fontproperties=serif_extra_light.prop
)
radar2.draw_param_labels(
    ax=axs["radar"],
    fontsize=25,
    curved=True,
    fontproperties=serif_regular.prop,
)

axs["endnote"].text(
    0.99,
    0.5,
    "The theme is inspired by Camille Walala",
    fontproperties=serif_extra_light.prop,
    fontsize=15,
    ha="right",
    va="center",
)
axs["title"].text(
    0.01,
    0.65,
    "Player name",
    fontsize=20,
    fontproperties=rubik_regular.prop,
    ha="left",
    va="center",
)
axs["title"].text(
    0.01,
    0.25,
    "Player team",
    fontsize=15,
    fontproperties=rubik_regular.prop,
    ha="left",
    va="center",
    color="#fa1b38",
)
axs["title"].text(
    0.99,
    0.65,
    "Radar Chart",
    fontsize=20,
    fontproperties=rubik_regular.prop,
    ha="right",
    va="center",
)
axs["title"].text(
    0.99,
    0.25,
    "Position",
    fontsize=15,
    fontproperties=rubik_regular.prop,
    ha="right",
    va="center",
    color="#fa1b38",
)

fig.set_facecolor("#f2dad2")
saved_paths.append(save_plot(fig, "17_gallery_camille_walala"))

print("Saved radar curved-text PNG files:")
for saved_path in saved_paths:
    print(saved_path)

plt.show()
