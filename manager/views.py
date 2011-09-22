from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import ldap

def index(request):

    return render_to_response('manager/index.html')

def getpass(username=None):
    if username is not None:
        fp = open('/home/shashi/projects/unimig/data/userinfo.txt','r')
        users = fp.readlines()
        for l in users:
            l = l.replace('\n','')
            lu = l.split('|') 
            if (lu[0] == username):
                d = lu[0].split('@')[1]
                ld = {'user': lu[0], 'passw': lu[1], 'dom': d}
                return ld
        fp.close()
    else:
        return False


def verify(request):

    login = False
    try:
        user = request.POST['user']
        passw = request.POST['passw']
    except (KeyError):
        return render_to_response('manager/verify.html', {
                'error_message': "Provider username/password"
                })
    
    l = ldap.initialize("ldap://202.141.128.200")
    if (len(user.split('@')) > 1):
        d=user.split('@')[1]
        dn="mail="+user+",vd="+d+",o=hosting,dc=uni-mysore,dc=ac,dc=in"
# dn: mail=support@icd.uni-mysore.ac.in,vd=icd.uni-mysore.ac.in,o=hosting,dc=uni-mysore,dc=ac,dc=in
#     g = l.search_s("dc=uni-mysore,dc=ac,dc=in", ldap.SCOPE_SUBTREE, "mail="+user, ['mail'])
#     if (len(g) > 0):

        try:
            if(l.simple_bind_s(dn,passw)):
                login=True            
            else:
                login=False
        except ldap.INVALID_CREDENTIALS:
            login=False        

    if (login):
        up = getpass(user)
    else:
        up = {}

    return render_to_response('manager/verify.html', {'login': login, 'up': up})

