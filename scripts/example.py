import pymysql
from ..plots.select_molecole_entity_value import select_molecule_entity_value
from ..plots.heat_map import heat_map

# 使用时修改
conn = pymysql.connect(
	host="very secret",
	port=999,
	user="very secret",
	passwd="very secret",
	db='very secret'
)

gene = 'ENSG00000000457'
feature = 'altp'
dataset = 'gse68086'
specimen = 'tep'

molecule, entity, value = select_molecule_entity_value(dataset, feature, specimen, conn)

fig = heat_map(gene, feature, dataset, specimen, conn)
fig.show()
