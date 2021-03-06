#Risk Analysis
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#pretty printing
np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)
#np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

#MACROS
SHOWNUMBERSPLOT = True
METRICLIST = ["RP","ERP","PRP", "CRIT"]


def plotLine(x,y1,y2,y3,path,fileName):
	line, = plt.plot(x, y1, '-', linewidth=2, color='blue', label='PR')
	line, = plt.plot(x, y2, '--', linewidth=2, color='red', label='ERP')
	line, = plt.plot(x, y3, '-', linewidth=2, color='green', label='PRP')

	#tick no eixo x
	plt.xticks(np.arange(min(x), max(x)+1, 1.0))
	#tick no eixo y
	plt.yticks(np.arange(min(x), max(x)+1, .05))

	#define o range
	plt.axis([0,5,1,2])

	# draw vertical line from [xfinal,xinicial][yfinal,yinicial]
	for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]:	
		plt.plot([i, i], [2, 1], 'k--')

	#plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
	plt.legend( loc=2, borderaxespad=0.)

	#dashes = [10, 5, 100, 5] # 10 points on, 5 off, 100 on, 5 off
	#line.set_dashes(dashes)
	#plt.show()
	checkDir(path)
	plt.savefig(path +"/"+fileName)
	plt.clf()
	plt.close()

def vmax(y):
	l = []
	for i in y:
		l += i
	return max(l)
def vmin(y):
	l = []
	for i in y:
		l += i
	return min(l)

def plotIndicatorLine(values,curvesNames,path,fileName):
	y = values
	x = range(1,len(y[0])+1)
	botPlot = np.floor(vmin(values))
	topPlot = np.ceil(vmax(values))
	botPlot = (vmin(values))
	topPlot = (vmax(values))
	xyRange = [0,len(y[0])+1,botPlot,topPlot]
	curves = len(y)
	colors = ["r","g","b","c","m","y","k"]
	fig = plt.figure()
	for c in range(curves):
		#values on points
		ax = fig.add_subplot(111)
		ax.set_ylim(botPlot,topPlot)
		for i,j in zip(x,y[c]):
			if SHOWNUMBERSPLOT:
				ax.annotate(str("%.3f"%j),xy=(i,j),xytext=(5,5), textcoords='offset points')
		#curve plot
		plt.plot(x,y[c],'-ro',linewidth=2,color=colors[c],label=curvesNames[c])
		
	#tick no eixo x
	plt.xticks(np.arange(min(x), max(x)+1, 1.0))
	#tick no eixo y
	ytickSize = float(topPlot+1-botPlot)/20#20 ticks
	plt.yticks(np.arange(botPlot, topPlot+1, ytickSize))

	#define o range
	plt.axis(xyRange)#plt.axis([0,5,1,2])

	# draw vertical line from [xfinal,xinicial][yfinal,yinicial]
	for i in range(xyRange[0],xyRange[1]):	
		plt.plot([i, i], xyRange[2:], 'k--')

	#plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
	plt.legend( loc=0, borderaxespad=0.)# loc=0-> best

	#dashes = [10, 5, 100, 5] # 10 points on, 5 off, 100 on, 5 off
	#line.set_dashes(dashes)
	#plt.show()
	checkDir(path)
	plt.savefig(path +"/"+fileName)
	plt.clf()
	plt.close()

