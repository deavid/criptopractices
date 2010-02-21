import sys, os
szcompare = 2

combinations = {}
dupes = []

def compare(text, where):
    global combinations
    if text not in combinations: combinations[text] = 0
    elif combinations[text]==1: dupes.append(text)
    #if len(combinations[text])>5: return False
    combinations[text]+= 1 #.append(where)
    #print repr(text)
    return True

f1 = open("testfile1.out.random4", "rb")
#f1 = open("/dev/urandom", "rb")

compqueue = []
cnum = 0
while True:
    cnum += 1
    if cnum % (1024*512) == 0:
        n=float(cnum)/1024/1024
        print "%.1fMb" % (n)
        if n >=7: break
    try:
        char = f1.read(1)
    except:
        break
    compqueue.append(char)
    if len(compqueue)>szcompare: compqueue=compqueue[-szcompare:]
    if len(compqueue)==szcompare: 
        if not compare("".join(compqueue), cnum): break
        
dupes = set(dupes)
fset = []
for dupe in combinations:
    cptxt = "".join([ "%02X" % ord(c) for c in dupe])
    t = (combinations[dupe], cptxt)
    fset.append(t)
    #print "%02X%02X\t%d" % (dupe1,dupe2, combinations[dupe])
    
for t in sorted(fset)[0:32]:
    print t
print "..."    
for t in sorted(fset)[-32:]:
    print t

print "total", len(fset), "in set."
    
    
    
print cnum, "bytes read."    