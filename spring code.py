#SPRING
pi=3.141592
a=input('Welcome\ninput P setpoint: (bar)\n')
P_setpoint=(float(a))/10
d1=9
do=10
Fmin=(P_setpoint)*(pi/4)*((d1)**2)
print('\nFmin =',Fmin,'N')
P_reseating=Fmin/pi*4/(do**2)
print('P_reseating =',P_reseating*10,'bar')
blow_down=P_setpoint-P_reseating
print('blow_down =',blow_down*10,'bar')
Ymin=10
k=Fmin/Ymin
print('k =',k,'N/mm')
Ymax=20
Fmax=Ymax*k
print('Fmax =',Fmax,'N')
P_max=Fmax/pi*4/do**2
print('P_max (full open mode) =',P_max*10,'bar\n')
Fa=(Fmax-Fmin)/2
Fm=(Fmax+Fmin)/2

#Start trial and error
d=.1
FOM=[]
all_springs={}
while d<10:
    d=d+.1
    #print(d)
    dict_d={}
    dict_d['d']=d
    #2  Ssy
    A=1783
    m=.19
    Sut=A/(d**m)
    dict_d['Sut']=Sut
    Ssy=.45*A/(d**m)
    dict_d['Ssy']=Ssy
    #print('Ssy = ',Ssy)
    Ssu=.67*A/(d**m)
    #3  C
    q=241/1.5
    w=(8*Fa)/(pi*d**2)
    C=((2*q-w)/(4*w))+(((2*q-w)/(4*w))**2-(3*q)/(4*w))**(.5)
    dict_d['C']=C
    #print('C = ',C)
    if type(C) is complex:
        continue
    if C<=4 or C>=12:
        continue
    #4  D
    D=C*d
    dict_d['D']=D
    #print('D = ',D)
    # Fs
    Fs=1.15*Fmax
    dict_d['Fs']=Fs
    #5  Na
    if d<0.8128:
        G=80700
    elif d>=0.8128 and d<=1.6002:
        G=80000
    elif d>=1.6002 and d<=3.175:
        G=79300
    elif d>=3.175:
        G=78600
    Na=(G*(d**4)*Ymax)/(8*(D**3)*Fmax)
    dict_d['Na']=Na
    #print('Na = ',Na)
    if Na<=3 or Na>=15:
        continue
    #6 Nt
    Nt=Na+2 #takht va sang
    #print('Nt = ',Nt)
    #7 Ls
    Ls=d*Nt
    dict_d['Ls']=Ls
    dict_d['k']=k
    #print('Ls =',Ls)
    #8 Lo
    Lo=Ls+Fs/k
    dict_d['Lo']=Lo
    #print('Lo =',Lo)
    #ys
    ys=Lo-Ls
    dict_d['ys']=ys
    #print('ys =',ys)
    #9 Locr
    Locr=2.63*D/.5
    dict_d['Locr']=Locr
    #print('Locr = ',Locr)
    if Lo>Locr:
        continue
    #10 ns
    KB=(4*C+2)/(4*C-3)
    ta=KB*(8*Fa*D)/(pi*d**3)
    tm=ta*Fm/Fa
    ts=ta*Fmax/Fa
    nf=241/ta
    dict_d['nf']=nf
    #print('nf =',nf)
    ns=Ssy/ts
    dict_d['ns']=ns
    #print('ns = ',ns)
    if ns<1.1:
        continue
    #11 fom
    fom=-(pi**2)*(d**2)*Nt*D/4
    FOM.append(fom)
    dict_d['fom']=fom
    #print('fom = ',fom)
    all_springs[fom]=dict_d

try:
    FOM.sort()
    fomj=FOM[len(FOM)-1]
    print('Specifications of The best spring : \n',all_springs[fomj])
    p2=input('\nyou can use this spring for other set points with screw\ninput your next set pressure:\n')
    F2=(float(p2)/10)*(pi/4)*((d1)**2)
    y1=F2/k
    print(y1)
except(IndexError):
      print('We cant design this spring with set point =',P_setpoint*10,'bar')


