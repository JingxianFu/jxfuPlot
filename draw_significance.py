import seaborn as sns
import scipy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
mm = StandardScaler()


def convert_pvalue_to_asterisks(pvalue):
    if pvalue <= 0.0001:
        return "****"
    elif pvalue <= 0.001:
        return "***"
    elif pvalue <= 0.01:
        return "**"
    elif pvalue <= 0.05:
        return "*"
    return "ns"

# iris = sns.load_dataset("iris")
# data_p = iris[["sepal_length", "species"]]
# print(data_p)
# stat,p_value = scipy.stats.ttest_ind(data_p[data_p["species"]=="setosa"]["sepal_length"],
#                                      data_p[data_p["species"]=="versicolor"]["sepal_length"],
#                                      equal_var=False)
def plot_sig_bar(df=pd.DataFrame,
                 CK_name='CK',
                 tag_delimiter='-',
                 title='',
                 p=True,
                 figsize=(5, 4),
                 palette = ['#B4C2D8', '#9DB3CB', '#7D97B6', '#356CA5', '#2C5A8B']):
    '''
    绘制带有*显著性的bar图，适用于单因素之间的单尾t检验——显著性分析
    df: 输入格式为Dataframe
    第一列为标签号，第二列为数据，确保标签和repeat之间通过'-'隔开。当然也可以自定义。
    CK_name: 设置对照的名称，可以通过'-'与后面的repeat隔开
    tag_delimiter: 标签号与repeat之间的字符，可以自定义，但是每个标签的格式都要统一
    :return 各处理，平均值字典
    '''
    mean_dict = {}
    data = df
    # data['LCA'] = mm.fit_transform(data['LCA'].values.reshape(-1, 1))
    data["tag"] = [i.split(tag_delimiter)[0] for i in data[data.columns[0]]]
    treat_name = []
    for i in data['tag']:
        if i not in treat_name and i != CK_name:
            treat_name.append(i)
    plt.rcParams['font.family'] = ['Times New Roman']
    plt.rcParams["axes.labelsize"] = 15

    fig, ax = plt.subplots(figsize=figsize, dpi=300, facecolor="w")
    ax = sns.barplot(x="tag", y=data.columns[1], data=data, palette=palette,
                     estimator=np.mean, ci="sd", capsize=.1, errwidth=1, errcolor="k",
                     ax=ax,
                     **{"edgecolor": "k", "linewidth": 1})
    CK_mean = np.mean(data[data["tag"] == CK_name][data.columns[1]])
    mean_dict[CK_name] = CK_mean
    # 添加P值
    if p == True:
        for i in tqdm(range(len(treat_name))):
            if data[data["tag"] == treat_name[i]].shape[0] > 1:
                treat_mean = np.mean(data[data["tag"] == treat_name[i]][data.columns[1]])
                mean_dict[treat_name[i]] = treat_mean
                stat, p_value = scipy.stats.f_oneway(data[data["tag"] == CK_name][data.columns[1]],
                                                     data[data["tag"] == treat_name[i]][data.columns[1]])
                print(f'{CK_name}与{treat_name[i]}比较\n均值：{treat_mean/CK_mean}\nF值：{stat}, p值：{p_value}\n')
                p_value_cov = convert_pvalue_to_asterisks(p_value)  # 计算p值
                x1, x2 = 0, i+1
                y, h = data[data.columns[1]].max()*(1+0.15*i), 0.
                # 绘制横线位置
                ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1, c="k")
                # 添加P值
                ax.text((x1 + x2) * .5, y + h, p_value_cov, ha='center', va='bottom', color="k")
                # ax.tick_params(which='major', direction='in', length=3, width=1., labelsize=14, bottom=False)
    for spine in ["top", "left", "right"]:
        ax.spines[spine].set_visible(False)
    # ax.set_ylim(0, 0.8)  # outliers only
    ax.spines['bottom'].set_linewidth(2)
    ax.grid(axis='y', ls='--', c='gray')
    plt.xticks(rotation=30)
    ax.set_axisbelow(True)
    ax.set_xlabel('Treatment')
    ax.set_ylabel('content (mg/g)',)
    ax.set_title(f'{title}',)
    plt.show()
    return mean_dict



if __name__ == '__main__':
    f = pd.read_csv('/Users/fujingxian/Downloads/PycharmProjects/pythonProject/大田处理SAHA_羟胺/NH4.csv',
                    delimiter='\t',
                    index_col=0)
    data = f.T
    df = pd.DataFrame()
    df['tag'] = data.index
    df['content'] = data['LCA'].values
    print(df)
    plot_sig_bar(df)