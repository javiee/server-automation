from subprocess import call 
import logging
import argparse
#parted --script /dev/sdc mklabel msdos unit MB	 mkpart primary ext4 1 300MB mkpart primary linux-swap 301MB 400MB mkpart primary ext4 400MB 1000MB toggle 1 raid toggle 3 raid

SWAP = 100

class Main(object):
    
    def __init__(self):

        swap=100
        opt=argparse.ArgumentParser(description="Server deployment script")
        opt.add_argument('-n', '--disks', help = "More than 4 hardware array",type = int)
        #opt.add_argument('-o', '--home', help = "Home partition size in GB",type = int)
        opt.add_argument('-r', '--root', help = "Home partition size in GB",type = int) #add choices
        args = opt.parse_args()

        if args.disks == 4:
            self.create_partitions(args.root,swap,args.disks)
        else:
           # self.create_virtualdisk(args.root,swap)
           print "hardware"
    
    def create_partitions (self,root,swap,ndisk):
        #expected disk letters
        run ('ls /dev/sd? | wc -l')

        letter = ['b','c','d','e']
        for number in range(0 , ndisk):
            if number <=1:
                call (["ls","/dev/sd%s%d"% (letter[number],number+1)])
            else:
                print "disk 3 y 4"

if __name__ == "__main__":
    main = Main()
