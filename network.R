library("igraph")
#导入数据
data <- read.csv("C:\\Users\\xianyun yehe\\matrix.csv",header=FALSE)
#转化为矩阵
matrix <- as.matrix(data)
#转化为邻接矩阵
graph <- graph_from_adjacency_matrix(matrix)
#保存图
write_graph(graph,"C:\\Users\\xianyun yehe\\graph.gml")
#计算网络的度
degree <- degree(graph)
#计算邻近度
closeness <- closeness(graph)
#计算间接度
betweenness <- betweenness(graph)
