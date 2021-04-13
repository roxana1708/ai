import math

class NodParcurgere:
    gr = None  # trebuie setat sa contina instanta problemei

    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        le = [self]
        nod = self
        while nod.parinte is not None:
            le.insert(0, nod.parinte)
            nod = nod.parinte
        print(le)
        return le

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        le = self.obtineDrum()
        for nod in le:
            if nod.parinte is not None:
                if nod.parinte.info[3] == 1:
                    mbarca1 = self.__class__.gr.malInitial
                    mbarca2 = self.__class__.gr.malFinal
                else:
                    mbarca1 = self.__class__.gr.malFinal
                    mbarca2 = self.__class__.gr.malInitial
                print(
                    # nodCurent.info va contine un tuplu (    0    ,     1    ,     2    ,   3  ,   4   ,    5  ,   6   ,    7     ,    8     ,     9    )
                    # nodCurent.info va contine un tuplu (v_initial, c_initial, l_initial, barca, v_opus, c_opus, l_opus, v_magazie, c_magazie, l_magazie)
                    ">>> Barca s-a deplasat de la malul {} la malul {} cu {} verze, {} capre, {} lupi".format(mbarca1,
                    mbarca2, abs(nod.parinte.info[0] - nod.info[0]), abs(nod.info[1] -nod.parinte.info[1]), abs(nod.info[2] - nod.parinte.info[2])))
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisCost:
            print("Nr noduri: ", len(le))
        return len(le)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return (sir)

    # euristica banala: daca nu e stare scop, returnez 1, altfel 0

    def __str__(self):
        if self.info[3] == 1:
            barcaMalInitial = "<barca>"
            barcaMalFinal = "       "
        else:
            barcaMalInitial = "       "
            barcaMalFinal = "<barca>"

        return (
                    "Mal: " + self.gr.malInitial + " Verze: {} Capre: {} Lupi: {} {}  |||  Mal:" + self.gr.malFinal + " Verze: {} Capre: {} Lupi: {} {}").format(
            self.info[0], self.info[1], self.info[2], barcaMalInitial, self.info[4]+self.info[7], self.info[5]+self.info[8], self.info[6]+self.info[9], barcaMalFinal)


