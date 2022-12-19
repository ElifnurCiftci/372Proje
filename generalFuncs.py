from queries import *

def whatRole(username):
    userrole=""
    admin = select("kullanıcı_id","admin","admin_ad='{}'".format(username),asDict=True)
    uye =select("kullanıcı_id","uye","uye_ad='{}'".format(username),asDict=True)
    if admin.__len__()>0:
        return "admin"
    if uye.__len__()>0:
        return "Üye"
    return userrole