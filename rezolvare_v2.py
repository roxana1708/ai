import copy
import time

import pygame
import sys

import statistics
# adancimea pt incepator, se schimba in functie de inputul utilizatorului
ADANCIME_MAX = 2



def margine(x):
    if x == 0 or x == 6:
        return True

    return False

# verificam daca mai avem "patratele" libere
def full_board(lista, jucator):
    for i in lista:
        if i == Joc.GOL:
            return False

    return jucator

# verificam daca dreptunghiul selectat nu acopera patratele deja ocupate
def verif_liber(lista, l_st, c_st, l_dr, c_dr):
    # verificam daca dreptunghiul selectat este ocupat sau nu
    for i in range(l_st, l_dr+1):
        for j in range(c_st, c_dr+1):
            if lista[i*7 + j] != '#':
                return False
    return True

def verif_conectate(lista, l_st, c_st, l_dr, c_dr, jucator):
    for i in range(l_st, l_dr + 1):
        for j in range(c_st, c_dr + 1):
            if i-1 >= 0:
                if lista[(i-1)*7+j] == jucator:
                    return True
            if i+1 <= 6:
                if lista[(i+1)*7+j] == jucator:
                    return True
            if j-1 >= 0:
                if lista[i*7+(j-1)] == jucator:
                    return True
            if j+1 <= 6:
                if lista[i*7+(j+1)] == jucator:
                    return True
    return False

#print(verif_conectate(['x', 'x','x','x','*', '#', '#', '#', '*', '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','x', 'x', 'x','x','#','#','*','x','x','x','x','0','0','0','x','x','x','x',], 4, 0, 5, 1, '0'))

# verificam conditia ca dupa o mutare restul patratelelor libere sa fie conectate
# un fel de dfs
def connected(lista):
    directions = [1, -1, -7, 7]
    to_visit = []
    for i in range(len(lista)):
        if lista[i] == '#':
            to_visit.append(i)
            #print(i)
            break
    visited = []
    nr = 0

    if len(to_visit) == 0:
        return True

    while len(to_visit) > 0:
        current = to_visit.pop(0)
        #print(current)

        if current in visited:
            continue

        for direction in directions:
            new_position = current + direction
            if (current % 7 == 6 and new_position % 7 == 0) or (new_position % 7 == 6 and current % 7 == 0):
                continue
            elif len(lista) > new_position >= 0 and lista[new_position] == '#' and new_position not in visited:
                #print(str(current) + " " + str(new_position))
                to_visit.append(new_position)

        visited.append(current)
        nr += 1


    #print(lista.count('#'))
    #print(nr)

    if lista.count('#') == nr:
        return True
    else:
        return False



