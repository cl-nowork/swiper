import pymysql

from libs.orm import patch_orm


pymysql.install_as_MySQLdb()
patch_orm()
