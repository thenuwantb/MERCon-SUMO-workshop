import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# 1. Setting the working directory

os.chdir("E:\\MERCon\\pythonProject\\Guide\\1_real_world_simulation")

# 2. Set fonts
plt.rcParams["font.family"] = "Times New Roman"

# 3. Read Data
edge_data_df = pd.read_csv('simulation_output/edge_output_base_agg_300.csv')

# 4. Data Preprocessing
edge_data_df = edge_data_df[
    ['interval_begin', 'interval_end', 'interval_id', 'edge_speed', 'edge_density', 'edge_entered', 'edge_left'
        , 'edge_timeLoss', 'edge_traveltime', 'edge_waitingTime', 'scenario', 'random_seed']]
# 4.2. Calculate speed in kmph and create a new column
edge_data_df['speed_kmph'] = edge_data_df['edge_speed'] * 3.6


# 5. Visualize Data
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(12, 2.5), constrained_layout=True)
sns.lineplot(data=edge_data_df, x='interval_begin', y='speed_kmph', ax=axs,
             hue='interval_id', marker='v')
xlim = np.arange(900, 4500, 300)
time_labels = ['06:00', '06:05', '06:10', '06:15', '06:20', '06:25', '06:30', '06:35', '06:40', '06:45', '06:50',
               '06:55']
axs.set_xlabel("Time", fontsize=10)
axs.set_ylabel("Simulated Speed (kmph)", fontsize=10)
axs.set_xticks(xlim, labels=time_labels)
axs.set_xticklabels(time_labels, rotation=45, ha='right', fontsize=8)
fig.suptitle("Speed Variation")

plt.show()