class Joc:
    NR_COLOANE = 7
    JMIN = None
    JMAX = None
    GOL = '#' #patratica libera
    OTR = '*' #patratica otravita

    @classmethod
    def initializeaza(cls, display, NR_COLOANE = 7, dim_celula = 100):
        # pentru interfata grafica
        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load('ics.png')
        cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula, dim_celula))
        cls.zero_img = pygame.image.load('zero.png')
        cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula, dim_celula))
        cls.otrava_img = pygame.image.load('otrava.png')
        cls.otrava_img = pygame.transform.scale(cls.otrava_img, (dim_celula, dim_celula))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        for linie in range(NR_COLOANE):
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid.append(patr)

    def deseneaza_grid(self, marcaj=None):
        # pentru interfata grafica
        for ind in range(len(self.matr)):
            linie = ind // 7
            coloana = ind % 7

            if marcaj == ind:
                culoare = (255, 0, 0)
            else:
                # altfel o desenez cu alb
                culoare = (255, 255, 255)
            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])
            if self.matr[ind] == '*':
                self.__class__.display.blit(self.__class__.otrava_img, (
                coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[ind] == 'x':
                self.__class__.display.blit(self.__class__.x_img, (
                coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[ind] == '0':
                self.__class__.display.blit(self.__class__.zero_img, (
                coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))

        #  pentru a actualiza interfata
        pygame.display.flip()

    def __init__(self, tabla=None):  # Joc()
        self.matr = tabla or [Joc.GOL] * self.NR_COLOANE ** 2
        # patratelele otravite sunt aceleasi
        self.matr[4] = '*'
        self.matr[8] = '*'
        self.matr[26] = '*'
        self.matr[37] = '*'


    @classmethod
    def jucator_opus(cls, jucator):
        # schimbam jucatorul cand celalalt a terminat de mutat
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN


    def final(self, jucator):
        # jocul nu se termina pana cand tabla nu este acoperita complet (inafara de patratelele otravite)
        rez = full_board(self.matr, self.jucator_opus(jucator))

        if rez:
            return rez
        else:
            return False


    def mutari(self, jucator):
        # generare mutari pentru vaarianta generalizata
        # functia ia fiecare patratica libera si formeaza toate dreptunghiurile pentru care aceasta poate reprezenta coltul stanga sus
        l_mutari = []

        #if self.matr.count(Joc.JMAX) == 0:

        for i in range(len(self.matr)):
            min_linie_colt_dr_jos = i / 7
            min_coloana_colt_dr_jos = i % 7

            #print(self.matr)

            for linie in range(int(min_linie_colt_dr_jos), 7):
                for coloana in range(min_coloana_colt_dr_jos, 7):
                    copie_matr = copy.deepcopy(self.matr)
                    #print(str(int(i / 7)) + " " + str(i % 7) + " " + str(linie) + " " + str(coloana))

                    if self.matr.count(jucator) == 0:
                        if (margine(int(i/7)) or margine(i%7) or margine(linie) or margine(coloana)) \
                                and verif_liber(copie_matr, int(i/7), i%7, linie, coloana):
                            # print("here libera")
                            # print(str(int(i/7)) + " " + str(i%7) + " " + str(linie) + " " + str(coloana))
                            # print(copie_matr)
                            # print(copie_matr)
                            for x in range(int(i / 7), linie + 1):
                                for y in range(i % 7, coloana + 1):
                                    copie_matr[x * 7 + y] = jucator
                            # print(copie_matr)

                            # verificam daca mutarea este valida (adica daca patratelele ramase libere sunt conectate
                            if connected(copie_matr):
                                # print("here valida")
                                l_mutari.append(Joc(copie_matr))
                    else:
                        if ((margine(int(i/7)) or margine(i%7) or margine(linie) or margine(coloana)) or verif_conectate(copie_matr, int(i/7), i%7, linie, coloana, jucator)) and verif_liber(copie_matr, int(i/7), i%7, linie, coloana):
                            #print("here libera")
                            #print(str(int(i/7)) + " " + str(i%7) + " " + str(linie) + " " + str(coloana))
                            #print(copie_matr)
                            #print(copie_matr)
                            for x in range(int(i/7), linie+1):
                                for y in range(i%7, coloana+1):
                                    copie_matr[x*7+y] = jucator
                            #print(copie_matr)

                            # verificam daca mutarea este valida (adica daca patratelele ramase libere sunt conectate
                            if connected(copie_matr):
                                #print("here valida")
                                l_mutari.append(Joc(copie_matr))
        #print(l_mutari)
        return l_mutari


    # estimare scor in functie de numarul de patratele libere
    def estimeaza_scor(self, adancime, j_curent):
        t_final = self.final(j_curent)
        # daca suntem intr-o stare finala intoarcem o valoare in functie de jucatorul castigator
        if t_final == self.__class__.JMAX:
            return 99 + adancime
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        # altfel ne uitam sa vedem cate patratele mai putem acoperi
        elif j_curent == self.__class__.JMAX:
            return self.matr.count(Joc.GOL)
        else:
            return -self.matr.count(Joc.GOL)

    # estimare scor in functie de numarul de patratele ocupate
    def estimeaza_scor_2(self, adancime, j_curent):
        t_final = self.final(j_curent)
        # daca suntem intr-o stare finala intoarcem o valoare in functie de jucatorul castigator
        if t_final == self.__class__.JMAX:
            return 99 + adancime
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        # altfel ne uitam sa vedem cate patratele am reusit sa ocupam
        # cu cat mai multe patratele acoperite de calculator cu atat mai putine sanse are utilizatorul sa ocupe si astfel sa ramana fara mutari
        elif j_curent == self.__class__.JMAX:
            return self.matr.count(self.__class__.JMAX)
        else:
            return -self.matr.count(self.__class__.JMIN)

    # estimare scor in functie de paritatea patratelelor ramase
    def estimeaza_scor_3(self, j_curent):
        t_final = self.final(j_curent)
        # daca suntem intr-o stare finala intoarcem o valoare in functie de jucatorul castigator
        if t_final == self.__class__.JMAX:
            return 99
        elif t_final == self.__class__.JMIN:
            return -99
        else:
            if j_curent == 'x':
                if self.matr.count('#') % 2 == 0:
                    return -self.matr.count('#')
                else:
                    return self.matr.count('#')
            else:
                if self.matr.count('#') % 2 == 0:
                    return self.matr.count('#')
                else:
                    return -self.matr.count('#')





    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.NR_COLOANE)]) + "\n"
        sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
        for i in range(self.NR_COLOANE):
            sir += str(i) + " |" + " ".join(
                [str(x) for x in self.matr[self.NR_COLOANE * i: self.NR_COLOANE * (i + 1)]]) + "\n"
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    O instanta din clasa stare este un nod din arborele minimax
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    # TO DO 2
    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        self.adancime = adancime
        self.estimare = estimare
        self.mutari_posibile = []
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        #print(l_mutari)
        juc_opus = Joc.jucator_opus(self.j_curent)

        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir



def min_max(stare):
    # daca suntem la o frunza in arborele minimax sau la o stare finala
    #print("cccc")
    #print(stare.tabla_joc.final)
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()
    #print(stare.mutari_posibile)

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(x) for x in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)

    stare.estimare = stare.stare_aleasa.estimare

    return stare



