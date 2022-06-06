from math import gcd

N = 25059693027490518228188939470373635065456203073319867209977949623515493737430287865750893002763495373360254441112343483798994468254892993659168593390427633826749503529765436671550641172987184898387715546593524331258155650478461198384089631509549000426330336924147906692772305083997847954752063842427171280286479237113443445726349151279976943896381990599387083229581527068955498326987227061262059392559274150808580307165878564039211472027686164584062667471098252054263555297504230520345961114701236267839724451054904902833144686076893160362762741060885009169833562032289866278657071802946701962487165458978518123706149
e = 65537
m = 62583843215221120636897297615798101107004929195670774199609739386851894805096

S = 14924896270743029407125096876411695409976070579394025037825986844389399845676592792471061227173693226468051983326985343880105192540991605628494919732570458402858535943968042901796190730550323921988436191313667765984117899229549565623928723137403669588325038154331608704601406667414061631478364362268605861721019254903054105605048256781705209182879637608516092353515018476941978157832614701555812764802875091520632561582045448050908676788359886673616100283966158660059064412198757110892440853637677210559880703195718592394282221892342357500120332399482678407930796931042493272342881944969821468479073519479120111746554
Sp = 12155673077742522283656155507099493371426732516185638743366364157286426151214280935745046670232574206305117438871354876055446522845273602683170471336102670712591476208789294248124363747081268551877488326244967540389938899205435400101199139016826775578945871190190638604657811062035700769052021754531148815337166320684728019850922460655235835833833127292851008888347754516007475960451840177677944748423538961797730146959895168736781102618365639747179101220315437229390768046250474967854593643591157762034815666280953849624525362209641764922779349864811983547588144232418814966665260702836704821028026423694928971170109

dm = m - pow(Sp, e, N)
q = gcd(dm % N,N)
p = N // q

print(f"test: {N == p*q}")

d = pow(e, -1, (p-1)*(q-1))
print(d)

print(f"test: {S == pow(m,d,N)}")