from Crypto.Util.number import *

n = 95593382112797270045497836514999308524326160650345266525670495575191979116591752182138270308274446464071024826510473429700676303637674960212123982700153540490805215151070356646141514736282385755143090035980011032465519861526291865888128545478530962058792257703950616556136479933021373472378679162332202365371
c = 92084942302809419329882275131365664619817865820237979575321652348851871468885232665120732298048355621943772250718055278615366362227084559410831820721620242260588398786014654743749734106956509345330468686120026908164376320923131751798117799981744551407234489862207435686504148347452579942637697333568788391594
e = 65537
extra_information = 18247071175606431398122118602371784578875472790915317892207044424588309397797319375039984309368393267673885302107217184699052743790470091033147110959310433418937324145720036262540098007724458652548486534453030546582214242131458903058169536052488501597969216020092796160475487905223265691093061136660574497410399108890645909789835984721231354187679269066357591297035974333220513134895660609801438138623213711900681512310067292949714127564635579383633589101296120704659647911638787823818973909534106275908594589830353183557722172234952579827423906720754070119865452363350814918812923981729393142874903734028229195885438296963982680724071663211427931391032589901737528717167662646147224323491202696402122261699504048973334902281462240308032014697804531871922566779026958815207465755155123070196922127199447785648102152027431894178737946151518726929361221425189695069653652163012000609320105988830299015364692678902927254273154427301473090465612473379114039284029813071586214536353994345527805408387636097772645156970939979500155578289301143563369142329343932852167241705090287661795

import math
q = math.gcd(n,extra_information)
p = n//q

phi = n-p-q+1
d = pow(e,-1,phi)
m = pow(c,d,n)

print("The flag is : " + long_to_bytes(m).decode())