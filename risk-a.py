#Risk Analysis
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

#pretty printing
np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)
#np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

def plotLine(x,y1,y2,y3,fileName):
	line, = plt.plot(x, y1, '-', linewidth=2, color='red', label='PR')
	line, = plt.plot(x, y2, '-', linewidth=2, color='blue', label='ERP')
	line, = plt.plot(x, y3, '-', linewidth=2, color='green', label='PRP')

	#tick no eixo x
	plt.xticks(np.arange(min(x), max(x)+1, 1.0))
	#tick no eixo y
	plt.yticks(np.arange(min(x), max(x)+1, .05))

	#define o range
	plt.axis([0,17,1,2])

	# draw vertical line from [xfinal,xinicial][yfinal,yinicial]
	for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]:	
		plt.plot([i, i], [2, 1], 'k--')

	#plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
	plt.legend( loc=2, borderaxespad=0.)

	#dashes = [10, 5, 100, 5] # 10 points on, 5 off, 100 on, 5 off
	#line.set_dashes(dashes)
	#plt.show()
	plt.savefig(fileName)



def getDBCursor():
	db = sqlite3.connect('cri_db')
	c = db.cursor()
	return c

def getValues(query):
	ret = []
	c = getDBCursor()
	for i in c.execute(query):
		a = []
		for j in range(len(i)):
			a.append(i[j])
		ret.append(a)
	return np.array(ret)

def getRiscos():
	r = getValues('select * from risk_tb')
	formatColumn(r,1)
	formatColumn(r,2)
	return r

def formatColumn(matrix,index):
	for r in matrix:
		r[index] = r[index].encode('utf-8')

def getREList(coleta):
	a = getValues('SELECT  riskexposure_id AS _id, prob, impact, risk_id from (SELECT _id AS collect_tb_id, timestamp, project_id, answerlist FROM collect_tb), (SELECT _id AS riskexposure_tb_id, prob, impact, risk_id FROM riskexposure_tb), collect_riskexposure_tb WHERE collect_tb_id = collect_id AND riskexposure_tb_id = riskexposure_id AND collect_id = %d' %coleta)
	return a

def getRP(coleta):
	#sem FCP
	pr = 0
	for r in getREList(coleta):
		RE = r[1]*r[2]
		peso = 0
		if ((RE > 0) & (RE <= .2)):
			peso = 1 
		if ((RE >.2) & (RE <=.4)):
			peso = 2 
		if ((RE >.4) & (RE <=.6)):
			peso = 3 
		if ((RE >.6) & (RE <=.8)):
			peso = 4 
		if ((RE >.8) & (RE <=1)):
			peso = 5 
		pr += peso
	return pr

def getERP(coleta):
	#sem FCP
	pr = 0
	for r in getREList(coleta):
		RE = r[1]*r[2]
		peso = 0
		if ((RE > 0) & (RE <= .2)):
			peso = 1 
		if ((RE >.2) & (RE <=.4)):
			peso = 2 
		if ((RE >.4) & (RE <=.6)):
			peso = 4 
		if ((RE >.6) & (RE <=.8)):
			peso = 8 
		if ((RE >.8) & (RE <=1)):
			peso = 16 
		pr += peso
	return pr

def getPRP(coleta):
	#sem FCP
	pr = 0
	for r in getREList(coleta):
		pr += 1
	return pr

def getRPc(coleta):
	#sem FCP
	pr = 0
	for r in getREList(coleta):
		RE = r[1]*r[2]
		peso = 0
		if ((RE > 0) & (RE <= .2)):
			peso = 1 
		if ((RE >.2) & (RE <=.4)):
			peso = 2 
		if ((RE >.4) & (RE <=.6)):
			peso = 3 
		if ((RE >.6) & (RE <=.8)):
			peso = 4 
		if ((RE >.8) & (RE <=1)):
			peso = 5 
		pr += (peso*RE)
	return pr


def getPRC(coleta):
	#sem FCP
	pr = 0
	for r in getREList(coleta):
		pr += r[1]*r[2] 
	return pr

rp=[]
erp=[]
prp=[]
print 'normal'
#coletas = range(1,11)
coletas = [1,7,2,8,3,6,11,4,9,5,10,11,12,13,14,15]
for i in coletas:
	a = (float(getRP(i))/len(getREList(i)))
	rp.append(a)
	print a
print '* ER'
for i in coletas:
	a = (float(getERP(i))/len(getREList(i)))
	erp.append(a)
	print a
for i in coletas:
	#N.append(float(getRP(i))/len(getREList(i)))
	prp.append(float(getPRP(i))/len(getREList(i)))
	#prp.append((float(getERP(i))-getRP(i))#relacao entre ERP e RP
	#normalizador /len(getREList(i)) -> qtd riscos


plotLine(range(1,len(rp)+1),rp,erp,prp,'foo')






