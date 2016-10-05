import time
import mysql.connector
import concurrent.futures
import requests
from jsonpath_rw import jsonpath, parse
import json
import logging
from multiprocessing import Pool

logger = logging.getLogger('BookParses')

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Initialize coloredlogs.
import coloredlogs
coloredlogs.install(level='DEBUG')

sleep_timer=5
trade_window=15
requests_timeout=7

user, password, database, buffered=('pycrypto', 'crypto098', 'pycrypto', True)

def getKey(item,):
	a,b=item
	return a

# Retrieve a single page and report the url and contents
def load_url(ExPair, processID):
	start_time=time.time()

	cnx = mysql.connector.connect(user=user, password=password, database=database, buffered=buffered)
	cursor = cnx.cursor()

	ExchangeID=ExPair[0]
	PairID=ExPair[1]
	sellpath=ExPair[3]
	buypath=ExPair[4]
	sellvolpath=ExPair[5]
	buyvolpath=ExPair[6]
	
	logger.debug("process "+str(processID)+" started: "+ExPair[2])
	
	r = requests.get(ExPair[2], timeout=requests_timeout, verify=False)

	if (r.status_code!=200):
		logger.error("process "+str(processID)+": status code is not OK: "+ str(r.status_code))
	
	textjson=json.loads(r.text)
	
	jsonsell_expr = parse(sellpath)
	jsonsellvol_expr = parse(sellvolpath)
	jsonbuy_expr = parse(buypath)
	jsonbuyvol_expr = parse(buyvolpath)

	sellrates=[match.value for match in jsonsell_expr.find(textjson)]
	sellvolumes=[match.value for match in jsonsellvol_expr.find(textjson)]
	
	buyrates=[match.value for match in jsonbuy_expr.find(textjson)]
	buyvolumes=[match.value for match in jsonbuyvol_expr.find(textjson)]

	sell=zip(sellrates, sellvolumes)
	buy=zip(buyrates, buyvolumes)

	sorted(sell, key=getKey)
	sorted(sell, key=getKey, reverse=True)

	sell=sell[:5]
	buy=buy[:5]

	sell = [s+(ExchangeID,PairID) for s in sell]
	buy = [b+(ExchangeID,PairID) for b in buy]
	
	logger.debug("process "+str(processID)+" inserting: "+str(len(sell))+"+"+str(len(buy)))

	insert_sell_query=("insert into SELL (RATE, VOLUME, EXCHANGEID, PAIRID) values (%s, %s, %s, %s)")
	insert_buy_query=("insert into BUY (RATE, VOLUME, EXCHANGEID, PAIRID) values (%s, %s, %s, %s)")

	cursor.executemany(insert_sell_query, sell)
	cursor.executemany(insert_buy_query, buy)	
	
	cnx.commit()
	cursor.close()
	cnx.close()

	find_trade(PairID)

	logger.debug("process "+str(processID)+" sleeping ")
	time.sleep(sleep_timer)
	logger.debug("process "+str(processID)+" finished in "+"{:.2}".format(time.time()-start_time))

	return sell, buy

