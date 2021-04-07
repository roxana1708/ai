import math

# informatii despre un nod din arborele de parcurgere (nu din graful initial)
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
        # nodCurent.info va contine un tuplu (v_i, c_i, l_i, barca, magazie)
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
            if verzeBarca == 0:
                maxCapreBarca = min(Graph.compartiment1, Graph.compartiment2, capreMalCurent)
                minCapreBarca = 0
            else:
                maxCapreBarca = min(Graph.compartiment1, Graph.compartiment2)
                minCapreBarca = 0

            for capreBarca in range(minCapreBarca, maxCapreBarca + 1):

                if capreBarca == 0 and verzeBarca == 0:
                    maxLupiBarca = min(Graph.compartiment1, Graph.compartiment2, lupiMalCurent)
                    minLupiBarca = 0
                elif :
                    maxLupiBarca =
                else:


                for lupiBarca in range(minLupiBarca, maxLupiBarca + 1):
                    # consideram mal curent nou ca fiind acelasi mal de pe care a plecat barca
                    canMalCurentNou = canMalCurent - canBarca
                    misMalCurentNou = misMalCurent - misBarca
                    canMalOpusNou = canMalOpus + canBarca
                    misMalOpusNou = misMalOpus + misBarca


                    if not test_conditie(misMalCurentNou, canMalCurentNou):
                        continue
                    if not test_conditie(misMalOpusNou, canMalOpusNou):
                        continue
                    if barca == 1:  # testul este pentru barca nodului curent (parinte) deci inainte de mutare
                        infoNodNou = (canMalCurentNou, misMalCurentNou, 0)
                    else:
                        infoNodNou = (canMalOpusNou, misMalOpusNou, 1)
                    if not nodCurent.contineInDrum(infoNodNou):
                        costSuccesor = canBarca * 2 + misBarca
                        listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, cost=nodCurent.g + costSuccesor,
                                            h=NodParcurgere.gr.calculeaza_h(infoNodNou, tip_euristica)))

        return listaSuccesori