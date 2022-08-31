# Sounderkennung mit Hilfe des Mojo V3 FPGA Boards und dem Sound

## Einleitung
Diese Projektarbeit beschäftigt sich mit der Evaluation des [Sound Erkennungs](https://alchitry.com/sound-locating-mojo)
Tutorials der Webiste [Alchitry](https:E//alchitry.com/). 

In diesem Tutorial nutzt Alchitry ihr eigens entwickelten Mojo v3 Board und ein Soundshield mit sieben Mikrofonen um die
Richtung einer Soundquelle zu ermitteln. 

Das Mojo v3 Board ist ein Board, dass für das Erlernen der Erstellung von digitalen Schaltungen mit Hilfe von
Field-Programmable-Gate-Arrays (FPGA) genutzt werden kann. Wie man bereits am Namen erkennen kann bietet ein FPGA die
Möglichkeit es jederzeit neu zu flashen (Field-Programmable). Dabei wird die Hardware mithilfe einer
Hardwarebeschreibungssprache wie VHDL, Verilog oder wie im vorliegenden Projekt Lucid beschrieben.Die Hardware nimmt
entsprechend der Beschreibung exakt die Funktion die mit der Logik der Beschreibung intendiert ist. Die
Beschreibungssprache bewirkt, dass Logikgatter innerhalb des FPGA entsprechend der Funktion miteinander verknüpft
werden. So kann der Mojo V3 genutzt werden um einen LED Ring anzusteuern und entsprechend die Richtung anzuzeigen aus
der ein Ton erkannt worden ist.


Im Folgenden wird die Hardware beschrieben. Im Anschluss wird die Einrichtung der Toolchain Schritt für Schritt
erklärt. Außerdem wird der Aufbau eines Projektes erläutert und im speziellen wird auf das Sound Locator Projekt
eingegangen. In diesem Zusammenhang wird auf die so genannten IP-Cores eingegangen. Da Hardware und Software
erfahrungsgemäß selten so funkionieren wie es der Entwickler vorgesehen hat, wird außerdem auf Probleme eingangen und
wie diese behoben werden können. Hiernach wird eine Übersicht über den Signalfluss gegeben, Ausgehend von der Tonquelle,
über die Aufnahme bis hin zur visuellen Darstellung. Für das bessere Verständnis wie die Signalwandlung und
Signalanalyse von statten geht wird noch einmal auf die Darstellung von Signalen im Zeit und Frequenzbereich
eingegangen. Außerdem wird der Prinzipielle Aufbau der verwendeten Mikrophone beschrieben. Als letztes wird noch die
Puls-Dichte-Modulation (PDM) erklärt, bevor es im letzten Teil dieser Arbeit um den Funktionstest und ein Ausloten der
Grenzen der Sounderkennung gehen wird.


## [Der Mojo](https://www.adafruit.com/product/1553) [Baby](https://www.youtube.com/watch?v=c4ytuS8pVp4)

```{figure} ../images/mojo/MojoBoard.png 
:name: 01_fig_025

Das Mojo Entwicklungsboard {cite:p}`sparkfun`
```

Das Mojo v3 Board, zu erkennen in [Abbildung 1]( 01_fig_025), ist ein preiswertes (~70€, bei
[AliExpress](https://de.aliexpress.com/item/32798926767.html?spm=a2g0o.ppclist.product.2.dc57fhXPfhXPEo&pdp_npi=2%40dis%21EUR%21%E2%82%AC%2068%2C61%21%E2%82%AC%2068%2C61%21%21%21%21%21%40211b5a9616552327883654477e07b2%2164982667969%21btf&_t=pvid%3Ab5fae29b-1699-49ff-9cdf-7850da36c207&afTraceInfo=32798926767__pc__pcBridgePPC__xxxxxx__1655232788&gatewayAdapt=glo2deu)
stand: Juni 2022) FPGA Entwicklungsboard auf dem ein Spartan 6 FPGA eingebaut ist sowie ein ATmega32 Microprozessor der
Arduino Kompatibel ist. Dieser wird im Wesentlichen für die Programmierung des FPGA genutzt. Nach der Programmierung
wechselt der ATmegea32 in den Slave Modus und das FPGA kann über den Mikrocontroller auf den Seriellen Port, analoge
inputs und andee Funktionen des Mikrocontrollers zugreifen. Außerdem verfügt das Board üb 84 Digitale I/O die über die
Steckleisten herausgeführt sind und 8 LEDs die für allgemeine Programmierung genutzt werden können. {cite:p}`sparkfun`


```{figure} ../images/mojo/MicrophoneShield.png 
:name: 01_fig_026

Das Microphone Shield {cite:p}`aliexpress`
```
Auf dem Microphon Shield in [Abbildung 2]( 01_fig_026) befinden sich sechs konzentrische Mikrophone, die um ein siebtes
Mikrophon in der Mitte herum auf dem Shield angebracht sind. Die Anschlüsse dieser Mikrophone erfolgt über an der
Unterseite angebrachten Stiftleiste des Shields. So kann dieses auf das Mojo Board gesteckt werden.


## Genutzte Toolchain
Um eine Hardware beschreiben zu können Bedarf es auch immer eine Toolchain die es uns möglich macht Hardware zu
flashen. Die Toolchain für die Inbetriebnahme des MOJO v3 Boards besteht aus einem Projektierungstool [Alchitry
Labs](https://alchitry.com/alchitry-labs) und einem Builder. 


Für das Mojo v3 board bedarf es das [ISE
WebPack](https://www.xilinx.com/products/design-tools/ise-design-suite/ise-webpack.html) von
[Xilinx](https://www.xilinx.com/).

Alchitry Labs wird hierbei genutzt um das Projekt zu organisieren und die unterschiedlichen Teile des Projektes zu
beschreiben. Der Builder ISE WebPack übersetzt letzten Endes die Beschreibung aus den unterschiedlichen Bestandteilen
des Projektierungstools in die eigentliche Hardware innerhalb des FPGA.

Das genutzte Betriebssystem in diesem Projekt ist Linux [Debian 11](https://www.debian.org/News/2021/20210814). Im
folgenden Kapitel wird die Einrichtung der Toolchain ausführlich beschrieben.



### Installation des ISE WebPack
Vor der Installation von Alchitry Labs ist es ratsam zunächst das ISE WebPack zu installieren. Auch eine Überprpfung der
Partitionierung des Rechners und des freien Festplattenspeicher ist ratsam, da das Archiv das aus dem Internet geladen
wird bereits 6,5GB groß ist. Für die Installation benötigt das ISE WebPack weitere 18GB Speicherplatz. Nachdem
sichergestellt wurde, dass ausreichend Speicherplatz für die Installation vorhanden ist kann das
Installationsverzeichnis von der [Website](https://www.xilinx.com/downloadNav/vivado-design-tools/archive-ise.html)
heruntergeladen werden. Hier wird die die Version 14.7 ausgewählt. Unter diesem Punkt wird die ISE Design Suite - 14.7
Full Product ausgewählt und heruntergeladen. Es muss an dieser Stelle erwähnt werden, dass ein Nutzeraccount benötigt
wird um diese Software herunter zu laden und zu installieren.

Nach dem Download geht es weiter zur eigentlichen Installation. Als erstes wird das Installationsverzeichnis
entpackt.Mit Hilfe des Terminals und des change directory Befehls **cd** wird in das Verzeichnis gewechselt in dem das
heruntergeladene Verzeichnis gespeichert ist.(Hier: Downloads):


Terminalausgabe
:       mojo@fpga:~$ cd Downloads/

Im Verzeichnis wird das Archiv als nächstes entpackt.:

Terminalausgabe
:       mojo@fpga:/Downloads/$ tar -xvf Xilinx_ISE_DS_Lin_14.7_1015_1.tar

Die Optionen **xvf** beschreiben, dass das Archiv entpackt werden soll (x), dass die verarbeiteten Dateien ausführlich
aufeglistet werden (v) und dass das Archiv aus dem aktuellen Verzeichnis genommen werden soll (f).{cite:p}`Ubuntuusers`
Nach diesen Vorarbeiten kann das Setup des Programmes gestartet werden. 


:::{note}
Die Installation des ISE WebPack sollte nach Möglichkeit mit Adminrechten ausgeführt werden. Das erleichtert im weiteren
Verlauf die Nutzung mit der weiteren Toolchain.
:::

Die Installation kann mit dem folgenden Befehl gestartet werden:

Terminalausgabe
:       mojo@fpga:/Downloads/Xilinx_ISE_DS_Lin_14.7_1015_1$ sudo ./xsetup

In [Abbildung 3]( 01_fig_01) sind die Geschäftsbedingungen aufgeführt, denen während der Installation zugestimmt werden müssen.

```{figure} ../images/Terms_and_conditions.png 
:name: 01_fig_01

Zustimmung zu den Terms and Conditions geben
```

Nach der Zustimmung wird in [Abbildung 4]( 01_fig_02) gezeigt, welches Produkt für die Installation ausgewählt werden
muss.

```{figure} ../images/mojo/AuswahlISE.png
:name: 01_fig_02

Auswahl des ISE WebPACKs für die Installation
```

Im Folgefenster werden alle Hacken gelassen wie der Installationswizard vorschlägt.Eine Nutzung mehrer CPU-Kerne ist
sinnvoll um die Installationszeit zu verringern.


Während der Installation kann die Zeit genutzt werden um eine entsprechende Lizenz auf
[Xlilinx](https://www.xilinx.com/member/forms/license-form.html) zu erstehen. Nach Eingabe der persönlichen Daten wird
die Lizenz für das ISE WebPack ausgewählt und die Lizenzdatei kann heruntergeladen werden und dem Programm hinzugefügt
werden.

Beim erstmaligen Start öffnet sich zunächst der Lizenzmanager hier wird nochmal auf das Erlangen der Lizenz hingewiesen
wie in [Abbildung 5]( 01_fig_03) dargestellt.


```{figure} ../images/mojo/Licence_Manager_1.png 
:name: 01_fig_03

Möglichkeit zur Auswahl des Lizenztypes
```

Wurde die Lizenz heruntergeladen kann die unter "Manage License" hinzugefügt werden. Innerhalb des Dialogfeldes
[Abbildung 6]( 01_fig_04) kann zum Speicherort der Lizenzdatei navigiert werden.


```{figure} ../images/mojo/Licence_Manager_2.png 
:name: 01_fig_04

Unter Load Licence wird der Speicherort der Lizenzdatei ausgewählt
```

Nachdem das ISE WebPack 

1. heruntergeladen

2. installiert

3. gestartet und

4. lizensiert 

wurde, wird im nächsten Schritt die Programmierumgebung installiert werden.


### Installation von Alchitry Labs
Den Großteil der Installation der Toolchain ist zu diesem Zeitpunkt bereits abgeschlossen. Das Einrichten von Alchitry
Labs stellt sich wesentlich leichter dar, als es bei der Xilinx Software der Fall war.

Die Software ist auf der (Website)[https://alchitry.com/alchitry-labs] von Alchitry Labs unter den Reiter Alchitry Labs
zu finden. Die Download Links sind am unterhalb der Abbildung vom Programm zu finden.Für dieses Projekt wurde die Linux
version genutzt. Die Linux Version bietet bei der Installation deutliche Vorteile in der Einrichtung im Vergleich zu
Windows Version, da diese für Windows 10 und 11 nicht mehr optimiert ist. Nach dem Download von knapp 18 MB muss das
geladene Archiv erneut ausgepackt werden. Hierfür kann der gleiche Befehl mit geändertem Dateinamen genutzt werden.


Terminalausgabe
:       mojo@fpga:/Downloads/$ tar -xvf alchitry-labs-1.2.7-linux.tar 

Nach der Installation wird in den Unterordner "alchitry-labs-1.2.7" navigiert und das Programm mit folgendem Befehlt gestartet:
Terminalausgabe
:       bash alchitry-labs


Ist die Installation bisher erfolgreich und korrekt öffnet sich nun die Programmierumgebung. Die Software erfragt beim
ersten Starten den Installationsort des Builders. Im Programmfenster kann über "Settings" und "ISE Location" über ein
Dialogfeld der Installationsort des ISE WEbPack ausgewählt werden.( siehe: [Abbildung 7]( 01_fig_05)). Hierbei ist
darauf zu achten, dass der Ordner mit der entsprechenden Versionsnummer ausgewählt wird ( hier: 14.7). Die Software gibt
entsprechende Hinweise innerhalb des Dialoges.


```{figure} ../images/mojo/Alchitry_Licence.png 
:name: 01_fig_05

Auswahl des ISE WebPack Installationsortes
```

Ab diesem Zeitpunkt ist es möglich Projekte zu öffnen und zu erstellen.


### Öffnen des Projektes
Beim ersten Starten von Alchitry Labs startet automatisch ein Dialog, in dem erfragt wird ob bereits ein Projekt
vorhanden ist. Siehe: [Abbildung 8]( 01_fig_06)

```{figure} ../images/mojo/First_Start.png 
:name: 01_fig_06

Erste Projektauswahl
```

Durch die Auswahl "No" wird der User in ein weiteres Dialogfenster geführt, indem dieser ein Projekt erstellen kann.

Dieses Dialogfenster ist in [Abbildung 9]( 01_fig_07) zu sehen. Im Feld "Project Name:" wird der Wunschname des neuen
Projektes eingegeben. Im folgenden Reiter "Workspace" steht die Arbeitsumgebung. Hier werden die Projekte abgespeichert
und die Projektierungsumgebung erstellt hier die nötigen Dateien für das Builden des Projektes. Im dritten Reiter wird
das entsprechende Board ausgewählt. Für dieses Projekt ist das der Mojo Board. Das Programm erstellt hier für
automatisch die Bezüge zu Hardware, damit das Projekt funktionsfähig gebaut werden kann. Die Sprache ("Language") die
ausgewählt werden muss um ein funktionierendes Beispielprojekt laden zu können ist hier das programmeigene Lucid. Es ist
ebenfalls möglich innerhalb der Umgebung in Lucid zu coden, allerdings gibt es für Lucid keine Beispielprojekte. Die
Beispielprojekte sind auschließlich in Lucid geschrieben. Über ein Dropdown Menüs ist es nun möglich das Sound Locator
Projekt auszuwählen und zu laden.


```{figure} ../images/mojo/New_Project.png 
:name: 01_fig_07

Einstellungen zum öffnen des Sound locator Beispiels
```


Durch einen letzten Mausklick auf den Button "Create" wird das Beispielprojekt erstellt. Im nöchsten Abschnitt wird
beschrieben welche Arten von Files man innerhalb des Projektes finden kann und was diese tun. Die Inbetriebnahme des
Projektes wird im darauffolgenden Kapitel beschrieben.


## Aufbau eines Projektes

- <u>**Source**</u>

Der erste Teil innerhalb dieses Projektes sind die Source-Dateien auch Module genannt. Diese beschreiben alle Ein- und
Ausgänge der unterschiedlichen Hardware. Die im Projekt genutzten Source Dateien sind in [Abbildung 10]( 01_fig_08)
dargestellt. Für das Sound Locator Projekt wären das zum einen die Hann Funktion, der LED-Ring, das mojo-top modul,
welches das Mojo Board beschreibt, die pdm-mics zur Definition der Mikrophone und das sound_locator modul in der der
Delay zur Sound Erkennung ermittelt wird.


```{figure} ../images/mojo/Source.png 
:name: 01_fig_08
	
Die Source-Dateien findest du zu oberst im Projekt
```

- <u>**Components**</u>

Components sind teils vorinstallierte teils selbst geschriebene Bausteine, die für spezielle Funktionen verwendet werden
können. Im vorliegenden Projekt finden sich vielfach Lucid-Files, **.luc**. Diese wurden vom Entwickler erstellt, können
sich aber auch in der Xilinx Umgebung finden. Die in diesem Projekt genutzten sind in [Abbildung 11]( 01_fig_09)
dargestellt.


```{figure} ../images/mojo/Components.png 
:name: 01_fig_09

Als Zweites findest du die Components im Projekt
```
- <u>**Cores**</u>

Die Cores oder auch IP-Cores sind vorgefertigte weitestgehend geteste Bausteine die spezielle Aufgaben erledigen können
und werden von Xilinx mitgeliefert. IP steht für Intellectual Property also Geistiges Eigentum. Diese Bausteine sind
weitestgehend spezifiziert und bieten somit den Vorteil, dass diese in einem Design mehrfach wiederverwendet werden
können. Fertige IP-Cores gibt es von Buskommunikation über digitale Signalverarbeitung wie FFT bis hin zu Multimedia wie
Ethernet oder Bluetooth. In diesem Projekt gibt es drei IP cores. Zum einen den decimation Filter, welcher die
einkommende PDM Signale downssampled um die Informationen mit verringerter Samplefrequenz zu extrahieren. Als zweites
gibt es den mag_phase_calculator der aus den einkommenden Signalen die Amplitude und die Phase errechnet und als letztes
den xfft_v8_0-core der die FFT auf die einkommenden Signale anwendet.


```{figure} ../images/mojo/Cores.png 
:name: 01_fig_010

Der dritte Reiter beinhaltet die IP-Cores
```
- <u>**Constraints**</u>


Daregstellt in [Abbildung 13]( 01_fig_011)sind die drei User-constraints-files von debugger, microphone shield und vom
mojo board.In diesen Dateien werden die Timing-Eigenschaften sowie die Pineigenschaften und physikalischen Eigenschaften
und Grenzen beschrieben. Diese Dateien werden benötigt um dem synthetisierungs Programm (ISE WebPack) die letzten
Informationen zu geben wie das Projekt erstellt werden soll.


```{figure} ../images/mojo/Constraints.png 
:name: 01_fig_011

Als letztes gibt es noch die Constraints
```

## Sound Locator Projekt

Im Vorfeld wurden bereits die Hardware sowie die unterschiedlichen Funktionsblöcke die das Sound Locator Projekt besitzt
beschrieben. Die Dokumentation des Projektes von O'Reilly verspricht ein Plug in Play mit der Hardware. Die
Untersuchungen innerhalb dieses Projekts haben jedoch gezeigt, dass noch weitere Probleme gelöst werden müssen, bevor
das Projekt auf den FPGA geflasht werden kann. In diesem Abschnitt werden diese Probleme genauer beleuchtet, wie diese
zu lösen sind und schauen uns im Anschluss die Funktion der Sound-Erkennung an.


### Probleme mit den IP-cores lösen

Erinnern wir uns an die IP-Cores die im letzten Abschnitt beschrieben wurden. Sie stellt eine fertige Funktionseinheit
wie zum Beispiel den Decimation-Filter dar, die nach Definition seiner Funktion zum FPGA Design hinzugefügt werden
kann. Ausgerechnet diese IP-Cores machen beim ersten Flash-Versuch Probleme und es kommt folgende Meldung in [Abbildung
14]( 01_fig_012).


```{figure} ../images/mojo/Fehlermeldung_Cores.png 
:name: 01_fig_012

Angezeigte Fehlermeldung beim ersten Flashversuch
```

Alchitry Labs zeigt an, dass es die Dateien für die IP-Cores nicht lesen kann. Schaut man in die Ordner Struktur und
vergleich diese mit dem agezeigten Pfad so scheint sich hier ein Fehler bei der Programmierung der Software
eingeschlichen zu haben, der es zunächst unmöglich macht das Projekt zu bauen.



> <span style="color:green">**erik@erik:**</span><span style="color:blue">**~/alchitry/SoundLocator**</span>$ ls
> 
> <span style="color:blue">**constraint**</span>  <span style="color:blue">**coreGen**</span> SoundLocator.alp 
<span> style="color:blue">**source**</span>  <span style="color:blue">**work**</span>


Es sind in dieser Ansicht vier Ordner zu sehen. Vergeich man diese vier Ordner mit dem geforderten Pfad von Alchitry
Labs aus [Abbildung 12]( 01_fig_012) ist zu erkennen, dass der Ordner **cores** vergeblich in diesem Verzeichnis zu
suchen ist. Dieses Vezeichnis wurde automatisch vom Programm erstellt was die Vermutung nahelegt, dass der Aufbau des
Verzeichnises Hard gecoded ist. Nach einiger Suche innerhalb des Programmverzeichnises konnte die Codezeile die dafür
verantwortich ist nicht gefunden werden. Statdessen wurde für die Inbetriebnahme der Hardware ein Workaround
gefunden. Die nötigen Dateien befinden sich alle im **coreGen** Ordner. Ist das händische erstellen des Pfades in drei
schritten:

1. Umbenennen des  **coreGen** zu **cores**.

2. Innerhalb dieses Ordners, erstellen der jeweiligen Ordner für **Decimation Filter**, **xfft_v8.0** und
   **mag_phase_calculator**.

3. Verschieben der Dateien für den jeweiligen core in den entsprechenden erstellten Ordner.


Nachdem diese Schritte durchgeführt wurden kann das Projekt gebaut werden und ermöglicht es uns das Mojo Board zu
flashen und die Funktion des Programmes zu testen.


## Funktionsprinzip des Projektes

In diesem Kapitel wird die Funktion des gesamten Aufbaus evaluiert. Innerhalb dieses Kapitels wird zunächst das
Funktionsprinzip des Projektes erläutert. In [Abbildung 15]( 01_fig_013) ist der Signalfluss der Sounderkennung
dargestellt. Alle Dargestellten Blöcke werden innerhalb dieses und des des nächsten Abschnitts erläutert. Zunächst steht
ein Ton in Form einer Sinuswelle an. Diese besteht nicht aus nur einer Frequenz wie in [Abbildung 15]( 01_fig_013)
dargestellt, sondern setzt sich aus verschiedenen Frequenzen zusammen. Dieses Frequenzspektrum wird ebenfalls dargestelt
und erläutert. Die analoge Sinuswelle wird durch ein Wandlungssystem in die digitale Domäne Übertragen. Hier sind es so
genannte digitale MEMS PDM Mikrofone. Die ausgegebene PDM wird ebenfalls theoretisch erläutert und messtechnisch
aufgenommen. Das Signal Processing wird vom FPGA übernommen. Hier findet die Auswertung der einkommenden Signale statt
und damit die Erkennung. Am Ende steht die optische Ausgabe der erkannten Richtung vom FPGA.



```{figure} ../images/mojo/SignalFlow.png
:name: 01_fig_013

Übersicht Signalfluss
```

Der erste Block des Signalflusses enthält die akustische Welle. Diese Schallwelle entsteht durch das komprimieren und
dekomprimieren der Luft. In der Physik wird eine ideale winzige Punktschallquelle angenommen von der aus kugelförmig die
Schallwellen in alle Richtungen abgestrahlt werden. Diese Punktquelle und die Ausbreitung der Schallwellen von dort aus
sind in [Abbildung 16]( 01_fig_014) dargestellt. Diese Wellenfronten in verbindung mit den Strahlen kennzeichnen die
Richtung der Schallwellen. Wellenfronten sind hierbei Flächen, bei der die Luftteilchen wertgleiche Auslenkungen
besitzen aufgrund der erzeugten Schwingung {cite:p}`Halliday`.


```{figure} ../images/mojo/Schallwellen.png
:name: 01_fig_014

Zweidimensionale Darstellung zur Ausbreitung einer Schallwelle {cite:p}`Halliday`
```

Wie bereits erwähnt verbreiten sich diese Schallwellen kugelförmig und dreidimensional im Raum und werden darum auch
sphärische Wellen genannt. Je weiter man sich jedoch von der Punktquelle entfernt umso geringer wird diese Krümmung und
die Schallwelle kann als Ebene verstanden werden. Diese Wellen werden dann ebene oder planare Wellen
genannt. {cite:p}`Halliday`


Die Intensität der Schallwelle ist abhängig von der Amplitude der Schallwelle. Die Intensität verringert sich
quadratisch in Abängigkeit zum Abstand zur Tonquelle:

$$
I = \frac{P_{s}}{4 \, \pi \, r^{2}}
$$


Wobei I die Intensität der Schallwelle ist P die Leistung durch die Schallwelle und r der Abstand zur
Schallquelle. {cite:p}`Halliday`


Da das menschliche Ohr ein breites Spektrum an Intensitäten wahrnehmen kann wurde hierfür die Dezibel Skala
eingeführt. Die Angabe in der Dezibelskala wird als Schallpegel oder Schalldruckpegel bezeichnet und kann folgendermaßen
berechnet werden:

$$
\beta = 10 dB \cdot \frac{I}{I_{0}}
$$


Wobei $\beta$ der resultierende Schalldruckpegel ist. $I$ beschreibt die Intensität der gemessenen Schallwelle und $I_{0}$
beschreibt einen standardisierten Referenzwert für die Intensität ($I_0 = 10^{-12} \frac{W}{m^{2}}$). {cite:p}`Halliday`


Um einen Ton zu erzeugen muss diese (De-) Komrimierung der Luft mit einer definierten Frequenz erzeugt werden. Um den
Kammerton C zu erzeugen muss ein Ton mit einer Frequenz von $ f=440 Hz $ erzeugt werden. Idealerweise sähe dieser Ton
aus wie in [Abbildung 17](01_fig_015) dargestellt.


```{figure} ../images/mojo/Sine_Only.png
:name: 01_fig_015

Sinuswelle mit $f$=440 Hz
```

Aus dieser Darstellung wäre es ein einfiaches die Frequenz des Signals hinaus zu lesen und damit das Signal zu
rekonstruieren. In der realen Welt ist die Wahrheit häufig nicht so eindeutig und das eintreffende Signal auf das
Mikrofon ist in der Regel mit einem Rauschen belegt.


```{figure} ../images/mojo/Noisy_Source_Signal.png
:name: 01_fig_016

Sinuswelle mit $f$=440 Hz überlagert mit Rauschen
```


In [Abbildung 18]( 01_fig_016) ist dieses Signal dargestellt. Im dargestellten Zeitbereich ist es nicht einzuschätzen
welches Signal das Hauptsignal ist und welche Frequenz es hat.

Um die Reaktion der Hardware auf die eintreffenden Töne besser einschätzen oder erklären zu können ist es deshalb
interessant das Signal außerhalb des Zeitbereichs zu betrachten und das ganze mit Hilfe einer
Fast-Fourier-Transformation (FFT) in den Frequenzbereich zu überführen und ein Frequenzspektrum zu erzeugen.

Das Frequenzspektrum des Signals aus [Abbildung 18](01_fig_016) ist in [Abbildung 19](01_fig_017) zu finden.

```{figure} ../images/mojo/FFT_Source.png
:name: 01_fig_017

Frequenzspektrum des verrauschten Signals
```

An der Y-Achse ist die Amplitude der Frequenzanteile aufgetragen und auf der X-Achse sind die unterschiedlichen
Frequenzen dargestellt. Sie zeigt uns aus welchen Frequenzanteilen das Ausgangssignal zusammengesetzt ist. Das Rauschen
mit seinem vielen Frequenzen, die gleichermaßen im Signal enthalten sind verschwinden förmlich im Gegensatz zum
eigentlichen Signal. Mit Hilfe dieser Methode ist es uns möglich auch aus im Zeitbereich verrauschten oder uneindeutigen
Signalen das gesuchte Signal herauszufinden bzw zu erfahren, welche Frequenzen im Signal erkannt werden.


Nachdem geklärt wurde welche Eingangssignale zu erwarten sind kann der Fokus auf die akustische Aufnahme gerichtet
werden. Auf dem Microphoneshield sind sieben Mikrophone mit der Bezeichnung SPK0415HM4H zu finden. Diese Mikrophone sind
digitale Mikro-Elektronisch-Mechanische Systeme (MEMS). Das bedeutet, dass durch Herstellungsmethoden der
Halbleiterindustrie ein Bauteil erzeugt wurde, dass sowohl elektronische als auch mechanische Eigenschaften vereint. Wie
in [Abbildung 20](01_fig_018) zu erkennen ist, besitzt ein solches Mikrofon einen Sound Port, dies ist eine Öffnung im
Gehäuse (Can) des Bauteils. Hier kann der Ton auf die eigentliche Struktur auftreffen. Die Öffnung ist hier oben kann
bei anderen Mikrofonen aber auch am Boden des Gehäuses sein. Darunter befindet sich eine Membran (Glob Top Molding) über
einer Halbleiter Trägerstruktur. Die Membran und die Trägerstruktur sind zwei Gerade, gegenüberliegende Flächen zwischen
denen ein Material zu finden ist das als Dielektrikum verstanden werden kann. Dies ist nichts weiter als ein Kondensator
mit einer dazugehörigen Kapazität. Beim Auftreffen von Schall gerät die Membran in Bewegung, was die Kapazität des
Kondensators ändert. Diese Änderung wird von der Anwender Spezifischen Schaltung (ASIC) erkannt und entsprechend
verarbeitet. Ob ein Analoges oder Digitales Signal ausgegeben wird entscheidet sich hier. Entweder das Analoge Signal
wird vom ASIC bereit gestellt oder ein weiterer Wandler (Transducer) befindet sich innerhalb des Systems, welches dieses
analoge zu einem digitalen Signal wandelt. Bei den digitalen Signalen kann es sich um Pulse-Code-Modulierte (PCM) oder
auch um Puls-Dichte-Modulierte Signale handeln. Puls-Code-Modulierte Signale werden hier nicht weiter behandelt, sollen
aber der Vollständigkeit halber Erwähnung finden. {cite:p}`DigiMEMS`


```{figure} ../images/mojo/MEMS.png
:name: 01_fig_018

Aufbau eines MEMS Mikrofons {cite:p}`DigiMEMS`
```

In diesem Projekt wurden Mikrofone verwendet, die Puls-Dichte-Modulierte (PDM) Signale verwenden. Bei der PDM wird die
Information der Amplitude des Signals über die Puls-Dichte dargestellt. Das heißt, dass eine Häufung on logischen High
(1) Pegeln eine hohe Amplitude und eine Häufung von logischen Lows (0) eine niedrige Amplitude bedeutet. Bei der
Wandlung durch ein MEMS Mikrophon kann die das PDM eines Sinussignals folgendermaßen aussehen.


```{figure} ../images/mojo/Pulse_Density.png
:name: 01_fig_019

Übersicht zwischen analogem Signal und Puls-Dichte-moduliertem Signal {cite:p}`Devzone`
```


In [Abbildung 21](01_fig_019) ist wie beschrieben zu erkennen, dass mit höhren Amplituden vermehrt ein High Signal zu
finden ist. Das PDM kodierte Signal ist der letze Punkt, bevor die Verarbeitung des FPGA beginnt. Als nächstes kann die
Funktion des Projektes betrachtet werden.


Für die Funktion des Projektes werden zunächst Annahmen vom Autor getroffen. Die wichtigste Annahme ist, dass die
Richtung des Tons nur in einem zweidimensionalen Raster horizontal zum Mojo Board auf das FPGA auftreffen darf. Das ist
dem physikalischen Aufbau des Microphone Shields geschuldet, da alle Mikrophone auf einer Ebene verbaut sind. Außerdem
wird angenommen, dass es sich bei den auftreffenden Schallwellen um eine eine gerade Wellenfront handelt. Das heißt,
dass sich jeder Punkt einer Welle mit der gleichen Geschwindigkeit ausbreitet.Die letzte Annahme ist, dass jede Frequenz
eines Soundsamples aus einer einzigen Richtung kommt {cite:p}`Rajewski`.


Die Sounderkennung mit dem Mojo errechnet sich die Richtung aus der der Sound auf ihn trifft aus der Phasenverschiebung
zwischen den äußeren und dem zentralen Mikrophon. Die auf den Mikrophonen auftreffende Frequenz wird in ein PDM
umgewandelt und dieses PDM Signal wird simultan vom FPGA abgetastet. Auf diese Fragmente wird eine FFT durchgeführt,
wodurch das Signal von der Zeit- in die Frequenzdomäne überführt wird. Als Ausgabe aus der FFT erhält man nun für jedes
Fragment eine komplexe Zahl. Bestehend aus dem Realteil, der die Amplitude des eingehenden Signals darstellt und dem
Imaginärteil, der die Phase des eingehenden Signals darstellt. Diese können in einem Koordinatensystem aufgetragen
werden. In [Abbildung 22](01_fig_020) ist beispielfhaft für drei Mikrophone das Prinzip dargestellt. Die schwarzen
Kreise stellen die Position von drei Mikrofonen des Mojos dar. Ihre Koordinaten sind in den Klammern dargestellt. Der
Mittelpunkt des Koordinatensystems ist ebenfalls als Koordinate des zentralen Mikrophons zu verstehen. In blau in der
oberen linken Ecke ist die Richtung dargestellt aus der ein Ton auf die Mikrophone trifft. Das Auftreffen bewirkt eine
Verzögerung (Delay) der jeweiligen äußeren Mikrophone im Vergleich zum mittleren Mikrofon. Mithilfe dieses Delays
bzw. mit der Phasenverschiebung zueinander ( die Verzögerung ist lediglich der quotient aus Phasenverschiebung und
Frequenz wodurch diese beiden Werte proportinal zueniander sind) und der Positionsvectoren der unterschiedlichen
Mikrophone kann nun die Richtung des Tons bestimmt werden. Hierzu werden die Ortsvektoren mit dem errechneten Delay
Skaliert, wodurch die violetten skalierten Vektoren entstehen. Durch Vektoraddition dieser Vektoren kann ein
Summenvektor erstellt  werden, der in die Richtung der Tonquelle zeigt (gelb){cite:p}`Rajewski`.


```{figure} ../images/mojo/SoundirectionPrinciple.png
:name: 01_fig_020

Vektorielle Darstellung des Erkennungsprinzips {cite:p}`Rajewski`
```


### Funktionstest

Das oben beschrieben Funktionsprinzip wird im nächsten Abschnitt getestet. Für den ersten Test wird der Mojo auf einem
Holztisch platziert und es wird das Alphabet durchgesprochen. Die Lärmquelle ist in diesem Video von Links und die
Quelle ist auf der horizontal verschoben zum Mojo um die Funktion zu gewährleisten. Es ist zu erkennen, dass bei den
S-Lauten (die Buchstaben C, S, X, Z) führen dazu, dass mehr als nur eine LED leuchtet. Alle anderen Buchstaben haben
insgesamt eine eindeutige Antwort des Mojos verursacht. 


<div class="video_container">
	<video width="320" height="240" controls="true" allowfullscreen="true" title="Testtitel">
		<source src="../mov/Alphabet.mp4" label="Alphabet"/>
	</video>
    <div class="overlay"> <p>Alphabet Test</p> </form>  </div>
</div>


Betrachtet man zu den Beobachtungen nun das Frequenzsspektrum zu den ersten sieben Buchstaben des Alphabets ist zu
erkennen, dass der größete Schallpegel bei Frequenzen zwischen $f$=60 Hz und $f$=400 Hz zu finden ist. Der Buchstabe "C"
ist in dieser [Abbildung 23]( 01_fig_021) der dritte Balken von links. Das Diagramm ist ein
Frequenz-Zeit-Diagramm. Hierbei sind auf der Y-Achse die unterschiedlichen Frequenzanteile aufgeführt. Auf der X-Achse 
findet sich die Zeit der Audiospur. Die Codierung des Schallwellenpegels ist in der Helligkeit der der Balken zu
erkennen. Diese Darstellung war die beste für diese Anwendung, da durch die Art des Versuchs verschiedene Töne zu
unterschiedlichen Zeiten auftreffen. Dieses Diagramm bietet eine übersichtliche Darstellung für diese Zwecke. Für den
Buchstaben C ist zu erkennen, dass zu Beginn des Buchstaben ein höherer Schalldruckpegel zu erkennen ist. Diese reicht
von einer Frequenz von $f$=4 kHz bis zu über $f$=16 kHz. Interessanterweise ist eine konträre Beobachtung beim
Buchstaben "F" zu erkennen. Der zweite Balken von rechts hat zu Beginn des Buchstabens ein ähnliches Frequenzmuster wie
die anderen. Nach einer kurzen Zeit verteilt sich der Schalldruckpegel gleichmäßig auf eine größere Bandbreite an
Frequenzen. Hier konnte jedoch eine gute Funktion des Mojo beobachtet werden. Der Schalldruckpegel bei diesem Versuch
konnte etwa zwischen $\beta$=60 dB und $\beta$=70 dB mit dem Schalldruckpegelmesser gemessen werden.

$$
\frac{A}{B}
$$


```{figure} ../images/mojo/AlphaG.png 
:name: 01_fig_021

Frequenzspektrum für die Buchstaben A bis G
```

Nach dieser Beobachtung ist ein weiterer grundsätzlicher Funktionstest mit einer anderen Tonquelle durchgeführt
worden. In diesem Funktionstest wurde der Song "Come as you are" von Nirvana angespielt um die Reaktion vom Mojo zu
testen. Die Quelle des Geräusches ist in diesem Video unterhalb des Mojo boards. Es ist zu erkennen, dass die unterste
LED am hellsten leuchtet und die Richtung damit erkannt wird. Allerdings ist ebenfalls zu sehen, dass auch LEDs auf der
anderen Seite des Kreises aufleuchten.


<div class="video_container">
    <video width="320" height="240" controls="true" allowfullscreen="true" title="Testtitel">
      <source src="../mov/Come_as_you_are.mp4" label="Gitarren Spiel"/>
    </video>
    <div class="overlay">
        <p>Test mit Gitarrenspiel</p>
        </form>
    </div>
</div>


Das Frequenzspektrum ist in der nachfolgenden [Abbildung 24]( 01_fig_022) zu erkennen. Die Energie der Frequenzen
scheint hier weniger breit gefächert zu sein als bei dem vorangegangenen Funktionstest. Die Funktion konnte auch hierbei
im Wesentlichen nachgewiesen werden, auch wenn es bei diesem Test zum leuchten der gegenüberliegenden LED gekommen
ist. Der Schalldruckpegel der während des Versuchs gemsesen wurde lag bei rund $\beta$ = 70 dB.


```{figure} ../images/mojo/comeasyouare.png 
:name: 01_fig_022

Frequenzspektrum des Intros von "Come as you are" von Nirvana
```

Die Funktionstest konnte die prinzipielle Funktion nachweisen. Die Frage nach den Grenzen der Erkennung ist allerdings
hiermit noch nicht geklärt. Um die Grenzen der Sounderkennung zu ermitteln wurde sich in diesem Experiment dazu
entschieden dieses im privaten Wohnzimmer durchzuführen und nicht in einem speziell eingerichtetem Schallarmen Raum, da
die Sounderkennung dazu dienen soll Geräuschquellen zu unterscheiden und die Richtung des gewollten Sounds zu
ermitteln. Der Aufbau für dieses Experiments ist in den vorangegangenen Videos schon erkennbar ist schematisch jedoch
nochmal in [Abbildung 25]( 01_fig_023) zu erkennen. Das Mojo Board mitsamt des Microphone Shield ist im Zentrum des
Aufbaus platziert. Die Soundquelle ist eine Bluetoothbox der Firma Bose und wurde 10 cm oberhalb des Mojoboards
aufgestellt worden. Hier wird ein Sinussignal einer definierten Frequenz und Lautstärke ausgegeben. Um die Lautsärke in
Decibel (dB) gegenprüfen zu können, wird ein Schalldruckpegel Messgerät auf der gleichen Höhe wie das zentrale Mikrophons auf dem
Microphone Shield platziert um möglichst genau die Lautstärke einstellen bzw. gegenprüfen zu können. Bei dem Experiment
wurde Höhrschutz getragen, da Schalldruckpegel von bis zu $\beta$=111 dB getestet wurden.


:::{note}
Bei so einem Versuch muss immer ein Gehörschutz getragen werden! Solche Lautstärken können das Hörvermögen verringern
und gesundheitsschädlich sein!
:::


```{figure} ../images/mojo/Setup_experiment.png 
:name: 01_fig_023
	
Versuchsaufbau für den Funktionstest
```

Getestet werden mit diesem Aufbau zwei Grenzen. Zunächst wird die Grenze der Lautstärke ermittelt. Hierfür wird die
Lautsärke einen Sinustones mit einer Frequenz von $f=1000 Hz$langsam von $/beta= 40 dB$ Schalldruckpegel bis 111dB
Schaldruckpegel erhöht und die Funktion wird beobachtet. Jede Lautstärke wird für eine Zeit $t= 3$ Sekunden
gehalten. Die Funktion gilt als sicher vorhanden, solange ausschließlich die LED leuchtet, die in die Richtung der
Geräuschquelle ausgerichtet ist. Die gewählte Frequenz wurde anhand des Datenblattes der Mikrofone gewählt. Die
angegebenen Testbedigungen für die Angaben im Datenblatt beziehen sich auf eine Frequenz von $f=1000 Hz$.

Für die Soundausgabe wurde folgendes Pythonscript mit dem Paket PyAudio genutzt.


```{literalinclude} ../files/math/mojo/Soundoutput.py
:language: python
```

Aus dem Code ist zu erkennen, dass mit jedem Schleifendurchlauf die Lautsärke um 0.1 also 10% erhöht wird. Der Versuch
musste allerdings in vier Durchläufen durchgeführt werden wobei das Skript in jedem der Durchläufe einmal ausgeführt
wurde. Bei jedem Durlauf wurde die Systemlautstärke des genutzten Laptops erhöht, da es nicht möglich war inerhalb einer
Systemeinstellung den gesamten Lautstärkebereich von $\beta$=40 dB bis $\beta$=111 dB zu durchlaufen. Die genutzten
Systemlautstärken in Prozent sind am Ende des Pythonskriptes im Kommentar zu erkennen.


<div class="video_container">
    <video width="320" height="240" controls="true" allowfullscreen="true" title="Testtitel">
      <source src="../mov/Projekt_dB_Test-1.mp4" label="dB-Sweep"/>
    </video>
    <div class="overlay"> <p>dB-Sweep von 40 dB bis 111 dB Schallpegel</p> </form> </div>
</div>


In dem Video ist zu erkennen, dass die Funktion sicher ab einem Schalldruckpegel von $\beta$=47dB zu erkennen ist. Mit
steigender Lautstärke ist die Funktion immer deutlicher, bis zu einem Schalldruckpegel von $\beta$=99,9 dB laut
Anzeige des Schalldruckpegelmessers. Oberhalb dieses Pegels ist zu erkennen, dass auf dem Microphone Shield alle LEDs
beginnen zu leuchten und damit keine eindeutige Erkennung des Sounds gegeben ist.


Mit diesem Versuch konnten die Grenzen in Bezug auf die Lautstärke getestet werden. Die ersten Funktionstest durch
Sprache und Gitarrenspiel führen zu der Annahme, dass die Grenzen nicht alleine von der Lautstärke abhängen sondern
ebenfalls von der Frequenz des eingehenden Signals. Aus diesem Grund wurde ein weiteres Exeriment durchgeführt. Der
Aufbau bleibt wie dargestellt in [Abbildung 22]( 01_fig_020). In diesem Experiment wird die Lautstärke konstant gehalten
bei 91 dB und die Frequenz wird angepasst. Der Grund für die 91dB Schalldruckpegel lassen sich ebenfalls im Datenblatt
der Mikrofone finden, da diese ebenfalls die Testbediungen darstellen. Hierfür wird das Pythonskript insofern
abgeändert, als dass lediglich eine Frequenz einmalig ausgegeben wird. Die For-Schleife wird für diesen Versuch
ausgeblendet. Bei jeder Frequenz wurde die Lautstärke jedes mal auf 91 dB Schalldruckpegeleingestellt, bevor das Video
aufgenommen wurde.


<div class="video_container">
    <video width="320" height="240" controls="true" allowfullscreen="true" title="Testtitel">
      <source src="../mov/Projekt_Frequenz_test.mp4" label="Frequenz Test"/>
    </video>
    <div class="overlay"> <p>Test Frequenzmessung</p> </form> </div>
</div>


Es ist zu beobachten, dass die Funktion im unteren Frequenzbereich ($f$ = 440 Hz bis $f$ = 700 Hz) zwar zu erkennen ist,
allerdings leuchten die Richtungs LEDs nur schwach. Ein eindeutiges Erkennen der LED ist ab einer Frequenz von $f= 710
Hz$ gegeben. Die höchste Frequenz bei der eine eindeutige Funktion beobachtet werden konnte war $f$ = 4937 Hz. Darüber
hinaus kann beobachtet werden, dass nicht mehr die oberste LED leuchtet oder aber, dass mehrere LEDs gleichzeitig
leuchten.


Das Frequenzspectrum der Audioline des Videos ist in [Abbildung 26](01_fig_024) zu sehen. Es ist zu erkennen, dass die
Energiedichte bei den unteren Frequenzen erwartungsgemäß höher ist, als bei den oberen. Interessanterweise sind bei den
nierigeren Frequenzen außerdem Oberwellen/Harmonische erkennbar. Die Funktion war gegeben, allerdings nicht den
aufgestellten Kriterien entsprechend.


```{figure} ../images/mojo/Spec_project.png 
:name: 01_fig_024

Spectrumsverlauf des Frequenztests
```

## Zusammenfassung

Ziel des Projektes war es das Sound Locator Projekt mit dem Mojo FPGA-Board sowie dem dazugehörigen Microfone shield in
Betrieb zu nehmen und die Funktion des Aufbaus zu evaluieren. Hierfür wurde die Toolchain bestehend aus dem ISE WEB Pack
von Xilinx, sowie Alchitry Labs auf einem Debian Linux-System installiert. Das bauen des Projektes führte zunächst zu
Problemen, da Laut Fehlermeldung diverse Dateien nicht gelesen werden konnten. Diese Dateien wurde im Laufe der Analyse
gefunden und in die nötigen Archive übertragen. Dadurch war es möglich, das Projekt zu bauen und auf das FPGA zu
flashen. Die Funktion des Mojo konnte mit einem Sprachtest in Form des Buchstabierens des Alphabets verifiziert
werden. Außerdem konnte eine grundsätzliche Funktion beim Erkennen eines Gitarrenspiels erkannt werden. Im Anschluss an den
grundsätzlichen Funktionstest wurden zwei Experimente durchgeführt, um die Grenzen der Sounderkennung im Hinblick auf die
Lautstärke und im Hinblick auf die Frequenz. Im Hinblick auf die Lautstärke konnte eine sichere Funktion im Bereich von
$\beta$ = 47 dB bis 91 dB Schalldruckpegel festgestellt werden. Beim Frequenztest konnte bei einer konstanten Lautstärke von
90 dB eine sichere Funktion im Frequenzband von 710 Hz bis 4937 Hz beobachtet werden. Insgesamt konnte beim Umgang
mit dem Mojo und dem Microphone Shield erkannt werden, dass die Funktion eindeutiger war je eindeutiger das eingehende
Signal war.


Folgende Aufgaben können für zukünftige Projekte interessant sein:


1. Übertragen der Projekt files von Lucid in VHDL oder Verilog. Lucid ist eine von Alchitry Labs entwickelte
   Beschreibungssprache die es Mikrocontroller Programmierern leichter machen soll von der Mikrocontroller
   Programmierung auf die FPGA Programmierung umzusteigen, bzw. dieses überhaupt zu probieren.
   
2. Ein weiterer Versuch könnte sein zu testen ob andere Frequenzgrenzen erreicht werden können, wenn andere
   Lautstärkepegel genutzt werden können.
   
3. Das Gleiche gilt umgekehrt bei der Frage ob andere Lautstärkepegel erreicht werden können, wenn eine andere Frequenz
   für den Versuch genutzt wird. 
   


```{bibliography}
:style: unsrt
```
