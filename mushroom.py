# Decision Tree using Hunt's algorithm

import csv
import pydot

fileh=open('mushroom.csv','r')
dataset=list()

reader = csv.reader(fileh, delimiter=',')
i=1
for row in reader:
	if i==1:
		actual_attr=row
		i=0
	else:
		dataset.append(row)

attr=range(len(dataset[0])-1)

# Calculating Gini index
def gini(dataset,attr):
	d=dict()
	for i in dataset:
		if i[attr] not in d:
			d[i[attr]]={}
		if i[-1] not in d[i[attr]]:
			d[i[attr]][i[-1]]=1
		else:
			d[i[attr]][i[-1]]+=1
	gini_list=list()
	total_each=list()
	
	for (k,v) in d.items():
		val=sum(v.values())
		total_each.append(val)
		t=0
		for (k1,v1) in v.items():
			try:
				t+=(v1/float(val))*(v1/float(val))
			except:
				t+=0
		t=1-t
		gini_list.append(t)
	tot=sum(total_each)
	wavg=0
	for i in range(len(gini_list)):
		wavg+=(total_each[i]/float(tot))*gini_list[i]
	return wavg

def chooseBestSplit(dataset,labels):
	gini_list=[]
	for i in labels:
		gini_list.append(gini(dataset,i))
	return labels[gini_list.index(min(gini_list))]


def countLabel(dataset):
	d=dict()
	for i in dataset:
		if i[-1] not in d:
			d[i[-1]]=1
		else:
			d[i[-1]]+=1
	return d

def stoppingCond(dataset,attr):
	d=countLabel(dataset)
	for (k,v) in d.items():
		if v==len(dataset):
			return 1
	if attr==[]:
		return 1
	return 0

def classify(dataset,attr):
	d=countLabel(dataset)
	l=d.values()
	m=max(l)
	for (k,v) in d.items():
		if v==m:
			return k

def TreeGrowth(dataset,attr):
	if stoppingCond(dataset,attr):
		label=classify(dataset,attr)
		return label
	else:
		d=dict()
		best=chooseBestSplit(dataset,attr)
		V=list()
		for i in dataset:
			if i[best] not in V:
				V.append(i[best])
		
		attr.remove(best)
		best1=actual_attr[best]
		d[best1]={}
		for i in range(len(V)):
			Ev=list()
			for j in dataset:
				if j[best]==V[i]:
					Ev.append(j)
			d[best1][V[i]]=TreeGrowth(Ev,attr)
	return d

d=TreeGrowth(dataset,attr)
#print d

def makeDecision(d):
	if type(d) is not dict:
		return d
	else:
		a=d.keys()
		attribute=a[0]
		print '\nTell me the value for '+attribute
		inp=raw_input().strip()
		d=d[attribute][inp]
		result=makeDecision(d)
		return result

#print d

def draw(parent_name, child_name):
    edge = pydot.Edge(parent_name, child_name)
    graph.add_edge(edge)

def visit(node, parent=None):
    for k,v in node.iteritems():
        if isinstance(v, dict):
            # We start with the root node whose parent is None
            # we don't want to graph the None node
            if parent:
                draw(parent, k)
            visit(v, k)
        else:
            draw(parent,k)
            # drawing the label using a distinct name
            draw(k, k+'_'+v)

graph = pydot.Dot(graph_type='graph')
visit(d)
graph.write_png('mushroom.png')

result=makeDecision(d)
print result