class Graph:  # graful problemei
    def __init__(self, nume_fisier):

        f = open(nume_fisier, "r")
        textFisier = f.read()
        listaInfoFisier = textFisier.split()
        print(listaInfoFisier)
        self.__class__.V = int(listaInfoFisier[0])
        self.__class__.C = int(listaInfoFisier[2])
        self.__class__.L = int(listaInfoFisier[4])
        self.__class__.compA = int(listaInfoFisier[6])
        self.__class__.compB = int(listaInfoFisier[7])
        self.__class__.magazie = int(listaInfoFisier[8])
        self.__class__.caprePerLup = int(listaInfoFisier[9])
        self.__class__.lupiPerLup = int(listaInfoFisier[10])
        self.__class__.verzePerCapra = int(listaInfoFisier[11])
        self.__class__.finalVerze = int(listaInfoFisier[12])
        self.__class__.finalCapre = int(listaInfoFisier[14])
        self.__class__.finalLupi = int(listaInfoFisier[16])
        self.__class__.malInitial = "est"
        self.__class__.malFinal = "vest"
        #print(self.__class__.finalLupi)

        # nodCurent.info va contine un tuplu (    0    ,     1    ,     2    ,   3  ,   4   ,    5  ,   6   ,    7     ,    8     ,     9    )
        # nodCurent.info va contine un tuplu (v_initial, c_initial, l_initial, barca, v_opus, c_opus, l_opus, v_magazie, c_magazie, l_magazie)

        self.start = (self.__class__.V, self.__class__.C, self.__class__.L, 1, 0, 0, 0, 0, 0, 0) # informatia nodului de start: verze, capre, lupi, malul pe care este barca (1 = dreapta)

        #self.scopuri = [(0, 0, 0, 0, self.__class__.finalVerze, self.__class__.finalCapre, self.__class__.finalLupi, 0, 0, 0)]

        # TODO: scopuri sunt toate variantele de "resturi" pe malul initial
        #for i in range(self.__class__.finalVerze, self.__class__V):
            #for j in range(self.__class__.finalCapre, self.__class__C):
                #for k in range(self.__class__.finalLupi, self.__class__L):



    def testeaza_scop(self, nodCurent):
        if (nodCurent[4] + nodCurent[7] >= self.finalVerze) and (nodCurent[5] + nodCurent[8] >= self.finalCapre) and (nodCurent[6] + nodCurent[9] >= self.finalLupi):
            return 1
        return 0


    def calculeaza_h(self, infoNod, tip_euristica):
        if tip_euristica == "euristica banala":
            if self.testeaza_scop(infoNod):
                return 1
            return 0
        else:
            # calculez cati oameni mai am de mutat si impart la nr de locuri in barca
            # totalOameniDeMutat=infoNod[0]+infoNod[1]
            return 2 * math.ceil(((self.finalVerze - (infoNod[4] + infoNod[7])) + (self.finalCapre - (infoNod[5] + infoNod[8])) + (self.finalLupi - (infoNod[6] + infoNod[9]))) / (self.compA + self.compB)) + (1 - infoNod[3]) - 1

    # functia de generare a succesorilor, facuta la laborator
    def genereazaSuccesori(self, nodCurent, tip_euristica):

        def get_costSucc(verzeA, capreA, lupiA, verzeB, capreB, lupiB, barca):
            # TODO: calculat cost
            '''
            if barca == 1:
                if verzeA == 0 and verzeB == 0 and capreA == 0 and capreB == 0 and lupiA == 0 and lupiB == 0:
                    return 1000
                elif verzeA + verzeB == 0 and capreA + capreB == 0 and lupiA + lupiB > 0:
                    return 0
                elif verzeA + verzeB == 0 and capreA + capreB > 0 and lupiA + lupiB == 0:
                    return 700
                elif verzeA + verzeB > 0 and capreA + capreB == 0 and lupiA + lupiB == 0:
                    return 700
                elif (verzeA > 0 and verzeB > 0) or (capreA > 0 and capreB > 0) or (lupiA > 0 and lupiB > 0):
                    return 500
                else:
                    return 0
            else:
                if verzeA == 0 and verzeB == 0 and capreA == 0 and capreB == 0 and lupiA == 0 and lupiB == 0:
                    return 0
                elif (verzeA > 0 and verzeB > 0) or (capreA > 0 and capreB > 0) or (lupiA > 0 and lupiB > 0):
                    return 500
                elif verzeA + verzeB == 0 and capreA + capreB == 0 and lupiA + lupiB > 0:
                    return 400
                elif verzeA + verzeB == 0 and capreA + capreB > 0 and lupiA + lupiB == 0:
                    return 700
                elif verzeA + verzeB > 0 and capreA + capreB == 0 and lupiA + lupiB == 0:
                    return 700
                else:
                    return 1000
            '''


            '''
            costSuccesor = 0
            if verzeA == 0 and verzeB == 0 and capreA == 0 and capreB == 0 and lupiA == 0 and lupiB == 0 and barca == 1:
                return 1000
            elif verzeA == 0 and verzeB == 0 and capreA == 0 and capreB == 0 and lupiA == 0 and lupiB == 0 and barca == 0:
                return 0

            if verzeA and verzeB and barca == 1:
                return 1000 - verzeA + (verzeB / 2) * 1.5
            elif verzeA and verzeB and barca == 0:
                return 1000 + verzeA + (verzeB / 2) * 1.5
            if capreA and capreB and barca == 1:
                return 1000 - capreA * 2 + (capreB / 2) * 3
            elif capreA and capreB and barca == 0:
                return 1000 + capreA * 2 + (capreB / 2) * 3
            if lupiA and lupiB and barca == 1:
                return 1000 - lupiA * 3 + (lupiB / 2) * 4.5
            elif lupiA and lupiB and barca == 0:
                return 1000 + lupiA * 3 + (lupiB / 2) * 4.5

            if verzeA:
                costSuccesor += verzeA
            elif capreA:
                costSuccesor += capreA * 2
            elif lupiA:
                costSuccesor += lupiA * 3

            # pt compB
            if verzeB:
                costSuccesor += verzeB * 1.5
            elif capreB:
                costSuccesor += capreB * 3
            elif lupiB:
                costSuccesor += lupiB * 4.5

            if barca == 1:
                return 1000 - costSuccesor
            else:
                return 1000 + costSuccesor
                
            '''

        def test_conditie(verzeMC, capreMC, lupiMC, verzeMO, capreMO, lupiMO):
            if verzeMC - Graph.verzePerCapra * capreMC + verzeMO - Graph.verzePerCapra * capreMO < Graph.finalVerze:
                return 0

            if capreMC - Graph.caprePerLup * lupiMC + capreMO - Graph.caprePerLup * lupiMO < Graph.finalCapre:
                return 0

            if capreMC == 0 and lupiMC > 0:
                # TO DO: functie care sa calculeze lupi ramasi
                copy = lupiMC
                lup = 1
                while lup < copy:
                    copy -= Graph.lupiPerLup
                    lup += 1

            if capreMO == 0 and lupiMO > 0:
                # TO DO: functie care sa calculeze lupi ramasi
                copy2 = lupiMO
                lup2 = 1
                while lup2 < copy2:
                    copy2 -= Graph.lupiPerLup
                    lup2 += 1

            if copy + copy2 < Graph.finalLupi:
                return 0

            return 1


        def genereaza_combinatii_magazie(verzeA, verzeB, capreA, capreB, lupiA, lupiB, nodCurent, tip_euristica):
            '''
            print("........")
            print (verzeA)
            print (verzeB)
            print (capreA)
            print (capreB)
            print (lupiA)
            print (lupiB)
            print (nodCurent.info[7])
            print (nodCurent.info[8])
            print (nodCurent.info[9])
            print("........")
            '''
            if nodCurent.info[3] == 1:
                verzeMEstNou = nodCurent.info[0] - (verzeA + verzeB)
                capreMEstNou = nodCurent.info[1] - (capreA + capreB)
                lupiMEstNou = nodCurent.info[2] - (lupiA + lupiB)

                maxVM = min(verzeA+verzeB+nodCurent.info[4], Graph.magazie)
                #print("vmvmvmv " + str(maxVM))
                for nr_v in range(maxVM+1):
                    if nr_v == 0:
                        maxCM = min(capreA+capreB+nodCurent.info[5], Graph.magazie)
                    else:
                        maxCM = 0
                    #print("cmcmcmc " + str(maxCM))
                    for nr_c in range(maxCM+1):
                        if nr_v == 0 and nr_c == 0:
                            maxLM = min(lupiA+lupiB+nodCurent.info[6], Graph.magazie)
                        else:
                            maxLM = 0

                        #print (" lmlmlm " + str(maxLM))
                        for nr_l in range(maxLM+1):
                            #print("----")
                            #print(nr_l)
                            #print(nr_c)
                            #print(nr_v)
                            #print("----")
                            verzeMalVestNou = (nodCurent.info[4] + verzeA + verzeB + nodCurent.info[7]) - nr_v
                            capreMalVestNou = (nodCurent.info[5] + capreA + capreB + nodCurent.info[8]) - nr_c
                            lupiMalVestNou = (nodCurent.info[6] + lupiA + lupiB + nodCurent.info[9]) - nr_l

                            # nodCurent.info va contine un tuplu (v_initial, c_initial, l_initial, barca, v_opus, c_opus, l_opus, v_magazie, c_magazie, l_magazie)
                            infoNodNou = (verzeMEstNou, capreMEstNou, lupiMEstNou, 0, verzeMalVestNou, capreMalVestNou, lupiMalVestNou, nr_v, nr_c, nr_l)
                            #print(infoNodNou)
                            #if not test_conditie():
                                #continue

                            costSuccesor = get_costSucc(verzeA, capreA, lupiA, verzeB, capreB, lupiB, nodCurent.info[3])
                            #print("cost = " + str(costSuccesor))
                            listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, cost=nodCurent.g + costSuccesor, h=NodParcurgere.gr.calculeaza_h(infoNodNou, tip_euristica)))

            else:
                verzeMEstNou = nodCurent.info[0] + (verzeA + verzeB)
                capreMEstNou = nodCurent.info[1] + (capreA + capreB)
                lupiMEstNou = nodCurent.info[2] + (lupiA + lupiB)

                if nodCurent.info[7] > 0:
                    maxVM = min(nodCurent.info[7], verzeA + verzeB)
                    if nodCurent.info[4] - (verzeA+verzeB) < 0:
                        minVM = verzeA + verzeB - nodCurent.info[4]
                    else:
                        minVM = 0
                else:
                    maxVM = 0#min(nodCurent.info[4], verzeA + verzeB)
                    minVM = 0

                for nr_v in range(minVM, maxVM+1):
                    if nodCurent.info[8] > 0:
                        maxCM = min(nodCurent.info[8], capreA + capreB)
                        if nodCurent.info[5] - (capreA + capreB) < 0:
                            minCM = capreA + capreB - nodCurent.info[5]
                        else:
                            minCM = 0
                    else:
                        maxCM = 0#min(nodCurent.info[5], capreA + capreB)
                        minCM = 0

                    for nr_c in range(minCM, maxCM+1):
                        if nodCurent.info[9] > 0:
                            maxLM = min(nodCurent.info[9], lupiA + lupiB)
                            if nodCurent.info[6] - (lupiA + lupiB) < 0:
                                minLM = lupiA + lupiB - nodCurent.info[6]
                            else:
                                minLM = 0
                        else:
                            maxLM = 0#min(nodCurent.info[6], lupiA + lupiB)
                            minLM = 0

                        for nr_l in range(minLM, maxLM+1):
                            verzeMalVestNou = nodCurent.info[4] - (verzeA+verzeB-nr_v)
                            capreMalVestNou = nodCurent.info[5] - (capreA+capreB-nr_c)
                            lupiMalVestNou = nodCurent.info[6] - (lupiA+lupiB-nr_l)

                            infoNodNou = (verzeMEstNou, capreMEstNou, lupiMEstNou, 1, verzeMalVestNou, capreMalVestNou,
                                          lupiMalVestNou, nodCurent.info[7] - nr_v, nodCurent.info[8] - nr_c, nodCurent.info[9] - nr_l)
                            #print(infoNodNou)
                            #if not test_conditie(infoNodNou):
                             #   continue

                            costSuccesor = get_costSucc(verzeA, capreA, lupiA, verzeB, capreB, lupiB, nodCurent.info[3])
                            #print("cost = " + str(costSuccesor))
                            listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, cost=nodCurent.g + costSuccesor, h=NodParcurgere.gr.calculeaza_h(infoNodNou, tip_euristica)))

        # functia principala
        listaSuccesori = []

        barca = nodCurent.info[3]
        if barca == 1:
            verzeMalCurent = nodCurent.info[0]
            capreMalCurent = nodCurent.info[1]
            lupiMalCurent = nodCurent.info[2]
        else:
            verzeMalCurent = nodCurent.info[4] + nodCurent.info[7]
            capreMalCurent = nodCurent.info[5] + nodCurent.info[8]
            lupiMalCurent = nodCurent.info[6] + nodCurent.info[9]

        maxVerzeBarca = min(verzeMalCurent, Graph.compA + Graph.compB)
        #print(maxVerzeBarca)
        for v in range(maxVerzeBarca+1):
            #print(v)
            if v == 0:
                maxCapreBarca = min(capreMalCurent, Graph.compA + Graph.compB)
            elif v >= Graph.compA and v >= Graph.compB:
                maxCapreBarca = 0
            else:
                if v <= Graph.compA:
                    maxCapreBarca = min(capreMalCurent, Graph.compB)
                else:
                    maxCapreBarca = min(capreMalCurent, Graph.compA)

            for c in range(maxCapreBarca+1):
                if v == 0 and c == 0:
                    maxLupiBarca = min(lupiMalCurent, Graph.compA + Graph.compB)
                elif (v > 0 and c > 0) or (v >= Graph.compA and v >= Graph.compB) or (c >= Graph.compA and c >= Graph.compB):
                    maxLupiBarca = 0
                elif v > 0 and c == 0:
                    if v <= Graph.compA:
                        maxLupiBarca = min(lupiMalCurent, Graph.compB)
                    else:
                        maxLupiBarca = min(lupiMalCurent, Graph.compA)
                elif v == 0 and c > 0:
                    if c <= Graph.compA:
                        maxLupiBarca = min(lupiMalCurent, Graph.compB)
                    else:
                        maxLupiBarca = min(lupiMalCurent, Graph.compA)

                for l in range(maxLupiBarca+1):
                    if v == 0 and c == 0 and l == 0:
                        genereaza_combinatii_magazie(0, 0, 0, 0, 0, 0, nodCurent, tip_euristica)
                    if v > 0 and c > 0:
                        if v <= Graph.compA and c <= Graph.compB:
                            genereaza_combinatii_magazie(v, 0, 0, c, 0, 0, nodCurent, tip_euristica)
                        else:
                            genereaza_combinatii_magazie(0, v, c, 0, 0, 0, nodCurent, tip_euristica)
                    elif c > 0 and l > 0:
                        if c <= Graph.compA and l <= Graph.compB:
                            genereaza_combinatii_magazie(0, 0, c, 0, 0, l, nodCurent, tip_euristica)
                        else:
                            genereaza_combinatii_magazie(0, 0, 0, c, l, 0, nodCurent, tip_euristica)

                    elif v > 0 and l > 0:
                        if v <= Graph.compA and l <= Graph.compB:
                            genereaza_combinatii_magazie(v, 0, 0, 0, 0, l, nodCurent, tip_euristica)
                        else:
                            genereaza_combinatii_magazie(0, v, 0, 0, l, 0, nodCurent, tip_euristica)

                    elif v > Graph.compA:
                        genereaza_combinatii_magazie(Graph.compA, v - Graph.compA, 0, 0, 0, 0, nodCurent, tip_euristica)
                    elif v <= Graph.compA and v > 0:
                        genereaza_combinatii_magazie(v, 0, 0, 0, 0, 0, nodCurent, tip_euristica)

                    elif c > Graph.compA:
                        genereaza_combinatii_magazie(0, 0, Graph.compA, c - Graph.compA, 0, 0, nodCurent, tip_euristica)
                    elif c <= Graph.compA and c > 0:
                        genereaza_combinatii_magazie(0, 0, c, 0, 0, 0, nodCurent, tip_euristica)

                    elif l > Graph.compA:
                        genereaza_combinatii_magazie(0, 0, 0, 0, Graph.compA, l - Graph.compA, nodCurent, tip_euristica)
                    elif l <= Graph.compA and l > 0:
                        genereaza_combinatii_magazie(0, 0, 0, 0, l, 0, nodCurent, tip_euristica)

                    #print(listaSuccesori)

        print(nodCurent.info)
        #print(listaSuccesori)
        return listaSuccesori




