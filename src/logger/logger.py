# -*- coding: utf-8 -*-
import logging,datetime
import logging.handlers  
def info(str):
    ISOTIMEFORMAT='%Y-%m-%d %H:%M:%S'
    log_str = 'marginer : '
    cur_time = datetime.datetime.now().strftime(ISOTIMEFORMAT);
    print unicode(cur_time + ':::' + log_str+str, 'utf8')