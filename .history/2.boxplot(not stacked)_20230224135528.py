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
feature = 'expr' #此处值是范例，实际上需要根据网页决定
dataset = 'GSE133684' #此处值是范例，实际上需要根据网页决定
specimen = 'ev' #此处值是范例，实际上需要根据网页决定

#以下变量由上述选择自动决定，因为具有关联性
molecule = 'cfrna'
entity = 'entity'
value = 'iclv'

#根据以上条件查询所有可能的疾病类型
sql_disease = f"""
	SELECT *
	FROM (
        SELECT SUBSTRING_INDEX(TABLE_NAME,'-',1) AS NT,
			SUBSTRING_INDEX(SUBSTRING_INDEX(TABLE_NAME,'-',-6),'-',1) AS Omics,
			SUBSTRING_INDEX(SUBSTRING_INDEX(TABLE_NAME,'-',-5),'-',1) AS Dataset,
			SUBSTRING_INDEX(SUBSTRING_INDEX(TABLE_NAME,'-',-4),'-',1) AS Entity,
			SUBSTRING_INDEX(SUBSTRING_INDEX(TABLE_NAME,'-',-3),'-',1) AS Disease_condition,
			SUBSTRING_INDEX(SUBSTRING_INDEX(TABLE_NAME,'-',-2),'-',1) AS Specimen,
			SUBSTRING_INDEX(TABLE_NAME,'-',-1) AS Value_type
		FROM information_schema.`TABLES`
		WHERE table_schema='exOmics'
        	AND (TABLE_NAME LIKE '%gse%'
            OR TABLE_NAME LIKE '%prjeb%' 
            OR TABLE_NAME LIKE '%prjna%' OR TABLE_NAME LIKE '%gse%' 
		OR TABLE_NAME LIKE '%srp%' OR TABLE_NAME LIKE '%pxd%') AND TABLE_NAME NOT LIKE '%gsea%'
        )ori
	WHERE Dataset LIKE '%{dataset}%'
		AND
"""


diseases 

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


#! 需要注意的是, boxplot在设计中有2种形式, 即一般的boxplot和堆叠的boxplot。具体设计在「数据展示形式」ppt中有。

#* 1.非堆叠的batplot，适用于Alt.polyadenylation, BS-seq, DIP-seq, Fragment size, NO, Expression（第一类数据）
x = np.arange(table.shape[0]) #行数

fig = Figure()
ax = fig.subplots(constrained_layout=True)