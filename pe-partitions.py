from subprocess import call 
import logging
import argparse
import pyudev
#parted --script /dev/sdc mklabel msdos unit MB	 mkpart primary ext4 1 300MB mkpart primary linux-swap 301MB 400MB mkpart primary ext4 400MB 1000MB toggle 1 raid toggle 3 raid

SWAP = 100
4DISKS = false 

class Main(object):
    
    def __init__(self):

        swap=100
        opt=argparse.ArgumentParser(description="Server deployment script")
        opt.add_argument('-a', '--array', help = "It selects software or hardware array")
        opt.add_argument('-o', '--home', help = "Home partition size in GB",type = int)
        opt.add_argument('-r', '--root', help = "Home partition size in GB",type = int)
        args = opt.parse_args()
        if args.array == "software":
            self.create_partitions(args.home,args.root,swap)
        if args.array == "hardware":
            self.create_virtualdisk(args.home,args.root,swap)

    def disk_info():
        #find out sda size
        blocks = int (open('/sys/block/sdb/size'.format(**locals())).read())
        disk_size (blocks * 512) /1024/1024/1024  #in GB
        
        return disk size

    
    def create_virtualdisk(self):
        print "nothing yet"

    def initialize_mirrors(self):
         
        for i in partitions(starts = 1):
            #sda and sdb mirrors
            call ([ "yes" "|" "mdadm" "--create" "-l1" "-n2" "/dev/md%s"% i-1 "/dev/sda%s"%i, "/dev/sdb%s"%i])
            call (["/dev/md%s",% i -1,"/dev/sdb%s",% i])
                raise "failed mirrors"
            
    if 4DISKS:
        if call ([ "yes" "|" "mdadm" "--create" "-l1" "-n2" "/dev/md%s"% partitons "/dev/sdc1", "/dev/sdd1"%s])
            raise "failed mirrors"




    def create_partitions (self,home,root,swap):
        print home,root,swap
        #discover how many disks the server has attached
        number_disk = pyudev.Context()
        disks=[]
        for device in number_disk.list_devices(MAJOR=8):
            if (device.device_type == 'disk'):
                disks.append(format(device.device_node))
        #this line is to avoid partitioning /dev/sda. To be removed
        disks.pop(0)
        for element in enumerate(disks, start =1):
            #print disks
            if element[0] <= 2:
                # create partitions for sda and sdb. /dev/sda1 boot flag
               if call(["parted","--script",element[1],"mklabel","msdos","unit","MB","mkpart","primary","ext4","1","%s" %root,"mkpart","primary","linux-swap","%s" %root,"%s" %swap,"mkpart","primary","ext4","%s" %swap,"100%","toggle","1","raid","toggle","3","raid"]) !=0:
                    raise "Partitions has failed"
            else:
                print "disk 3 and 4 %s",element
                # partition for 3 and 4 disks
                if call(["parted","--script",element[1],"mklabel","msdos","unit","%","mkpart","primary","ext4","1%","100%","toggle","1","raid"]) !=0:
                    raise "partitions has failed"

        return partitions 

if __name__ == "__main__":
    main = Main()
