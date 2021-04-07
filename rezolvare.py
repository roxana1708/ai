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
        l = [self];
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            if nod.parinte is not None:
                if nod.parinte.info[2] == 1:
                    mbarca1 = self.__class__.gr.malInitial
                    mbarca2 = self.__class__.gr.malFinal
                else:
                    mbarca1 = self.__class__.gr.malFinal
                    mbarca2 = self.__class__.gr.malInitial
                print(
                    ">>> Barca s-a deplasat de la malul {} la malul {} cu {} canibali si {} misionari.".format(mbarca1,
                    mbarca2, abs(nod.info[0] -nod.parinte.info[0]), abs(nod.info[1] -nod.parinte.info[1])))
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisCost:
            print("Nr noduri: ", len(l))
        return len(l)

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
        if self.info[2] == 1:
            barcaMalInitial = "<barca>"
            barcaMalFinal = "       "
        else:
            barcaMalInitial = "       "
            barcaMalFinal = "<barca>"
        return (
                    "Mal: " + self.gr.malInitial + " Canibali: {} Misionari: {} {}  |||  Mal:" + self.gr.malFinal + " Canibali: {} Misionari: {} {}").format(
            self.info[0], self.info[1], barcaMalInitial, self.__class__.gr.N - self.info[0],
            self.__class__.gr.N - self.info[1], barcaMalFinal)