def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica))]

    verif = 0
    while len(c) > 0:
        nodCurent = c.pop(0)
        print("aaa")
        print(nodCurent.info)
        print("aaa")
        print(gr.testeaza_scop(nodCurent.info))
        print("aaa")
        if gr.testeaza_scop(nodCurent.info):
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            #input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        print("bbb")
        print(lSuccesori)
        print("bbb")
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)
        print(c)
        '''
        if verif < 50:
            verif += 1
        else:
            break
        '''


gr = Graph("input2.txt")
#gr.genereazaSuccesori(NodParcurgere((17, 6, 2, 1, 3, 4, 0, 0, 0, 0), None, 0, gr.calculeaza_h(gr.start)), tip_euristica="euristica banala")
#print(gr.testeaza_scop(((17, 6, 2, 1, 3, 4, 1, 0, 0, 0))))
'''
print(gr.V)
print(gr.C)
print(gr.L)
print(gr.compA)
print(gr.compB)
print(gr.magazie)
print(gr.caprePerLup)
print(gr.lupiPerLup)
print(gr.verzePerCapra)
print(gr.finalVerze)
print(gr.finalCapre)
print(gr.finalLupi)
print(gr.malInitial)
print(gr.malFinal)
'''
NodParcurgere.gr = gr
nrSolutiiCautate = 1
a_star(gr, nrSolutiiCautate=1, tip_euristica="euristica nebanala")
