# DOCUMENTATIE: https://docs.google.com/document/d/1fokREYc3RLQ03MQ2_FdijuWlsxUvrzFjMDzIz3yReUQ/edit?usp=sharing

import math, time
import sys

output_ucs_1 = open("output_1_ucs.txt", "w")
output_ucs_2 = open("output_2_ucs.txt", "w")
output_ucs_3 = open("output_3_ucs.txt", "w")
output_ucs_4 = open("output_4_ucs.txt", "w")

output_a_star_opt_1 = open("output_1_a_star_opt.txt", "w")
output_a_star_opt_2 = open("output_2_a_star_opt.txt", "w")
output_a_star_opt_3 = open("output_3_a_star_opt.txt", "w")
output_a_star_opt_4 = open("output_4_a_star_opt.txt", "w")

output_a_star_1 = open("output_1_a_star.txt", "w")
output_a_star_2 = open("output_2_a_star.txt", "w")
output_a_star_3 = open("output_3_a_star.txt", "w")
output_a_star_4 = open("output_4_a_star.txt", "w")

output_ida_star_1 = open("output_1_ida_star.txt", "w")
output_ida_star_2 = open("output_2_ida_star.txt", "w")
output_ida_star_3 = open("output_3_ida_star.txt", "w")
output_ida_star_4 = open("output_4_ida_star.txt", "w")

'''
Folosesc clasele NodParcurgere si Graph de la laborator.
nodCurent.info va contine un tuplu:
(v_initial, c_initial, l_initial, barca, v_opus, c_opus, l_opus, v_magazie, c_magazie, l_magazie)
Deoarece numarul total pentru fiecare element se modifica in functie de cum "se mananca" intre ele,
m-am gandit ca ar fi mai bine sa retin elementele de pe ambele maluri si din magazie,
nu sa le calulez unele in functie de altele (pentru a economisi timp)
'''
class NodParcurgere:
    gr = None  # trebuie setat sa contina instanta problemei

    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self, f):
        le = [self]
        nod = self
        while nod.parinte is not None:
            le.insert(0, nod.parinte)
            nod = nod.parinte
        return le

    def afisDrum(self, f, afisCost=False):  # returneaza si lungimea drumului
        le = self.obtineDrum(f)
        index_nod = 1
        for nod in le:
            '''
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
                        mbarca2, abs(nod.parinte.info[0] - nod.info[0]), abs(nod.info[1] - nod.parinte.info[1]),
                        abs( nod.info[2] - nod.parinte.info[2]))
                )
            '''
            f.write(str(index_nod) + str(nod) + "\n")
            index_nod += 1
        if afisCost:
            f.write("Cost: " + str(self.g) + "\n")
        if afisCost:
            f.write("Nr noduri: " + str(len(le)) + "\n")
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


    def __str__(self):
        if self.info[3] == 1:
            barcaMalInitial = "<barca>"
            barcaMalFinal = "       "
        else:
            barcaMalInitial = "       "
            barcaMalFinal = "<barca>"

        return (
                "Mal: " + self.gr.malInitial + " Verze: {} Capre: {} Lupi: {} {}  |||  Mal:" + self.gr.malFinal + " Verze: {} Capre: {} Lupi: {}. In magazie sunt {} verze, {} capre, {} lupi. {}").format(
            self.info[0], self.info[1], self.info[2], barcaMalInitial, self.info[4], self.info[5], self.info[6],
            self.info[7], self.info[8], self.info[9], barcaMalFinal)


