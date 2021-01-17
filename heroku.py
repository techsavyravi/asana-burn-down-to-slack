from random import randint
import os
import heroku3
from slack import send2SlackCustomURL

otp = randint(100000, 999999)


heroku_conn = heroku3.from_key('2781f904-f5db-4d3f-b8b8-ccf085c59167')

app_staging = heroku_conn.apps()['b2c-user-auth-ms-staging']
app_production = heroku_conn.apps()['b2c-user-auth-ms']


app_staging.config()['OTP']=str(otp)
app_production.config()['OTP']=str(otp)

send2SlackCustomURL("OTP for Today", str(otp), "https://hooks.sla ck.com/services/TPMAJ1G13/B01KA6R5E73/tmM1NBwnuCItDJZiem7FrxiW")