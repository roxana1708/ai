import time
import copy

ADANCIME_MAX = 3


def elem_identice(lista):
    if (len(set(lista)) == 1):
        return lista[0] if lista[0] != Joc.GOL else False
    return False


def full_board(lista, jucator):
    for i in lista:
        if i == Joc.GOL:
            return False

    return jucator

def verif_liber(lista, l_st, c_st, l_dr, c_dr):
    # verificam daca dreptunghiul selectat este ocupat sau nu
    for i in range(l_st, l_dr+1):
        for j in range(c_st, c_dr+1):
            if lista[i*7 + j] != '#':
                return False
    return True

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
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 7
    JMIN = None
    JMAX = None
    GOL = '#'
    OTR = '*' #patratica otravita

    def __init__(self, tabla=None):  # Joc()
        self.matr = tabla or [Joc.GOL] * self.NR_COLOANE ** 2
        self.matr[4] = '*'
        self.matr[8] = '*'
        self.matr[26] = '*'
        self.matr[37] = '*'



    @classmethod
    def jucator_opus(cls, jucator):
        # val_true if conditie else val_false
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    # TO DO 5
    def final(self, jucator):
        rez = full_board(self.matr, self.jucator_opus(jucator))

        if rez:
            return rez
        else:
            return False

    # TO DO 3,6
    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        l_mutari = []
        #generare mutari pentru vaarianta generalizata
        for i in range(len(self.matr)):
            min_linie_colt_dr_jos = i / 7
            min_coloana_colt_dr_jos = i % 7

            #print(self.matr)

            for linie in range(int(min_linie_colt_dr_jos), 7):
                for coloana in range(min_coloana_colt_dr_jos, 7):
                    copie_matr = copy.deepcopy(self.matr)
                    #print(str(int(i / 7)) + " " + str(i % 7) + " " + str(linie) + " " + str(coloana))

                    if verif_liber(copie_matr, int(i/7), i%7, linie, coloana):
                        #print("here libera")
                        #print(str(int(i/7)) + " " + str(i%7) + " " + str(linie) + " " + str(coloana))
                        #print(copie_matr)
                        #print(copie_matr)
                        for x in range(int(i/7), linie+1):
                            for y in range(i%7, coloana+1):
                                copie_matr[x*7+y] = jucator
                        #print(copie_matr)
                        if connected(copie_matr):
                            #print("here valida")
                            l_mutari.append(Joc(copie_matr))
                    #else:
                        #break
        #print(l_mutari)
        return l_mutari

    # TO DO 7
    def estimeaza_scor(self, adancime, j_curent):
        t_final = self.final(j_curent)
        # if (adancime==0):
        if t_final == self.__class__.JMAX:  # self.__class__ referinta catre clasa instantei
            return 99 + adancime
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        elif j_curent == self.__class__.JMAX:
            return self.matr.count(Joc.GOL)
        else:
            return -self.matr.count(Joc.GOL)

    #def estimeaza_scor_2(self, adancime, j_curent):


    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.NR_COLOANE)]) + "\n"
        sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
        for i in range(self.NR_COLOANE):  # itereaza prin linii
            sir += str(i) + " |" + " ".join(
                [str(x) for x in self.matr[self.NR_COLOANE * i: self.NR_COLOANE * (i + 1)]]) + "\n"
        # [0,1,2,3,4,5,6,7,8]
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

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile (tot de tip Stare) din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        # e de tip Stare (cel mai bun succesor)
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)  # lista de informatii din nodurile succesoare
        #print(l_mutari)
        juc_opus = Joc.jucator_opus(self.j_curent)

        # mai jos calculam lista de noduri-fii (succesori)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    # daca sunt la o frunza in arborele minimax sau la o stare finala
    #print("cccc")
    #print(stare.tabla_joc.final)
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()
    #print(stare.mutari_posibile)

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(x) for x in
                        stare.mutari_posibile]  # expandez(constr subarb) fiecare nod x din mutari posibile

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)  # def f(x): return x.estimare -----> key=f
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)

    stare.estimare = stare.stare_aleasa.estimare
    #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')  # in aceasta variabila calculam maximul

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)  # aici construim subarborele pentru stare_noua

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')
        # completati cu rationament similar pe cazul stare.j_curent==Joc.JMAX
        for mutare in stare.mutari_posibile:
            # calculeaza estimarea
            stare_noua = alpha_beta(alpha, beta, mutare)  # aici construim subarborele pentru stare_noua

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final(stare_curenta.j_curent)  # metoda final() returneaza "remiza" sau castigatorul ("x" sau "0") sau False daca nu e stare finala
    if (final):
        if final == 'x':
            print("A castigat 0")
        else:
            print("A castigat x")
        return True

    return False


