# Sounderkennung mit Hilfe des Mojo V3 FPGA Boards und dem Sound

## Einleitung
Diese Projektarbeit beschäftigt sich mit der Evaluation des [Sound Erkennungs](https://alchitry.com/sound-locating-mojo) Tutorials der Webiste [Alchitry](https:E//alchitry.com/).
In diesem Tutorial nutzt Alchitry ihr eigens entwickelten Mojo v3 Board und ein Soundshield mit sieben Mikrofonen um die Richtung zu ermitteln aus der ein Ton auf das Board trifft.
Das Mojo v3 Board ist ein Board, dass für das Erlernen der Erstellung von digitalen Schaltungen mit Hilfe von Field-Programmable-Gate-Arrays (FPGA) genutzt werden kann. Wie man bereits am Namen erkennen kann bietet ein FPGA die Möglichkeit es jederzeit neu zu flashen (Field-Programmable). Dabei beschreiben wir die Hardware mihilfe einer Hardwarebeschreibungssprache wie VHDL, Verilog oder wie in diesem Beispiel mit Lucid und die Hardware nimmt entsprechend unserer Beschreibungssprache exakt die Funktion ein die wir erzielen möchten. Die Beschreibungssprache bewirkt, dass Logikgatter innerhalb des FPGA entsprechend der Funktion miteinander verknüpft werden. So kann der Mojo v3 genutzt werden um eine LED zum blinken zu bringen oder komplexere Aufgaben wie Sounderkennung.

Im Folgenden könnt ihr eine kurze Erläuterung zur Hardware finden. Die Einrichtung der Toolchain wird Schritt für Schritt erklärt. Außerdem wird der Aufbau eines Projektes erläutert und im speziellen wird auf das Sound Locator Projekt eingegangen. In diesem Zusammenhang wird auf die so genannten IP-Cores eingegangen. Da Hardware und Software offenkundig nie so funkionieren wie es der Entwickler vorgesehen hat, wird außerdem auf Probleme eingangen und wie diese Behoben werden können. Es folgt ein Vergleich über die intendierte Funktion und der tatsächlichen Funktion des Projektes wobei im Nachgang noch ein ausführlicher Versuch vorgestellt wird, der die Funktion genauer unter die Lupe nimmt.

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

Es sind in dieser Ansicht vier Ordner zu sehen. Vergeich man diese vier Ordner mit dem geforderten Pfad von Alchitry Labs aus Abbildung 12 ist zu erkennen, dass der Ordner **cores** nicht in diesem Verzeichnis existiert. Dieses Vezeichnis wurde automatisch vom Programm erstellt was die Vermutung nahelegt, dass der Aufbau des Verzeichnises Hard gecoded ist. Nach einiger Suche innerhalb des Programm Verzeichnises konnte die Codezeile die dafür Verantwortich ist nicht gefunden werden. Statdessen wurde für die Inbetriebnahme der Hardware ein Workaround gefunden. Die nötigen Dateien befinden sich alle im **coreGen** Ordner. Ist das händische erstellen des Pfades in drei schritten:

1. Umbennen des von **coreGen** zu **cores**
2. Innerhalb dieses Ordners, erstellen der jeweiligen Ordner für Decimation Filter, xfft_v8.0 und mag_phase_calculator
3. Verschieben der Dateien für den jeweiligen core in den entsprechenden erstellten Ordner.

Weitere Beschreibungen

## Funktion des Projektes

### Funktion laut Tutorial

### Funktion tatsächlich

## Versuch?

## VHDL-Projekte Übertragen?



```{literalinclude} ../files/meas/Experiment_01/01_Amplitudengangmessung.py
:language: python
```



[^1]: https://www.elektronik-kompendium.de/sites/bau/0209092.htm - besucht am 21.03.2022
[^2]: ANS-Abschlussbericht SoSe21 von M. Lüters, L. Lagona und Ch. Stelling.
[^3]: Die Angaben sind aus den jeweiligen Datenblättern zu entnehmen.