class Graph:  # graful problemei
    def verif_input(self):
        '''
            verificam daca din input putem obtine outputul cerut
        '''
        if self.__class__.V < self.__class__.finalVerze:
            #print("Numarul de verze de pe malul initial este mai mic decat numarul de verze dorit pentru a se gasi pe malul final")
            return 0
        if self.__class__.C < self.__class__.finalCapre:
            #print("Numarul de capre de pe malul initial este mai mic decat numarul de capre dorit pentru a se gasi pe malul final")
            return 0
        if self.__class__.L < self.__class__.finalLupi:
            #print("Numarul de lupi de pe malul initial este mai mic decat numarul de lupi dorit pentru a se gasi pe malul final")
            return 0

        return 1

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

        '''verificam daca din input putem obtine outputul cerut'''
        self.true_input = self.verif_input()


        '''
        nodCurent.info va contine un tuplu (   0 ,   1  ,   2  ,   3  ,   4   ,    5  ,   6   ,    7     ,    8     ,     9    ) -> indicii
        nodCurent.info va contine un tuplu (v_est, c_est, l_est, barca, v_vest, c_vest, l_vest, v_magazie, c_magazie, l_magazie)
        informatia nodului de start: verze, capre, lupi (malul de est il initializam cu datele din input), malul pe care este barca (1 = est), 0, 0, 0 (animale pe malul de vest), 0, 0, 0 (animale in magazie)
        '''
        self.start = (self.__class__.V, self.__class__.C, self.__class__.L, 1, 0, 0, 0, 0, 0, 0)

    '''
    nodCurent este stare finala (scop) daca pe malul de vest avem cel putin nr cerut in input
    '''
    def testeaza_scop(self, nodCurent):
        if (nodCurent[4] + nodCurent[7] >= self.finalVerze) and (nodCurent[5] + nodCurent[8] >= self.finalCapre) and (
                nodCurent[6] + nodCurent[9] >= self.finalLupi):
            return 1
        return 0

    def calculeaza_h(self, infoNod, tip_euristica, nodCurent):
        if tip_euristica == "euristica banala":
            if self.testeaza_scop(infoNod):
                return 0
            return 1
        elif tip_euristica == "euristica 1":
            '''
            Pentru prima euristica calculez cati oameni mai am de mutat si impart la nr de locuri in barca
            '''

            if nodCurent == None:
                return 0

            return 2 * math.ceil(((self.finalVerze - (infoNod[4] + infoNod[7])) + (
                    self.finalCapre - (infoNod[5] + infoNod[8])) + (self.finalLupi - (infoNod[6] + infoNod[9]))) /
                                 (self.compA + self.compB)) + (1 - infoNod[3]) - 1
        elif tip_euristica == "euristica 2":
            '''
            Cu cat sunt mancate mai multe animale cu atat cresc sansele sa ajungem la un nod care nu mai indeplineste 
            conditia (avem mai putine elemente de un tip decat minimul care este cerut la final)
            '''

            final_h = 0

            if nodCurent == None:
                return 0

            final_h += (nodCurent.info[0] + nodCurent.info[4] + nodCurent.info[7]) - (infoNod[0] + infoNod[4]
                                                                                      + infoNod[7])
            final_h += (nodCurent.info[1] + nodCurent.info[5] + nodCurent.info[8]) - (
                    infoNod[1] + infoNod[5] + infoNod[8])
            final_h += (nodCurent.info[2] + nodCurent.info[6] + nodCurent.info[9]) - (
                    infoNod[2] + infoNod[6] + infoNod[9])
            return final_h
        else:
            '''
            Euristica neadmisibila
            Daca nu avem niciun animal in magazie ii scad sansele sa gaseasca o solutie valida
            (daca nu e niciun element "la adapost" pentru a nu fi mancat sau a nu manca alte elemente,
            atunci dupa ce "se mananaca" vom avea mai putine elemente si deci cresc sansele
            sa ramanem cu mai putine obiecte decat avem nevoie la final)
            In mod normal o astfel de varianta ar trebui sa fie dupa o varianta in care avem ceva in magazie,
            dar euristica neadmisibila ii va da prioritate mai mare variantei fara obiecte in magazie
            '''

            if infoNod[7] == 0 and infoNod[8] == 0 and infoNod[9] == 0:
                return 0
            else:
                return 1000

    '''functia de generare a succesorilor, facuta la laborator'''
    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):

        def get_costSucc(verzeA, capreA, lupiA, verzeB, capreB, lupiB, barca):
            costSuccesor = 0
            if verzeA == 0 and verzeB == 0 and capreA == 0 and capreB == 0 and lupiA == 0 and lupiB == 0 and barca == 1:
                return 50
            elif verzeA == 0 and verzeB == 0 and capreA == 0 and capreB == 0 and lupiA == 0 and lupiB == 0 and barca == 0:
                return 0

            if verzeA and verzeB and barca == 1:
                return 50 - verzeA + (verzeB / 2) * 1.5
            elif verzeA and verzeB and barca == 0:
                return 50 + verzeA + (verzeB / 2) * 1.5

            if capreA and capreB and barca == 1:
                return 50 - capreA * 2 + (capreB / 2) * 3
            elif capreA and capreB and barca == 0:
                return 50 + capreA * 2 + (capreB / 2) * 3

            if lupiA and lupiB and barca == 1:
                return 50 - lupiA * 3 + (lupiB / 2) * 4.5
            elif lupiA and lupiB and barca == 0:
                return 50 + lupiA * 3 + (lupiB / 2) * 4.5

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
                return 50 - costSuccesor
            else:
                return 50 + costSuccesor

        '''verific daca numarul curent de animale este suficient pentru a ajunge la numerele finale cerute in input'''
        def test_conditie(info):
            # print("-------- " + str(info[0]) + " " + str(info[1]) + " " + str(info[2]) + " " + str(info[4]) + " "
            # + str(info[5]) + " " + str(info[6]) + " " + str(info[7]) + " " + str(info[8]) + " " + str(info[9]))
            if info[0] < 0 or info[1] < 0 or info[2] < 0 or info[4] < 0 or info[5] < 0 or info[6] < 0:
                return 0

            if info[0] + info[4] + info[7] < Graph.finalVerze:
                return 0

            if info[1] + info[5] + info[8] < Graph.finalCapre:
                return 0

            if info[2] + info[6] + info[9] < Graph.finalLupi:
                return 0

            return 1

        '''calculez cate obiecte raman pe malul pe care nu este taranul'''
        def mancare(info, mal_nou_taran):
            # print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            # print("-------- " + str(info[0]) + " " + str(info[1]) + " " + str(info[2]) + " " + str(info[4]) + " "
            # + str(info[5]) + " " + str(info[6]) + " " + str(info[7])+ " " + str(info[8])+ " " + str(info[9])
            # + " ------- " + str(mal_nou_taran))
            if mal_nou_taran == 1:
                '''
                Taranul este pe malul de est deci calculam pt malul de vest:
                vMVN, cMVN, lMVN
                '''

                if info[4] - Graph.verzePerCapra * info[5] > 0:
                    vMVN = info[4] - Graph.verzePerCapra * info[5]
                else:
                    vMVN = 0

                if info[5] - Graph.caprePerLup * info[6] > 0:
                    cMVN = info[5] - Graph.caprePerLup * info[6]
                else:
                    cMVN = 0

                lMVN = info[6]

                if cMVN == 0 and info[6] > 0:
                    copy2 = info[6]
                    lup2 = 1
                    while lup2 < copy2:
                        copy2 -= Graph.lupiPerLup
                        lup2 += 1

                    lMVN = copy2
                # print(str(info[0]) + " " + str(info[1]) + " " + str(info[2]) + " " + str(vMVN) + " " + str(cMVN)
                # + " " + str(lMVN) + " " + str(info[7]) + " " + str(info[8]) + " " + str(info[9]))
                return (info[0], info[1], info[2], 1, vMVN, cMVN, lMVN, info[7], info[8], info[9])

            else:
                '''
                Taranul este pe malul de vest deci calculam pt malul de est:
                vMEN, cMEN, lMEN
                '''
                if info[0] - Graph.verzePerCapra * info[1] > 0:
                    vMEN = info[0] - Graph.verzePerCapra * info[1]
                else:
                    vMEN = 0

                if info[1] - Graph.caprePerLup * info[2] > 0:
                    cMEN = info[1] - Graph.caprePerLup * info[2]
                else:
                    cMEN = 0

                lMEN = info[2]
                if cMEN == 0 and info[2] > 0:
                    copy2 = info[6]
                    lup2 = 1
                    while lup2 < copy2:
                        copy2 -= Graph.lupiPerLup
                        lup2 += 1

                    lMEN = copy2
                # print(str(vMEN) + " " + str(cMEN) + " " + str(lMEN) + " " + str(info[4]) + " " + str(
                # info[5]) + " " + str(info[6]) + " " + str(info[7]) + " " + str(info[8]) + " " + str(info[9]))
                return (vMEN, cMEN, lMEN, 0, info[4], info[5], info[6], info[7], info[8], info[9])

        '''  
        Functie care genereaza combinatiile in functie de ce avem in magazie.
        Daca plecam de pe malul de est genereaza combinatiile pe care putem sa le punem in magazie.
        Daca plecam de pe malul de vest genereaza combinatiile de obiecte pe care le putem face pentru a avea in barca
        configuratia data ca parametrii.
        '''

        def genereaza_combinatii_magazie(verzeA, verzeB, capreA, capreB, lupiA, lupiB, nodCurent,
                                         tip_euristica="euristica banala"):
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

                maxVM = min(verzeA + verzeB + nodCurent.info[4], Graph.magazie)
                # print("vmvmvmv " + str(maxVM))
                for nr_v in range(maxVM + 1):
                    if nr_v == 0:
                        maxCM = min(capreA + capreB + nodCurent.info[5], Graph.magazie)
                    else:
                        maxCM = 0
                    # print("cmcmcmc " + str(maxCM))
                    for nr_c in range(maxCM + 1):
                        if nr_v == 0 and nr_c == 0:
                            maxLM = min(lupiA + lupiB + nodCurent.info[6], Graph.magazie)
                        else:
                            maxLM = 0

                        # print (" lmlmlm " + str(maxLM))
                        for nr_l in range(maxLM + 1):
                            # print("----")
                            # print(nr_l)
                            # print(nr_c)
                            # print(nr_v)
                            # print("----")
                            verzeMalVestNou = (nodCurent.info[4] + verzeA + verzeB + nodCurent.info[7]) - nr_v
                            capreMalVestNou = (nodCurent.info[5] + capreA + capreB + nodCurent.info[8]) - nr_c
                            lupiMalVestNou = (nodCurent.info[6] + lupiA + lupiB + nodCurent.info[9]) - nr_l

                            '''nodCurent.info va contine un tuplu (v_est, c_est, l_est, barca, v_vest, c_vest, l_vest, v_magazie, c_magazie, l_magazie)'''
                            info_inainte_de_mancare = (
                            verzeMEstNou, capreMEstNou, lupiMEstNou, 0, verzeMalVestNou, capreMalVestNou,
                            lupiMalVestNou, nr_v, nr_c, nr_l)

                            # print("--------")
                            # print(info_inainte_de_mancare)
                            # infoNodNou = (verzeMEstNou, capreMEstNou, lupiMEstNou, 0, verzeMalVestNou, capreMalVestNou, lupiMalVestNou, nr_v, nr_c, nr_l)
                            infoNodNou = mancare(info_inainte_de_mancare, 0)

                            # print(infoNodNou)
                            if not test_conditie(infoNodNou):
                                continue

                            costSuccesor = get_costSucc(verzeA, capreA, lupiA, verzeB, capreB, lupiB, nodCurent.info[3])
                            # print(infoNodNou)
                            listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, cost=nodCurent.g + costSuccesor,
                                                                h=NodParcurgere.gr.calculeaza_h(infoNodNou,
                                                                                                tip_euristica,
                                                                                                nodCurent)))

            else:
                verzeMEstNou = nodCurent.info[0] + (verzeA + verzeB)
                capreMEstNou = nodCurent.info[1] + (capreA + capreB)
                lupiMEstNou = nodCurent.info[2] + (lupiA + lupiB)

                if nodCurent.info[7] > 0:
                    maxVM = min(nodCurent.info[7], verzeA + verzeB)
                    if nodCurent.info[4] - (verzeA + verzeB) < 0:
                        minVM = verzeA + verzeB - nodCurent.info[4]
                    else:
                        minVM = 0
                else:
                    maxVM = 0
                    minVM = 0

                for nr_v in range(minVM, maxVM + 1):
                    if nodCurent.info[8] > 0:
                        maxCM = min(nodCurent.info[8], capreA + capreB)
                        if nodCurent.info[5] - (capreA + capreB) < 0:
                            minCM = capreA + capreB - nodCurent.info[5]
                        else:
                            minCM = 0
                    else:
                        maxCM = 0
                        minCM = 0

                    for nr_c in range(minCM, maxCM + 1):
                        if nodCurent.info[9] > 0:
                            maxLM = min(nodCurent.info[9], lupiA + lupiB)
                            if nodCurent.info[6] - (lupiA + lupiB) < 0:
                                minLM = lupiA + lupiB - nodCurent.info[6]
                            else:
                                minLM = 0
                        else:
                            maxLM = 0
                            minLM = 0

                        for nr_l in range(minLM, maxLM + 1):
                            verzeMalVestNou = nodCurent.info[4] - (verzeA + verzeB - nr_v)
                            capreMalVestNou = nodCurent.info[5] - (capreA + capreB - nr_c)
                            lupiMalVestNou = nodCurent.info[6] - (lupiA + lupiB - nr_l)

                            info_inainte_de_mancare = (
                            verzeMEstNou, capreMEstNou, lupiMEstNou, 1, verzeMalVestNou, capreMalVestNou,
                            lupiMalVestNou, nodCurent.info[7] - nr_v, nodCurent.info[8] - nr_c,
                            nodCurent.info[9] - nr_l)
                            # print("--------")
                            # print(info_inainte_de_mancare)
                            # infoNodNou = (verzeMEstNou, capreMEstNou, lupiMEstNou, 1, verzeMalVestNou, capreMalVestNou, lupiMalVestNou, nodCurent.info[7] - nr_v, nodCurent.info[8] - nr_c,nodCurent.info[9] - nr_l)
                            infoNodNou = mancare(info_inainte_de_mancare, 1)

                            # print(infoNodNou)
                            if not test_conditie(infoNodNou):
                                continue

                            costSuccesor = get_costSucc(verzeA, capreA, lupiA, verzeB, capreB, lupiB, nodCurent.info[3])
                            # print(infoNodNou)
                            listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, cost=nodCurent.g + costSuccesor,
                                                                h=NodParcurgere.gr.calculeaza_h(infoNodNou,
                                                                                                tip_euristica,
                                                                                                nodCurent)))

        '''
        Functia "principala" de generare a succesorilor care face toate combinatiile de obiecte pe care le putem pune in barca.
        Dupa ce se calculeaza o astfel de configuratie se apeleaza functia cu care obtinem si combinatiile in functie de magazie.
        '''
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
        # print(maxVerzeBarca)
        for v in range(maxVerzeBarca + 1):
            # print(v)
            if v == 0:
                maxCapreBarca = min(capreMalCurent, Graph.compA + Graph.compB)
            elif v >= Graph.compA and v >= Graph.compB:
                maxCapreBarca = 0
            else:
                if v <= Graph.compA:
                    maxCapreBarca = min(capreMalCurent, Graph.compB)
                else:
                    maxCapreBarca = min(capreMalCurent, Graph.compA)

            for c in range(maxCapreBarca + 1):
                if v == 0 and c == 0:
                    maxLupiBarca = min(lupiMalCurent, Graph.compA + Graph.compB)
                elif (v > 0 and c > 0) or (v >= Graph.compA and v >= Graph.compB) or (
                        c >= Graph.compA and c >= Graph.compB):
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

                for l in range(maxLupiBarca + 1):
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

                    # print(listaSuccesori)

        # print(nodCurent.info)
        # print(listaSuccesori)
        return listaSuccesori


