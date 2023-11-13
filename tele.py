from twilio.rest import Client
sid = "AC4e853e6c6b73e63ae6cb2544850c2cf6"
token = "af3ed0d518ec940c349533988ea7bb0e"

send = "+17738400744"
recieve = "+919384565379"

msg = Client(sid,token)
mms = '''
Time       : {datetime.datetime.now()}
Exposure   : {exposure}
Signal     : {direction}
Symbol     : {SYMBOL}
Timeframe  : H4
'''
message = msg.messages.create(
        body = "\nTrade Bot Status\n\n\n"+mms,
        from_ = send,
        to = "+919384565379" 
    )