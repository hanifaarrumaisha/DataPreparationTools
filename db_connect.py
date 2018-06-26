import mysql.connector

class Database:
	conn = None

	def connect(self):
		if self.conn is not None:
			return self.conn
		else:
			self.conn = mysql.connector.connect(user='fida', password='FIDA876rs', host='rds-dataaqutition.clshsikuwhsj.ap-southeast-1.rds.amazonaws.com', port='3306', database='db_preparation_tools')
			return self.conn
