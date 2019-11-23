import sys,os
def change(s):
    if s == 1:os.system('sudo date -s "sat Nov 23 22:05:00 2019"')#don't forget to change it , i've used date command for linux 
    elif s == 2:
        try:
          import pywin32
        except ImportError:
          print( 'pywin32 module is missing')
          sys.exit(1)
        pywin32.SetSystemTime(year, month , dayOfWeek , day , hour , minute , second , millseconds )# fill all Parameters with int numbers
    else:print( 'wrong param')
def check_os():
    if sys.platform=='linux2':change(1)
    elif  sys.platform=='win32':change(2)
    else:print ('unknown system')
    
    
change(1)