# Sounderkennung mit Hilfe des Mojo V3 FPGA Boards und dem Sound

## Einleitung
Diese Projektarbeit beschäftigt sich mit der Evaluation des [Sound Erkennungs](https://alchitry.com/sound-locating-mojo) Tutorials der Webiste [Alchitry](https:E//alchitry.com/).
In diesem Tutorial nutzt Alchitry ihr eigens entwickelten Mojo v3 Board und ein Soundshield mit sieben Mikrofonen um die Richtung zu ermitteln aus der ein Ton auf das Board trifft.
Das Mojo v3 Board ist ein Board, dass für das Erlernen der Erstellung von digitalen Schaltungen mit Hilfe von Field-Programmable-Gate-Arrays (FPGA) genutzt werden kann. Wie man bereits am Namen erkennen kann bietet ein FPGA die Möglichkeit es jederzeit neu zu flashen (Field-Programmable). Dabei beschreiben wir die Hardware mihilfe einer Hardwarebeschreibungssprache wie VHDL, Verilog oder wie in diesem Beispiel mit Lucid und die Hardware nimmt entsprechend unserer Beschreibungssprache exakt die Funktion ein die wir erzielen möchten. Die Beschreibungssprache bewirkt, dass Logikgatter innerhalb des FPGA entsprechend der Funktion miteinander verknüpft werden. So kann der Mojo v3 genutzt werden um eine LED zum blinken zu bringen oder eben auch komplexere Aufgaben wie Sounderkennung.

Im folgenden könnt ihr eine kurze Erläuterung zur Hardware finden. Die Einrichtung der Toolchain wird Schritt für Schritt erklärt. Außerdem wird der Aufbau eines Projektes erläutert und im speziellen wird auf das Sound Locator Projekt eingegangen. In diesem Zusammenhang wird auf die so genannten IP-Cores eingegangen. Da Hardware und Software offenkundig nie so funkionieren wie es der Entwickler vorgesehen hat, wird außerdem auf Probleme eingangen und wie diese Behoben werden können. Es folgt ein Vergleich über die intendierte Funktion und der tatsächlichen Funktion des Projektes wobei im Nachgang noch ein ausführlicher Versuch vorgestellt wird, der die Funktion genauer unter die Lupe nimmt.

## [Der Mojo](https://www.adafruit.com/product/1553) [Baby](https://www.youtube.com/watch?v=c4ytuS8pVp4)

Das Mojo v3 Board ist ein preiswertes (~70€, bei [AliExpress](https://de.aliexpress.com/item/32798926767.html?spm=a2g0o.ppclist.product.2.dc57fhXPfhXPEo&pdp_npi=2%40dis%21EUR%21%E2%82%AC%2068%2C61%21%E2%82%AC%2068%2C61%21%21%21%21%21%40211b5a9616552327883654477e07b2%2164982667969%21btf&_t=pvid%3Ab5fae29b-1699-49ff-9cdf-7850da36c207&afTraceInfo=32798926767__pc__pcBridgePPC__xxxxxx__1655232788&gatewayAdapt=glo2deu)) FPGA Entwicklungsboard auf dem ein Spartan 6 FPGA eingebaut ist sowie ein ATmega32 Microprozessor der Arduino Kompatibel ist. Dieser wird im Wesentlichen für die Programmierung des FPGA genutzt. Nach der Programmierung kann der Controller als Analog-Digital Wandler eingesetzt werden. Außerdem verfügt das Board üb 84 Digitale I/O die über die Steckleisten herausgeführt sind und 8 LEDs die für allgemeine Programmierung genutzt werden können.

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

```{figure} img/AuswahlISE.png
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

Auswahl des ISE WEbPack Installationsortes
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
Bevor wir zu Problemen innerhalb dieses Projektes kommen, machen wir eine kurze Erklärung dazu, was wir alles in diesem Projekt finden können.
## Aufbau eines Projektes


## Sound Locator Projekt

### Probleme mit den cores lösen

## Funktion des Projektes

### Funktion laut Tutorial

### Funktion tatsächlich

## Versuch?

## VHDL-Projekte Übertragen?

Eine Unity Gain-Schaltung, auch Impedanzwandler oder Spannungsfolger genannt, ist ein Operationsverstärker, dessen
Ausgang mit dem invertierenden Eingang kurzgeschlossen ist {numref}`01_fig_02`. 


```{figure} img/Experiment_01/Abbildung01.png 
:name: 01_fig_01

Schematische Darstellung einer UnityGain-Schaltung.
```

Aufgrund der erwähnten *Rückkopplung* kann die Unity Gain - Schaltung als eine Regelstrecke betrachtet
werden. Systemtheoretisch ist nun das Verhältnis von Ausgang zu Eingang eine Übertragungsfunktion H(s).

$$
	U_{OUT} = A_0 \cdot (U_+ - U_-)
$$ (01_eq_01)

Aufrund der direkten Rückkopplung (ohne andere Bauteile, Kurzschluss) kann idealisiert angenommen werden, dass
$A_0$ gegen Unendlich strebt. Durch diese Annahme folgt nach dem Kürzen der das Übersetzungverhältnis für eine
Unity Gain-Schaltung:

$$
	\frac{U_{OUT}}{U_{IN}} = \frac{A_0}{1+A_0}
$$ (01_eq_02)


Mit dieser Erkenntnis könnte man nun den Nutzen der Unity Gain - Schaltung in Frage stellen. Tatsächlich ist sie aber
eine sehr nützliche Schaltung eines Operationsverstärkers. Wie bereits erwähnt, wird diese Schaltung auch
Spannungsfolger oder Impedanzwandler genannt. Die Namen werden aus der grundlegenden Funktion dieser Schaltung
abgeleitet. **Eine Unity Gain - Schaltung liefert am Ausgang die vom Eingang vorgegebene Spannung. Diese ist
lastunabhängig.** Durch diese Eigenschaft kann der Unity Gain als Spannungsstabilisator oder als Entkoppler zweier
Teilsysteme eingesetzt werden. Die Übertragungsfunktion des Unity Gain ist 1. Das heißt, dass die Ausgangsspannung
gleich der Differenz der Eingangsspannungen $U_{+}$ und $U_{-}$ ist.

$$
	\frac{U_{OUT}}{U_{IN}} = 1
$$ (01_eq_03)


```{figure} img/Experiment_01/Abbildung02.svg
:name: 01_fig_02

Messung und Simulation der Ein- und Ausgangsspannungen der Unity Gain - Schaltung* [^2]
```

Die Mess- und Simulationsergebnisse sind in {numref}`01_fig_02` dargestellt. Daraus ist ersichtlich, dass die beiden
Signale nahezu identisch sind, was einer Übertragung von 1 entspricht.


## Nicht-invertierender und invertierender Verstärker

Zwei weitere grundlegende Schaltungen des Operationsverstärkers sind die sogenannten nicht-invertierenden und
invertierenden Schaltung.

```{figure} img/Experiment_01/Abbildung03.png
:name: 01_fig_03

Nicht-invertierender Verstärker[^2]
```

Sowohl beim nicht-invertierenden als auch beim invertierenden Verstärker hängt der Verstärkungsfaktor $A_0$ vom
Verhältnis der beiden Widerstände ab. Für den nicht-invertieren Verstärker ergibt sich:

$$
	\frac{U_{OUT}}{U_{IN}} = 1 + \frac{R_2}{R_1}
$$ (01_eq_04)


Nach Ausmultiplizieren egibt sich für die Ausgangsspannung $U_{OUT}$ 

$$
	U_{OUT} = U_{IN} + \frac{R_2}{R_1} \cdot U_{IN}
$$ (01_eq_05)

Dabei ist $R_1$ der Widerstand, der am invertierenden Eingang $U_-$ anliegt und $R_2$ der zwischen dem Ausgang $U_{OUT}$
und dem invertierenden Eingang liegt {numref}`01_fig_04`. $U_{IN}$ ist die Eingangsspannung, die an einem der Eingänge des
Opamps anliegt.

```{figure} img/Experiment_01/Abbildung04.svg
:name: 01_fig_04

Messung und Simulation der Ein- und Ausgangsspannungen des Nicht-invertierenden Verstärkers[^2]
```

Aus {numref}`01_fig_04` ist ersichtlicht, dass bei einem nicht-invertierenden Verstärker die Eingangsspannung verstärkt
wird. Die Ausgangsspannung liegt mit der Eingangsspannung in Phase.


```{figure} img/Experiment_01/Abbildung05.png
:name: 01_fig_05

Invertierender Verstärker[^2]
```

Für den invertierenden Verstärker ist das Verhältnis von Ausgangsspannung zu Eingangsspannung gegeben als

$$
	\frac{U_{OUT}}{U_{IN}} = -\frac{R_2}{R_1}.
$$ (01_eq_06)

Nach Ausmultiplizieren ergibt sich für die Ausgangsspannung $U_{OUT}$

$$
	U_{OUT} = -\frac{R_2}{R_1} \cdot U_{IN}.
$$ (01_eq_07)

Nach {eq}`01_eq_07` bekommt man eine um $\pi$ gedrehte und um das Widerstandsverhältnis verstärkte Ausgangsspannung
$U_{OUT}$. Diese ist in {numref}`01_fig_06` graphisch dargestellt.

```{figure} img/Experiment_01/Abbildung06.svg
:name: 01_fig_06

Invertierender Verstärker[^2]
```


### Messtechnische Untersuchung der Grenzbereiche

Wie oben beschrieben unterliegt ein Operationsverstärker physikalischen Grenzen. Diese Grenzen sollen hier untersucht
werden.


### Bandbreite

Zunächst soll die Bandbreite und ihre Abhängigkeit von der Verstärkung untersucht werden. Die kann z.B. mit Hilfe von
Red Pitaya und der sich darauf befindenden App *Bode-Analyser* durchgeführt werden. Aufgrund von unzureichender
Datenexportmöglichkeiten, wurde an dieser Stelle ein Programm zur Bode-Plot-Darstellung entwickelt. Gundsätzlich wird
das Programm zur Messautomatisierung des Red Pitayas eingesetzt und ist ohne Weiteres nur mit diesem kompatibel:

```{literalinclude} ../files/meas/Experiment_01/01_Amplitudengangmessung.py
:language: python
```

Mit Hilfe des Programms konnten die Bandbreiten der jeweiligen Schaltung ermittelt werden. Um eine fundierte Aussage
über die Messgenauigkeit treffen zu können, wurden die Amplitudengänge der entsprechenden Schaltungen simuliert. Diese
sind zusammen mit den Messungen in `01_fig_06`{.interpreted-text role="numref"} dargestellt.

```{figure} img/Experiment_01/Abbildung07.png
:name: 01_fig_07

Vergleich der Messungen mit den Simulationen
```

Die Simulationsergebnisse zeigen prinzipiell das gleiche Tiefpassverhalten wie die Messergebnisse. Der Amplitudengang
der Messungen weicht kaum von den Simulationsergebnissen ab. Die Abweichungen liegen nur im hohen Frequenzbereich. Daher
liegen die Fehlerquellen in den kapazitiven Eigenschaften der Messspitzen und den langen Leitung. Andererseits scheinen
die Simulationsdaten des Operationsverstärkers sehr exakt zu sein, das die beiden Ergebnisse kaum von einander abweichen.

Mit Hilfe von [Matlab](https://de.mathworks.com/products/matlab.html) können die $-3\,dB$ - Grenzen der jeweiligen
gemessenen Schaltungen ermittelt werden. Es ergeben sich für:

- Unity Gain = $3,16 \cdot 10^6\,Hz$

- Nicht-invertierender Verstärker = $1,05 \cdot 10^6\,Hz$

- Invertierender Verstärker = $1,05 \cdot 10^6\,Hz$


Diese Information liefert eine wichtige Erkenntnis: Die Bandbreite der Operationsverstärker hängt scheinbar mit dem
Verstärkungsfaktor $A_0$ zusammen. Je größer der Verstärkungsfaktor, desto schmaler ist die Bandbreite des Opamps. Diese
Erkenntniss ist wichtig für die Auslegung hochfrequenter Schaltung mit einer Verstärkung. Auf eine mathematische
Herleitung der Bandbreite wird an dieser Stelle verzichtet. 


### Maximale Verstärkung

Nun soll der Verstärkungsfakor $A_0$ auf seinen maximalen und minimalen Wert untersucht werden. Abgeleitet aus
{eq}`01_eq_05` und {eq}`01_eq_06`, besteht die Abhängigkeit zwischen dem Verstärkungsfaktor $A_0$, der
Eigangsspannungdifferenz $U_{IN}$ und der Ausgangsspannung $U_{OUT}$.

```{math}
:label: 01_eq_08
U_{OUT} = A_0 \cdot U_{IN}
```


Da theoretisch die Eigangsspannung und der Verstärkungsfaktor variable sind, wird hier die Ausgangsspannung des Opamps
auf ihre Grenzen überprüft. Dazu wird ein DC-Sweep durchgeführt. Zu diesem Zweck wurde ein weiteres Programm erstellt

```{literalinclude} ../files/meas/Experiment_01/03_DCsweep.py
:language: python
```

Es soll mit Hilfe des nicht-invertierenden Verstärkers ein Gleichspannungsdurchlauf durchgeführt werden. Für die
Ausgangsspannung ergibt sich ein Spannungsverlauf nach {numref}`01_fig_07`.

```{figure} img/Experiment_01/Abbildung08.png
:name: 01_fig_08

Grenzmessung der Ausgangsspannung
```


Das Ergebnis zeigt, dass die Ausgangsspannung bei ca. $9\,V$ ihr Maximum und bei ca. $-9\,V$ ihr Minimum
aufweist. Hier wird der Zusammenhang zwischen der Ausgangsspannung und der Versorgungsspannung des Operationsverstärkers
deutlich. Die Maximalwerte der Ausgangsspannung sind gleich der Versorgungsspannung [^3]. Die Flankensteilheit ist
abhängig vom Verstärkungsfaktor.


### Fazit und Beispiele

Mit Hilfe der durchgeführten Messungen konnten die grundlegende Funktionen und die realen Grenzen eines
Operationsverstärkers aufgezeigt werden. Der Einsatz des Red Pitaya Messlabors erwies sich für hohen Frequenzbereich
eher unzuverlässig. Des Weiteren verdrehte der Red Pitaya je nach Päriodenauflösung die Phase, sodass der Datenexport
oft fehlerhaft war. Trotzdessen ist die Möglichkeit der Messautomatisierung von großem Vorteil. Daher bietet sich der
Eisatz von SCPI-fähigen Geräten bei diesen Messungen an. 

Als erstes Beispiel wird ein negativ rückgekoppelter Verstärker betrachtet. Prinzipiell ist das eine Kaskadierung
(Hintereinanderschaltung) der drei Grundschaltungen {numref}`01_fig_08`. 

```{figure} img/Experiment_01/Abbildung09.png
:name: 01_fig_09

Negativ-rückgekoppelter Verstärker
```

Hier wird statt eines Sinussignals ein Rechtecksignal eingespeist. Die Ausgänge der Schaltung sind in {numref}`01_fig_09`
graphisch dargestellt.

```{figure} img/Experiment_01/Abbildung10.png
:name: 01_fig_10

Messergebnisse der Ausgangsspannungen des negativ-rückgekoppelten Verstärkers
```

Aus der Messung ist zu entnehmen, dass die bei einem Rechteckeingangssignal, die Ausgangssignale bei den Grenzübergängen
eine Abrundung aufweisen. Dieses Phänomen bezeichnet man als [Slew Rate](https://en.wikipedia.org/wiki/Slew_rate) und
ist auf die kapazitive Eigeschaften des OPAMS zurück zu führen.

Als zweites Beispiel wird ein Instrumentenverstärker betrachtet. Dieser kann aus zwei oder drei Operationsverstärkern 
vgl. {numref}`01_fig_10`, aufgebaut werden und wird oft, aufgrund seiner Eigenschaften, in der Medizintechnik eingesetzt. 


```{figure} img/Experiment_01/Abbildung11.png
:name: 01_fig_11

Instrumentenverstärker mit drei Opamps (li.) und zwei Opamps (re.)
```

Aus der Abbildung wird deutlich, dass die Verstärkung lediglich vom Widerstand $nR$ abhängt. Dies erleichtert die
Einstellung des Instumentenverstärkers. Als Beispiel wurde ein Instrumentenverstärker aus zwei Operationsverstärkern
aufgebaut und der Ausgang gemessen. Die Messergebnisse sind in der {numref}`01_fig_11` graphisch dargestellt. 

```{figure} img/Experiment_01/Abbildung12.png
:name: 01_fig_12

Eingangs- und Ausgangssignale eines Instrumentenverstärkers aus 2 Opamps
```

[^1]: https://www.elektronik-kompendium.de/sites/bau/0209092.htm - besucht am 21.03.2022
[^2]: ANS-Abschlussbericht SoSe21 von M. Lüters, L. Lagona und Ch. Stelling.
[^3]: Die Angaben sind aus den jeweiligen Datenblättern zu entnehmen.
