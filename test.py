import numpy as np

m=int(input("질량[kg]?"))
c=int(input("댐핑계수[Ns/m]"))
k=int(input("스프링 상수[N/m]"))
zeta=c/(2*np.sqrt(m*k))
Wn=np.sqrt(k/m)
Wd=Wn*(np.sqrt((1-zeta)**2))

print('고유진동수=',Wn,'감쇠고유진동수=',Wd,'zeta=',zeta)
pole5= - Wn
if zeta<1:
    if zeta>0:
        pole1=complex(-Wn*zeta,(-c+np.sqrt(4*m*k-c**2))/2*m)
        pole2=complex(-Wn*zeta,(-c-np.sqrt(4*m*k-c**2))/2*m)
        print('고유진동수=',Wn,'감쇠고유진동수=',Wd,'zeta=',zeta,'부족감쇠','pole=',pole1,pole2)
elif zeta==0:
    print('고유진동수=',Wn,'감쇠고유진동수=',Wn,'zeta=',zeta,'임계감쇠')
elif zeta>1:
    Wd1=Wn*np.sqrt((zeta**2)-1)
    pole3=complex(-Wn*zeta,(-c-np.sqrt(c**2-4*m*k))/2*m)
    pole4=complex(-Wn*zeta,(-c+np.sqrt(c**2-4*m*k))/2*m)
    print('고유진동수=',Wn,'감쇠고유진동수=',Wd1,'zeta=',zeta,"과감쇠",'pole=',pole3,pole4)