def main():
    # initializare algoritm
    raspuns_valid = False

    # TO DO 1
    while not raspuns_valid:
        tip_algoritm = input("Algoritmul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
        if (Joc.JMIN in ['x', '0']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")
    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    # expresie= val_true if conditie else val_false  (conditie? val_true: val_false)

    # initializare tabla
    tabla_curenta = Joc();  # apelam constructorul
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX)
    print(stare_curenta)
    #print("llll")

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul utilizator

            # TO DO 4
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

            # dupa iesirea din while sigur am valide atat linia cat si coloana
            # deci pot plasa simbolul pe "tabla de joc"
            #stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana] = Joc.JMIN
            #y = int(coloana % 5)
            #for ii in range(linie * Joc.NR_COLOANE + coloana, 25, 5):
                #for j in range(0, 5 - y):
                    # print(j)
                    #if stare_curenta.tabla_joc.matr[ii + j] == Joc.GOL:
                        #stare_curenta.tabla_joc.matr[ii + j] = Joc.JMIN

            for i in range(linie_st, linie_dr + 1):
                for j in range(coloana_st, coloana_dr + 1):
                    stare_curenta.tabla_joc.matr[i*7 + j] = Joc.JMIN



            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))
            # TO DO 8a
            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            print("Acum muta calculatorul cu simbolul", stare_curenta.j_curent)
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))

            # stare actualizata e starea mea curenta in care am setat stare_aleasa (mutarea urmatoare)
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)

            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc  # aici se face de fapt mutarea !!!
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            # TO DO 8b
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare.  jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


#main()
#stare = Stare(Joc(['x', 'x', 'x', 'x', '*', 'x', 'x','0', '*', '0', '0', '0', 'x', 'x','#', '#', '#', '#', '#', 'x', 'x','#', '0', '#', '#', '#', '*', 'x','x', 'x', 'x', 'x', 'x', 'x', 'x','x', 'x', '*', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']), '0', 3)
#print(stare.mutari())

