class ConfiguracionDesarrollo():
    DEBUG = True
    MYSQL_HOST = 'mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com'
    MYSQL_USER = 'bsale_test'
    MYSQL_PASSWORD = 'bsale_test'
    MYSQL_DB = 'bsale_test'


configuracion = {
    'development': ConfiguracionDesarrollo
}