import pandas as pd
from matplotlib.figure import Figure
import numpy as np
import matplotlib.cm as cm
import matplotlib as mpl
from .select_molecole_entity_value import select_molecule_entity_value
import seaborn as sns
from textwrap import wrap

def table_bar(gene: str, feature: str, dataset: str, disease: str, specimen: str, entity: str, conn):
    """
    gene = 'ENSG00000000457' #基因主页所对应的基因 \\
    feature = 'altp' #此处值是范例，实际上需要根据网页决定 \\
    dataset = 'gse68086' #此处值是范例，实际上需要根据网页决定 \\
    disease = 'lihc' #此处值是范例，实际上需要根据网页决定 \\
    specimen = 'tep' #此处值是范例，实际上需要根据网页决定 \\
    entity = ''
    """
    #以下变量由上述选择自动决定，因为具有关联性
    # molecule = 'cfrna'
    # entity = 'entity'
    # value = 'count'
    with conn:
        molecule, value = select_molecule_entity_value(dataset, feature, specimen, entity, conn)

        #查询语句
        query_sql = f"""
            SELECT c.*
            FROM `{molecule}-{feature}-{dataset}-{entity}-{disease}-{specimen}-{value}` c, gene_index g
            WHERE c.feature LIKE CONCAT('%',g.ensembl_gene_id,'%')
                AND g.ensembl_gene_id LIKE '%{gene}%'
        """

        #获得表格，可以直接在网页中展示
        table = pd.read_sql_query(query_sql, conn)
        table.iloc[:,1:] = table.iloc[:,1:].astype('float')
        table = table.set_index('feature') #feature列设为index

        #作图
        #将获得一个多行多列的表，每一行代表一个entity，每一列代表一个样本或一个疾病类型（当disease是mean时）。因此做barplot选择做dodged barplot (即grouped bat chart)。
        x = np.arange(table.shape[0]) #行数向量
        y = table.shape[1]
        fig = Figure()
        ax = fig.subplots()

        width_all = 0.9
        width = width_all/y  # the width of the bars
        multiplier = 0
        cm.ScalarMappable(cmap=mpl.cm.cool)

        for coli in range(table.shape[1]): #每一列
            attribute = table.columns[coli] #第i列的列名
            measurement = table.iloc[:,coli] #第i列的数据
            offset = width * multiplier #每个group的偏移量
            rects = ax.bar(x + offset, measurement, width, label=attribute)
            #ax.bar_label(rects, padding=3)
            multiplier += 1

        ax.set_ylabel(f'{value.upper()}')
        ax.set_title(f'{value.upper()} of {gene.upper()} in dataset {dataset.upper()} in specimen {specimen.upper()} of disease {disease.upper()}')

        labels = [ '\n'.join(wrap(l, 15)) for l in list(table.index)]
        ax.set_xticks(x + width_all/2, labels)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        return fig, table.to_json()
