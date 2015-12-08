# -*- coding: utf-8 -*-
import logging  
import logging.handlers  
def info(str):
    log_str = '=========================>'
    # 配置日志信息
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='marginer.log',
                        filemode='w')
    # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # 设置日志打印格式
    formatter = logging.Formatter('%(name)-1s: %(message)s')
    console.setFormatter(formatter)
    # 将定义好的console日志handler添加到root logger
    logging.getLogger('').addHandler(console)
    
    logger = logging.getLogger('marginer')
    logger.info(unicode(log_str+str, 'utf8'))