def a_star(gr, nrSolutiiCautate, tip_euristica, f):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica, None))]

    #verif = 0
    while len(c) > 0:
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        if milis >= int(sys.argv[3]):
            f.write("Gasirea solutiei depaseste timeout-ul")
            break
        nodCurent = c.pop(0)
        '''
        print("aaa")
        print(nodCurent.info)
        print("aaa")
        print(gr.testeaza_scop(nodCurent.info))
        print("aaa")
        '''
        if gr.testeaza_scop(nodCurent.info):
            f.write("Solutie: ")
            nodCurent.afisDrum(afisCost=True, f=f)
            t2 = time.time()
            milis = round(1000 * (t2 - t1))
            f.write(str(milis))
            f.write("\n----------------\n")
            # input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        '''
        print("bbb")
        print(lSuccesori)
        print("bbb")
        '''
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
        # print(c)
        '''
        if verif < 50:
            verif += 1
        else:
            break
        '''


def uniform_cost(gr, nrSolutiiCautate, f):
    c = [NodParcurgere(gr.start, None, 0)]

    while len(c) > 0:
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        if milis >= int(sys.argv[3]):
            f.write("Gasirea solutiei depaseste timeout-ul")
            break
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent.info):
            f.write("Solutie: ")
            nodCurent.afisDrum(afisCost=True, f=f)
            t2 = time.time()
            milis = round(1000 * (t2 - t1))
            f.write(str(milis))
            f.write("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici ??i ??n desenele de pe site)
                if c[i].g > s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star_opt(gr, tip_euristica, f):
    l_open = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica, None))]

    l_closed = []
    while len(l_open) > 0:
        # print("Coada actuala: " + str(l_open))
        # input()
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        if milis >= int(sys.argv[3]):
            f.write("Gasirea solutiei depaseste timeout-ul")
            break

        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent.info):
            f.write("Solutie: ")
            nodCurent.afisDrum(afisCost=True, f=f)
            t2 = time.time()
            milis = round(1000 * (t2 - t1))
            f.write(str(milis))
            f.write("\n----------------\n")
            return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        if s in lSuccesori:
                            lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        l_open.remove(nodC)
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            if s in lSuccesori:
                                lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            l_closed.remove(nodC)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(l_open)):
                # diferenta fata de UCS e ca ordonez crescator dupa f
                # daca f-urile sunt egale ordonez descrescator dupa g
                if l_open[i].f > s.f or (l_open[i].f == s.f and l_open[i].g <= s.g):
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i, s)
            else:
                l_open.append(s)


def dfi(gr, nodCurent, adancime, nrSolutiiCautate, f):
    # print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    # input()
    if adancime == 1 and gr.testeaza_scop(nodCurent.info):
        f.write("Solutie: ")
        nodCurent.afisDrum(afisCost=True, f=f)
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        f.write(str(milis))
        f.write("\n----------------\n")
        # input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                nrSolutiiCautate = dfi(gr, sc, adancime - 1, nrSolutiiCautate, f)
    return nrSolutiiCautate


def depth_first_iterativ(gr, nrSolutiiCautate, tip_euristica, f):
    for i in range(1, 101):
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        if milis >= int(sys.argv[3]):
            f.write("Gasirea solutiei depaseste timeout-ul")
            break
        if nrSolutiiCautate == 0:
            return
        nrSolutiiCautate = dfi(gr, NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica, None)), i,
                               nrSolutiiCautate, f)



gr = Graph("/Users/roxana/PycharmProjects/tema_ai_proiect1/inputs/input_1.txt")
#verificam daca starea initiala este stare finala
if gr.testeaza_scop(gr.start):
    output_ucs_1.write("Starea initiala este si stare finala")
    output_a_star_1.write("Starea initiala este si stare finala")
    output_a_star_opt_1.write("Starea initiala este si stare finala")
    output_ida_star_1.write("Starea initiala este si stare finala")
elif gr.true_input:
    #verificam daca din configuratia initiala este posibil sa ajungem in cea finala
    NodParcurgere.gr = gr
    nrSolutiiCautate = int(sys.argv[1])


    print("UCS")
    t1 = time.time()
    uniform_cost(gr, nrSolutiiCautate=nrSolutiiCautate, f=output_ucs_1)
    

    print("A STAR")
    t1 = time.time()
    a_star(gr, nrSolutiiCautate=nrSolutiiCautate, tip_euristica=str(sys.argv[2]), f=output_a_star_1)


    print("A STAR OPT")
    t1 = time.time()
    a_star_opt(gr, tip_euristica=str(sys.argv[2]), f=output_a_star_opt_1)


    print("IDA STAR")
    t1 = time.time()
    depth_first_iterativ(gr, nrSolutiiCautate, "euristica banala", f=output_ida_star_1)
else:
    output_ucs_1.write("Nu se poate ajunge din starea initiala in cea finala")
    output_a_star_1.write("Nu se poate ajunge din starea initiala in cea finala")
    output_a_star_opt_1.write("Nu se poate ajunge din starea initiala in cea finala")
    output_ida_star_1.write("Nu se poate ajunge din starea initiala in cea finala")




gr2 = Graph("/Users/roxana/PycharmProjects/tema_ai_proiect1/inputs/input_2.txt")
#verificam daca starea initiala este stare finala
if gr2.testeaza_scop(gr2.start):
    output_ucs_2.write("Starea initiala este si stare finala")
    output_a_star_2.write("Starea initiala este si stare finala")
    output_a_star_opt_2.write("Starea initiala este si stare finala")
    output_ida_star_2.write("Starea initiala este si stare finala")
elif gr2.true_input:
    #verificam daca din configuratia initiala este posibil sa ajungem in cea finala
    NodParcurgere.gr = gr2
    nrSolutiiCautate = int(sys.argv[1])

    print("UCS")
    t1 = time.time()
    uniform_cost(gr2, nrSolutiiCautate=nrSolutiiCautate, f=output_ucs_2)

    print("A STAR")
    t1 = time.time()
    a_star(gr2, nrSolutiiCautate=nrSolutiiCautate, tip_euristica=str(sys.argv[2]), f=output_a_star_2)

    print("A STAR OPT")
    t1 = time.time()
    a_star_opt(gr2, tip_euristica=str(sys.argv[2]), f=output_a_star_opt_2)

    print("IDA STAR")
    t1 = time.time()
    depth_first_iterativ(gr2, nrSolutiiCautate, "euristica banala", f=output_ida_star_2)
else:
    output_ucs_2.write("Nu se poate ajunge din starea initiala in cea finala")
    output_a_star_2.write("Nu se poate ajunge din starea initiala in cea finala")
    output_a_star_opt_2.write("Nu se poate ajunge din starea initiala in cea finala")
    output_ida_star_2.write("Nu se poate ajunge din starea initiala in cea finala")



gr3 = Graph("/Users/roxana/PycharmProjects/tema_ai_proiect1/inputs/input_3.txt")
#verificam daca starea initiala este stare finala
if gr3.testeaza_scop(gr3.start):
    output_ucs_3.write("Starea initiala este si stare finala")
    output_a_star_3.write("Starea initiala este si stare finala")
    output_a_star_opt_3.write("Starea initiala este si stare finala")
    output_ida_star_3.write("Starea initiala este si stare finala")
elif gr3.true_input:
    #verificam daca din configuratia initiala este posibil sa ajungem in cea finala
    NodParcurgere.gr = gr3
    nrSolutiiCautate = int(sys.argv[1])

    print("UCS")
    t1 = time.time()
    uniform_cost(gr3, nrSolutiiCautate=nrSolutiiCautate, f=output_ucs_3)

    print("A STAR")
    t1 = time.time()
    a_star(gr3, nrSolutiiCautate=nrSolutiiCautate, tip_euristica=str(sys.argv[2]), f=output_a_star_3)

    print("A STAR OPT")
    t1 = time.time()
    a_star_opt(gr3, tip_euristica=str(sys.argv[2]), f=output_a_star_opt_3)

    print("IDA STAR")
    t1 = time.time()
    depth_first_iterativ(gr3, nrSolutiiCautate, "euristica banala", f=output_ida_star_3)
else:
    output_ucs_3.write("Nu se poate ajunge din starea initiala in cea finala")
    output_a_star_3.write("Nu se poate ajunge din starea initiala in cea finala")
    output_a_star_opt_3.write("Nu se poate ajunge din starea initiala in cea finala")
    output_ida_star_3.write("Nu se poate ajunge din starea initiala in cea finala")



gr4 = Graph("/Users/roxana/PycharmProjects/tema_ai_proiect1/inputs/input_4.txt")
#verificam daca starea initiala este stare finala
if gr4.testeaza_scop(gr4.start):
    output_ucs_4.write("Starea initiala este si stare finala")
    output_a_star_4.write("Starea initiala este si stare finala")
    output_a_star_opt_4.write("Starea initiala este si stare finala")
    output_ida_star_4.write("Starea initiala este si stare finala")
elif gr4.true_input:
    #verificam daca din configuratia initiala este posibil sa ajungem in cea finala
    NodParcurgere.gr = gr4
    nrSolutiiCautate = int(sys.argv[1])

    print("UCS")
    t1 = time.time()
    uniform_cost(gr4, nrSolutiiCautate=nrSolutiiCautate, f=output_ucs_4)

    print("A STAR")
    t1 = time.time()
    a_star(gr4, nrSolutiiCautate=nrSolutiiCautate, tip_euristica=str(sys.argv[2]), f=output_a_star_4)

    print("A STAR OPT")
    t1 = time.time()
    a_star_opt(gr4, tip_euristica=str(sys.argv[2]), f=output_a_star_opt_4)

    print("IDA STAR")
    t1 = time.time()
    depth_first_iterativ(gr4, nrSolutiiCautate, "euristica banala", f=output_ida_star_4)
else:
    output_ucs_4.write("Nu se poate ajunge din starea initiala in cea finala")
    output_a_star_4.write("Nu se poate ajunge din starea initiala in cea finala")
    output_a_star_opt_4.write("Nu se poate ajunge din starea initiala in cea finala")
    output_ida_star_4.write("Nu se poate ajunge din starea initiala in cea finala")


# gr.genereazaSuccesori(NodParcurgere((15, 1, 2, 0, 0, 7, 0, 0, 0, 0), None, 0, 0), tip_euristica="euristica banala")
# print(gr.testeaza_scop(((17, 6, 2, 1, 3, 4, 1, 0, 0, 0))))
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

output_ucs_1.close()
output_ucs_2.close()
output_ucs_3.close()
output_ucs_4.close()

output_a_star_opt_1.close()
output_a_star_opt_2.close()
output_a_star_opt_3.close()
output_a_star_opt_4.close()

output_a_star_1.close()
output_a_star_2.close()
output_a_star_3.close()
output_a_star_4.close()

output_ida_star_1.close()
output_ida_star_2.close()
output_ida_star_3.close()
output_ida_star_4.close()
