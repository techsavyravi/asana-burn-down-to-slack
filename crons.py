from validate_project import isProjectValid
from slack import send2SlackCustomURL

isProjectValid(True)

send2SlackCustomURL("Everything is Great!", "-")