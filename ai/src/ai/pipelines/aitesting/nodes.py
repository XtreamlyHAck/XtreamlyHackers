from pyspark.sql import DataFrame
import os
import pandas as pd
pd.set_option('display.max_columns', None)
import pytz
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, LinearSegmentedColormap, Normalize
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta
import joblib

def reporting(_:bool, df_dm: DataFrame):
    folder = 'aitesting'
    col_y = ['y_std_60sec'][0] # obj is actually the return but lets skip it for now
    col_x = [
        'ids_mean_240sec',
        'qty_stddev_14400sec',
        'price_ema_240sec',
        'price_stddev_240sec',
        'price_max_240sec',
        'price_beta_240sec',
        'price_perc10_240sec',
        'price_stddev_3600sec',
        'price_stddev_14400sec',
    ]
    model_name = 'model_xgb_y_std_60sec'
    model_filename = os.path.join('models', f'{model_name}.joblib')
    model = joblib.load(model_filename)
    pred_std = model.predict(df_dm[col_x])

    # =============================================================================
    # Meta model (combine various models and maybe soomth - not sure here because we loose sudden close signals)
    df_bt = df_dm.copy()[['_time', col_y, 'y_ret_60sec']]
    df_bt['_time'] = [datetime.fromisoformat(str(t)).replace(tzinfo=pytz.utc) for t in df_bt['_time']]

    pred = (pred_std+pred_std)/2
    df_bt['pred'] = pred

    # =============================================================================
    # Policy thresholds
    df_policy = df_bt.copy()[["_time", col_y]]
    df_policy['pred'] = pred
    df_policy.set_index('_time', inplace=True)
    windows, colors_i = [60, 240], [500, 700]
    for i, (w, c_i) in enumerate(zip(windows, colors_i)): 0
    w = 240
    data = {
        'score_pred': [],
    }
    for idx, r in df_policy.iloc[:].iterrows():
        df_hist = df_policy[
            (df_policy.index >= idx - timedelta(minutes = w)) &
            (df_policy.index < idx)]
        data['score_pred'] += [(r['pred']-df_hist[col_y].mean())/(df_hist[col_y].mean()**.5)]
    df_roll = pd.DataFrame(data).bfill()
    df_roll = df_roll.rename(columns = {c: f"pred_{w}min_{c}" for c in df_roll.columns} )
    df_policy.loc[:, df_roll.columns] = df_roll.values
    df_policy = df_policy.reset_index(drop=False)
    df_policy = df_policy.rename(columns={"pred_240min_score_pred": "score_240min"})


    # =============================================================================
    # Data simulate
    df = df_bt.copy()[['_time', col_y, 'pred']]
    df_p = df_dm.copy()
    df_p['_time'] = [datetime.fromisoformat(str(t)).replace(tzinfo=pytz.utc) for t in df_p['_time']]
    df = df.merge(df_p, on="_time", how="inner")
    df = df.merge(df_policy[["_time", "score_240min"]], on="_time", how="inner")
    df['ret'] = df['close']/df['open']-1

    df_pred = df_bt.copy()[['_time', col_y, 'pred']].rename(columns = {col_y: 'y'})

    # =============================================================================
    # Model stats
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    import numpy as np

    # Actual values and predictions
    y_true = df_pred['y']
    y_pred = df_pred['pred']

    # Calculate metrics
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    out = f"""
    Model evaluation metrics for the predictions against the actual values:
    mae: {mae.round(8).astype(float)}
    mse: {np.round(mse, 8)} 
    rmse: {np.round(rmse, 8)}
    r2: {np.round(r2, 8)}
    """
    print(out)

    # =============================================================================
    # Color
    palette = [
        "#3B82F6",
        "#14B8A6",
        "#F59E0B",
        "#EAB308",
        "#A16207",
        "#C2410C",
    ]
    def _pred_color(pred, palette=palette, extreme = True, outliers=False):
        cmap = LinearSegmentedColormap.from_list('custom_palette', palette, N=1000)
        if extreme:
            q = np.quantile(pred, 0.99)
            norm = Normalize(vmin=np.min(pred), vmax=q)
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            colors = [to_hex(sm.to_rgba(p)) if p <= q else "#F87171" for p in pred]
        else:
            if outliers:
                q = np.percentile(np.abs(pred),99)
                norm = Normalize(vmin=-q, vmax=q)
                sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
                colors = [to_hex(sm.to_rgba(p)) if np.abs(p) <= q else "#1C1917" for p in pred]
            else:
                norm = Normalize(vmin=-np.max(np.abs(pred)), vmax=np.max(np.abs(pred)))
                sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
                colors = [to_hex(sm.to_rgba(p)) for p in pred]
        return colors

    df['color_pred'] = _pred_color(pred)
    df['color_score_240min'] = _pred_color(df['score_240min'], [
        "#3B82F6",
        "#1C1917",
        "#F87171",
    ])



    # =============================================================================
    # plots

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.scatter(df['pred'], df[col_y],color=df['color_pred'],alpha=.9, s=15, label=f"predicted")
    ax.set_xlim((0, df[col_y].quantile(.995)))
    ax.set_ylim((0, df[col_y].quantile(.995)))
    ax.set_yticks(ax.get_yticks())
    ax.set_xticks(ax.get_xticks())
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, fontsize=12)
    ax.grid(linewidth=1, color='black', alpha=.1)
    ax.set_title("Real 1min std vs Predictions", fontsize=24, pad=30)
    ax.set_ylabel(f"Values of {col_y}", fontsize=16, labelpad=20)
    ax.set_xlabel(f"Predicted of {col_y}", fontsize=16, labelpad=20)
    legend = ax.legend(loc='upper left', frameon=True, fontsize=16)
    for text in ax.legend_.get_texts():
        text.set_color('black')
    legend.get_frame().set_alpha(0.6)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.tight_layout(rect=[0.04, 0.04, .96, .96])
    fig.savefig(os.path.join(folder, f'scatter pred.png'), dpi=200)
    fig.clf()

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.scatter(df['score_240min'], df[col_y],color=df['color_pred'],alpha=.9, s=15, label=f"predicted")
    ax.set_xlim((0, df['score_240min'].quantile(.995)))
    ax.set_ylim((0, df[col_y].quantile(.995)))
    ax.set_yticks(ax.get_yticks())
    ax.set_xticks(ax.get_xticks())
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, fontsize=12)
    ax.grid(linewidth=1, color='black', alpha=.1)
    ax.set_title("Scores (Poisson distribution) vs Predictions", fontsize=24, pad=30)
    ax.set_ylabel(f"Values of {col_y}", fontsize=16, labelpad=20)
    ax.set_xlabel(f"score_240min of {col_y}", fontsize=16, labelpad=20)
    legend = ax.legend(loc='upper left', frameon=True, fontsize=16)
    for text in ax.legend_.get_texts():
        text.set_color('black')
    legend.get_frame().set_alpha(0.6)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.tight_layout(rect=[0.04, 0.04, .96, .96])
    fig.savefig(os.path.join(folder, f'scatter score_240min.png'), dpi=200)
    fig.clf()

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.scatter(df['pred'], df['ret'],color=df['color_pred'],alpha=.9, s=15, label=f"returns 1min")
    ax.set_xlim((0, df[col_y].quantile(.995)))
    ax.set_ylim((-df['ret'].abs().quantile(.995), df['ret'].abs().quantile(.995)))
    ax.set_yticks(ax.get_yticks())
    ax.set_xticks(ax.get_xticks())
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, fontsize=12)
    ax.grid(linewidth=1, color='black', alpha=.1)
    ax.set_title("Returns vs Predictions", fontsize=24, pad=30)
    ax.set_ylabel(f"Returns over next 1min", fontsize=16, labelpad=20)
    ax.set_xlabel(f"Predicted of {col_y}", fontsize=16, labelpad=20)
    legend = ax.legend(loc='upper left', frameon=True, fontsize=16)
    for text in ax.legend_.get_texts():
        text.set_color('black')
    legend.get_frame().set_alpha(0.6)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.tight_layout(rect=[0.04, 0.04, .96, .96])
    fig.savefig(os.path.join(folder, f'scatter ret.png'), dpi=200)
    fig.clf()


    fig, ax = plt.subplots(figsize=(16, 9))
    df_plt = df[df[col_y] <= df[col_y].quantile(0.995)]
    bin_edges = np.linspace(0, df_plt[col_y].max(), 501)
    ax.hist(df_plt['pred'], bins=bin_edges, color="#14B8A6", alpha=0.5, label="predicted")
    ax.hist(df_plt[col_y], bins=bin_edges, color="#1C1917", alpha=0.5, label=f"{col_y}")
    ax.set_xlim((0, df_plt[col_y].max()))
    ax.set_yticks(ax.get_yticks())
    ax.set_xticks(ax.get_xticks())
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, fontsize=12)
    ax.grid(linewidth=1, color='black', alpha=0.1)
    ax.set_title("Histogram of real and predicted std", fontsize=24, pad=30)
    ax.set_ylabel(f"Count", fontsize=16, labelpad=20)
    ax.set_xlabel(f"Values of {col_y}", fontsize=16, labelpad=20)
    legend = ax.legend(loc='upper left', frameon=True, fontsize=16)
    for text in ax.legend_.get_texts():
        text.set_color('black')
    legend.get_frame().set_alpha(0.6)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout(rect=[0.04, 0.04, .96, .96])
    fig.savefig(os.path.join(folder, 'hist pred.png'), dpi=200)
    fig.clf()


    fig, ax = plt.subplots(figsize=(32, 9))
    ax.plot(df['_time'], df['open'].values,
            '-',linewidth=.995, color='black',alpha=.7, label=f"ETHUSD price")
    ax.scatter(df['_time'], df['open'],color=df['color_pred'],alpha=.9, s=15, label=f"predicted")
    ax.set_yticks(ax.get_yticks())
    ax.set_xticks(ax.get_xticks())
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, fontsize=12)
    ax.grid(linewidth=1, color='black', alpha=.1)
    ax.set_xlim((df['_time'].iloc[0], df['_time'].iloc[-1]))
    ax.set_title("Predictions Applied to ETHUSDT ", fontsize=24, pad=30)
    ax.set_ylabel("ETHUSDT", fontsize=16, labelpad=20)
    legend = ax.legend(loc='upper left', frameon=True, fontsize=16)
    for text in ax.legend_.get_texts():
        text.set_color('black')
    legend.get_frame().set_alpha(0.6)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.tight_layout(rect=[0.04, 0.04, .96, .96])
    fig.savefig(os.path.join(folder, f'timeline ETHUDT pred.png'), dpi=200)
    fig.clf()

    fig, ax = plt.subplots(figsize=(32, 9))
    ax.plot(df['_time'], df['open'].values,
            '-',linewidth=.995, color='black',alpha=.7, label=f"ETHUSD price")
    ax.scatter(df['_time'], df['open'],color=df['color_score_240min'],alpha=.9, s=15, label=f"scores")
    ax.set_yticks(ax.get_yticks())
    ax.set_xticks(ax.get_xticks())
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, fontsize=12)
    ax.grid(linewidth=1, color='black', alpha=.1)
    ax.set_xlim((df['_time'].iloc[0], df['_time'].iloc[-1]))
    ax.set_title("Poisson Scores Applied to ETHUSDT ", fontsize=24, pad=30)
    ax.set_ylabel("ETHUSDT", fontsize=16, labelpad=20)
    legend = ax.legend(loc='upper left', frameon=True, fontsize=16)
    for text in ax.legend_.get_texts():
        text.set_color('black')
    legend.get_frame().set_alpha(0.6)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.tight_layout(rect=[0.04, 0.04, .96, .96])
    fig.savefig(os.path.join(folder, f'timeline ETHUDT score.png'), dpi=200)
    fig.clf()

    return True
