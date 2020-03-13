#!/usr/bin/env python
#-*-coding:utf-8-*-
import re
import os
import datetime
import numpy as np
import subprocess



rx_dict = {
   
    'device': re.compile(r'(?P<device>.*)\tdevice\n'),
    'UniqueDeviceID': re.compile(r'(?P<UniqueDeviceID>.*)\n'),
  }

def _parse_line(line):
  
    for key, rx in rx_dict.items():
        match = rx.findall(line)
        if match:
            return key, match

    return None, None

def iosInstaller(ipaPath,ipaBundle):

    iosDevices = []
    Command = subprocess.Popen(['idevice_id','-l'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = Command.communicate()
    #print(stdout)
    #print(stderr)
    
    key, match = _parse_line(stdout.decode('utf-8'))
    if key == 'UniqueDeviceID':
        iosDevices = match
        print(iosDevices)
    
    #ios delete app from connected devices
    for device in iosDevices:
        Command = subprocess.Popen(['ideviceinstaller', '-u',device,'-U',ipaBundle],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout,stderr = Command.communicate()
        if stdout.decode("utf-8").find("Complete") > -1:
            print('IOS '+ device+' : '+'uninstall complete')

        print(stderr)
    
    #ios install app to connected devices
    for device in iosDevices:
        Command = subprocess.Popen(['ideviceinstaller', '-u',device,'-i',ipaPath],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout,stderr = Command.communicate()
        if stdout.decode("utf-8").find("Complete") >-1 :
            print('IOS '+device+' : '+'install complete')

        print(stderr)

def androidInstaller(apkPath,apkPackage):

    androidDevices = []
    
    Command = subprocess.Popen(['adb', 'devices'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = Command.communicate()
    #print(stdout)
    #print(stderr)
    
    key, match = _parse_line(stdout.decode('utf-8'))
    if key == 'device':
        androidDevices = match
        print(androidDevices)
    
    #android uninstall app from connected devices
    for device in androidDevices:
        Command = subprocess.Popen(['adb', '-s',device,'uninstall',apkPackage],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout,stderr = Command.communicate()
        
        if stdout.decode("utf-8").find("Success") > -1:
            print('Android '+device+' : '+'uninstall complete')
        print(stderr)
    
    #android install app to connected devices
    for device in androidDevices:
        Command = subprocess.Popen(['adb', '-s',device,'install',apkPath],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout,stderr = Command.communicate()
        
        if stdout.decode("utf-8").find("Success")  > -1:
            print('Android '+device+' : '+'install complete')

        print(stderr)


if __name__== "__main__":

    apkPath = "/Users/appname.apk"
    apkPackage = "com.package.name"
   
    ipaPath = "/Users/appname.ipa"
    ipaBundle = "com.bundle.name"
   
    androidInstaller(apkPath,apkPackage)
    iosInstaller(ipaPath,ipaBundle)
