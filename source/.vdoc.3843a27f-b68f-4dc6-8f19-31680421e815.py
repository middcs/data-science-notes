# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
sns.set_style("whitegrid")

n_points = 20
x = np.random.rand(n_points)
y = 2 * x + 1

fig, ax = plt.subplots(figsize=(6, 4))
sns.lineplot(x=x, y=y, color = "black", ax=ax, label = r"$f(x) = 2x + 1$")

ax.set(title = "True linear relationship", xlabel = r"Feature $x$", ylabel = r"Target $y$")
ax.legend()
#
#
#
#
#
x_new = 0.5
y_new = 2 * x_new + 1

ax.scatter(x_new, y_new, color='black', s=100, label = "Prediction for $x=0.5$")
ax.legend()
fig
#
#
#
#
#
y = 2 * x + np.random.normal(0, 0.2, size=n_points) + 1

df = pd.DataFrame({
    'x': x,
    'y': y
})

fig_1, ax = plt.subplots(figsize=(6, 4))

sns.scatterplot(data=df, x='x', y='y', ax=ax)
ax.set(title = "Simulated Data", xlabel = r"Feature $x$", ylabel = r"Target $y$")
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
k_params = 5

model_df = pd.DataFrame({
    'w': 2*(np.random.rand(k_params) - 0.5) + 2,
    'b': 2*(np.random.rand(k_params) - 0.5) + 1
})

model_df
#
#
#
#
#
#---
for i in range(k_params):     
    w = model_df.loc[i, 'w']
    b = model_df.loc[i, 'b']
    
    df["y_pred"] = w * df["x"] + b
    sns.lineplot(data=df, x='x', y='y_pred', ax=ax, label = f'Model {i}')
#---

fig_1
#
#
#
#
#

fig, ax = plt.subplots(figsize=(6, 4))

sns.scatterplot(data=df, x='x', y='y', ax=ax)

# example model parameters
w = 2.1
b = 0.9

df['y_pred'] = w * df['x'] + b

# plot regression line
x_vals = np.linspace(df['x'].min(), df['x'].max(), 200)
ax.plot(x_vals, w * x_vals + b, color='black', linewidth=2, label=fr'Model: $\hat{{y}}={w:.1f}x+{b:.1f}$')

# draw residuals as vertical lines from observed y to predicted y
ax.vlines(df['x'], df['y'], df['y_pred'], color='gray', linestyle='--', alpha=0.8, linewidth=1, label = "Residuals")

ax.legend()
fig
#
#
#
#
#
def score_model(model_df, df, metric):
    return model_df.apply(lambda row: metric(df["y"], row['w'] * df["x"] + row['b']), axis=1)
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: false
#| column: margin
#| fig-cap: The same five candidate models as above. 
fig_1
#
#
#
#---
def mean_residuals(y, y_pred):
    return (y_pred - y).mean()

model_df["mean_residuals"] = score_model(model_df, df, mean_residuals)
model_df.sort_values("mean_residuals")
#---
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#---
def mse(y, y_pred):
    return ((y_pred - y) ** 2).mean()
#---
#
#
#
#
#
#---
model_df["mse"] = score_model(model_df, df, mse)
model_df.sort_values("mse", inplace=True)
model_df
#---
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
df = pd.read_csv("https://raw.githubusercontent.com/middcs/data-science-notes/refs/heads/main/data/abalone/abalone.csv")
#
#
#
#
#
df.head()
#
#
#
#
#
sns.pairplot(df, x_vars = ["height (mm)", "length (mm)", "shell_weight (g)"], y_vars = ["rings"], diag_kind='kde', plot_kws={'alpha':0.5}, )
#
#
#
#
#
df["summed_weight (g)"]  = df["shucked_weight (g)"] + df["viscera_weight (g)"] + df["shell_weight (g)"]
sns.scatterplot(data=df, x='whole_weight (g)', y='summed_weight (g)', alpha = 0.2)
#
#
#
#
#
df.drop(columns=["whole_weight (g)"], axis=1, inplace=True)
#
#
#
#
#
#
#
#
#
#
#
#
w_1_guess = 15
w_2_guess = 4
b_guess = 1.5

df['rings_pred'] = w_1_guess * df['diameter (mm)'] + w_2_guess * df['shucked_weight (g)'] + b_guess

mse_value = mse(df['rings'], df['rings_pred'])
#
#
#
#
#
df.drop(columns=['rings_pred', 'summed_weight (g)'], inplace=True)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
from sklearn.linear_model import LinearRegression
#
#
#
#
#
df = pd.get_dummies(df, columns=['sex'], drop_first=True, dtype=int)

df.columns
#
#
#
#
#
#
#
X = df.drop(columns=['rings'])
y = df['rings']
#
#
#
#
#
LR = LinearRegression()
fit = LR.fit(X, y)
#
#
#
#
#
y_pred = LR.predict(X)
#
#
#
#
#
mse(y, y_pred)
#
#
#
#
#
#
#
pd.DataFrame({
    'feature': LR.feature_names_in_,
    'coefficient': LR.coef_
}).sort_values(by='coefficient', ascending=False)
#
#
#
#
#