def find_trade(pairId):
	cnx = mysql.connector.connect(user=user, password=password, database=database, buffered=buffered)
	cursor = cnx.cursor()

	query = ("select distinct rate, exchangeid, volume, e.id, e.name from sell join EXCHANGE e on exchangeid=e.id and pairid="+str(pairId)+" where CURRENT_TIMESTAMP()-DATE<"+str(trade_window)+" and rate=(select min(rate) from sell where CURRENT_TIMESTAMP()-DATE<"+str(trade_window)+")")
	cursor.execute(query)

	for rate, exchangeid, volume, eid, exname in cursor:
		min_sell=rate
		sell_exchange=exname
		sell_volume=volume
		fromex=eid

	query = ("select distinct rate, exchangeid, volume, e.id, e.name from buy join EXCHANGE e on exchangeid=e.id and pairid="+str(pairId)+" where CURRENT_TIMESTAMP()-DATE<"+str(trade_window)+" and rate=(select max(rate) from buy where CURRENT_TIMESTAMP()-DATE<"+str(trade_window)+")")
	cursor.execute(query)

	for rate, exchangeid, volume, eid, exname in cursor:
		max_buy=rate
		buy_exchange=exname
		buy_volume=volume
		toex=eid

	trade_volume=min(sell_volume, buy_volume)
	profit=max_buy-min_sell

	if profit>0:
		last_trade_query = ("select FROMEX, TOEX, BUYPRICE, SELLPRICE, VOLUME from TRADE where PAIRID="+str(pairId)+" and date=(select max(date) from trade where pairid="+str(pairId)+")")

		cursor.execute(last_trade_query)
		old_from_ex,old_to_ex,old_sell,old_buy,old_volume=0,0,0,0,0
		
		for (a) in cursor:
			(old_from_ex,old_to_ex,old_sell,old_buy,old_volume)=a
		
		if (old_volume==trade_volume and old_sell==min_sell and old_buy==max_buy):
			logger.info("Previous trade still available")
		else:
			logger.info("Buying "+"{:10.8f}".format(trade_volume)+" "+PAIRS[pairId]+" at "+str(min_sell)+" in "+sell_exchange+ " and selling at "+str(max_buy)+" in "+buy_exchange)
			logger.info("{:10.8f}".format(trade_volume*min_sell)+" spent for transaction")
			logger.info("Getting "+"{:10.8f}".format(profit*trade_volume)+ " profit")
			insert_trade_query=("insert into TRADE (FROMEX, TOEX, BUYPRICE, SELLPRICE, VOLUME, PAIRID) values (%s, %s, %s, %s, %s, %s)")
			trade=(fromex, toex, min_sell, max_buy, trade_volume, pairId)
			cursor.execute(insert_trade_query, trade)
			cnx.commit()
			logger.debug("inserted "+str(cursor.rowcount))
	else:
		logger.info("Price difference: "+"{:10.8f}".format(profit))
		logger.info("Trade is not yet profitable for "+PAIRS[pairId])
	
	cursor.close()
	cnx.close()
	return

def run_requests(EXCHANGEPAIRS, httpWorkers):

	pool = Pool()
	
	for ExPair in EXCHANGEPAIRS:
		if ExPair in httpWorkers.keys():
			if httpWorkers[ExPair].ready():
				httpWorkers[ExPair]=pool.apply_async(load_url, (ExPair,EXCHANGEPAIRS.index(ExPair)+1))
			#else:
			#	logger.debug("Still not finished: "+str(EXCHANGEPAIRS.index(ExPair)+1)+" : "+ ExPair[2])
		else:
			httpWorkers[ExPair]=pool.apply_async(load_url, (ExPair,EXCHANGEPAIRS.index(ExPair)+1))
	
	pool.close()
	time.sleep(2)
	return httpWorkers

cnx = mysql.connector.connect(user=user, password=password, database=database, buffered=buffered)
cursor = cnx.cursor()

query = ("select ID,NAME from PAIR")
cursor.execute(query)

PAIRS={}

for (a) in cursor:
	(pairId,PairName)=a
	PAIRS[pairId]=PairName

query = ("select EXCHANGEID, PAIRID, APIURL, SELLPATH, BUYPATH, SELLVOLUMEPATH, BUYVOLUMEPATH from EXCHANGEPAIR EP join EXCHANGE E on EP.EXCHANGEID=E.ID and EP.ENABLED=1")
cursor.execute(query)

EXCHANGEPAIRS=[]
for (a) in cursor:
	EXCHANGEPAIRS.append(a)


logger.debug(PAIRS)
logger.debug(EXCHANGEPAIRS)

httpWorkers={}

cursor.close()
cnx.close()

while True:
	httpWorkers=run_requests(EXCHANGEPAIRS, httpWorkers)







