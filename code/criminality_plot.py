import matplotlib.pyplot as plt
import os
from get_data import *

COLORS = ["#48b96f", "#164560", "#939191", "#0abf9c", "#74c63e"]
DATA_URL = 'https://www.ssp.rs.gov.br/upload/arquivos/202204/27145002-lei-15-610-art-3-dados-abertos-ocorrencias-jan-fev-mar-2022-publicacao.CSV'

df = extract(DATA_URL)
df_poa = transform(df)

# CREATING FIGURE AND AXES
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(18,9), dpi=72)
fig.patch.set_facecolor('w')

# PLOT INTO AX
df_poa.plot(
    kind='scatter',
    x='date',
    y='count',
    ax=ax,
    color=COLORS[0]
)
df_poa.plot(
    kind='line',
    ax=ax,
    x='date',
    y='mv_avg_7d',
    color=COLORS[1],
    linewidth=4
)
df_poa[df_poa['count']==df_poa['count'].max()].plot(
    kind='scatter',
    x='date',
    y='count',
    ax=ax,
    color=COLORS[0],
    s=150
)

# FILL BETWEEN
ax.fill_between(
    df_poa.index,
    df_poa['mv_avg_7d'],
    where=(
        (df_poa.index >= '2022-02-26') &
        (df_poa.index <= '2022-03-01')
    ),
    color = COLORS[2],
    alpha=0.6
)

# CUSTOMIZING SPINES
ax.spines[['right', 'top']].set_visible(False)

# CUSTOMIZING LABELS
ax.set_ylabel('')
ax.set_xlabel('')

# CUSTOMIZING AXIS
ax.set_ylim(150, top=None)
ax.set_xlim('2021-12-31', '2022-03-01')

# CUSTOMIZING LEGENDS
ax.legend(
    ['Crimes in a day', '7-day moving avg'],
    fontsize=12
)

# CUSTOMIZING TICKS
ax.minorticks_off()
plt.yticks(
    [200, 250, 300, 350, 400, 450],
    ['200', '250', '300', '350', '400', '450'],
    fontsize=15
)
ax.set_xticks(
    ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01']
)
ax.set_xticklabels(
    ['January', 'February', 'March', 'April/2022'],
    fontsize=15
)

# CUSTOMIZE TITLES AND SUBTITLES
ax.text(
    0, 1.1,
    'Criminality in Porto Alegre',
    transform=ax.transAxes,
    fontsize=30,
    fontweight='bold',
    color='#58555A'
)
ax.text(
    0, 1.05,
    'Crimes registered per day and 7-day moving average in the first 3 months of 2022.',
    transform=ax.transAxes,
    fontsize=18,
    color='#58555A'
)

# CREATING ANNOTATIONS
ax.annotate(
    'Higher register of\ncrimes in a day: {:.0f}'.format(df_poa['count'].max()),
    xy=('2022-03-07', 449),
    xycoords='data',
    xytext=('2022-02-15', 440),
    textcoords='data',
    weight='bold',
    color=COLORS[1],
    fontsize=15,
    arrowprops=dict(
        color=COLORS[1],
        shrink=0.05
    )
)

ax.text(
    x='2022-03-01', y=160,
    s='Carnaval\n(national holiday)',
    fontsize=15,
    color='#58555A',
    fontweight='bold',
    bbox=dict(
        boxstyle='round',
        fc='w',
        ec='0.5',
        lw=2,
        alpha=0.9
    )
)

# ADD CAPTION
fig.text(
    0.12, 0.031,
    "Source: Secretaria de Segurança Pública do Estado do Rio Grande do Sul",
    color='#58555A',
    fontsize=16,
    fontfamily="Econ Sans Cnd"
)

# ADD SUPCAPTION
fig.text(
    0.12, 0.005,
    "https://www.ssp.rs.gov.br/",
    color='#58555A',
    fontsize=13.5,
    fontfamily="Econ Sans Cnd"
)

plt.savefig(
    "criminality_poa.png"
)

plt.show()

