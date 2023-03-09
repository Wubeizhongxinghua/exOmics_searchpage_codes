import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from .select_molecole_entity_value import select_molecule_entity_value


def heat_map(gene: str, feature: str, dataset: str, specimen: str, entity: str, conn) -> Figure:
	"""
	gene = 'ENSG00000000457' #基因主页所对应的基因 \\
	feature = 'altp' #此处值是范例，实际上需要根据网页决定 \\
	dataset = 'gse68086' #此处值是范例，实际上需要根据网页决定 \\
	specimen = 'tep' #此处值是范例，实际上需要根据网页决定 \\
	entity = 'entity'
	"""
	with conn:
		#以下变量由上述选择自动决定，因为具有关联性
		# molecule = 'cfrna'
		# entity = 'entity'
		# value = 'count'
		molecule, value = select_molecule_entity_value(dataset, feature, specimen, entity, conn)


		#根据以上条件查询所有可能的疾病类型
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

		#查询语句
		diseases_data = pd.DataFrame()
		for disease in diseases['Disease_condition']:
			query_sql = f"""
				SELECT c.*
				FROM `{molecule}-{feature}-{dataset}-{entity}-{disease}-{specimen}-{value}` c, gene_index g
				WHERE c.feature LIKE CONCAT('%',g.ensembl_gene_id,'%')
					AND g.ensembl_gene_id LIKE '%{gene}%'
			"""
			temp = pd.read_sql_query(query_sql, conn).set_index('feature').astype('float').mean(axis=1)
			temp = temp.to_frame()
			temp.columns = [disease.upper()]
			diseases_data = pd.concat([diseases_data,temp],axis=1)
		diseases_data = diseases_data.T

		#作图
		fig = Figure()
		ax = fig.subplots()
		xLabel = diseases_data.columns.to_list()
		yLabel = diseases_data.index.to_list()

		im = ax.imshow(diseases_data.values, cmap=plt.cm.cool)
		ax.set_yticks(range(len(yLabel)))
		ax.set_yticklabels(yLabel)
		ax.set_xticks(range(len(xLabel)))
		ax.set_xticklabels(xLabel,rotation=90)
		fig.colorbar(im,label=value.upper())
		#ax.set_title(f"Heatmap of {feature.upper()} of {gene.upper()} in {specimen.upper()} of dataset {dataset.upper()}")
		#fig.tight_layout()
		return fig
