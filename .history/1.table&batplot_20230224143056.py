import pandas as pd
from matplotlib.figure import Figure
import pymysql
import numpy as np
import matplotlib.pyplot as plt

#建立连接
conn = pymysql.connect(
	host="114.116.114.149",
	port=10022,
	user="exomics_admin",
	passwd="exomics_2022",
	db='exOmics'
)

#设定要查询的数据类型和基因
gene = 'ENSG00000067221' #基因主页所对应的基因
feature = 'splc' #此处值是范例，实际上需要根据网页决定
dataset = 'GSE68086' #此处值是范例，实际上需要根据网页决定
disease = 'lihc' #此处值是范例，实际上需要根据网页决定
specimen = 'ev' #此处值是范例，实际上需要根据网页决定

#以下变量由上述选择自动决定，因为具有关联性
molecule = 'cfrna'
entity = 'entity'
value = 'iclv'

#查询语句
query_sql = f"""
    SELECT c.*
    FROM `{molecule}-{feature}-{dataset}-{entity}-{disease}-{specimen}-{value}` c, gene_index g
    WHERE c.feature LIKE CONCAT('%',g.ensembl_gene_id,'%')
        AND g.ensembl_gene_id LIKE CONCAT('%',{gene},'%')
"""

#获得表格，可以直接在网页中展示
table = pd.read_sql_query(query_sql, conn)
table = table.set_index('feature') #feature列设为index

#作图
#将获得一个多行多列的表，每一行代表一个entity，每一列代表一个样本或一个疾病类型（当disease是mean时）。因此做barplot选择做dodged barplot (即grouped bat chart)。
x = np.arange(table.shape[0]) #行数

fig = Figure()
ax = fig.subplots()

width = 0.25  # the width of the bars
multiplier = 0

for coli in range(table.shape[1]): #每一列
    attribute = table.columns[coli] #第i列的列名
    measurement = table.iloc[:,coli] #第i列的数据
    offset = width * multiplier #每个group的偏移量
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

ax.set_ylabel(f'{value.upper()}')
ax.set_title(f'{value.upper()} of {gene.upper()} in dataset {dataset.upper()} in specimen {specimen.upper()} of disease {disease.upper()}')
ax.set_xticks(x + width, list(table.index))
ax.legend(loc='upper left', ncols=table.shape[1])
