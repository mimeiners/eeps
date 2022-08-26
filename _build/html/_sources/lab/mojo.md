# Sounderkennung mit Hilfe des Mojo V3 FPGA Boards und dem Sound

## Einleitung
Diese Projektarbeit beschäftigt sich mit der Evaluation des [Sound Erkennungs](https://alchitry.com/sound-locating-mojo) Tutorials der Webiste [Alchitry](https:E//alchitry.com/).
In diesem Tutorial nutzt Alchitry ihr eigens entwickelten Mojo v3 Board und ein Soundshield mit sieben Mikrofonen um die Richtung zu ermitteln aus der ein Ton auf das Board trifft.
Das Mojo v3 Board ist ein Board, dass für das Erlernen der Erstellung von digitalen Schaltungen mit Hilfe von Field-Programmable-Gate-Arrays (FPGA) genutzt werden kann. Wie man bereits am Namen erkennen kann bietet ein FPGA die Möglichkeit es jederzeit neu zu flashen (Field-Programmable). Dabei beschreiben wir die Hardware mihilfe einer Hardwarebeschreibungssprache wie VHDL, Verilog oder wie in diesem Beispiel mit Lucid und die Hardware nimmt entsprechend unserer Beschreibungssprache exakt die Funktion ein die wir erzielen möchten. Die Beschreibungssprache bewirkt, dass Logikgatter innerhalb des FPGA entsprechend der Funktion miteinander verknüpft werden. So kann der Mojo v3 genutzt werden um eine LED zum blinken zu bringen oder komplexere Aufgaben wie Sounderkennung.

Im Folgenden könnt ihr eine kurze Erläuterung zur Hardware finden. Die Einrichtung der Toolchain wird Schritt für Schritt erklärt. Außerdem wird der Aufbau eines Projektes erläutert und im speziellen wird auf das Sound Locator Projekt eingegangen. In diesem Zusammenhang wird auf die so genannten IP-Cores eingegangen. Da Hardware und Software offenkundig nie so funkionieren wie es der Entwickler vorgesehen hat, wird außerdem auf Probleme eingangen und wie diese Behoben werden können. Es folgt ein Vergleich über die intendierte Funktion und der tatsächlichen Funktion des Projektes wobei im Nachgang noch ein ausführlicher Versuch vorgestellt wird, der die Funktion genauer unter die Lupe nimmt.

## [Der Mojo](https://www.adafruit.com/product/1553) [Baby](https://www.youtube.com/watch?v=c4ytuS8pVp4)

Das Mojo v3 Board ist ein preiswertes (~70€, bei [AliExpress](https://de.aliexpress.com/item/32798926767.html?spm=a2g0o.ppclist.product.2.dc57fhXPfhXPEo&pdp_npi=2%40dis%21EUR%21%E2%82%AC%2068%2C61%21%E2%82%AC%2068%2C61%21%21%21%21%21%40211b5a9616552327883654477e07b2%2164982667969%21btf&_t=pvid%3Ab5fae29b-1699-49ff-9cdf-7850da36c207&afTraceInfo=32798926767__pc__pcBridgePPC__xxxxxx__1655232788&gatewayAdapt=glo2deu) stand: Juni 2022) FPGA Entwicklungsboard auf dem ein Spartan 6 FPGA eingebaut ist sowie ein ATmega32 Microprozessor der Arduino Kompatibel ist. Dieser wird im Wesentlichen für die Programmierung des FPGA genutzt. Nach der Programmierung kann der Controller als Analog-Digital Wandler eingesetzt werden. Außerdem verfügt das Board üb 84 Digitale I/O die über die Steckleisten herausgeführt sind und 8 LEDs die für allgemeine Programmierung genutzt werden können.

Auf dem Microphone Shield befinden sich sechs konzentrische Mikrofone, die um ein siebtes Mikrofon in der Mitte herum auf dem Shield angebracht sind. Diese Mikrofone werden so genutzt das über die Verzögerung des einkommenden Tones die Richtung bestimmt werden kann. Die Erklärung dafür kann hier nochmal eingefügt werden:
PDM? Delay? FFT? MEMS?

## Genutzte Toolchain
Nachdem wir eine kleine Einführung in die genutzte Hardware erhalten haben wollen wir uns jetzt die Einrichtung und Installation der Toolchain anschauen. 
Die Toolchain für die Inbetriebnahme des MOJO V3 Boards besteht aus einem Projektierungstool [Alchitry Labs](https://alchitry.com/alchitry-labs) und einem Builder. 

Für das Mojo v3 board bedarf es dem [ISE WebPack](https://www.xilinx.com/products/design-tools/ise-design-suite/ise-webpack.html) von [Xilinx](https://www.xilinx.com/).
Alchitry Labs wird hierbei genutzt um das Projekt zu organisieren und die unterschiedlichen Teile des Projektes zu beschreiben. Der Builder ISE WebPack übersetzt letzten Endes die Beschreibung aus den unterschiedlichen Bestandteilen des Projektierungstools in die eigentliche Hardware innerhalb des FPGA.
Das genutzte Betriebssystem in diesem Projekt ist Linux [Debian 11](https://www.debian.org/News/2021/20210814).


### Installation des ISE WebPack
Vor der Installation von Alchitry Labs ist es ratsam zunächst das ISE WebPack zu installieren. Auch ratsam ist es zunächst die Partitionierung des Rechners und den freien Festplattenspeicher im Blick zu haben. Das Archive was wir aus dem Internet laden werden ist bereits 6,5GB groß. Für die Installation benötigt das ISE WebPack weitere 18GB Speicherplatz. Nachdem wir sicher gestellt haben, dass wir einen geeigneten Speicherplatz für die Installation haben können wir das Installationsverzeichnis von der [Website](https://www.xilinx.com/downloadNav/vivado-design-tools/archive-ise.html) herunterladen. Hier wählen wir die Version 14.7 und unter diesem Punkt laden wir die ISE Design Suite - 14.7 Full Product Installation herunter und holen uns einen Kaffee oder Tee für die Überbrückung der Zeit. Es muss an dieser Stelle erwähnt werden, dass wir einen Nutzeraccount benötigen um diese Software herunter zu laden und zu installieren.
Nach dem Download geht es weiter zur eigentlichen Installation. Als erstes müssen wir das Installationsverzeichnis entpacken. Hierfür solltet ihr mit Hilfe des Terminals und des change directory Befehls **cd** in den Ordner wechseln in dem ihr die Datei heruntergeladen habt (Hier: Downloads):

Terminalausgabe
:       mojo@fpga:~$ cd Downloads/

Seid ihr im Verzeichnis angekommen müsst ihr das Verzeichnis entpacken:

Terminalausgabe
:       mojo@fpga:/Downloads/$ tar -xvf Xilinx_ISE_DS_Lin_14.7_1015_1.tar

Die Optionen **xvf** beschreiben, dass das Archiv entpackt werden soll (x), dass die verarbeiteten Dateien ausführlich aufeglistet werden (v) und dass das Archiv aus dem aktuellen Verzeichnis genommen werden soll (f). Aufgrund der Datenmenge wird es entsprechend lange dauern. Sollte der Kaffee von vorhin noch nicht kalt geworden sein. Nehmt euch ein Stück Kuchen dazu.
Nach diesen Vorarbeiten können wir nun das Setup des Programmes Starten. 

:::{note}
Beachtet, dass ihr die Installation von ISE WebPACK nach Möglichkeit ohne Adminrechte durchführen solltet. Hierfür müsst ihr den Installationspfad auf einen lokalen Benutzerpfad ändern!
:::

Wenn ihr die Istallation zum Beispiel folgendermaßen startet:

Terminalausgabe
:       mojo@fpga:/Downloads/Xilinx_ISE_DS_Lin_14.7_1015_1$ sudo ./xsetup

Werdet ihr zunächst darum gebeten allerlei Konditionen und Vereinbarungen zuzustimmen. 

```{figure} img/Terms_and_conditions.png 
:name: 01_fig_01

Zustimmung zu den Terms and Conditions geben
```

Wir stimmen diesen zu und müssen als nächstes das Product auswählen, dass wir installieren wollen. In unserem Fall ist es das ISE WebPACK.

```{figure} img/MojoLab/AuswahlISE.png
:name: 01_fig_02

Auswahl des ISE WebPACKs für die Installation
```
Im Folgefenster lassen wir alle Häckchen so wie sie sind. Wichtig ist, dass ihr mehrere CPU kerne nutzt um die Installation schneller abzuschließen. Ansonsten erhöht sich die Installationszeit immens.

Während die Installation läuft, könnt ihr die Zeit nutzen und euch eine Lizenz für das ISE WebPack holen.
Dise bekommt ihr auf der [Internetseite](https://www.xilinx.com/member/forms/license-form.html).
Hier gebt ihr eure persönlichen Daten ein und Wählt die Lizenz für das ISE Webpack aus, ladet diese herunter und fügt diese dann dem dem Programm zu.
Für das einmalige Starten des WebPacks geht ihr am besten wie folgt vor.


Habt ihr das Programm einmal gestartet wird euch das Programm daruf hinweisen, dass es keine Lizenz gefunden hat. Es öffnet euch freundlicherweise direkt den Lizenzmanager.
```{figure} img/MojoLab/Licence_Manager_1.png 
:name: 01_fig_03

Möglichkeit zur Auswahl des Lizenztypes
```
Solltet ihr bis zu diesem Zeitpunkt noch keine Lizenz haben ist hier noch einmal eine gute Möglichkeit den Lizenzierungsprozess anzuschieben.

Habt ihr eure Lizenz herunter geladen, könnt ihr eure Lizenz nun über den "Manage Licences" Reiter zum Programm hinzufügen. Navigiert dazu innerhalb des Dialogfeldes zu dem Ort an dem ihr eure Lizenz abgespeichert habt.
```{figure} img/MojoLab/Licence_Manager_2.png 
:name: 01_fig_04

Load Licence bringt uns unserem Ziel näher
```

Nachdem wir nun endlich das ISE WebPack 
1. Heruntergeladen
2. Installiert
3. Gestartet und
4. Lizensiert 

haben, können wir jetzt damt anfangen unsere Programmierumgebung für das Projekt einzurichten.

### Installation von Alchitry Labs
Den Großteil der Installation unserer Toolchain haben wir bis zu diesem Zeitpunkt bereits erledigt. Das Einrichten von Alchitry Labs stellt sich wesentlich leichter dar, als es bei der Xilinx Software der Fall war.
Geht hierfür auf die (Website)[https://alchitry.com/alchitry-labs] von Alchitry Labs unter den Reiter Alchitry Labs ( Als kleine Dienstleistung schickt euch der Link direkt dorthin). Scrollt zu den Download Links für die aktuelle Version und ladet euch die entsprechende Variante herunter. Ich empfehle euch an dieser Stelle noch einmal wirklich Linux zu nutzen und euch dementprechend die Linux Variante herunter zu laden. Die Einrichtung auf Linux verhält sich deutlich einfacher als die auf Windows.  Knappe 18 MB wandern jetzt aus dem Internet auf euer Endgerät.
Ihr erhaltet wie auch beim letzten Programm ein Dateinarchiv das ihr zunächst entpacken  müsst. Ihr könnt hierfür natürlich die selben Befehle nutzen wie im letzten Kapitel besprochen. Ihr müsst lediglich den Dateinamen ändern.

Terminalausgabe
:       mojo@fpga:/Downloads/$ tar -xvf alchitry-labs-1.2.7-linux.tar 

Habt ihr das Archiv entpackt navigiert mit dem change directory Befehl über das Terminal in den neuen Unterordner "alchitry-labs-1.2.7". Hier angekommen müsst ihr nur noch das shell skrpt ausführen, dass sich in diesem Ordner befindet. Das könnt ihr folgendermaßen machen:

Terminalausgabe
:       bash alchitry-labs

Solltet ihr bis hierher alles richtig gemacht haben, öffnet sich endlich unsere Programmierumgebung.
Allerdings werden wir zunächst darauf hingewiesen, dass wir den Installationsort unseres Builders angeben sollen. Hierfür geht klickt im Alchitry Labs Fenster bitte auf "Settings" und dann auf "ISE Location" und wählt dann den Ordner mit der Versionsnummer eurer ISE aus ( hier: 14.7). Keine Sorge, einen ausführlichen Hinweis darüber was ihr auswählen sollt, gibt euch das Programm ebenfalls.

```{figure} img/MojoLab/Alchitry_Licence.png 
:name: 01_fig_05

Auswahl des ISE WebPack Installationsortes
```
Ab jetzt solltet ihr in der Lage sein ein Projekt zu öffnen und endlich den Mojo zu flashen. Dieser Vorgang wird in den nächsten Abschnitten geklärt.

### Öffnen des Projektes
Beim ersten Starten von Alchitry Labs werdet ihr direkt gefragt ob ihr ein bestehendes Projekt öffnen wollt, oder ob ihr ein neues erstellen wollt. 

```{figure} img/MojoLab/First_Start.png 
:name: 01_fig_06

Erste Projektauswahl
```
Da wir noch kein bestehendes Projekt besitzen beantworten wir die Frage hier mit "No" um ein neues Projekt zu erstellen. 

Das folgende Dialogfenster könnt ihr in Abbildung 7 sehen. Im Feld "Project Name:" tragen wir unseren Wunschnamen für unser Projekt ein. Im folgenden Reiter "Workspace" steht unser Arbeitsumgebung. Hier werden unsere Projekte abgespeichert und unsere Projektierungsumgebung erstellt hier die nötigen Dateien für das Builden des Projektes. Im dritten Reiter wählen wir unser Mojo Board aus. Das Programm erstellt hier für uns die Bezüge zu Hardware, damit das Projekt funktionsfähig gebaut werden kann. Die Sprache ("Language") die ausgewählt werden muss um ein funktionierendes Beispielprojekt laden zu können ist hier die Programmeigene Lucid Sprache. Ihr könnt in dieser Umgebung ebenfalls in Verilog coden, allerdings werdet ihr hier keine Beispielprojekte finden. Wir wählen für dieses Projekt Lucid aus und Nehmen das Beispiel Sound Locator aus dem letzten Dropdown Menüs dieses Fensters.

```{figure} img/MojoLab/New_Project.png 
:name: 01_fig_07

Einstellungen zum öffnen des Sound locator Beispiels
```
Durch einen letzten Mausklick auf den Button "Create" wird unser Beispielprojekt erstellt. 
Bevor wir zu Problemen innerhalb dieses Projektes kommen, machen wir eine kurze Erklärung dazu, was wir alles in diesem Projekt finden können. Für die Inbetriebnahme des Projektes kannst du den Abschnitt über den Aufbau eines Projektes überspringen und später hierher zurückkehren wenn du mehr über Sources, Components, Cores und Constraints erfahren möchtest.

## Aufbau eines Projektes

- <u>**Source**</u>
 Der erste Teil innerhalb dieses Projektes sind die Source-Dateien auch Module genannt. Diese beschreiben alle Ein- und Ausgänge der unterschiedlichen Hardware. Für das Sound Locator Projekt wären das zum einen die Hann Funktion, der LED-Ring, das mojo-top modul, welches unser Mojo Board beschreibt, die pdm-mics zur Definition unserer Mikrophone und das sound_locator modul in der der Delay zur Sound Erkennung ermittelt wird.

```{figure} img/MojoLab/Source.png 
:name: 01_fig_08

Die Source-Dateien findest du zu oberst im Projekt
```
- <u>**Components**</u>m

Components sind teils vorinstallierte teils selbst geschriebene Bausteine, die für spezielle Funktionen verwendet werden können. In unserem Projekt finden wir vielfach Lucid-Files, **.luc**. Diese wurden vom Hersteller erstellt, können sich aber auch in der Xilinx Umgebung finden. In deisem Projekt befinden sich:

```{figure} img/MojoLab/Components.png 
:name: 01_fig_09

Als Zweites findest du die Components im Projekt
```
- <u>**Cores**</u>
```{figure} img/MojoLab/Cores.png 
:name: 01_fig_010

Der dritte Reiter beinhaltet die IP-Cores
```
- <u>**Constraints**</u>

Daregstellt sind die drei User-constraints-files von debugger, microphone shield und vom mojo board.In diesen Dateien werden die Timing-Eigenschaften sowie die Pineigenschaften und physikalischen Eigenschaften und grenzen beschrieben. Diese Dateien werden benötigt um dem synthetisierungs Programm (ISE WebPack) die letzten Informationen zu geben wie das Projekt erstellt werden soll.

```{figure} img/MojoLab/Constraints.png 
:name: 01_fig_011

Als letztes gibt es noch die Constraints
```


## Sound Locator Projekt

Im Vorfeld wurden bereits die Hardware sowie die unterschiedlichen Funktionsblöcke die das Sound Locator Projekt besitzt beschrieben. Die Dokumentation des Projektes von O'Reilly verspricht ein Plug in Play mit der Hardware. Die Untersuchungen innerhalb dieses Projekts haben jedoch gezeigt, dass noch weitere Probleme gelöst werden müssen, bevor das Projekt auf den FPGA geflasht werden kann. In diesem Abschnitt schauen wir uns diese Probleme an, wie wir diese einfach lösen können und schauen uns im Anschluss die Funktion der Sound-Erkennung an.

### Probleme mit den IP-cores lösen

Erinnern wir uns an die IP-Cores die im letzten Abschnitt beschrieben wurden. Sie stellt eine fertige Funktionseinheit wie zum Beispiel den Decimation-Filter dar, die nach Definition seiner Funktion zum FPGA Design hinzugefügt werden kann. Ausgerechnet diese IP-Cores machen beim ersten Flash-Versuch Probleme und es kommt folgende Meldung.

```{figure} img/MojoLab/Fehlermeldung_Cores.png 
:name: 01_fig_012

Angezeigte Fehlermeldung beim ersten Flashversuch
```
Alchitry Labs zeigt an, dass es die angezeigten Dateien für die IP-Cores nicht lesen kann. Schaut man in die Ordner Struktur und vergleich diese mit dem agezeigten Pfad so scheint sich hier ein Fehler eingeschlichen zu haben, der es zunächst unmöglich macht das Projekt zu bauen.


> <span style="color:green">**erik@erik:**</span><span style="color:blue">**~/alchitry/SoundLocator**</span>$ ls
> 
> <span style="color:blue">**constraint**</span>  <span style="color:blue">**coreGen**</span>  SoundLocator.alp  <span style="color:blue">**source**</span>  <span style="color:blue">**work**</span>

Es sind in dieser Ansicht vier Ordner zu sehen. Vergeich man diese vier Ordner mit dem geforderten Pfad von Alchitry Labs aus Abbildung 12 ist zu erkennen, dass wir den Ordner **cores** vergeblich in diesem Verzeichnis suchen. Dieses Vezeichnis wurde automatisch vom Programm erstellt was die Vermutung nahelegt, dass der Aufbau des Verzeichnises Hard gecoded ist. Nach einiger Suche innerhalb des Programm Verzeichnises konnte die Codezeile die dafür Verantwortich ist nicht gefunden werden. Statdessen wurde für die Inbetriebnahme der Hardware ein Workaround gefunden. Die nötigen Dateien befinden sich alle im **coreGen** Ordner. Ist das händische erstellen des Pfades in drei schritten:

1. Umbennen des von **coreGen** zu **cores**
2. Innerhalb dieses Ordners, erstellen der jeweiligen Ordner für Decimation Filter, xfft_v8.0 und mag_phase_calculator
3. Verschieben der Dateien für den jeweiligen core in den entsprechenden erstellten Ordner.

Nachdem diese Schritte durchgeführt wurden kann das Projekt gebaut werden und ermöglicht es uns das Mojo Board zu flashen.

## Funktionsprinzip des Projektes

In diesem Kapitel wird die Funktion des gesamten Aufbaus evaluiert. Innerhalb dieses Kapitels wird zunächst das Funktionsprinzip des Projektes erläutert. In Abbildung 13 ist der Signalfluss der Sounderkennung dargestellt. Alle Dargestellten Blöcke werden innerhalb dieses und des des nächsten Abschnitts erläutert. Zunächst steht ein Ton in Form einer Sinuswelle an. Diese besteht nicht aus nur einer Frequenz wie in Abbildung 13 dargestellt, sondern setzt sich aus verschiedenen Frequenzen zusammen. Dieses Frequenzspektrum wird ebenfalls dargestelt und erläutert. Die analoge Sinuswelle wird durch ein Wandlungssystem in die digitale Domäne Übertragen. Hier sind es so genannte digitale MEMS PDM Mikrofone. Die ausgegebene PDM wird ebenfalls theoretisch erläutert und messtechnisch aufgenommen. Das Signal Processing wird vom FPGA übernommen. Hier findet die Auswertung der einkommenden Signale statt und damit die Erkennung. Am Ende steht die optische Ausgabe der erkannten Richtung.

```{figure} img/MojoLab/SignalFlow.png
:name: 01_fig_013

Übersicht Signalfluss
```

Der erste Block des Signalflusses enthält die akustische Welle. Diese Schallwelle entsteht durch das komprimieren und dekomprimieren der Luft. In der Physik wird eine ideale winzige Punktschallquelle angenommen von der aus kugelförmig die Schallwellen in alle Richtungen abgestrahlt werden. Diese Wellenfronten in verbindung mit den Strahlen kennzeichnen die Richtung der Schallwellen. Wellenfronten sind hierbei Flächen, bei der die Luftteilchen wertgleiche Auslenkungen besitzen aufgrund der erzeugten Schwingung.DARSTELLUNG DES KREISES[Halliday]

Wie bereits erwähnt verbreiten sich diese Schallwellen kugelförmig und dreidimensional im Raum und werden darum auch sphärische Wellen genannt. Je weiter man sich jedoch von der Punktquelle entfernt umso geringer wird diese Krümmung und die Schallwelle kann als Ebene verstanden werden. Diese Wellen werden dann ebene oder planare Wellen genannt. [Halliday]

Um einen Ton zu erzeugen muss diese (De-) Komrimierung der Luft mit einer definierten Frequenz erzeugt werden. Um den Kammerton (C) zu erzeugen muss ein Ton mit einer Frequenz von f=440 Hz erzeugt werden. Idealerweise sähe dieser Ton aus wie in Abbildung X dargestellt. HIER PYTHON PLOT EINFÜGEN 

Aus dieser Darstellung wäre es ein einfiaches die Frequenz des Signals hinaus zu lesen und damit das Signal zu rekonstruieren. In der realen Welt ist die Wahrheit häufig nicht so eindeutig und das eintreffen Signal auf das Mikrofon ist immer mit einem Hintergrundrauschen belegt. HIER PYTHON MIT RAUSCHEN EINFÜGEN
Um die Reaktion der Hardware auf die eintreffenden Töne besser einschätzen oder erklären zu können ist es deshalb interessant das Signal außerhalb des Zeitbereichs zu betrachten und das ganze in den Frequenzbereich zu überführen und damit ein Frequenzspektrum zu erzeugen.

Das Frequenzspektrum...

Nachdem geklärt wurde welche Eingangssignale zu erwarten sind kann der Fokus auf die akustische Aufnahme gerichtet werden. Auf dem Microphoneshield sind sieben Mikrofone mit der Bezeichnung SPK0415HM4H zu finden. Diese Mikrophone sind digitale Mikro-Elektronisch-Mechanische Systeme (MEMS). Das bedeutet, dass durch Herstellungsmethoden der Halbleiterindustrie ein Bauteil erzeugt wurde, dass sowohl elektronische als auch mechanische Eigenschaften vereint. Wie in Abbildung 14 zu erkennen ist, besitzt ein solches Mikrofon einen Sound Port, dies ist eine Öffnung im Gehäuse (Can) des Bauteils. Hier kann der Ton auf die eigentliche Struktur auftreffen. Die Öffnung ist hier oben kann bei anderen Mikrofonen aber auch am Boden des Gehöuses sein. Darunter befindet sich eine Membran (Glob Top Molding) über einer Halbleiter Trägerstruktur. Die Membran und die Trägerstruktur sind zwei Gerade, gegenüberliegende Flächen zwischen denen ein Material zu finden ist das als Dielektrikum verstanden werden kann. Dies ist nichts weiter als ein Kondensator mit einer dazugehörigen Kapazität. Beim Auftreffen von Schall gerät die Membran in Bewegung, was die Kapazität des Kondensators ändert. Diese Änderung wird von der Anwender Spezifischen Schaltung (ASIC) erkannt und entsprechend verarbeitet. Ob ein Analoges oder Digitales Signal ausgegeben wird entscheidet sich hier. Entweder das Analoge Signal wird vom ASIC bereit gestellt oder ein weiterer Wandler (Transducer) befindet sich innerhalb des Systems, welches dieses analoge zu einem digitalen Signal wandelt. Bei den digitalen Signalen kann es sich um Pulse-Code-Modulierte (PCM) oder auch um Puls-Dichte-Modulierte Signale handeln. Puls-Code-Modulierte Signale werden hier nicht weiter erläutert, sollen aber der Vollständigkeit halber erwähnt werden.
 
```{figure} img/MojoLab/MEMS.png
:name: 01_fig_014

Aufbau eines MEMS Mikrofons
```

In diesem Projekt wurden Mikrofone verwendet, die Puls-Dichte-Modulierte Signale verwenden. Und wat dat is sach isch euch jetze....


Für die Funktion des Projektes müssen zunächst einige Annahmen getroffen werden. Die wichtigste Annahme ist, dass die Richtung des Tons nur in einem zweidimensionalen Raster horizontal zum Mojo Board auf das FPGA auftreffen darf. Das ist dem physikalischen Aufbau des Microphone Shields geschuldet, da alle Mikrophone auf einer Ebene verbaut sind. Außerdem wird angenommen, dass es sich bei den auftreffenden Schallwelen um eine eine gerade Wellenfront handelt. Das heißt, dass sichjeder Punkt einer Welle mit der gleichen Geschwindigkeit ausbreitet.Die letzte Annahme ist, dass jede Frequenz eines Soundsamples aus einer einzigen Richtung kommt.

Die Sounderkennung mit dem Mojo errechnet sich die Richtung aus der der Sound auf ihn trifft aus der Phasenverschiebung zwischen den äußeren und dem zentralen Mikrofon. Die auf den Mikrophonen auftreffende Frequenz wird simultan vom FPGA abgetastet. Auf diese Fragmente wird eine Fast-Fourier-Transformation (FFT) durchgeführt, wodurch das Signal von der Zeit- in die Frequenzdomäne überführt. Als Ausgabe aus der FFT erhält man nun für jedes Fragment eine Komplexe Zahl. Bestehend aus dem Realteil, der die Amplitude des eingehenden Signals darstellt und dem Imaginärteil, der die Phase des eingehenden Signals darstellt. Diese können in einem Koordinatensystem aufgetragen werden. In Abbildung 13 ist beispielfhaft für drei Mikrophone das Prinzip dargestellt. Die schwarzen Kreise stellen die Position von drei Mikrofonen des Mojos dar. Ihre Koordinaten sind in den Klammern dargestellt. Der Mittelpunkt des Koordinatensystems ist ebenfalls als Koordinate des zentralen Mikrophons zu verstehen. In blau in der oberen linken Ecke ist die Richtung dargestellt aus der ein Ton auf die Mikrophone trifft. Das Auftreffen bewirkt eine Verzögerung (Delay) der jeweiligen äußeren Mikrophone im Vergleich zum mittleren Mikrofon. Mithilfe dieses Delays bzw. mit der Phasenverschiebung zueinander ( die Verzögerung ist lediglich der quotient aus Phasenverschiebung und Frequenz wodurch diese beiden Werte proportinal zueniander sind) und der Positionsvectoren der unterschiedlichen Mikrophone kann nun die Richtung des Tons bestimmt werden. Hierzu werden die Ortsvektoren mit dem errechneten Delay Skaliert, wodurch die violetten skalierten Vektoren entstehen. Durch Vektoraddition dieser Vektoren kann ein Summenvektor erstellt  werden, der in die Richtung der Tonquelle zeigt. (gelb)

```{figure} img/MojoLab/SoundirectionPrinciple.png
:name: 01_fig_015

Versuchsaufbau für den Funktionstest
```

### Funktionstest

Das oben beschrieben Funktionsprinzip wird im nächsten Abschnitt getestet. Für den ersten Test wird der Mojo auf einem Holztisch platziert und es wird das Alphabet durchgesprochen. Die Lärmquelle ist in diesem Video von Links und die Quelle ist auf der horizontal verschoben zum Mojo um die Funktion zu gewährleisten. Es ist zu erkennen, dass bei den S-Lauten ( die Buchstaben C, S, X, Z) führen dazu, dass mehr als nur eine LED leuchtet. Alle anderen Buchstaben haben insgesamt eine eindeutige Antwort des Mojos verursacht. 

<div class="video_container">
    <video width="320" height="240" controls="true" allowfullscreen="true"                        title="Testtitel">
      <source src="../_static/videos/Alphabet.mp4" label="Alphabet"/>
    </video>
    <div class="overlay">
        <p>Alphabet Test</p>
        </form>
    </div>
</div>
Betrachtet man zu den Beobachtungen nun das Frequenzsspektrum zu den ersten sieben Buchstaben des Alphabets ist zu erkennen, dass die größte Energiedichte bei Frequenzen zwischen 60 Hz und 400 Hz zu finden ist. Der Buchstabe C ist in dieser Abbilung der dritte Balken von links. Hier ist zu erkennen, dass zu Beginn des Buchstaben eine höhere Energiedichte zu finden ist. Diese reicht von einer Frequenz von 4 kHz bis zu über 16 kHz. Interessanterweise ist eine konträre Beobachtung beim Buchstaben "F" zu erkennen. Der zweite Balken von rechts hat zu Beginn des Buchstabens ein Ähnliches Frequenzmuster wie die Anderen. nach einer kurzen Zeit verteilt sich die Energie gleichmäßig auf eine größere Badnbreite an Frequenzen. Hier konnte jedoch eine gute Funktion des Mojo beobachtet werden. Der Schalldruckpegel bei diesem Versuch konnte etwa zwischen 60 dB und 70 dB gemessen werden.´

```{figure} img/MojoLab/AlphaG.png 
:name: 01_fig_016

Frequenzspektrum für die Buchstaben A bis G
```


Nach dieser Beobachtung ist ein weiterer grundsätzlicher Funktionstest mit einer anderen Geräuschquelle durchgeführt worden. In diesem Funktionstest wurde der Song "Come as you are" von Nirvana angespielt um die Reaktion vom Mojo zu testen. Die Quelle des Geräusches ist in diesem Video unterhalb des Mojo boards. Es ist zu erkennen, dass die unterste LED am hellsten leuchtet und die Richtung damit erkannt wird. Allerdings ist ebenfalls zu sehen, dass auch LEDs auf der anderen Seite des Kreises aufleuchten.

<div class="video_container">
    <video width="320" height="240" controls="true" allowfullscreen="true"                        title="Testtitel">
      <source src="../_static/videos/Come_as_you_are.mp4" label="Gitarren Spiel"/>
    </video>
    <div class="overlay">
        <p>Test mit Gitarrenspiel</p>
        </form>
    </div>
</div>

Das Frequenzspektrum ist in der nachfolgenden Abbildung 16 zu erkennen. Die Energie der Frequenzen scheint hier weniger breit gefächert zu sein als bei dem vorangegangenen Funktionstest. Die Funktion konnte auch hierbei im Wesentlichen nachgewiesen werden, auch wenn es bei diesem Test zum leuchten der gegenüberliegenden LED gekommen ist. Der Schalldruckpegel der während des Versuchs gemssen wurde lag bei rund 70dB. 

```{figure} img/MojoLab/comeasyouare.png 
:name: 01_fig_017

Frequenzspektrum für das Intro von "Come as you are" von Nirvana
```

Die Funktionstest konnte die prinzipielle Funktion nachweisen. Die Frage nach den Grenzen der Erkennung ist allerdings hiermit noch nicht geklärt. Um die Grenzen der Sounderkennung zu ermitteln wurde sich in diesem Experiment dazu entschieden dieses im privaten Wohnzimmer durchzuführen und nicht in einem speziell eingerichtetem Schallarmen Raum, da die Sounderkennung dazu dienen soll Geräuschquellen zu unterscheiden und die Richtung des gewollten Sounds zu ermitteln. Der Aufbau für dieses Experiment ist in den vorangegangenen Videos schon erkennbar ist schematisch jedoch nochmal in Abbildung 17 zu erkennen. Das Mojo Board mitsamt des Microphone Shield ist im Zentrum des Aufbaus platziert. Die Soundquelle ist eine Bluetoothbox der Firma Bose und wurde 10 cm oberhalb des Mojoboards platziert. Hier wird ein Sinussignal einer defenierten Frequenz und Lautstärke ausgegeben. Um die Lautsärke in dB gegenprüfen zu können wird ein Schalldruckpegel Messgerät auf der gleichen Höhe wie das zentrale Mikrofons auf dem Microphone Shield platziert um möglichst genau die Lautstärke einstellen bzw. gegenprüfen zu können. Bei dem Experiment wurde Höhrschutz getragen, da Schalldruckpegel von bis zu 110dB getestet wurden.

```{figure} img/MojoLab/Setup_experiment.png 
:name: 01_fig_018

Versuchsaufbau für den Funktionstest
```

Getestet werden mit diesem Aufbau zwei Grenzen. Zunächst wird die Grenze der Lautstärke ermittelt. Hierfür wird die Lautsärke einen Sinustones mit einer Frequenz von f=1000 Hz langsam von 40dB Schalldruckpegel bis 111dB Schaldruckpegel erhöht und die Funktion wird beobachtet. Jede Lautstärke wird für eine Zeit t= 3 Sekunden gehalten. Die Funktion gilt als sicher vorhanden, solange ausschließlich die LED leuchtet, die in die Richtung der Geräuschquelle ausgerichtet ist. Die gewählte Frequenz wurde anhand des Datenblattes der Mikrofone gewählt. Die angegebenen Testbedigungen für die Angaben im Datenblatt beziehen sich auf eine Frequenz von f=1000 Hz.
Für Sound ausgabe wurde folgendes Pythonscript mit dem Paket PyAudio genutzt.

```{literalinclude} ../files/ProjectFiles/Soundoutput.py
:language: python
```
Aus dem Code ist zu erkennen, dass mit jedem Schleifendurchlauf die Lautsärke um 0.1 also 10% erhöht wird. Der Versuch musste allerdings in vier Durchläufen durchgeführt werden wobei die Schleife in jedem der Durchläufe einmal ausgeführt wurde. Bei jedem Durlauf wurde die Systemlautstärke des genutzten Laptops erhöht, da es nicht möglich war inerhalb einer Systemeinstellung den gesamten Lautstärkebereich von 40dB bis 111dB zu durchlaufen. Die genutzten Systemlautstärken in Prozent sind am Ende des Pythonskriptes im Kommentar zu erkennen.


<div class="video_container">
    <video width="320" height="240" controls="true" allowfullscreen="true"                        title="Testtitel">
      <source src="../_static/videos/Projekt_dB_Test-1.mp4" label="dB-Sweep"/>
    </video>
    <div class="overlay">
        <p>dB-Sweep von 40 dB bis 110 dB Schallpegel</p>
        </form>
    </div>
</div>

In dem Video ist zu erkennen, dass die Funktion sicher ab einem Schalldruckpegel von 47dB zu erkennen ist. Mit steigender Lautstärke ist die Funktion immer deutlicher, bis zu einem Schalldruckpegel von 99,9 dB laut Anzeige des Schalldruckpegelmessers. Oberhalb dieses Pegels ist zu erkennen, dass auf dem Microphone Shield alle LEDs beginnen zu leuchten und damit keine eindeutige Erkennung des Sounds gegeben ist.

Mit diesem Versuch konnten die Grenzen in Bezug auf die Lautstärke getestet werden. Die ersten Funktionstest durch Sprache und Gitarrenspiel führen zu der Annahme, dass die Grenzen nicht alleine von der Lautstärke abhängen sondern ebenfalls von der Frequenz des eingehenden Signals. Aus diesem Grund wurde ein weiteres Exeriment durchgeführt. Der Aufbau bleibt wie dargestellt in Abbildung 15. In diesem Experiment wird die Lautstärke konstant gehalten bei 91dB und die Frequenz wird angepasst. Der Grund für die 91dB Schalldruckpegel lassen sich ebenfalls im Datenblatt der Mikrofone finden, da diese ebenfalls die Testbediungen darstellen. Hierfür wird das Pythonskript insofern abgeändert, als dass lediglich eine Frequenz einmalig ausgegeben wird. Die For-Schleife wird für diesen Versuch ausgeblendet. Bei jeder Frequenz wurde die Lautstärke jedes mal auf 91dB Schalldruckpegeleingestellt, bevor das Video aufgenommen wurde.

<div class="video_container">
    <video width="320" height="240" controls="true" allowfullscreen="true"                        title="Testtitel">
      <source src="../_static/videos/Projekt_Frequenz_test.mp4" label="Frequenz Test"/>
    </video>
    <div class="overlay">
        <p>Test Frequenzmessung</p>
        </form>
    </div>
</div>

Es ist zu beobachten, dass die Funktion im unteren Frequenzbereich (440 Hz bis 700 Hz) zwar zu erkennen ist, allerdings leuchten die Richtungs LEDs nur schwach. Ein eindeutiges Erkennen der LED ist ab einer Frequenz von 710 Hz gegeben. Die höchste Frequenz bei der eine eindeutige Funktion beobachtet werden konnte war f=4937 Hz. Darüber hinaus kann beobachtet werden, dass nicht mehr die oberste LED leuchtet oder aber, dass mehrere LEDs gleichzeitig leuchten.

Das Frequenzspectrum der Audioline des Videos ist in Abbildung 18 zu sehen. Es ist zu erkennen, dass die Energiedichte bei den unteren Frequenzen erwartungsgemäß höher ist, als bei den oberen. Interessanterweise sind bei den nierigeren Frequenzen außerdem Oberwellen/Harmonische erkennbar. Die Funktion war gegeben, allerdings nich unseren aufgestellten Kriterien entsprechend.

```{figure} img/MojoLab/Spec_project.png 
:name: 01_fig_019

Spectrumsverlauf des Frequenztests
```

## Auswertung

Woran hat es jelegen? Fragt man sich am Ende ja immer woran es jelegen hat...

## VHDL-Projekte Übertragen?



```{literalinclude} ../files/meas/Experiment_01/01_Amplitudengangmessung.py
:language: python
```



[^1]: https://www.elektronik-kompendium.de/sites/bau/0209092.htm - besucht am 21.03.2022
[^2]: ANS-Abschlussbericht SoSe21 von M. Lüters, L. Lagona und Ch. Stelling.
[^3]: Die Angaben sind aus den jeweiligen Datenblättern zu entnehmen.
