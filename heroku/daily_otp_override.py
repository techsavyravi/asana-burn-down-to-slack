from random import randint
import subprocess, os
import shlex

otp = randint(100000, 999999)

my_env = {**os.environ, 'PATH': os.environ['PATH'] }

subprocess.Popen(shlex.split('heroku config:set OTP=728432 --app b2c-user-auth-ms-staging'), shell=True)
