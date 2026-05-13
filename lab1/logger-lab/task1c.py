import logging
logging.basicConfig(filename='app.log',
filemode='w',
format='%(levelname)s - %(name)s - %(message)s')
logging.error('This is an error message')
