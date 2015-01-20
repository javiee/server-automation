from pexpect import * 
from subprocess import call
#disks =  run('ls /sys/class/scsi_disk')
#print disks 
import pexpect
#print "new try"

dev = pexpect.spawn('stat /dev/sda')
dev1 = run ('/bin/bash -c "ls /dev/sd?"')
print dev1

#dev1.expect(pexpect.EOF)
#dev.sendline('ls /dev/sda')
#print dev.before
#print dev

#dev1 = call (["ls","/dev/sda"])
#print dev1
