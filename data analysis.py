import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.txt',
                sep='\s+',
                 header=None,
                 names=['depth', 'seed', 'strategy', 'parameter',
                        'solution_length', 'states_processed',
                        'states_visited', 'max_depth', 'time'],encoding='UTF-16LE')

df_bfs = df[df['strategy'] == 'bfs']
df_dfs = df[df['strategy'] == 'dfs']

group_bfs = df_bfs.groupby(['parameter'])
group_dfs = df_dfs.groupby(['parameter'])

mean_bfs_sp = group_bfs['states_processed'].mean()
mean_dfs_sp = group_dfs['states_processed'].mean()
mean_bfs_md = group_bfs['max_depth'].mean()
mean_dfs_md = group_dfs['max_depth'].mean()
mean_bfs_sl = group_bfs['solution_length'].mean()
mean_dfs_sl = group_dfs['solution_length'].mean()
mean_bfs_t = group_bfs['time'].mean()
mean_dfs_t = group_dfs['time'].mean()
print(mean_dfs_sp)
print(mean_bfs_sp)
print(mean_dfs_md)
print(mean_bfs_md)
print(mean_dfs_sl)
print(mean_bfs_sl)
print(mean_dfs_t)
print(mean_bfs_t)

df_bfs_dfs = df[df['strategy'].isin(['bfs', 'dfs'])]

group_bfs_dfs = df_bfs_dfs.groupby(['strategy', 'depth'])

mean_bfs_dfs_states = group_bfs_dfs['states_processed'].mean()
mean_bfs_dfs_time   = group_bfs_dfs['time'].mean()
mean_bfs_dfs_mdepth = group_bfs_dfs['max_depth'].mean()
mean_bfs_dfs_sollength = group_bfs_dfs['solution_length'].mean()

print("=== BFS / DFS ===")
print("Średnia (states_processed):\n", mean_bfs_dfs_states)
print("Średnia (time):\n", mean_bfs_dfs_time)
print("Średnia (max_depth):\n", mean_bfs_dfs_mdepth)
print("Średnia (sollength):\n", mean_bfs_dfs_sollength)

df_astr = df[df['strategy'] == 'astr']

group_astr = df_astr.groupby(['strategy', 'parameter', 'depth'])

mean_astr_states = group_astr['states_processed'].mean()
mean_astr_time   = group_astr['time'].mean()
mean_astr_mdepth = group_astr['max_depth'].mean()
mean_astr_sollength = group_astr['solution_length'].mean()


print("\n=== A* ===")
print("Średnia (states_processed):\n", mean_astr_states)
print("Średnia (time):\n", mean_astr_time)
print("Średnia (max_depth):\n", mean_astr_mdepth)
print("Średnia (sollength):\n", mean_astr_sollength)

df_bfs_dfs_states = mean_bfs_dfs_states.unstack('strategy')


df_astr_states = (
    mean_astr_states
      .reset_index(level='strategy', drop=True)
      .unstack('parameter')
)

df_astr_states = df_astr_states.rename(columns={
    'hamm': 'A*hamm',
    'manh': 'A*manh'
})


def plotSomething(bfs_dfs, astr, param):
    df_bfs_dfs_metric = bfs_dfs.unstack('strategy')
    df_astr_metric = (astr
                      .reset_index(level='strategy', drop=True)
                      .unstack('parameter')
                      .rename(columns={'hamm': 'A*hamm', 'manh': 'A*manh'})
                      )

    df_metric = pd.concat([df_bfs_dfs_metric, df_astr_metric], axis=1).sort_index()

    for strategy in df_metric.columns:
        plt.figure()
        plt.plot(df_metric.index, df_metric[strategy], marker='o')
        plt.xlabel('głębokość')
        plt.ylabel(param)
        plt.title(f'{param} vs. głębokość dla {strategy}')
        plt.legend([strategy])
        plt.show()

plotSomething(mean_bfs_dfs_states, mean_astr_states, "stany przetworzone")
plotSomething(mean_bfs_dfs_time, mean_astr_time, "czas")
plotSomething(mean_bfs_dfs_mdepth, mean_astr_mdepth, "maks. głębokość rekurencji")
plotSomething(mean_bfs_dfs_sollength, mean_astr_sollength, "długość rozwiązania")