from queries import *

def whatRole(userid):
    userrole=""
    admin = select("kullanıcı_id,admin_ad","admin","kullanıcı_id='{}'".format(userid),asDict=True)
    ziyaretci = select("kullanıcı_id","ziyaretci","kullanıcı_id='{}'".format(userid),asDict=True)
    uye =select("kullanıcı_id,uye_ad","uye","kullanıcı_id='{}'".format(userid),asDict=True)
    username = ""
    if admin.__len__()>0 and userid in admin['kullanıcı_id']:
        return "admin",admin['admin_ad']
    if ziyaretci.__len__()>0 and userid in ziyaretci['kullanıcı_id']:
        return "ziyaretci", "Ziyaretçi"
    if uye.__len__()>0 and userid in uye['kullanıcı_id']:
        return "uye", uye['uye_ad']
    return userrole, username