def alpha_beta(alpha, beta, stare, nr_noduri):
    #print(nr_noduri)
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.estimare = stare.tabla_joc.estimeaza_scor_3(stare.j_curent) #stare.adancime
        return stare, nr_noduri

    if alpha > beta:
        return stare, nr_noduri

    stare.mutari_posibile = stare.mutari()
    if len(stare.mutari_posibile) == 0:
        print(stare.tabla_joc)

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            nr_noduri += 1
            stare_noua, nr_noduri = alpha_beta(alpha, beta, mutare, nr_noduri)

            if estimare_curenta < stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:
            nr_noduri += 1
            stare_noua, nr_noduri = alpha_beta(alpha, beta, mutare, nr_noduri)

            if estimare_curenta > stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    if stare.stare_aleasa == None:
        print("A castigat ", Joc.JMIN)
    else:
        stare.estimare = stare.stare_aleasa.estimare
        return stare, nr_noduri


class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0,culoareFundal=(53,80,115), culoareFundalSel=(89,134,194), text="", font="arial", fontDimensiune=16, culoareText=(255,255,255), valoare=""):
        self.display=display
        self.culoareFundal=culoareFundal
        self.culoareFundalSel=culoareFundalSel
        self.text=text
        self.font=font
        self.w=w
        self.h=h
        self.selectat=False
        self.fontDimensiune=fontDimensiune
        self.culoareText=culoareText

        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat=fontObj.render(self.text, True , self.culoareText)
        self.dreptunghi=pygame.Rect(left, top, w, h)

        self.dreptunghiText=self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare=valoare

    def selecteaza(self,sel):
        self.selectat=sel
        self.deseneaza()
    def selecteazaDupacoord(self,coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left=self.left
        self.dreptunghi.top=self.top
        self.dreptunghiText=self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF= self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat ,self.dreptunghiText)

