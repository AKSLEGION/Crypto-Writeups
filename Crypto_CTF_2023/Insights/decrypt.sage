n = 12765231982257032754070342601068819788671760506321816381988340379929052646067454855779362773785313297204165444163623633335057895252608396010414744222572161530653104640020689896882490979790275711854268113058363186249545193245142912930804650114934761299016468156185416083682476142929968501395899099376750415294540156026131156551291971922076435528869024742993840057342092865203064721826362149723366381892539617642364692012936270150691803063945919154346756726869466855557344213050973081755499746750276623648407677639812809665472258655462846021403503851719008687214848550916999977775070011121527941755954255781343103086789
d = next_prime(pow(n, 0.2919))
c = 10992248752412909788626396175372747713079469256270100576886987393986576680666320383209810005318254336440105142571546847427454822405793626080251363454531982746373841267986148332456716023293306870382809568309620264499225135226626560298741596462262513921032733814032790312163314776421380481083058518893602887082464123177575742160690315666730642727773288362853901330620841098230284739614618790097180848133698381487679399364400048499041582830157094876815030301231505774900176910650887780842536610942820066913075027528705150102760422836458745949063992228680293226303245265232017738712226154128654682937687199768621565945171
m = pow(c,d,n)

flag=bytes.fromhex(hex(m)[2:]).decode()
print(flag)