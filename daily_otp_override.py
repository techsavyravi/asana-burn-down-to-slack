from random import randint
import os
from slack import send2SlackCustomURL

otp = randint(100000, 999999)

os.system("heroku config:set OTP=" + str(otp) + " --app b2c-user-auth-ms-staging")
os.system("heroku config:set OTP=" + str(otp) + " --app b2c-user-auth-ms")

send2SlackCustomURL("OTP for Today", str(otp), "https://hooks.sla ck.com/services/TPMAJ1G13/B01KA6R5E73/tmM1NBwnuCItDJZiem7FrxiW")