class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10,left=0, top=0):
        self.listaButoane=listaButoane
        self.indiceSelectat=indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat=True
        self.top=top
        self.left=left
        leftCurent=self.left
        for b in self.listaButoane:
            b.top=self.top
            b.left=leftCurent
            b.updateDreptunghi()
            leftCurent+=(spatiuButoane+b.w)

    def selecteazaDupacoord(self,coord):
        for ib,b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat=ib
                return True
        return False

    def deseneaza(self):
        #atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
            ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="x", valoare="x"),
            Buton(display=display, w=35, h=30, text="zero", valoare="0")
            ],
        indiceSelectat=0)
    btn_nivel = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="incepator", valoare="2"),
            Buton(display=display, w=80, h=30, text="mediu", valoare="3"),
            Buton(display=display, w=80, h=30, text="avansat", valoare="4")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=270, left=30, w=40, h=30, text="ok", culoareFundal=(155,0,55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_nivel.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_nivel.selecteazaDupacoord(pos):
                            if ok.selecteazaDupacoord(pos):
                                display.fill((0,0,0)) #stergere ecran
                                tabla_curenta.deseneaza_grid()
                                return btn_juc.getValoare(), btn_alg.getValoare(), int(btn_nivel.getValoare())
        pygame.display.update()


def afis_daca_final(stare_curenta, nr_mutari_calculator, nr_mutari_jucator, timpi, noduri):
    final = stare_curenta.tabla_joc.final(stare_curenta.j_curent)
    # nu avem varianta de remiza deci vedem care este castigatorul
    if (final):
        if final == 'x':
            print("A castigat 0")
        else:
            print("A castigat x")

        print("Numarul de mutari ale utilizatorului: ", nr_mutari_jucator)
        print("Numarul de mutari ale calculatorului: ", nr_mutari_calculator)
        print("Timpul minim: ", min(timpi))
        print("Timpul maxim: ", max(timpi))
        print("Timpul mediu: ", round(sum(timpi)/len(timpi), 2))
        print("Mediana: ", statistics.median(timpi))

        print("Numar minim de noduri: ", min(noduri[:len(noduri)-1]))
        print("Numar maxim de noduri: ", max(noduri))
        print("Numar mediu de noduri: ", round(sum(noduri) / len(noduri), 2))
        print("Mediana nodurilor: ", statistics.median(noduri))

        return True
    return False



def main():
    '''
    # initializare algoritm
    raspuns_valid = False

    # utilizatorul alege algoritmul dorit
    while not raspuns_valid:
        tip_algoritm = input("Algoritmul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # utilizatorul alege simbolul cu care vrea sa joace
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu x sau cu 0?\n ").lower()
        if (Joc.JMIN in ['x', '0']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")


    # utilizatorul alege nivelul de experienta pe care il are
    raspuns_valid = False
    while not raspuns_valid:
        adancime = input("Nivelul dvs? (raspundeti cu 1, 2 sau 3)\n 1.Incepator\n 2.Mediu\n 3.Avansat\n")
        if adancime in ['1', '2', '3']:
            raspuns_valid = True
            ADANCIME_MAX = int(adancime) + 1
        else:
            print("Nu ati ales o varianta corecta.")

    '''
    nr_mutari_jucator = 0
    nr_mutari_calculator = 0

    timpi_calculator = []
    noduri_calculator = []

    pygame.init()
    pygame.display.set_caption('Gherghina Roxana - Chomp!')

    ecran = pygame.display.set_mode(size=(706, 706))
    Joc.initializeaza(ecran)



    # initializam tabla
    tabla_curenta = Joc()
    Joc.JMIN, tip_algoritm, ADANCIME_MAX = deseneaza_alegeri(ecran, tabla_curenta)

    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    print(Joc.JMIN)
    print(tip_algoritm)
    print(ADANCIME_MAX)
    print("Tabla initiala")
    print(str(tabla_curenta))

    # starea initiala
    stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX)
    print(stare_curenta)
    #print("llll")



    tabla_curenta.deseneaza_grid()

    # utilizatorul trebuie sa selecteze doua patratele (coltul stanga sus si coltul dreapta jos)
    # care determina dreptunghiul pe care vrea sa-l selecteze
    # astfel trebuie sa retinem doua miscari consecutive ale utilizatorului
    first_click = True
    first_move_jucator = True

    if Joc.JMIN == 'x':
        print("Acum muta utilizatorul cu simbolul ", Joc.JMIN)
        t_inainte = int(round(time.time() * 1000))

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul utilizator

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if first_click:
                        # a ales coltul stanga sus, retinem pozitia acestuia
                        print("click1")
                        pos = pygame.mouse.get_pos()

                        for np in range(len(Joc.celuleGrid)):
                            if Joc.celuleGrid[np].collidepoint(pos):
                                linie_st = np // 7
                                coloana_st = np % 7

                        first_click = False

                    else:
                        # a ales si coltul dreapta jos, retinem pozitia acestuia
                        print("click2")
                        pos2 = pygame.mouse.get_pos()
                        for np in range(len(Joc.celuleGrid)):

                            if Joc.celuleGrid[np].collidepoint(pos2):
                                linie_dr = np // 7
                                coloana_dr = np % 7


                        # stim pozitiile ambelor colturi
                        # verificam daca dreptunghiul selectat este liber si indeplineste conditia de mutare valida
                        if (linie_st in range(Joc.NR_COLOANE) and coloana_st in range(
                                Joc.NR_COLOANE) and linie_dr in range(Joc.NR_COLOANE) and coloana_dr in range(
                                Joc.NR_COLOANE)):
                            if first_move_jucator:
                                if (margine(linie_st) or margine(linie_dr) or margine(coloana_st) or margine(coloana_dr)) and verif_liber(stare_curenta.tabla_joc.matr, linie_st, coloana_st, linie_dr, coloana_dr):
                                    copie = copy.deepcopy(stare_curenta.tabla_joc.matr)
                                    for i in range(linie_st, linie_dr + 1):
                                        for j in range(coloana_st, coloana_dr + 1):
                                            copie[i * 7 + j] = Joc.JMIN

                                    if connected(copie):
                                        for i in range(linie_st, linie_dr + 1):
                                            for j in range(coloana_st, coloana_dr + 1):
                                                # stare_curenta.tabla_joc.matr[i * 7 + j] = Joc.JMIN

                                                if stare_curenta.tabla_joc.matr[i * 7 + j] == Joc.JMIN:
                                                    stare_curenta.tabla_joc.deseneaza_grid(i * 7 + j)
                                                if stare_curenta.tabla_joc.matr[i * 7 + j] == Joc.GOL:
                                                    stare_curenta.tabla_joc.matr[i * 7 + j] = Joc.JMIN

                                        # afisam tabla de joc in urma mutarii utilizatorului
                                        print("\nTabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))

                                        stare_curenta.tabla_joc.deseneaza_grid()
                                        # verificam daca starea curenta este finala
                                        if (afis_daca_final(stare_curenta, nr_mutari_calculator, nr_mutari_jucator+1, timpi_calculator, noduri_calculator)):
                                            break

                                        # am facut o mutare, este randul celuilalt jucator
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

                                    first_move_jucator = False

                                first_click = True

                            elif ((margine(linie_st) or margine(linie_dr) or margine(coloana_st) or margine(coloana_dr)) or verif_conectate(stare_curenta.tabla_joc.matr, linie_st, coloana_st, linie_dr, coloana_dr, stare_curenta.j_curent)) and verif_liber(stare_curenta.tabla_joc.matr, linie_st, coloana_st, linie_dr, coloana_dr):
                                # facem o copie pentru a nu altera momentan tabla de joc
                                copie = copy.deepcopy(stare_curenta.tabla_joc.matr)
                                for i in range(linie_st, linie_dr + 1):
                                    for j in range(coloana_st, coloana_dr + 1):
                                        copie[i * 7 + j] = Joc.JMIN

                                if connected(copie):
                                    for i in range(linie_st, linie_dr + 1):
                                        for j in range(coloana_st, coloana_dr + 1):
                                            #stare_curenta.tabla_joc.matr[i * 7 + j] = Joc.JMIN

                                            if stare_curenta.tabla_joc.matr[i*7+j] == Joc.JMIN:
                                                stare_curenta.tabla_joc.deseneaza_grid(i*7+j)
                                            if stare_curenta.tabla_joc.matr[i*7+j] == Joc.GOL:
                                                stare_curenta.tabla_joc.matr[i * 7 + j] = Joc.JMIN

                                    # afisam tabla de joc in urma mutarii utilizatorului
                                    print("\nTabla dupa mutarea jucatorului")
                                    print(str(stare_curenta))

                                    stare_curenta.tabla_joc.deseneaza_grid()
                                    # verificam daca starea curenta este finala
                                    if (afis_daca_final(stare_curenta, nr_mutari_calculator, nr_mutari_jucator+1, timpi_calculator, noduri_calculator)):
                                        break

                                    # am facut o mutare, este randul celuilalt jucator
                                    stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

                                first_click = True

                            t_dupa = int(round(time.time() * 1000))
                            print("Utilizatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
                            nr_mutari_jucator += 1
                            first_click = True



            '''
                       COD PENTRU AFISARE DOAR IN CONSOLA
                        print("Acum muta utilizatorul cu simbolul", stare_curenta.j_curent)
                        raspuns_valid = False
                        while not raspuns_valid:
                            try:
                                linie_st = int(input("linie capat stanga sus="))
                                coloana_st = int(input("coloana capat stanga sus="))
            
                                linie_dr = int(input("linie capat stanga sus="))
                                coloana_dr = int(input("coloana capat stanga sus="))
            
                                if (linie_st in range(Joc.NR_COLOANE) and coloana_st in range(Joc.NR_COLOANE) and linie_dr in range(Joc.NR_COLOANE) and coloana_dr in range(Joc.NR_COLOANE)):
                                    if verif_liber(stare_curenta.tabla_joc.matr, linie_st, coloana_st, linie_dr, coloana_dr):#stare_curenta.tabla_joc.matr[linie_st * Joc.NR_COLOANE + coloana_st] == Joc.GOL:
                                        copie = copy.deepcopy(stare_curenta.tabla_joc.matr)
                                        for i in range(linie_st, linie_dr + 1):
                                            for j in range(coloana_st, coloana_dr + 1):
                                                copie[i * 7 + j] = Joc.JMIN
            
                                        if connected(copie):
                                            raspuns_valid = True
                                    else:
                                        print("Exista deja un simbol in pozitia ceruta.")
                                else:
                                    print("Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0,1,2,3,4,5,6).")
            
            
                            except ValueError:
                                print("Linia si coloana trebuie sa fie numere intregi")
            
                        for i in range(linie_st, linie_dr + 1):
                            for j in range(coloana_st, coloana_dr + 1):
                                stare_curenta.tabla_joc.matr[i*7 + j] = Joc.JMIN
            
                        print("\nTabla dupa mutarea jucatorului")
                        print(str(stare_curenta))
                    
                        if (afis_daca_final(stare_curenta)):
                            break
            '''

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator


            print("Acum muta calculatorul cu simbolul", stare_curenta.j_curent)
            # retinem momentul de start pentru afisarea timpului de gandire al calculatorului
            t_inainte = int(round(time.time() * 1000))

            # alegem algoritmul in functie de inputul utilizatorului
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:
                stare_actualizata, nr_noduri = alpha_beta(-300, 300, stare_curenta, 0)
                noduri_calculator.append(nr_noduri)



            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc  # aici se face de fapt mutarea !!!


            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            stare_curenta.tabla_joc.deseneaza_grid()
            # retinem momentul de stop pentru afisarea timpului de gandire al calculatorului
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            timpi_calculator.append(t_dupa - t_inainte)

            if (afis_daca_final(stare_curenta, nr_mutari_calculator+1, nr_mutari_jucator, timpi_calculator, noduri_calculator)):
                break

            # am facut o mutare, este randul celuilalt jucator
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
            print("Acum muta utilizatorul cu simbolul ", stare_curenta.j_curent)
            t_inainte = int(round(time.time() * 1000))
            nr_mutari_calculator += 1




if __name__ == "__main__":
    t_inainte = int(round(time.time() * 1000))
    main()
    t_dupa = int(round(time.time() * 1000))
    print("Jocul a durat " + str(t_dupa - t_inainte) + " milisecunde.")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

