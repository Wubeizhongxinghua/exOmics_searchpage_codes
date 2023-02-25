# exOmics Searchpage Codes

**This repo. is for restoring and updating code used for exOmics search page.**

The site of web page prototype is: https://cc.mockplus.cn/s/7QMjg54avJO

*The following contents are updating records and todos.*

1. Table & barplot

- [X] Code
- [X] Prototype
- [ ] Tables of projection of sites of SNP, Editing to genes

- Use function:
  ```python
  from tableBar import tableBar
  import pandas as pd
  import pymysql
  import ...

  conn = ...
  fig, data_json = tableBar(gene, feature, dataset, disease, specimen, conn)
  ```

2. Boxplot

- [X] Code of not stacked barplot
- [X] Code of stacked barplot
- [X] Prototype

+ Use function:
  ```python
  from nonStackBox import nonStackBox
  from stackBox import stackBox
  import pandas as pd
  import pymysql
  import ...

  conn = ...
  fig_stack = stackBox(gene, feature, dataset, specimen, conn)
  fig_nonstack = nonStackBox(gene, feature, dataset, specimen, conn)
  ```

3. Heatmap

- [X] Code
- [X] Prototype
- [ ] Tables of projection of sites of SNP, Editing to genes

+ Use function:
  ```python
  from heatMap import heatMap
  import pandas as pd
  import pymysql
  import ...

  conn = ...
  fig = heatMap(gene, feature, dataset, disease, specimen, conn)
  ```

4. Comparison box plot

- [ ] TODO