'''
print(check(['x', 'x', 'x', 'x', '*', '0', 'x',
'x', '*', '#', '#', '#', '#', 'x',
'x', '#', '0', '0', '#', 'x', 'x',
'x', '#', '0', '#', '#', '*', 'x',
'x', '#', '#', 'x', 'x', 'x', 'x',
'x', '#', '*', 'x', 'x', 'x', 'x',
'x', 'x', 'x', 'x', 'x', 'x', 'x'], 0, 3, 0, 6))

print(check(['x', 'x', 'x', 'x', '*', '0', 'x',
'x', '*', '#', '#', '#', '#', 'x',
'x', '#', '0', '0', '#', 'x', 'x',
'x', '#', '0', '#', '#', '*', 'x',
'x', '#', '#', 'x', 'x', 'x', 'x',
'x', '#', '*', 'x', 'x', 'x', 'x',
'x', 'x', 'x', 'x', 'x', 'x', 'x'], 3, 6, 0, 6))


print(pot_comunica_sup_inf(['x', 'x', 'x', 'x', '*', '0', 'x',
'x', '*', '#', '#', '#', '#', 'x',
'x', '#', '0', '0', '#', 'x', 'x',
'x', '#', '0', '#', '#', '*', 'x',
'x', '#', '#', 'x', 'x', 'x', 'x',
'x', '#', '*', 'x', 'x', 'x', 'x',
'x', 'x', 'x', 'x', 'x', 'x', 'x'], 3, 3))

print(pot_comunica_st_dr(['x', 'x', 'x', 'x', '*', '0', 'x',
'x', '*', '#', '#', '#', '#', 'x',
'x', '#', '0', '0', '#', 'x', 'x',
'x', '#', '0', '#', '#', '*', 'x',
'x', '#', '#', 'x', 'x', 'x', 'x',
'x', '#', '*', 'x', 'x', 'x', 'x',
'x', 'x', 'x', 'x', 'x', 'x', 'x'], 2, 2))


print(connected(['x', 'x', 'x', 'x', '*', '0', 'x',
                 'x', '*', '0', '#', '#', '#', '#',
                 '#', '#', '0', '0', '#', 'x', 'x',
                 'x', '#', '#', '#', '#', '*', 'x',
                 'x', '0', '0', 'x', 'x', 'x', 'x',
                 'x', '0', '*', 'x', 'x', 'x', 'x',
                 'x', 'x', 'x', 'x', 'x', 'x', 'x']))

'''
print(connected(['#', '#', '#', '#', '*', '0', '0', '#', '*', '0', '0', '0', '0', '0', '#', '#', '0', '0', '0', '0', '0', '#', '#', '#', '#', '#', '*', '#', '#', '#', '#', 'x', 'x', 'x', 'x', '#', '#', '*', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']))

#if not pot_comunica_sup_inf(lista, linie_colt_st_sus, linie_colt_dr_jos):

#if not check(lista, 0, linie_colt_dr_jos, 0, 6) and not check(lista, linie_colt_st_sus, 6, 0, 6):

"""
here libera
['x', 'x', 'x', 'x', '*', '0', 'x', 
'x', '*', '#', '#', '#', '#', 'x', 
'x', '#', '0', '0', '#', 'x', 'x', 
'x', '#', '0', '#', '#', '*', 'x', 
'x', '#', '#', 'x', 'x', 'x', 'x', 
'x', '#', '*', 'x', 'x', 'x', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x']
here libera
['x', 'x', 'x', 'x', '*', 'x', 'x', 
'0', '*', '0', '0', '0', 'x', 'x', 
'#', '0', '#', '#', '#', 'x', 'x', 
'#', '0', '#', '#', '#', '*', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x', 
'x', 'x', '*', 'x', 'x', 'x', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x']
here libera
['x', 'x', 'x', 'x', '*', 'x', 'x', 
'0', '*', '0', '0', '0', 'x', 'x', 
'#', '#', '0', '#', '#', 'x', 'x', 
'#', '0', '#', '#', '#', '*', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x', 
'x', 'x', '*', 'x', 'x', 'x', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x']
here libera
['x', 'x', 'x', 'x', '*', 'x', 'x', 
'0', '*', '0', '0', '0', 'x', 'x', 
'#', '#', '#', '0', '#', 'x', 'x', 
'#', '0', '#', '#', '#', '*', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x', 
'x', 'x', '*', 'x', 'x', 'x', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x']
here libera
['x', 'x', 'x', 'x', '*', 'x', 'x', 
'0', '*', '0', '0', '0', 'x', 'x', 
'#', '#', '#', '#', '0', 'x', 'x', 
'#', '0', '#', '#', '#', '*', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x', 
'x', 'x', '*', 'x', 'x', 'x', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x']
here libera
['x', 'x', 'x', 'x', '*', 'x', 'x', 
'0', '*', '0', '0', '0', 'x', 'x', 
'#', '#', '#', '#', '#', 'x', 'x', 
'0', '0', '#', '#', '#', '*', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x', 
'x', 'x', '*', 'x', 'x', 'x', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x']
here libera
['x', 'x', 'x', 'x', '*', 'x', 'x', 
'0', '*', '0', '0', '0', 'x', 'x',
'#', '#', '#', '#', '#', 'x', 'x',
'#', '0', '0', '#', '#', '*', 'x',
'x', 'x', 'x', 'x', 'x', 'x', 'x',
'x', 'x', '*', 'x', 'x', 'x', 'x',
'x', 'x', 'x', 'x', 'x', 'x', 'x']
here libera
['x', 'x', 'x', 'x', '*', 'x', 'x',
'0', '*', '0', '0', '0', 'x', 'x',
'#', '#', '#', '#', '#', 'x', 'x',
'#', '0', '#', '0', '#', '*', 'x',
'x', 'x', 'x', 'x', 'x', 'x', 'x',
'x', 'x', '*', 'x', 'x', 'x', 'x',
'x', 'x', 'x', 'x', 'x', 'x', 'x']
here libera
['x', 'x', 'x', 'x', '*', 'x', 'x',
'0', '*', '0', '0', '0', 'x', 'x',
'#', '#', '#', '#', '#', 'x', 'x',
'#', '0', '#', '#', '0', '*', 'x',
'x', 'x', 'x', 'x', 'x', 'x', 'x', 
'x', 'x', '*', 'x', 'x', 'x', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x']



['x', 'x', 'x', 'x', '*', 'x', 'x', 
'0', '*', '0', '0', '0', 'x', 'x', 
'#', '#', '#', '#', '#', 'x', 'x', 
'#', '0', '#', '#', '#', '*', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x', 
'x', 'x', '*', 'x', 'x', 'x', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x']


['x', 'x', 'x', 'x', '*', 'x', 'x', 
'0', '*', '0', '0', '0', 'x', 'x', 
'#', '#', '#', '#', '#', 'x', 'x', 
'#', '0', '#', '#', '#', '*', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x', 
'x', 'x', '*', 'x', 'x', 'x', 'x', 
'x', 'x', 'x', 'x', 'x', 'x', 'x']


"""



