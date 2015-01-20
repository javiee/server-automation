#!/usr/bin/env python
from subprocess import call 
import logging
import argparse
import pyudev
import pexpect 

#parted --script /dev/sdc mklabel msdos unit MB	 mkpart primary ext4 1 300MB mkpart primary linux-swap 301MB 400MB mkpart primary ext4 400MB 1000MB toggle 1 raid toggle 3 raid
#parted --script /dev/sdc mklabel msdos unit MB mkpart primary ext4 1 105MB mkpart primary linux-swap 105MB 200MB  mkpart primary ext4 200MB 100% toggle 1 raid toggle 3 raid

SWAP = 100
letter = ['b','c','d','e']

class Main(object):
    
    def __init__(self):

        swap=100
        opt=argparse.ArgumentParser(description="Server deployment script")
        opt.add_argument('-n', '--disks', help = "Number of disks. More than 4 hardware array",required=True)
        #opt.add_argument('-o', '--home', help = "Home partition size in GB",type = int)
        opt.add_argument('-r', '--root', help = "Home partition size in GB",type = int) #add choices
        opt.add_argument('-a', '--array', choices=['software','hardware'], help = "Software or hardware array")
        opt.add_argument('-d', '--delete', help = "It deletes metedata from the disks", action='store_true')
        args = opt.parse_args()
        self.log = logging.getLogger()
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel(logging.INFO)

        if args.array == 'software':
            self.create_partitions(args.root,swap,args.disks)
            self.create_mirrors(args.disks)
        else:
           # self.create_virtualdisk(args.root,swap)
           print "hardware"
        if args.delete:
            self.delete_metadata(args.disks)

    def logical_volume(self):
        print "hola"
    
    def create_partitions (self,root,swap,ndisk):
        #check the number of disk is correct 
        rdisk = pexpect.run('/bin/bash -c "ls /dev/sd? | wc -l')
        #expected disk letters
        if not rdisk.rstrip() == ndisk:
            raise ValueError ("Number of disks does not match with the given value")
        letter = ['b','c','d','e']
        self.log.info('Creating partitions')
        for number in range(1,int(ndisk)):
            #self.log.info('Creating partitions on /dev/sd%s' %letter[number-1]) 
            if number <=2:
                if call (["parted", "--script","/dev/sd%s"%letter[number-1]," mklabel"," msdos","unit"," MB"," mkpart","primary","ext4","1","%sMB"%root,"mkpart","primary","linux-swap","%sMB"%root,"%sMB"%(root+swap), " mkpart", "primary", "ext4","%sMB"%(root+swap), "100%","toggle", "1" ,"raid", "toggle", "3","raid"]) !=0:
                    raise IOError("Failed to create partitions in /dev/sd%s"%letter[number-1])
            else: 
                if call (["parted", "--script", "/dev/sd%s" %letter[number-1], "mklabel", "msdos", "unit","MB", "mkpart", "primary", "ext4" ,"1", "100%", "toggle", "1", "raid"]) !=0:
                    raise IOError("Failed to create partitions in /dev/sd%s"%letter[number-1])
                if call (["parted", "--script","/dev/sd%s"%letter[number-1]," mklabel"," gpt"," unit","MB","mkpart","primary","ext4","1", "100%", "toggle", "1", "raid"])!=0:
                    raise IOError("Failed to create partions in /dev/sd%s"%letter[number-1])

    def create_mirrors (self,ndisk):
        #for number in range(1,int(ndisk)):
        number = 1
        if call([  "mdadm", "-C", "-l1", "-n2", "/dev/md%s"%(number-1), "/dev/sdb%s"%number, "/dev/sdc%s"%number]) and call(["mkfs.ext4","/dev/md%s"%(number-1)]) !=0:
            raise IOError("Error creating mirror or file system in /dev/md0")
        if number == 3:
            print "yes | mdadm --create -l1 -n2 /de/md%s /dev/sdc1 /dev/sdd1" %(number-1) 
            print "mdadm --manage -f /dev/md%s /dev/sdc1 /dev/sdd1"%(number-1)
            #break

    def delete_metadata (self,ndisk):
        self.log.info('deleting all metadata disk')
        for number in range(1,int(ndisk)):
            call (["mdadm","--stop","/dev/md%s"%(number-1)])
            #clean disk metadata
            #call (["mdadm", "--zero-superblock","/dev/sd%s"%letter[number-1]])

if __name__ == "__main__":
    main = Main()
