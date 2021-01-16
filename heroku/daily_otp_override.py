from random import randint
import subprocess, os

otp = randint(100000, 999999)

os.system("heroku config:set OTP=" + str(otp) + " --app b2c-user-auth-ms-staging")
os.system("heroku config:set OTP=" + str(otp) + " --app b2c-user-auth-ms")
