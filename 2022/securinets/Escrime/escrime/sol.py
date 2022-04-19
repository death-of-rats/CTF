#/usr/local/bin/sage -python3
from sage.all import *
from Crypto.Util.number import long_to_bytes

def main():
    prime= 10288862206522265548491095515168656477525126124487748561714968360821140813035366857049851221060982627755885655920945995256166965303092643565234471933471753
    fi1_org= 2573467084201708874166427893249437846395745397545855698319173947351314678936256903345837116191492486479839529179483188959731213590140049662859174962879837113761478386530635314940325208578484975969502409164780443342441068063618155067477897496671017228093836910453863947124651878651256446230522636476364605895908912291525529289472783428045871159743488316557779488426867728124470347009301794139849974908186832007416719187285462461941365126449836744042391167675460724
    fi2_org= 4087665301168020825798083143561427593888256464370045649891657553765281910566586774280695916049365560457943503468831216345782584880391584449841088200509970356209195159891879951935440735539589554326003469347731178208003980111045193186817121963648777499323413629167523378271805662750426713544056750624114369906408976714782302166847980854667613052475177605479729689055473869482560814911056101802784302419548208354842038075370500446594033529969715132143733531751351916
    n1 = 2573467084201708874166427893249437846395745397545855698319173947351314678936256903345837116191492486479839529179483188959731213590140049662859174962879837113761478386530635314940325208578484975969502409164780443342441068063618155070814620758794241531725834608172363855423784884876163437772652222052651058578748990161810472566692390400308049967365829391337921554598085552465830838761996176035867675326468670847790627425164646968299882839550481969719434913676608561
    n2 = 4087665301168020825798083143561427593888256464370045649891657553765281910566586774280695916049365560457943503468831216345782584880391584449841088200509970356209195159891879951935440735539589554326003469347731178208003980111045193190861106012684048682731017384733019063841372373480884605360832475876363425195007083906135512665262441575239472549440611809695441872975367123902821078482349928848186100692674995884705862532204804948591883414428748988832656324924482357
    e = 65537
    c1 = 1465333074823690719697988624680017273346599171341473045449321818660230520316236301255894905748788907779026118652329621698648178408128744483466369327189863865293830242385181088989378261437277630940355293752547657783752347221487655057789518697414309148432896740439433893445345259502062813864526753447860996137441408526157374361473132326439532419014816163100399319843555629530680435711842670895645488089619707413157946083536781377802572490380164743040052809028873053
    c2 = 1901816517224109673034163766796384921449874499260817487365490466768057031523113069171091373843020704134759738569823198350272248004913052075016733803357463992899243544657824808646545598638238256759515795089253635886168494308263588444501941542981965624753242274673876862378254310977327389743593403380184542444937899883555797753244868594647759750427035523170218957478290581870648845832768922719843732530571916117053751218205731709742325114663927889711976325454850342


    RANGE = 10
    # n1 = (2x a1 + 1)(2x b1 + 1) = 4x^2 a1*b1 + 2x (a1 + b1) + 1
    # n2 = (2x a2 + 1)(2x b2 + 1) = 4x^2 a2*b2 + 2x (a2 + b2) + 1

    # (n1 - 1)/2 = x(2*a1*b1*x + a1 + b1)
    # (n2 - 1)/2 = x(2*a2*b2*x + a2 + b2)


    # (n1 - 1)/2x = a1*b1*2x + a1 + b1
    # (n2 - 1)/2x = a2*b2*2x + a2 + b2
    # 2x a^2 + 2a - (n-1)/2x = 0
    prime512 = factor(gcd(n1-1,n2-1))[-1][0]
    #prime512 = 12397002878565866184412236037259205021945058505472864688501145731895119789392433217522880454989374040698621943547773164450323280239641723319936790061247301
    print(f"prime512: {prime512}")
    print(f"prime: {prime}")
    print(f"delta: {prime512 - prime}")

    ab1 = int((n1-1)//(2*prime512))
    for i in range(RANGE):
        fi1 = 4*prime512*prime512*(ab1-RANGE//2+i)
        d1 = lift(Mod(e,fi1)**(-1))
        print(f"[{i}] ({fi1_org - fi1}): {long_to_bytes(pow(c1, d1, n1))}")

    ab2 = int((n2-1)//(2*prime512))
    for i in range(RANGE):  
        fi2 = 4*prime512*prime512*(ab2-RANGE//2+i)
        d2 = lift(Mod(e,fi2)**(-1))
        print(f"[{i}] ({fi2_org - fi2}): {long_to_bytes(pow(c2, d2, n2))}")

main()
