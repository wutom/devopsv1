# -*- coding: utf-8 -*-
'''
定时更新redis数据
'''
from api.ali import cloud

cloud.update_Ali_Ecs()
cloud.update_Ali_Slb()
cloud.update_Jenkins_Builds_Pro()
cloud.update_Ali_Rds()
cloud.update_Jenkins_Builds_Pre()
cloud.update_Tx_Cns()