class Graph:  # graful problemei
    def __init__(self, nume_fisier):

        f = open(nume_fisier, "r")
        textFisier = f.read()
        listaInfoFisier = textFisier.split()
        self.__class__.V = int(listaInfoFisier[0])
        self.__class__.C = int(listaInfoFisier[2])
        self.__class__.L = int(listaInfoFisier[4])
        self.__class__.compartiment1 = listaInfoFisier[6]
        self.__class__.compartiment2 = listaInfoFisier[7]
        self.__class__.magazie = listaInfoFisier[8]
        self.__class__.verzeInMagazie = 0
        self.__class__.capreInMagazie = 0
        self.__class__.lupiInMagazie = 0
        self.__class__.caprePerLup = listaInfoFisier[9]
        self.__class__.lupiPerLup = listaInfoFisier[10]
        self.__class__.verzePerCapre = listaInfoFisier[11]
        self.__class__.finalVerze = listaInfoFisier[12]
        self.__class__.finalCapre = listaInfoFisier[13]
        self.__class__.finalLupi = listaInfoFisier[14]

        self.start = (self.__class__.V, self.__class__.C, self.__class__.L, 1, self.__class__.magazie)  # informatia nodului de start: verze, capre, lupi, malul pe care este barca (1 = dreapta)

        # TODO: scopuri sunt toate variantele de "resturi" pe malul initial
        self.scopuri = [(0, 0, 0, 0)]

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri

    # functia de generare a succesorilor, facuta la laborator
    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):

        def test_conditie(verze, capre, lupi):
            if verze - Graph.verzePerCapra * capre < Graph.finalVerze:
                return 0

            if capre - Graph.caprePerLup * lupi < Graph.finalCapre:
                return 0

            #if capre == 0 and lupi > 0:
                # TODO: functie care sa calculeze lupi ramasi



        listaSuccesori = []
        # nodCurent.info va contine un tuplu (v_initial, c_initial, l_initial, barca, v_opus, c_opus, l_opus, v_magazie, c_magazie, l_magazie)
        barca = nodCurent.info[3]
        if barca == 1:
            # mal curent
            verzeMalCurent = nodCurent.info[0]
            capreMalCurent = nodCurent.info[1]
            lupiMalCurent = nodCurent.info[2]

            # mal opus
            verzeMalOpus = Graph.V - verzeMalCurent
            capreMalOpus = Graph.C - capreMalCurent
            lupiMalOpus = Graph.L - lupiMalCurent
        else:
            # mal opus
            verzeMalOpus = nodCurent.info[0]
            capreMalOpus = nodCurent.info[1]
            lupiMalOpus = nodCurent.info[2]

            # mal curent
            verzeMalCurent = Graph.V - verzeMalOpus
            capreMalCurent = Graph.C - capreMalOpus
            lupiMalCurent = Graph.L - lupiMalOpus

            maxVerzeBarca = min(Graph.compartiment1, Graph.compartiment2, verzeMalCurent)

            comp1 = False
            comp2 = False

            if maxVerzeBarca == Graph.compartiment1:
                comp1 = True
            elif maxVerzeBarca == Graph.compartiment2:
                comp2 = True


        # TODO: for in for in for
        #for verze in barca
            #for capre in barca
                #for lupi in barca

        # TODO: cum influenteaza compartimentul ocupat alegerea pentru max de alt tip
        #  eventual folosim variabile pt a stii daca compartimentele sunt ocupate
        for verzeBarca in range(maxVerzeBarca + 1):
            if verzeBarca == 0 or (comp1 == False and comp2 == False):
                maxCapreBarca = min(Graph.compartiment1, Graph.compartiment2, capreMalCurent)
                minCapreBarca = 0

                if maxCapreBarca == Graph.compartiment1:
                    comp1 = True
                elif maxCapreBarca == Graph.compartiment2:
                    comp2 = True
            elif comp1 == False:
                maxCapreBarca = min(Graph.compartiment1, capreMalCurent)
                minCapreBarca = 0
                comp1 = True
            else:
                maxCapreBarca = min(Graph.compartiment2, capreMalCurent)
                minCapreBarca = 0
                comp2 = True


            if verzeBarca != 0 and capreBarca != 0:
                if comp1 == False:
                    comp1 = True
                if comp2 == False:
                    comp2 = True

            for capreBarca in range(minCapreBarca, maxCapreBarca + 1):

                if capreBarca == 0 and verzeBarca == 0:
                    maxLupiBarca = min(Graph.compartiment1, Graph.compartiment2, lupiMalCurent)
                    minLupiBarca = 0
                elif (capreBarca > 0 and verzeBarca == 0) or (capreBarca == 0 and verzeBarca > 0):
                    if comp1 == False:
                        maxLupiBarca = min(Graph.compartiment1, lupiMalCurent)
                        minLupiBarca = 0
                        comp1 = True
                    elif comp2 == False:
                        maxLupiBarca = min(Graph.compartiment2, lupiMalCurent)
                        minLupiBarca = 0
                        comp2 = True
                else:
                    continue


                for lupiBarca in range(minLupiBarca, maxLupiBarca + 1):
                    # consideram mal curent nou ca fiind acelasi mal de pe care a plecat barca

                    verzeMalCurentNou = verzeMalCurent - verzeBarca
                    verzeMalOpusNou = verzeMalOpus + verzeBarca
                    capreMalCurentNou = capreMalCurent - capreBarca
                    capreMalOpusNou = capreMalOpus + capreBarca
                    lupiMalCurentNou = lupiMalCurent - lupiBarca
                    lupiMalOpusNou = lupiMalOpus + lupiBarca


                    # TODO: variante mal opus cu magazie


                    if not test_conditie(verzeMalCurentNou, capreMalCurentNou, lupiMalCurentNou):
                        continue
                    if not test_conditie(verzeMalOpusNou, capreMalOpusNou, lupiMalOpusNou):
                        continue

                    # nodCurent.info va contine un tuplu (v_initial, c_initial, l_initial, barca, v_opus, c_opus, l_opus, v_magazie, c_magazie, l_magazie)

                    if barca == 1:  # testul este pentru barca nodului curent (parinte) deci inainte de mutare
                        infoNodNou = (verzeMalCurentNou, capreMalCurentNou, lupiMalCurentNou, 0, verzeMalOpusNou, capreMalOpusNou, lupiMalOpusNou) # completat magazie
                    else:
                        infoNodNou = (verzeMalCurentNou, capreMalCurentNou, lupiMalCurentNou, 0, verzeMalOpusNou, capreMalOpusNou, lupiMalOpusNou) # completat magazie
                    if not nodCurent.contineInDrum(infoNodNou):
                        # TODO: calculat cost
                        #costSuccesor =
                        #listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, cost=nodCurent.g + costSuccesor, h=NodParcurgere.gr.calculeaza_h(infoNodNou, tip_euristica)))

        return listaSuccesori


def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            #input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


gr = Graph("input.txt")
NodParcurgere.gr = gr
nrSolutiiCautate = 3
a_star(gr, nrSolutiiCautate=3, tip_euristica="euristica nebanala")
