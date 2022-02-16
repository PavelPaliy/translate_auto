from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def get_translate(value):
  try:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path=r"C:\Users\Pavel\geckodriver.exe", options=options)
    driver.get("https://translate.google.com/?hl=ru&sl=ru&tl=en&text="+value+"&op=translate")
    import time
    time.sleep(3)
    element = driver.find_element_by_xpath('//span[@jsname="W297wb"]')
    result = element.get_attribute('innerHTML')

    driver.close()
    return result
  except:
    print("selenium exception")
    return value

import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(user='root',
                                database='kapez_clnew')
  cursor = cnx.cursor(buffered=True)

  stmt = (
    "select * from _captions"
  )
  for result in cursor.execute("select * from _content_structure where locale = 'en' and section_name  REGEXP \"[А-Яа-я]+\"", multi=True):
    if result.with_rows:
      print("Rows produced by statement '{}':".format(
        result.statement))
      update_stmt = (
        "UPDATE _content_structure "
        "SET section_name = %s "
        "WHERE section_id = %s "
      )

      rows = result.fetchall()

      for row in rows:
        id = row[0]
        res = get_translate(row[3])

        data = (res, id)
        try:

          cursor.execute(update_stmt, data)

        except mysql.connector.Error as err:
          print(err)
        except:
          print('sql error')


      print('finish parse')


    else:
      print("Number of rows affected by statement '{}': {}".format(
        result.statement, result.rowcount))

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()