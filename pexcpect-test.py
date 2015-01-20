import pexpect
import pprint 

r = pexpect.run ('parted --script /dev/sdc mklabel gpt unit MB mkpart primary ext4 1 105MB mkpart primary linux-swap 105MB 200MeeB  mkpart primary ext4 200MB 100% toggle 1 raid toggle 3 raid')
print r
pprint r
#print r.before
#print (str(r))