def checkDir(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def getDBCursor():
	db = sqlite3.connect('cri_db')
	return db.cursor()

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
	return getValues('SELECT  riskexposure_id AS _id, prob, impact, risk_id from (SELECT _id AS collect_tb_id, timestamp, project_id, answerlist FROM collect_tb), (SELECT _id AS riskexposure_tb_id, prob, impact, risk_id FROM riskexposure_tb), collect_riskexposure_tb WHERE collect_tb_id = collect_id AND riskexposure_tb_id = riskexposure_id AND collect_id = %d' %coleta)

def getSubREList(coleta,riskList):
	REList = getREList(coleta)
	out = []
	for line in REList:
		if line[3] in riskList:
			out.append(line)
	return np.array(out)


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


def getRiskEst(collectList,var,riskList):#var: (prob or impact or RE )
	fullList = []
	if collectList == "all":
		collectList = coletas[0]+coletas[1]+coletas[2]+coletas[3]+coletas[4]
	for c in collectList:
		vList=[]
		REList = []
		if riskList == "all":
			REList = getREList(c)
		else:
			REList = getSubREList(c,riskList)
		#print REList
		if not REList.size == 0:
			if var == "RE":
				probList = REList[:,1]
				impactList = REList[:,2]
				for i in range (len(probList)):
					vList.append(probList[i]*impactList[i])
			elif var =="prob":
				vList = REList[:,1]
			elif var == "impact":
				vList = REList[:,2]
			for i in vList:
				fullList.append(i)
	fullList = np.array(fullList)
	#print "size %f" %fullList.size
	#print fullList
	if fullList.size == 0:
		return 0,0,0,0
	#print "EST: (max,min,avg,sigma)"
	maxV = np.max(fullList)
	minV = np.min(fullList)
	avgV = np.mean(fullList)
	sigmaV = np.std(fullList)
	return maxV,minV,avgV,sigmaV

def getRiskRank(collectList,var):
	rank = []
	dtype = [('value', float), ('risk', int)]
	#qtd riscos = 31 -> range(1,32)
	for risk in range(1,32):
		v = getRiskEst(collectList,var,[risk])
		rank.append((v[2],risk))
	rank = np.array(rank,dtype=dtype)
	rank = np.sort(rank, order=["value","risk"])
	out = []
	for i in rank:
		out.append(i[1])
	out.reverse()
	return out

def getIndicatorValuesList(project,indicator,normal):
	collectList = coletas[project]
	lst = []
	for i in collectList:
		v=0.
		if indicator == "RP":
			v = getRP(i)
		elif indicator =="ERP":
			v = getERP(i)
		elif indicator == "PRP":
			v = getPRP(i)
		elif indicator == "CRIT":
			v = (getERP(i)-getRP(i))	
		if normal:
			v = float(v)/len(getREList(i))
		lst.append(v)
	return lst

def stm(list):
	return ([np.mean(list[0:4]),np.mean(list[4:8])])




print 'normal'
coletas = [[1,7,12,12,12,18,18,35], #inscricoes => 0
		   [2,8,13,13,13,19,27,34], #tcc => 1
		   [3,6,11,16,20,26,30,31], #estante , => 2
		   [4,9,14,17,21,22,28,32], #turma D => 3
		   [5,10,15,23,24,25,29,33]] #academico => 4

projetos = ["inscricoes","tcc","estante","turma_D","academico"]

def main():
	for c in range(5):
		rp=[]
		erp=[]
		prp=[]
		print "Projeto: %s, Riscos" %projetos[c]
		cont = 1
		for i in coletas[c]:
			print "coleta: %d" %(cont)
			cont += 1
			getRiskInfo(i)
			getREInfo(i)
			print"\n"
		print"------------\n"
		nome = "metricas_projeto_%s" %(projetos[c])
		print nome	
		cont = 1
		for i in coletas[c]:
			v1 = (float(getRP(i))/len(getREList(i)))
			rp.append(v1)
			v2 = (float(getERP(i))/len(getREList(i)))
			erp.append(v2)
			v3 = float(getPRP(i))/len(getREList(i))
			prp.append(v3)
			print "Coleta %d: " %cont
			print "RP: %f, ERP %f, PRP %f" %(v1,v2,v3)
			cont += 1
			#N.append(float(getRP(i))/len(getREList(i)))
			#prp.append((float(getERP(i))-getRP(i))#relacao entre ERP e RP
			#normalizador /len(getREList(i)) -> qtd riscos
		##plotLine(range(1,len(rp)+1),rp,erp,prp,'foo')
		
		# test# plotLine(range(1,len(rp)+1),rp,erp,prp,"plots",nome)
		rp2 = getIndicatorValuesList(c,"RP",True)
		erp2 = getIndicatorValuesList(c,"ERP",True)
		prp2 = getIndicatorValuesList(c,"PRP",True)

		plotIndicatorLine([rp2,erp2,prp2],["RP","ERP","PRP"],"plots",nome)

		print "---------\n\n"
def projectEvaluate(projectID, normal):
	name = "%s_normal=%s"%(projetos[projectID],normal)
	print "evaluate: %s"%name
	metricsValues = []
	for metric in METRICLIST:
		v= getIndicatorValuesList(projectID,metric,normal)
		metricsValues.append(v)
	plotIndicatorLine(metricsValues,METRICLIST,"projects-plots",name)



def environmentEvaluate(metric,normal):
	name = "environment_metric=%s_normal=%s"%(metric,normal)
	print "EnvironmentEvaluate"
	print "metric = %s"  %metric
	metricsValues=[]
	for projID in range(5):
		v = getIndicatorValuesList(projID,metric,normal)
		metricsValues.append(v)
	plotIndicatorLine(metricsValues,projetos,"environment-plots",name)


#==============================#
#main()

def do():
	for proj in range(5):
		for norm in [True,False]:
			projectEvaluate(proj,norm)

	for metric in METRICLIST:
		for norm in [True,False]:
			environmentEvaluate(metric,norm)

#do()

#for c in coletas:
	
print getRiskEst(coletas[0],"RE","all")