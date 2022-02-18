import pymysql

connection = pymysql.connect(host="localhost",user="root",passwd="",database="test")
cursor = connection.cursor()

insert_reservation = "INSERT INTO reservations(customer_ID, check_in_date, check_out_date, hotel, price) VALUES('1', '2022-04-06', '2022-04-09', 'Park In', '139');"
cursor.execute(insert_reservation)

connection.commit()
connection.close()