import os

st = os.statvfs('/dev/sdb')
total = float (st.f_blocks * st.f_bsize)  # Megabytesprint total

blocks = int (open('/sys/block/sdb/size'.format(**locals())).read())
print (blocks * 512) /1024/1024
print blocks * 512
print blocks
