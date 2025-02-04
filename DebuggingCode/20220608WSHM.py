from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time
import pandas

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = [] #Initialize variable to store candle
    def historicalData(self, reqId, bar):
        print(f'Time: {bar.date} Close: {bar.close}')
        self.data.append([bar.date, bar.close])
    def wshMetaData(self, reqId: int, dataJson: str):
        super().wshMetaData(reqId, dataJson)
        print("WshMetaData.", "ReqId:", reqId, "Data JSON:", dataJson)
		
def run_loop():
	app.run()

app = IBapi()
app.connect('127.0.0.1', 7496, 123)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

#Create contract object
eurusd_contract = Contract()
eurusd_contract.symbol = 'EUR'
eurusd_contract.secType = 'CASH'
eurusd_contract.exchange = 'IDEALPRO'
eurusd_contract.currency = 'USD'

apple_contract = Contract()
apple_contract.symbol = 'AAPL'
apple_contract.secType = 'STK'
apple_contract.exchange = 'SMART'
apple_contract.currency = 'USD'

#Request historical candles
#app.reqHistoricalData(1, eurusd_contract, '', '2 D', '1 hour', 'BID', 0, 2, False, [])
#app.reqHistoricalData(1, apple_contract, '', False, False, [])
#app.reqHistoricalData(1, apple_contract, '', '2 D', '1 hour', 'BID', 0, 2, False, [])
app.reqWshMetaData(1, apple_contract)

time.sleep(5) #sleep to allow enough time for data to be returned
df = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s') 
print(df)
app.disconnect()