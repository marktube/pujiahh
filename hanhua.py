
f = open("EndingTextMsgTypeA.mbm","rb")
wf = open("text","w")

f.seek(0x10)

num_of_words = int(f.read(1).encode('hex'),16)

f.seek(31,1)

while True :
  words = int(f.read(1).encode('hex'),16)
  if words > num_of_words:break
  f.seek(3,1)
  length = int(f.read(1).encode('hex'),16) - 4
#  print length
  f.seek(3,1)
  address = int(f.read(1).encode('hex'),16)
  address += int(f.read(1).encode('hex'),16)*256
#  print hex(address)
  f.seek(6,1)
  tmp = f.tell()
  f.seek(address)
  wf.write( "#### "+str(words)+" ####\n")
  wf.write(f.read(length).decode('shift-jis').encode('utf8'))
  wf.write("\n")
  f.seek(tmp)
 
f.close() 
