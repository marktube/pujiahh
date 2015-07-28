import struct

f = open("text","r")
wf = open("encoded","wb")

#construct file head
#write into file in big endian
head = 0x00000000
wf.write(struct.pack('>L',head))#L for 4 bytes
head = 0x4d534732
#print head
wf.write(struct.pack('>L',head))
head = 0x0000
wf.write(struct.pack('>h',head))#h for 2 bytes
#print head
head = 0x01007407
wf.write(struct.pack('>L',head))
head = 0x00
wf.write(struct.pack('>h',head))

#start to construct the index & content
cknum = 1
seqNo = f.readline()
while seqNo:
    seqNo = seqNo[5:]
    seqNo = seqNo[:-5]
    seqNo = int(seqNo)
    tmp = f.readline()
    if cknum == seqNo:
        #print seqNo
        cknum += 1
        seqNo = f.readline()
    else:
        cknum = 0
        print 'The sequence number error'
        break
if cknum == 0:quit()

cknum -= 1
wf.write(struct.pack('>B',cknum))#B for 1 byte
wf.write(struct.pack('>B',0x00))
wf.write(struct.pack('>h',0x0000))
wf.write(struct.pack('>L',0x20000000))
wf.write(struct.pack('>L',0x00000000))
wf.write(struct.pack('>L',0x00000000))

f.seek(0)
seqNo = f.readline()
tmp = f.readline()
ibuffer = struct.pack('>L',0x00000000)
ibuffer += struct.pack('>L',0x00000000)
ibuffer += struct.pack('>L',0x00000000)
ibuffer += struct.pack('>L',0x00000000)
Tbuffer = ''
address = (3+cknum)*16
while seqNo:
    seqNo = seqNo[5:]
    seqNo = seqNo[:-5]
    seqNo = int(seqNo)
    ibuffer += struct.pack('>B',seqNo)
    ibuffer += struct.pack('>B',0x00)
    ibuffer += struct.pack('>h',0x00000)
    tmp = tmp[:-1]
    tmp = tmp.decode('utf8').encode('shift-jis')
    ibuffer += struct.pack('>B',len(tmp)+4)
    #print seqNo
    #print 'tmp:'+str(len(tmp))
    ibuffer += struct.pack('>B',0x00)
    ibuffer += struct.pack('>h',0x00000)
    Tbuffer += tmp
    Tbuffer += struct.pack('>L',0x8001FFFF)
    ibuffer += struct.pack('<h',address)
    ibuffer += struct.pack('>h',0x0000)
    ibuffer += struct.pack('>L',0x00000000)
    address += len(tmp)+4
    seqNo = f.readline()
    tmp = f.readline()

wf.write(ibuffer)
wf.write(Tbuffer)

f.close()
wf.close()
