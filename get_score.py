"""
	lambda code to get individual score at the end of the quiz
"""
import os
import sys
import logging
import pymysql

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def establish_connection():
	"""
		function to establish connection to the rds. The credentials are stored as environment variables
	"""
	rds_host  = os.environ['rds_host']
	name = os.environ['db_username']
	password = os.environ['db_password']
	db_name = os.environ['db_name']
	try:
		connection = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=15)
	except:
		logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
		sys.exit()
	logger.info("SUCCESS: Connection to RDS mysql instance succeeded")
	return connection
	
def get_individual_score(event):
	"""
		fucntion to get the individual score at the end of the quiz
	"""
	connection = establish_connection()
	phone = event['phone']
	with connection.cursor() as cur:
		cur.execute("RESET QUERY CACHE")
		command = """select sql_no_cache Phone, UserName, count(Phone), sum(TimeTaken) from `fastest_finger_first`.`user_info` where Phone = {}""".format(event['phone'])
		print command
		cur.execute(command)
		rows = ()
		for row in cur:
			rows = row
	print(row[2])
	try:
		return_data = {'correct_answers' : rows[2], 'total_time' : round(rows[3], 2)}
	except TypeError:
		return_data = {'correct_answers' : 0, 'total_time' : 0}
	return return_data
	
def handler(event, context):
	"""
		starting method of the lambda function
	"""
	print('input to the lambda:', event)
	return get_individual_score(event)