## AI Tema 1 - Prob. Lupi, Capre, Verze - rezolvare3.py

Problema se bazeaza pe jocul cunoscut cu taranul, lupul, capra si varza
Taranul vrea sa mute animalele si verzele de pe malul de est pe malul de vest. Presupuneam ca taranul nostru si-a dezvoltat afacerea, si de data asta a cumparat L lupi, C capre si V verze. Nu mai are doar o biata barca, ci un vaporas cu 2 compartimente (A si B) in care incap cate K1 si respectiv K2 elemente.
De asemenea, pe malul celalalt taranul are o magazie cu M locuri (adica, in care incap M elemente).
Atat in compartimente cat si in magazie taranul nu pune niciodata elemente de tipuri diferite (de exemplu, vor fi doar capre sau doar lupi, dar niciodata si lupi si capre). Cand taranul nu se afla impreuna cu caprele sau lupii, acestia mananca ce gasesc, mai exact: caprele mananca verze, lupii mamanca capre, si, numai cand nu au capre, alti lupi. Daca nu au ce manca, toti stau cuminti. Verzele sunt de asemenea cuminti, nu mananca pe nimeni. In magazie sau in compartimentele din barca nimeni nu va manca pe nimeni fiind mereu elemente de acelasi tip.
Barca nu pleaca fara taran, dar poate pleca cu compartimetele goale. Animalele mananca doar dupa ce a plecat barca
Starea finala e atinsa cand nu mai sunt animale pe malul initial si in plus pe malul opus sunt minim animalele cerute in fisier (de exemplu, daca se cer "3 verze 10 capre 1 lupi" este valida o solutie cu "10 verze 10 capre 1 lupi".



## AI Tema 2 - Jocul Chomp - rezolvare_v2.py

Sunt doi jucatori (in imagini notati cu rosu si albastru). Jocul foloseste o grila dreptunghiulara de n randuri si m coloane. Grila reprezinta o bucata de ciocolata (impartita in patratele din care cateva sunt otravite) din care doi jucatori flamanzi rup bucati dreptunghiulare. Numarul de randuri si de coloane va fi dat in constructorul jocului (puteti sa le hardcodati sau sa le cititi dintr-un fisier de setari). Jocul este bazat pe ture.
La fiecare pas un jucator rupe o bucata dreptunghiulara astfel incat sa nu lase nicio patratica in aer (neconectata), dar nici sa nu ia vreo bucatica otravita.
Pătrățelele nu pot fi decupate din mijlocul figurii. Un jucător poate mușca dintr-o margine neatinsă sau dintr-o zonă adiacentă cu un loc din care a mai mușcat el.
Pierde jucatorul care nu mai poate decupa o bucata dreptunghiulara fara sa desparta placa de ciocolata in doua, ori sa ia o bucatica otravita.
