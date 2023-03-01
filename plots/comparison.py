
#! Comparison的图，是对于一个entity，在所有疾病类型之间的比较。
#! 对于第一类数据，只需要一张图，因为一个基因对应表格中的一行。
#! 对于第二类数据，一个基因可能对应表格中的n行，因此需要选择其中一个来做图，详见原型。

import pandas as pd
from matplotlib.figure import Figure
import numpy as np
import matplotlib.cm as cm
from copy import copy
from .select_molecole_entity_value import select_molecule_entity_value
from statannotations.Annotator import Annotator
import matplotlib as mpl
import itertools
import matplotlib.pyplot as plt
import seaborn as sns

def comparison(gene: str, feature: str, dataset:str, specimen: str, entity: str, conn) -> Figure:
    """
    gene = 'ENSG00000000457' #基因主页所对应的基因 \\
    feature = 'altp' #此处值是范例，实际上需要根据网页决定 \\
    dataset = 'gse68086' #此处值是范例，实际上需要根据网页决定 \\
    specimen = 'tep' #此处值是范例，实际上需要根据网页决定 \\
    entity = 'entity' #此处值是范例，实际上需要根据网页决定
    """

    #1
    # gene = 'ENSG00000187608' #基因主页所对应的基因 \\
    # feature = 'bsseq' #此处值是范例，实际上需要根据网页决定 \\
    # dataset = 'gse93203' #此处值是范例，实际上需要根据网页决定 \\
    # specimen = 'serum' #此处值是范例，实际上需要根据网页决定
    # entity = 'gene'
    with conn:
        molecule, value = select_molecule_entity_value(dataset, feature, specimen, entity, conn)


        sql_disease = f"""
            SELECT ori.Disease_condition
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
                    AND (
                        TABLE_NAME LIKE '%gse%'
                        OR TABLE_NAME LIKE '%prjeb%'
                        OR TABLE_NAME LIKE '%prjna%'
                        OR TABLE_NAME LIKE '%gse%'
                        OR TABLE_NAME LIKE '%srp%'
                        OR TABLE_NAME LIKE '%pxd%'
                    )
                    AND TABLE_NAME NOT LIKE '%gsea%'
                )ori
            WHERE Dataset LIKE '%{dataset}%'
                AND Omics LIKE '%{feature}%'
                AND Entity LIKE '%{entity}%'
                AND Disease_condition NOT LIKE '%mean%'
        """
        diseases = pd.read_sql_query(sql_disease, conn)

        diseases_data = {}

        class FeatureError(Exception): #异常feature
            def __init__(self, feature):
                self.feature = feature

            def __str__(self):
                return f"Invalid feature name: {self.feature}"

        type = 0
        #查询数据
        if feature in ['altp','chim','edit','snp','splc']: #第二类数据
            type = 2
            for disease in diseases['Disease_condition']:
                query_sql = f"""
                    SELECT c.*
                    FROM `{molecule}-{feature}-{dataset}-{entity}-{disease}-{specimen}-{value}` c, gene_index g
                    WHERE c.feature LIKE CONCAT('%',g.ensembl_gene_id,'%')
                        AND g.ensembl_gene_id LIKE '%{gene}%'
                """
                temp = pd.read_sql_query(query_sql, conn) #选择某个疾病类型下的某个基因的所有样本的值，应当是1*n的矩阵
                fentities = list(temp['feature'])
                for fentity in fentities:
                    if fentity not in diseases_data.keys():
                        diseases_data[fentity] = {}
                    diseases_data[fentity][disease.upper()] = list(temp[temp['feature']==fentity].iloc[0,1:].astype('float'))
        elif feature in ['apa','bsseq','dipseq','fragsize','no','expr']: #第一类数据
            type = 1
            for disease in diseases['Disease_condition']:
                query_sql = f"""
                    SELECT c.*
                    FROM `{molecule}-{feature}-{dataset}-{entity}-{disease}-{specimen}-{value}` c, gene_index g
                    WHERE c.feature LIKE CONCAT('%',g.ensembl_gene_id,'%')
                        AND g.ensembl_gene_id LIKE '%{gene}%'
                """
                temp = pd.read_sql_query(query_sql, conn) #选择某个疾病类型下的某个基因的所有样本的值，应当是1*n的矩阵
                try:
                    diseases_data[disease.upper()] = list(temp.iloc[0,1:].astype('float'))
                except IndexError:
                    diseases_data[disease.upper()] = np.zeros(temp.shape[1],dtype='float')
        else:
            raise FeatureError(feature)

        #! 对于第二类数据，一个基因由于不同的疾病类型可能具有不同的entity数量。因此在上述查完数据之后，需要再根据查出来的数据来选择需要查看的entity
        if type == 2:
            n_entities = len(diseases_data.keys())
            fig = Figure(figsize=(10*n_entities,5))
            #ax = fig.subplots(n_entities,1)
            sns.set(style="whitegrid")
            for i in range(n_entities): #对于每个entity
                ax = fig.add_subplot(1,n_entities,i+1)
                anentity = list(diseases_data.keys())[i]
                data_of_an_entity = diseases_data[anentity]

                #重整数据
                data = pd.DataFrame(pd.DataFrame.from_dict(data_of_an_entity,orient='index').T.unstack())
                data = data.reset_index().drop(labels='level_1',axis=1).rename(columns={'level_0':'Diseases',0:'Value'}).dropna()

                labels = list(data_of_an_entity.keys())
                labels_combine = list(itertools.combinations(labels,2))
                #Boxplot
                plotfig = sns.boxplot(data=data, x='Diseases',y='Value',notch=False,ax=ax)

                ax.set_xlabel('Disease Conditions')
                ax.set_ylabel(f'{value.upper()}')
                ax.set_xticklabels(labels,rotation=90)
                ax.set_title(anentity,fontdict={'fontsize':8})
                # #Fill color
                # cmap = cm.ScalarMappable(cmap=mpl.cm.cool)
                # test_mean = [np.mean(x) for x in data]
                # for patch, color in zip(plotfig['boxes'], cmap.to_rgba(test_mean)):
                #     patch.set_facecolor(color)

                #统计注释
                annot = Annotator(plotfig, labels_combine, data=data, x='Diseases',y='Value', order=labels, hide_non_significant=True)
                annot.configure(test='Mann-Whitney', loc='outside', verbose=2, text_format='star', line_height=0.02, line_offset=0.05, text_offset=0.04)
                annot.apply_test()
                ax, test_results = annot.annotate()

                fig.tight_layout()
            #return fig
        elif type == 1:
            fig = Figure(figsize=(10,5))
            sns.set(style="whitegrid")
            ax = fig.add_subplot(1,1,1)

            #重整数据
            data = pd.DataFrame(pd.DataFrame.from_dict(diseases_data,orient='index').T.unstack())
            data = data.reset_index().drop(labels='level_1',axis=1).rename(columns={'level_0':'Diseases',0:'Value'}).dropna()

            labels = list(diseases_data.keys())
            labels_combine = list(itertools.combinations(labels,2))
            #Boxplot
            plotfig = sns.boxplot(data=data, x='Diseases',y='Value',notch=False,ax=ax)

            ax.set_xlabel('Disease Conditions')
            ax.set_ylabel(f'{value.upper()}')
            ax.set_xticklabels(labels,rotation=90)
            ax.set_title(gene,fontdict={'fontsize':8})
            # #Fill color
            # cmap = cm.ScalarMappable(cmap=mpl.cm.cool)
            # test_mean = [np.mean(x) for x in data]
            # for patch, color in zip(plotfig['boxes'], cmap.to_rgba(test_mean)):
            #     patch.set_facecolor(color)

            #统计注释
            annot = Annotator(plotfig, labels_combine, data=data, x='Diseases',y='Value', order=labels, hide_non_significant=True)
            annot.configure(test='Mann-Whitney', loc='outside', verbose=2, text_format='star', line_height=0.02, line_offset=0.05, text_offset=0.04)
            annot.apply_test()
            ax, test_results = annot.annotate()

        return fig