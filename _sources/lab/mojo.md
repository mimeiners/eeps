# Sounderkennung mit Hilfe des Mojo V3 FPGA Boards und dem Sound

## Einleitung
Diese Projektarbeit beschäftigt sich mit der Evaluation des [Sound Erkennungs](https://alchitry.com/sound-locating-mojo)
Tutorials der Webiste [Alchitry](https:E//alchitry.com/). 

In diesem Tutorial nutzt Alchitry ihr eigens entwickeltes Mojo V3 Board (XILINX SPARTAN FPGA) und Soundshield mit sieben
Mikrofonen, um Audioquelle zu lokalisieren. 

Das Mojo V3 Board ist ein Board, dass für das Erlernen der Erstellung von digitalen Schaltungen mit Hilfe von
Field-Programmable-Gate-Arrays (FPGA) genutzt werden kann. Wie man bereits am Namen erkennen kann, bietet ein FPGA die
Möglichkeit es jederzeit neu zu beschreiben (Field-Programmable). Dabei wird die Hardware mit Hilfe einer
Hardwarebeschreibungssprache (HDL) wie VHDL, Verilog oder wie im vorliegenden Projekt mit Lucid beschrieben. 
Die Hardware nimmt entsprechend der Beschreibung exakt die Funktion an, die mit der Logik der Beschreibung intendiert
ist. Die Beschreibungssprache bewirkt, dass Logikgatter innerhalb des FPGA's entsprechend der Funktion miteinander
verknüpft werden. So kann der Mojo V3 genutzt werden, um einen LED Ring anzusteuern und entsprechend die Richtung
anzuzeigen aus der ein Ton erkannt worden ist.


Im Folgenden wird die Hardware beschrieben und danach die Einrichtung der Toolchain Schritt für Schritt
erklärt. Außerdem wird der allgemeine Aufbau eines Hardware(FPGA)-Projektes erläutert; im Speziellen das Besipielprojekt 
Sound Locator vom Mojo V3 Tutorial. In diesem Zusammenhang werden die so genannten IP-Cores erläutert, da Hardware und
Software erfahrungsgemäß selten so funkionieren wie es der Entwickler vorgesehen hat, wird außerdem auf Probleme
eingangen und wie diese behoben werden können. Hiernach wird eine Übersicht über den Signalfluss gegeben, ausgehend von
der Tonquelle, über die Aufnahme bis hin zur visuellen Darstellung. Für ein besseres Verständnis der Signalanalyse
und Signalwandlung, wird noch einmal auf die Darstellung von Signalen im Zeit- und Frequenzbereich
eingegangen. Außerdem wird der prinzipielle Aufbau der verwendeten Mikrofone beschrieben. Als letztes wird noch die
Puls-Dichte-Modulation (PDM) erklärt, bevor es im letzten Teil dieser Arbeit um den Funktionstest und ein Testen der
Grenzen der Sounderkennung geht.


## [Der Mojo](https://www.adafruit.com/product/1553) [Baby](https://www.youtube.com/watch?v=c4ytuS8pVp4)


```{figure} ../images/mojo/MojoBoard.png 
:name: 01_fig_025

Das Mojo Entwicklungsboard {cite:p}`sparkfun`
```

Das Mojo V3 Board, zu erkennen in [Abbildung 1]( 01_fig_025), ist ein preiswertes (~70€, bei
[AliExpress](https://de.aliexpress.com/item/32798926767.html?spm=a2g0o.ppclist.product.2.dc57fhXPfhXPEo&pdp_npi=2%40dis%21EUR%21%E2%82%AC%2068%2C61%21%E2%82%AC%2068%2C61%21%21%21%21%21%40211b5a9616552327883654477e07b2%2164982667969%21btf&_t=pvid%3Ab5fae29b-1699-49ff-9cdf-7850da36c207&afTraceInfo=32798926767__pc__pcBridgePPC__xxxxxx__1655232788&gatewayAdapt=glo2deu)
stand: Juni 2022) FPGA Entwicklungsboard auf dem ein Spartan 6 FPGA eingebaut ist, sowie ein ATmega32 Mikrocontroller, der
Arduino kompatibel ist. Dieser wird im Wesentlichen für die Programmierung des FPGA genutzt. Nach der Programmierung
wechselt der ATmega32 vom aktiven Modus in den slave Modus und das FPGA kann über den Mikrocontroller auf den seriellen
Port, analoge Eingänge und andere Funktionen des Mikrocontrollers zugreifen. Außerdem verfügt das Board über 84 digitale
I/O, die über die Steckleisten herausgeführt sind und 8 LEDs, die für allgemeine Programmierung genutzt werden können
{cite:p}`sparkfun`. 


```{figure} ../images/mojo/MicrophoneShield.png 
:name: 01_fig_026

Das Microphone Shield {cite:p}`aliexpress`
```


Auf dem Microphone Shield in [Abbildung 2]( 01_fig_026) befinden sich sechs konzentrisch angeordnete Mikrofone, die um
ein siebtes Mikrofon in der Mitte herum auf dem Shield angebracht sind. Die Anschlüsse dieser Mikrofone sind über
Stiftleisten an der Unterseite des Boards herausgeführt und sind kompatibel zu den Steckleisten des Mojo Boards, wodurch
dieses auf das Mojo Board aufgesteckt werden kann. 


## Genutzte Toolchain
Um eine Hardware beschreiben zu können bedarf es einer Toolchain, die es möglich macht Hardware zu
flashen. Die Toolchain für die Inbetriebnahme des Mojo V3 Boards besteht aus einem Projektierungstool [Alchitry
Labs](https://alchitry.com/alchitry-labs) und einem Builder.


Für das Mojo V3 board bedarf es das 
[ISE WebPack](https://www.xilinx.com/products/design-tools/ise-design-suite/ise-webpack.html) von
[Xilinx](https://www.xilinx.com/).

Alchitry Labs wird hierbei genutzt, um das Projekt zu organisieren und die unterschiedlichen Teile des Projektes zu
erstellen. Der Builder ISE WebPack übersetzt letzten Endes die Beschreibung aus den unterschiedlichen Bestandteilen
des Projektierungstools in die eigentliche Logik innerhalb des FPGAs.

Das genutzte Betriebssystem in diesem Projekt ist Linux [Debian 11](https://www.debian.org/News/2021/20210814). 
Im folgenden Abschnitt wird die Einrichtung der Toolchain ausführlich beschrieben.



### Installation des ISE WebPack
Vor der Installation von Alchitry Labs ist es ratsam, zunächst das ISE WebPack zu installieren. Auch eine Überprüfung der
Partitionierung des Rechners und des freien Festplattenspeicher ist ratsam, da das Archiv das aus dem Internet geladen
wird bereits 6,5 GB groß ist. Für die Installation benötigt das ISE WebPack weitere 18 GB Speicherplatz. Nachdem
sichergestellt wurde, dass ausreichend Speicherplatz für die Installation vorhanden ist kann das
Installationsverzeichnis von der [Website](https://www.xilinx.com/downloadNav/vivado-design-tools/archive-ise.html)
heruntergeladen werden. Hier wird die die Version 14.7 ausgewählt. Unter diesem Punkt wird die ISE Design Suite - 14.7
Full Product ausgewählt und heruntergeladen. Es muss an dieser Stelle erwähnt werden, dass ein Nutzeraccount benötigt
wird, um diese Software herunter zu laden und zu installieren.

Nach dem Download geht es weiter zur eigentlichen Installation. Als erstes wird das Installationsverzeichnis
entpackt. Mit Hilfe des Terminals und des Befehls **cd** (change directory) wird in das Verzeichnis gewechselt in dem
das heruntergeladene Verzeichnis gespeichert ist. 

(Hier: Downloads):

Terminalausgabe
:       mojo@fpga:~$ cd Downloads/

Im Verzeichnis wird das Archiv als nächstes entpackt.:

Terminalausgabe
:       mojo@fpga:/Downloads/$ tar -xvf Xilinx_ISE_DS_Lin_14.7_1015_1.tar


Die Optionen **xvf** beschreiben, dass das Archiv entpackt werden soll (x), dass die verarbeiteten Dateien ausführlich
aufeglistet werden (v) und dass das Archiv aus dem aktuellen Verzeichnis genommen werden soll (f) {cite:p}`Ubuntuusers`.
Nach diesen Vorarbeiten kann das Setup des Programmes gestartet werden.


```{note}
Die Installation des ISE WebPacks sollte nach Möglichkeit mit Administrationsrechten ausgeführt werden. Das erleichtert
im weiteren Verlauf die Nutzung mit der weiteren Toolchain.
```

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

Im Folgefenster werden alle Haken gelassen wie der Installationswizard es vorschlägt. Eine Nutzung mehrer CPU-Kerne ist
sinnvoll, um die Installationszeit zu verringern.


Während der Installation kann die Zeit genutzt werden, um eine entsprechende Lizenz auf
[Xlilinx](https://www.xilinx.com/member/forms/license-form.html) zu erstehen. 
Nach Eingabe der persönlichen Daten wird die Lizenz für das ISE WebPack ausgewählt und die Lizenzdatei kann
heruntergeladen und dem Programm hinzugefügt werden.

Beim erstmaligen Start öffnet sich zunächst der Lizenzmanager, der noch einmal auf das Erlangen der Lizenz
hingeweist wie in [Abbildung 5]( 01_fig_03) dargestellt.


```{figure} ../images/mojo/Licence_Manager_1.png 
:name: 01_fig_03

Möglichkeit zur Auswahl des Lizenztypes.
```

Wurde die Lizenz heruntergeladen kann diese unter "Manage License" hinzugefügt werden. Innerhalb des Dialogfeldes
[Abbildung 6]( 01_fig_04) kann zum Speicherort der Lizenzdatei navigiert werden.


```{figure} ../images/mojo/Licence_Manager_2.png 
:name: 01_fig_04

Unter Load Licence wird der Speicherort der Lizenzdatei ausgewählt.
```

Nachdem das ISE WebPack 

1. heruntergeladen

2. installiert

3. gestartet und

4. lizensiert 

wurde, wird im nächsten Schritt die Programmierumgebung installiert.


### Installation von Alchitry Labs
Ein Großteil der Installation der Toolchain ist zu diesem Zeitpunkt bereits abgeschlossen. Das Einrichten von Alchitry
Labs stellt sich leichter dar, als es bei der Xilinx Software der Fall war.

Die Software ist auf der (Website)[https://alchitry.com/alchitry-labs] von Alchitry Labs unter dem Reiter Alchitry Labs
zu finden. Die Download Links sind unterhalb der Abbildung vom Programm zu finden. Für dieses Projekt wurde die
Linux-Version genutzt. Die Linux-Version bietet bei der Installation deutliche Vorteile in der Einrichtung im Vergleich
zur Windows-Version, da diese für Windows 10 und 11 nicht mehr optimiert ist. Nach dem Download von knapp 18 MB muss das
geladene Archiv ausgepackt werden. Hierfür kann der gleiche Befehl mit geändertem Dateinamen genutzt werden.


Terminalausgabe
:       mojo@fpga:/Downloads/$ tar -xvf alchitry-labs-1.2.7-linux.tar

Nach der Installation wird in den Unterordner "alchitry-labs-1.2.7" navigiert und das Programm mit folgendem Befehlt gestartet:

Terminalausgabe
:       bash alchitry-labs


Ist die Installation bisher erfolgreich und korrekt öffnet sich nun die Programmierumgebung. Die Software erfragt beim
ersten Starten den Installationsort des Builders ISE WebPack. Im Programmfenster kann über "Settings" und "ISE Location"
über ein Dialogfeld der Installationsort des ISE WEbPack ausgewählt werden.( siehe: [Abbildung 7]( 01_fig_05)). Hierbei
ist  darauf zu achten, dass der Ordner mit der entsprechenden Versionsnummer ausgewählt wird (hier: 14.7). Die Software
Alchitry Labs gibt entsprechende Hinweise innerhalb des Dialoges.


```{figure} ../images/mojo/Alchitry_Licence.png 
:name: 01_fig_05

Auswahl des ISE WebPack Installationsortes
```

Ab diesem Zeitpunkt ist es möglich Projekte zu öffnen und zu erstellen.


### Öffnen des Projektes

Beim ersten Starten von Alchitry Labs startet automatisch ein Dialog, in dem erfragt wird, ob bereits ein Projekt
vorhanden ist. Siehe: [Abbildung 8]( 01_fig_06)


```{figure} ../images/mojo/First_Start.png 
:name: 01_fig_06

Erste Projektauswahl
```

Durch die Auswahl "No" wird der User in ein weiteres Dialogfenster geführt, indem dieser ein Projekt erstellen kann.

Dieses Dialogfenster ist in [Abbildung 9]( 01_fig_07) zu sehen. Im Feld "Project Name:" wird der Wunschname des neuen
Projektes eingegeben. Im folgenden Reiter "Workspace" steht die Arbeitsumgebung. Hier werden Projekte abgespeichert
und Projektumgebungen (Arbeitsverzeichnisse) erstellt, die notwendige Dateien für den "Build-Prozess" bereitstellen. Im
dritten Reiter wird das entsprechende Board ausgewählt. Für dieses Projekt ist das das Mojo Board. Das Programm erstellt
hier für automatisch die Bezüge zu Hardware, damit das Projekt funktionsfähig gebaut werden kann. Die Sprache
("Language") die ausgewählt werden muss um ein funktionierendes Beispielprojekt laden zu können ist hier das
programmeigene Lucid. Es ist ebenfalls möglich innerhalb der Umgebung in Verilog zu coden, allerdings gibt es für
Verilog keine Beispielprojekte. Die Beispielprojekte sind auschließlich in Lucid geschrieben. Über ein Dropdown Menü ist
es nun möglich, das Sound Locator Projekt auszuwählen und zu laden.


```{figure} ../images/mojo/New_Project.png 
:name: 01_fig_07

Einstellungen zum Öffnen des Sound Locator Beispiels
```

Durch einen letzten Mausklick auf den Button "Create" wird das Beispielprojekt erstellt. Im nächsten Abschnitt wird
beschrieben, welche Arten von Files man innerhalb des Projektes finden kann und was diese tun. Die Inbetriebnahme des
Projektes wird im darauffolgenden Abschnitt beschrieben.


## Aufbau eines Projektes

- <u>**Source**</u>

Der erste Teil innerhalb dieses Projektes sind die Source-Dateien auch Module genannt. Diese beschreiben alle Ein- und
Ausgänge der unterschiedlichen Hardware. Die im Projekt genutzten Source-Dateien sind in [Abbildung 10]( 01_fig_08)
dargestellt. Für das Sound Locator Projekt sind das die Hann-Funktion, der LED-Ring, das mojo-top modul,
welches das Mojo Board beschreibt, die pdm-mics zur Definition der Mikrophone und das sound_locator Modul in dem das
Delay zur Sound Erkennung ermittelt wird.


```{figure} ../images/mojo/Source.png 
:name: 01_fig_08
	
Die Source-Dateien sind als erstes im Projekt zu finden
```

- <u>**Components**</u>

Components sind teils vorinstallierte, teils selbst geschriebene Bausteine, die für spezielle Funktionen verwendet werden
können. Im vorliegenden Projekt finden sich vielfach Lucid-Files, mit der Dateiendung **.luc**. Diese wurden vom
Entwickler erstellt, können sich aber auch in der XILINX-Umgebung befinden. Die in diesem Projekt genutzten sind in
[Abbildung 11]( 01_fig_09) dargestellt.


```{figure} ../images/mojo/Components.png 
:name: 01_fig_09

Als zweites sind die Components im Projekt aufgeführt.
```
- <u>**Cores**</u>

Die Cores oder auch IP-Cores sind vorgefertigte weitestgehend von XILINX geteste Bausteine, die spezielle Aufgaben
erledigen können und werden von XILINX mitgeliefert. IP steht für Intellectual Property, also geistiges Eigentum. Diese
Bausteine sind weitestgehend spezifiziert und bieten somit den Vorteil, dass diese in einem Design mehrfach
wiederverwendet werden können. Fertige IP-Cores gibt es von Buskommunikation über digitale Signalverarbeitung wie FFT
bis hin zu Multimedia wie Ethernet oder Bluetooth. In diesem Projekt gibt es drei IP cores. Zum einen den
Dezimationsfilter, welcher die einkommende PDM Signale dezimiert, um die Informationen mit verringerter Samplefrequenz
zu extrahieren. Als zweites gibt es den mag_phase_calculator der aus den einkommenden Signalen die Amplitude und die
Phase errechnet und als letztes den xfft_v8_0-core der die FFT auf die einkommenden Signale anwendet.


```{figure} ../images/mojo/Cores.png 
:name: 01_fig_010

Der dritte Reiter beinhaltet die IP-Cores
```
- <u>**Constraints**</u>


Dargestellt in [Abbildung 13]( 01_fig_011) sind die drei User-constraints-files von debugger, microphone shield und vom
Mojo Board. In diesen Dateien werden die Timing-Eigenschaften, sowie die Pin-Eigenschaften, physikalischen Eigenschaften
und Grenzen beschrieben. Diese Dateien werden benötigt, um dem Syntheseschritt (ISE WebPack) die letzten
Informationen zu geben, wie das Projekt erstellt werden soll.


```{figure} ../images/mojo/Constraints.png
:name: 01_fig_011

Als letztes gibt es die Constraints im Projekt
```

## Sound Locator Projekt

Im Vorfeld wurden bereits die Hardware, sowie die unterschiedlichen Funktionsblöcke, die das Sound Locator Projekt
besitzt beschrieben. Die Dokumentation des Projektes von O'Reilly verspricht ein Plug'n'Play mit der Hardware. Die 
Untersuchungen innerhalb dieses Projekts haben jedoch gezeigt, dass noch weitere Probleme gelöst werden müssen, bevor
das Projekt auf den FPGA geflasht werden kann. In diesem Abschnitt werden diese Probleme genauer beleuchtet, wie diese 
zu lösen sind und im Anschluss wird die Funktion der Sound-Erkennung getestet.


### Probleme mit den IP-cores lösen

Erinnern wir uns an die IP-Cores, die im letzten Abschnitt beschrieben wurden. Diese stellen eine fertige
Funktionseinheit, wie zum Beispiel den Dezimationsfilter, dar. Ausgerechnet diese IP-Cores machen beim ersten
Flash-Versuch Probleme und es kommt folgende Meldung die in [Abbildung 14]( 01_fig_012) dargestellt ist.


```{figure} ../images/mojo/Fehlermeldung_Cores.png 
:name: 01_fig_012

Angezeigte Fehlermeldung beim ersten Flashversuch
```

Alchitry Labs zeigt an, dass es die Dateien für die IP-Cores nicht lesen kann. Schaut man in die Ordnerstruktur und
vergleicht diese mit dem agezeigten Pfad, so scheint sich hier ein Fehler bei der Programmierung der Software
eingeschlichen zu haben, der es zunächst unmöglich macht, das Projekt zu bauen.


> <span style="color:green">**erik@erik:**</span><span style="color:blue">**~/alchitry/SoundLocator**</span>$ ls
> 
> <span style="color:blue">**constraint**</span>  <span style="color:blue">**coreGen**</span> SoundLocator.alp 
<span> style="color:blue">**source**</span>  <span style="color:blue">**work**</span>


Es sind in dieser Ansicht vier Ordner zu sehen. Vergeicht man diese vier Ordner mit dem geforderten Pfad von Alchitry
Labs aus [Abbildung 12]( 01_fig_012) ist zu erkennen, dass der Ordner **cores** vergeblich in diesem Verzeichnis zu
suchen ist. Dieses Vezeichnis wurde automatisch vom Programm erstellt, was die Vermutung nahelegt, dass der Aufbau des
Verzeichnises "hard coded" ist. Nach einiger Suche innerhalb des Programmverzeichnises konnte die Codezeile, die dafür
verantwortich ist, nicht gefunden werden. Statdessen wurde für die Inbetriebnahme der Hardware ein Workaround
gefunden. Die nötigen Dateien befinden sich alle im **coreGen** Ordner. 

Das händische korrigieren des Pfades in drei Schritten:

1. Umbenennen des  **coreGen** zu **cores**.

2. Innerhalb dieses Ordners, erstellen der jeweiligen Ordner für **Decimation Filter**, **xfft_v8.0** und
   **mag_phase_calculator**.

3. Verschieben der Dateien für den jeweiligen core in den entsprechend erstellten Ordner.


Nachdem diese Schritte durchgeführt wurden, kann das Projekt gebaut werden und ermöglicht es uns, das Mojo Board zu
flashen und die Funktion des Programmes zu testen.


## Funktionsprinzip des Projektes

In diesem Abschnitt wird die Funktion des gesamten Aufbaus bestehend aus Mojo mit aufgestecktem Microphone Shield
evaluiert. Zunächst wird das Funktionsprinzip des Projektes erläutert. In [Abbildung 15]( 01_fig_013) ist der
Signalfluss der Sounderkennung dargestellt. Am Anfang steht ein Ton in Form einer sinusförmigen Schallwelle an. Diese
besteht nicht aus nur einer Frequenz wie in [Abbildung 15]( 01_fig_013) dargestellt, sondern setzt sich aus
verschiedenen Frequenzen zusammen. Dieses Frequenzspektrum wird ebenfalls dargestellt und diskutiert. Die analoge
Sinuswelle wird durch ein Wandlungssystem in die digitale Domäne übertragen. Auf dem Microphone Shield sind für diese
Wandlung sogenannte digitale MEMS PDM Mikrofone, die diese Wandlung vornehmen. Die Mikrofone geben eine
Puls-Dichte-Modulation (PDM) aus, welche direkt auf das FPGA gegeben wird. Dieses Signal wir dann vom FPGA weiter
verarbeitet und anschließend wird das Ergebnis der Richtungserkennung auf dem LED-Ring für den Anwender sichtbar
gemacht.


```{figure} ../images/mojo/SignalFlow.png
:name: 01_fig_013

Übersicht Signalfluss
```

Der erste Block des Signalflusses enthält die akustische Welle. Die akustische Welle ist nichts anderes als eine
Schallwelle, welche durch das komprimieren und dekomprimieren der Luft entsteht. Für die theoretisch ideale Betrachtung
wird in der Physik eine ideale winzige Punktschallquelle angenommen von der aus kugelförmig, also dreidimensional, die 
Schallwellen in alle Richtungen abgestrahlt werden. Diese Punktquelle und die Ausbreitung der Schallwellen von dort aus
sind in [Abbildung 16]( 01_fig_014) dargestellt. Diese Wellenfronten in Verbindung mit den dargestellten Strahlen
kennzeichnen die Richtung der Schallwellen. Wellenfronten sind hierbei Flächen, bei der die Luftteilchen wertgleiche
Auslenkungen, also gleiche Amplituden, aufgrund der erzeugten Schwingung besitzen {cite:p}`Halliday`.


```{figure} ../images/mojo/Schallwellen.png
:name: 01_fig_014

Zweidimensionale Darstellung zur Ausbreitung einer Schallwelle {cite:p}`Halliday`
```

Wie bereits erwähnt breiten sich diese Schallwellen kugelförmig im Raum aus und werden deshalb auch
sphärische Wellen genannt. Diese sphärischen Wellen sind wie in [Abbildung 16]( 01_fig_014) gekrümmt.
Je weiter man sich von der Punktquelle entfernt, umso geringer wird diese Krümmung und die Schallwelle kann als Ebene
verstanden werden. Diese Wellen werden dann ebene oder planare Wellen genannt {cite:p}`Halliday`.


Die Intensität der Schallwelle ist abhängig von der Amplitude der Schallwelle. Die Intensität verringert sich
quadratisch in Abängigkeit zum Abstand zur Tonquelle:

$$
I = \frac{P_{s}}{4 \, \pi \, r^{2}}
$$


Wobei $I$ die Intensität der Schallwelle ist $P$ die Leistung durch die Schallwelle und $r$ der Abstand zur
Schallquelle {cite:p}`Halliday`.


Da das menschliche Ohr einen großen Bereich an Intensitäten wahrnehmen kann, wird für die Bewertung von Schallintensitäten
die Dezibelskala verwendet. Angaben in der Dezibelskala sind immer Vergleiche (Relationen), bei dem der gemessene Wert
mit einem Standardwert verglichen wird. In diesem Fall wird diese als Schallpegel oder Schalldruckpegel bezeichnet und
folgendermaßen berechnet: 

$$
\beta = 10 dB \cdot \frac{I}{I_{0}}
$$

Wobei $\beta$ der resultierende Schalldruckpegel ist. $I$ beschreibt die Intensität der gemessenen Schallwelle und $I_{0}$
beschreibt einen standardisierten Referenzwert für die Intensität ($I_0 = 10^{-12} \frac{W}{m^{2}}$). {cite:p}`Halliday`


Um einen Ton zu erzeugen muss diese (De-)Komprimierung der Luft mit einer definierten Frequenz erzeugt werden. Um
beispielsweise den Kammerton C zu erzeugen, muss eine Schallwelle mit einer Frequenz von $f$=440 Hz erzeugt
werden. Idealisiert sieht diese Schallwelle aus wie in [Abbildung 17](01_fig_015) dargestellt.


```{figure} ../images/mojo/Sine_Only.png
:name: 01_fig_015

Sinuswelle mit $f$=440 Hz
```

Aus dieser Darstellung ist es ein Einfaches, die Frequenz des Signals abzulesen und damit das Signal zu
rekonstruieren. In der realen Welt ist die Wahrheit nicht so eindeutig und das eintreffende Signal auf das 
Mikrofon ist mit Rauschen überlagert wie in [Abbildung 18]( 01_fig_016) dargestellt.


```{figure} ../images/mojo/Noisy_Source_Signal.png
:name: 01_fig_016

Sinuswelle mit $f$=440 Hz überlagert mit Rauschen
```


Im dargestellten Zeitbereich ist es nicht einzuschätzen, welches Signal der Grundton ist und welche Frequenz er hat.
Um die Reaktion der Hardware auf die eintreffenden Töne besser einschätzen oder erklären zu können, ist es deshalb
nötig, das Signal nicht im Zeitbereich zu betrachten, sondern mit Hilfe einer FFT (Fast-Fourier-Transformation) im
Frequenzbereich (Spektralanalyse). Das Frequenzspektrum des Signals aus [Abbildung 18](01_fig_016) ist in [Abbildung
19](01_fig_017) zu finden. 


```{figure} ../images/mojo/FFT_Source.png
:name: 01_fig_017

Frequenzspektrum des verrauschten Signals.
```

An der Y-Achse ist die Amplitude der Frequenzanteile aufgetragen und auf der X-Achse sind die unterschiedlichen
Frequenzen dargestellt. Sie zeigt uns aus welchen Frequenzanteilen das Ausgangssignal zusammengesetzt ist. Das Rauschen
mit seinen vielen Frequenzen, die gleichermaßen im Signal enthalten sind, verschwinden mit Hinblick auf die Amplitude
förmlich im Gegensatz zum eigentlichen Signal. Mit Hilfe dieser Methode ist es möglich auch aus im Zeitbereich
verrauschten oder uneindeutigen Signalen das gesuchte Signal herauszufinden bzw zu erfahren, welche Frequenzen im
untersuchten Signal enthalten sind.



Nachdem geklärt wurde, welche Eingangssignale zu erwarten sind, kann der Fokus auf die akustische Aufnahme gerichtet
werden. Auf dem Microphone Shield sind sieben Mikrofone mit der Bezeichnung SPK0415HM4H zu finden. Diese Mikrophone sind 
digitale Mikro-Elektro-Mechanische Systeme (MEMS). Das bedeutet, dass durch Herstellungsmethoden der Halbleiterindustrie
ein Bauteil erzeugt wurde, dass sowohl elektronische als auch mechanische Eigenschaften vereint. Wie in [Abbildung
20](01_fig_018) zu erkennen ist, besitzt ein solches Mikrofon einen Sound Port, dies ist eine Öffnung im Gehäuse (Can)
des Bauteils. Hier kann der Ton auf die eigentliche Struktur des Mikrofons auftreffen. Die Öffnung ist hier oben auf dem
Gehäuse, kann bei anderen Mikrofonen aber auch am Boden des Gehäuses sein. Darunter befindet sich eine Membran (Glob Top
Molding) über einer Halbleiterträgerstruktur. Die Membran und die Trägerstruktur sind zwei gerade, gegenüberliegende
Flächen zwischen denen ein Material zu finden ist, das als Dielektrikum verstanden werden kann. Dieser Aufbau verhält
sich wie ein Kondensator mit einer bekannten Kapazität. Beim Auftreffen von Schall gerät die Membran in Bewegung, was
zur Folge hat, dass sich die Kapazität des Kondensators, durch die Verringerung des Abstandes zwischen den zwei Flächen,
ändert. Diese Änderung wird von der Anwender Spezifischen Schaltung (ASIC) erkannt und entsprechend verarbeitet. Ob ein
analoges oder digitales Signal ausgegeben wird, entscheidet sich hier. Entweder das analoge Signal wird vom ASIC
bereitgestellt oder ein weiterer Wandler (ADC) befindet sich innerhalb des Systems, welcher das analoge Signal in ein
digitales Signal umsetzt. Bei den digitalen Signalen kann es sich um Pulse-Code-Modulierte (PCM) oder um
Puls-Dichte-Modulierte (PDM) Signale handeln. Puls-Code-Modulierte Signale werden hier nicht weiter behandelt, sollen 
aber der Vollständigkeit wegen Erwähnung finden {cite:p}`DigiMEMS`.


```{figure} ../images/mojo/MEMS.png
:name: 01_fig_018

Aufbau eines MEMS Mikrofons {cite:p}`DigiMEMS`
```

In diesem Projekt werden Mikrofone verwendet, die Puls-Dichte-Modulierte (PDM) Signale verwenden. Bei der
Puls-Dichte-Modulation wird die Information der Amplitude des Signals über die Puls-Dichte dargestellt. Das heißt, dass
eine Häufung von logischen High (1) Pegeln eine hohe Amplitude und eine Häufung von logischen Low (0) Pegeln eine
niedrige Amplitude bedeutet. Bei der Wandlung durch ein MEMS Mikrophon kann das PDM-Signal eines Sinustons
folgendermaßen aussehen.


```{figure} ../images/mojo/Pulse_Density.png
:name: 01_fig_019

Übersicht zwischen analogem Signal und Puls-Dichte-moduliertem Signal {cite:p}`Devzone`
```


In [Abbildung 21](01_fig_019) ist wie beschrieben zu erkennen, dass mit höheren Amplituden vermehrt ein High Pegel zu 
finden ist. Durch diese periodische Häufung von hohen und niedrigen Amplituden ist nicht nur die Amplitude sondern
ebenfalls die Frequenz im PDM-Signal kodiert. Das PDM-Signal ist der letzte Punkt, bevor die Verarbeitung des FPGAs
beginnt. Als nächstes kann die Funktion des Projektes betrachtet werden.

Für die Funktion des Projektes werden zunächst Annahmen vom Autor getroffen. Die wichtigste Annahme ist, dass die
Richtung des Tons nur in einem zweidimensionalen Raster horizontal zum Mojo Board auf das FPGA auftreffen darf. Das ist
dem physikalischen Aufbau des Microphone Shields geschuldet, da alle Mikrofone auf einer Ebene verbaut sind. Außerdem
wird angenommen, dass es sich bei den auftreffenden Schallwellen um eine eine gerade Wellenfront, also um eine planare
Welle handelt. Die letzte Annahme ist, dass jede Frequenz eines Soundsamples aus einer einzigen Richtung kommt
{cite:p}`Rajewski`.

Die Sounderkennung mit dem Mojo errechnet die Richtung des auftreffenden Sounds aus der Phasenverschiebung
zwischen den äußeren und dem zentralen Mikrophon. Der auf die Mikrofone treffende Ton wird in ein PDM-Signal
umgewandelt und dieses PDM-Signal wird simultan vom FPGA abgetastet. Auf diese Samples wird eine FFT angewandt,
wodurch das PDM-Signal von der Zeit- in die Frequenzdomäne überführt wird. Als Ausgabe aus der FFT erhält man 
nun für jedes Sample eine komplexe Zahl. Bestehend aus dem Realteil, der die Amplitude des eingehenden Signals darstellt
und dem Imaginärteil, der die Phase des eingehenden Signals darstellt. Diese können in einem Koordinatensystem
aufgetragen werden. In [Abbildung 22](01_fig_020) ist beispielfhaft für drei Mikrofone das Prinzip dargestellt. Die
schwarzen Kreise stellen die Position von drei Mikrofonen auf dem Microphone Shield dar mit ihren in Klammern
dargestellten Koordinaten. Der Mittelpunkt des Koordinatensystems ist ebenfalls als Koordinate des zentralen Mikrofons
zu verstehen. In Blau in der oberen linken Ecke ist die Richtung dargestellt, aus der ein Ton auf die Mikrofone
trifft. Das Auftreffen bewirkt eine Verzögerung (Delay) der jeweiligen äußeren Mikrofone im Vergleich zum mittleren
Mikrofon. Mithilfe dieses Delays bzw. mit der Phasenverschiebung zueinander (die Verzögerung ist lediglich der Quotient
aus Phasenverschiebung und Frequenz, wodurch diese beiden Werte proportinal zueinander sind) und der Positionsvektoren
der unterschiedlichen Mikrofone kann nun die Richtung des Tons bestimmt werden. Hierzu werden die Ortsvektoren mit dem
errechneten Delay skaliert, wodurch die violett skalierten Vektoren entstehen. Durch Vektoraddition kann ein
Summenvektor erstellt werden, der in die Richtung der Tonquelle zeigt (gelb){cite:p}`Rajewski`. Rajewski hat dies
Richtungen in 16 verschiedene Bins eingeteilt, wodurch die Einteilung auf die LEDs erfolgt.


```{figure} ../images/mojo/SoundirectionPrinciple.png
:name: 01_fig_020

Vektorielle Darstellung des Erkennungsprinzips {cite:p}`Rajewski`
```


### Funktionstest

Die beschriebene Funktion soll mit den nächsten Tests überprüft werden. Die grundsätzlichen Funktionstest beinhalten
einen Sprachtest und einen Test bei dem mit einer Gitarre ein Lied angespielt wird. Für den ersten Test wird der Mojo
auf einem Holztisch platziert und es wird das Alphabet durchgesprochen. Die Tonquelle ist in diesem Video von Links und die
Quelle ist horizontal verschoben zum Mojo, um die Annahmen des Erfinders zu berücksichtigen, dass die Tonquelle auf der
selben Ebene sein muss wie die Mikrofone. Es ist zu erkennen, dass bei S-Lauten (die Buchstaben C, S, X, Z) mehr als nur
eine LED leuchtet. Alle anderen Buchstaben haben insgesamt eine eindeutige Antwort des Mojos verursacht. Eine eindeutige
Antwort heißt, dass die LED geleuchtet hat, aus der der Ton auf den Mojo getroffen ist.


<div class="video_container">
	<video width="320" height="240" controls="true" allowfullscreen="true" title="Testtitel">
		<source src="../mov/Alphabet.mp4" label="Alphabet"/>
	</video>
    <div class="overlay"> <p>Alphabet Test</p> </form>  </div>
</div>


Betrachtet man zu den Beobachtungen nun das Frequenzsspektrum zu den ersten sieben Buchstaben des Alphabets, ist zu
erkennen, dass der größete Schallpegel bei Frequenzen zwischen $f$=60 Hz und $f$=400 Hz zu finden ist. Der Buchstabe "C" 
ist in dieser [Abbildung 23]( 01_fig_021) der dritte Balken von Links. Das Diagramm ist ein
Frequenz-Zeit-Diagramm. Hierbei sind auf der Y-Achse die unterschiedlichen Frequenzanteile aufgeführt. Auf der X-Achse 
findet sich der Zeitpunkt in der Audiospur. Die Codierung des Schallwellenpegels ist in der Helligkeit der Balken zu
erkennen. Diese Darstellung war die Beste für diese Anwendung, da durch die Art des Versuchs verschiedene Töne zu
unterschiedlichen Zeiten auftreffen. Dieses Diagramm bietet eine übersichtliche Darstellung für diese Zwecke. Für den
Buchstaben "C" ist zu erkennen, dass zu Beginn des Buchstabens ein höherer Schalldruckpegel zu erkennen ist. Dieser reicht
von einer Frequenz von $f$=4 kHz bis zu mehr als $f$=16 kHz. Interessanterweise ist eine konträre Beobachtung beim
Buchstaben "F" zu erkennen. Der zweite Balken von Rechts hat zu Beginn des Buchstabens ein ähnliches Frequenzmuster wie
die anderen. Nach einer kurzen Zeit verteilt sich der Schalldruckpegel gleichmäßig auf eine größere Bandbreite an
Frequenzen. Hier konnte jedoch eine gute Funktion des Mojo beobachtet werden. Der Schalldruckpegel bei diesem Versuch
konnte etwa zwischen $\beta$=60 dB und $\beta$=70 dB mit dem Schalldruckpegelmesser gemessen werden.


```{figure} ../images/mojo/AlphaG.png 
:name: 01_fig_021

Frequenzspektrum für die Buchstaben A bis G
```

Nach dieser Beobachtung ist ein weiterer grundsätzlicher Funktionstest mit einer anderen Tonquelle durchgeführt
worden. In diesem Funktionstest wurde der Song "Come as you are" von Nirvana angespielt, um die Reaktion vom Mojo zu
testen. Die Quelle des Geräusches ist in diesem Video unterhalb des Mojo's. Es ist zu erkennen, dass die unterste
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


Das Frequenzspektrum ist in der nachfolgenden [Abbildung 24]( 01_fig_022) zu erkennen. Der Schalldruckpegel der Frequenzen
scheint hier weniger breit gefächert zu sein als bei dem vorangegangenen Funktionstest. Die Funktion konnte auch hierbei
im Wesentlichen nachgewiesen werden, auch wenn es bei diesem Test zum leuchten der gegenüberliegenden LED gekommen
ist. Das mehrere LEDs leuchten könnte an der Art der Tonquelle liegen. Wie bei der Sprache ist es bei einem
Saiteninstrument wie bei einer Gitarre so, dass die Schwingung nicht sauber eine Frequnez besitzt. Eine Annahme des
Projektes war, dass eine Frequenz lediglich aus einer Richtung kommt. Die Durchführung des Projektes in einem üblichen
Raum kann allerdings dazu führen, dass Reflexionen an den Wänden des Raumes entstehen und somit eine Frequenz
ggf. scheinbar aus zwei oder mehreren Richtung kommen kann. Der Schalldruckpegel der während des Versuchs gemsesen wurde
lag bei rund $\beta$=70 dB. 


```{figure} ../images/mojo/comeasyouare.png 
:name: 01_fig_022

Frequenzspektrum des Intros von "Come as you are" von Nirvana.
```

Die Funktionstests konnten die prinzipielle Funktion nachweisen. Aus den Beobachtungen der ersten beiden Funktionstests
kann gefolgert werden, dass die Erkennung eines Tones frequenzabhängig ist, da beim Alphabettest die Buchstaben
nicht eindeutig erkannt wurden, bei denen höhere Frequenzanteile ($f > 10 \, kHz$ "C" und "F") enthalten sind. 
Damit stellt sich die Fragen, welche Grenzen der Erkennung bei der Frequenz zu finden sind. Eine weitere Frage die sich 
beim Konzipieren des Experimentes gestellt hat ist, ob ebenfalls die Lautstärke eines Tones eine Rolle spielt. Um die
Grenzen der Sounderkennung zu ermitteln wurde sich in diesem Experiment dazu entschieden, dieses weiter im privaten
Wohnzimmer durchzuführen und nicht in einem speziell eingerichtetem schallarmen Raum, da die Sounderkennung dazu dienen
soll, Geräuschquellen zu unterscheiden und die Richtung des gesuchten Tons zu ermitteln. Der Aufbau für dieses
Experiment ist in den vorangegangenen Videos schon erkennbar, ist der Übersicht wegen nochmal schematisch in [Abbildung
25]( 01_fig_023) dargestellt. Das Mojo Board mitsamt des Microphone Shield ist im Zentrum des Aufbaus platziert. Die
Soundquelle ist eine Bluetoothbox der Firma Bose und wurde 10 cm oberhalb des Mojo's aufgestellt. Hier wird ein
Sinussignal einer definierten Frequenz und Lautstärke ausgegeben. Um die Lautsärke in Decibel (dB) prüfen zu können,
wird ein Schalldruckpegel Messgerät auf der gleichen Höhe wie das zentrale Mikrofon auf dem Microphone Shield platziert,
um möglichst exakt die Lautstärke einstellen bzw. prüfen zu können. Bei dem Experiment wirde Gehörschutz getragen, da
Schalldruckpegel von bis zu $\beta$=111 dB getestet werden.


```{note}
Bei einem solchen Versuch muss immer ein Gehörschutz getragen werden! Diese Lautstärken können das Hörvermögen
verringern und sind gesundheitsschädlich!
```


```{figure} ../images/mojo/Setup_experiment.png 
:name: 01_fig_023
	
Versuchsaufbau für den Funktionstest
```

Zunächst wird die Grenze der Lautstärke getestet. Hierfür wird die Lautsärke einen Sinustones mit einer Frequenz von
$f$=1 kHz langsam von $\beta$= 40 dB Schalldruckpegel bis $\beta$=111 dB Schaldruckpegel erhöht und die Funktion wird
beobachtet. Jede Lautstärke wird für eine Zeit $t$=3 s gehalten. Die Funktion gilt als sicher vorhanden, solange
ausschließlich die LED leuchtet, die in die Richtung der Tonquelle ausgerichtet ist. Die gewählte Frequenz wurde anhand
des Datenblattes der Mikrofone gewählt. Die Testbedigungen für die Mikrofone sind im Datenblatt mit einer Frequenz von
$f$=1 kHz und einem Schalldruckpegel $\beta$=91 dB angegeben. 

Für die Soundausgabe wurde folgendes Pythonskript mit dem Paket PyAudio genutzt.


```{literalinclude} ../files/math/mojo/SoundOutput.py
:language: python
```

Aus dem Code ist zu erkennen, dass mit jedem Schleifendurchlauf die Lautsärke um 0.1, also 10% erhöht wird. Der Versuch
musste allerdings in vier Durchläufen durchgeführt werden wobei das Skript in jedem der Durchläufe einmal ausgeführt
wurde. Bei jedem Durlauf wurde die Systemlautstärke des genutzten Laptops erhöht, da es nicht möglich war inerhalb einer statischen
Systemeinstellung den gesamten Lautstärkebereich von $\beta$=40 dB bis $\beta$=111 dB zu durchlaufen. Die genutzten
Systemlautstärken in Prozent sind am Ende des Pythonskriptes im Kommentar zu erkennen.


<div class="video_container">
    <video width="320" height="240" controls="true" allowfullscreen="true" title="Testtitel">
      <source src="../mov/Projekt_dB_Test-1.mp4" label="dB-Sweep"/>
    </video>
    <div class="overlay"> <p>dB-Sweep von 40 dB bis 111 dB Schallpegel</p> </form> </div>
</div>


In dem Video ist zu sehen, dass die Funktion sicher ab einem Schalldruckpegel von $\beta$=47 dB gegeben ist. Mit
steigender Lautstärke ist die Funktion immer deutlicher, bis zu einem Schalldruckpegel von $\beta$=99,9 dB laut
Anzeige des Schalldruckpegelmessers. Oberhalb dieses Pegels beginnen alle LEDs auf dem Microphone Shield zu leuchten,
wodurch keine eindeutige Erkennung der Tonrichtung mehr möglich ist. 

Aus diesem Grund wurde ein weiteres Experiment durchgeführt. Der Aufbau bleibt wie dargestellt in 
[Abbildung 22](01_fig_020). In diesem Experiment wird die Lautstärke konstant gehalten bei 91 dB und die Frequenz wird
angepasst. Der Grund für die 91 dB Schalldruckpegel lassen sich wie erwähnt im Datenblatt der Mikrofone finden. Hierfür
wird das Pythonskript insofern abgeändert, als dass lediglich eine Frequenz einmalig ausgegeben wird. Die for-Schleife
wird für diesen Versuch ausgeblendet. Bei jeder Frequenz wurde die Lautstärke jedes mal auf 91 dB Schalldruckpegel
eingestellt, bevor das Video aufgenommen wurde.


<div class="video_container">
    <video width="320" height="240" controls="true" allowfullscreen="true" title="Testtitel">
      <source src="../mov/Projekt_Frequenz_test.mp4" label="Frequenz Test"/>
    </video>
    <div class="overlay"> <p>Test Frequenzmessung</p> </form> </div>
</div>


Es ist zu beobachten, dass die Funktion im unteren Frequenzbereich ($f$=440 Hz bis $f$=700 Hz) zwar zu erkennen
ist, allerdings leuchten die Richtungs-LEDs nur schwach. Ein eindeutiges Erkennen der LEDs ist ab einer Frequenz von 
$f$=710 Hz gegeben. Die höchste Frequenz bei der eine eindeutige Funktion beobachtet werden konnte war $f$=4937 Hz. Bei
höheren Frequenzen konnte beobachtet werden, dass entweder die oberste LED nicht mehr leuchtet oder das meherere LEDs
gleichzeitig leuchten, wodurch eine eindeutige Erkennung der Richtung nicht mehr gegeben ist.


Das Frequenzspektrum der Audiospur des Videos ist in [Abbildung 26](01_fig_024) zu sehen. Es ist zu erkennen, dass die 
Energiedichte bei den unteren Frequenzen höher ist, als bei den oberen Freqeunzen. Interessanterweise sind bei den
unteren Frequenzen außerdem Oberwellen/Harmonische erkennbar. 


```{figure} ../images/mojo/Spec_project.png 
:name: 01_fig_024

Spectrumsverlauf des Frequenztests
```

Bis hierher konnte die grundsätzliche Funktion und ihre Grenzen getestet werden. Einen Beweis ist diese Arbeit jedoch
noch schuldig geblieben. In der theoretischen Erläuterung des Signalflusses wurde erwähnt, dass das PDM-Signal die
Informationen über den eingehenden Ton beinhaltet. Hierfür wurde der Datenausgang eines Mikrofons mit einem Logic Analyzer
verbunden, um das ausgehende Signal aufzunehmen. Der Aufbau ist in [Abbildung 27]( 01_fig_027) zu erkennen. 


```{figure} ../images/mojo/Setup_spectrum.png 
:name: 01_fig_027

Frequenzspektrum des PDM Signals
```

Es wurde ein Ton mit einer Frequenz von $f$=1 kHz von der Bose Box abgespielt. Innerhalb dieses Zeitraums wurde
das ausgehende Signal vom Mikrofon und vom Datenlogger aufgenommen. Die erzeugten Daten wurden mit folgendem
Pythonskript ausgewertet: 

```{literalinclude} ../files/math/mojo/hanning.py
:language: python
```

Mit Hilfe dieses Skriptes wurde dann das Spektrum erzeugt, welches in [Abbildung 28]( 01_fig_028) dargestellt
ist. Im Spektrum ist zu erkennen, dass die höchste Amplitude des Frequenzspektrums bei $f \approx$ 1 kHz zu 
finden ist. Demnach trägt das PDM-Signal die Information über die Frequenz des eingespielten akustischen Signals.


```{figure} ../images/mojo/PDM_Spectrum.png 
:name: 01_fig_028

Aufbau zur Untersuchung des PDM Ausgangssignals.
```

Was hier ebenfalls sichtbar wird ist, dass die Betragsdifferenz nicht eindeutig wirkt. Das zeugt von einem
schlechten Signal-zu-Rausch-Verhältnis (SNR). Ein Grund für das schlechte SNR kann am Aufbau des Versuchs liegen. Die
Ausgangsfrequenz des PDM-Signals betrug messtechnisch $f_{Out}$=5.8 MHz und für die Verbindung von Logic Analyzer
und Microphone Shield wurden Jumper-Wire verwendet. Das kann dazu geführt haben, dass andere Signale auf die Leitung
eingekoppelt haben und somit störende Frequenzanteile mitgemessen wurden.


### Fazit

Das Mojo V3 Board bietet mit dem Microphone Shield eine gute Möglichkeit einen Einblick in komplexes FPGA Design zu
wagen. Neben diesem sehr interessanten Projekt für fortgeschrittenes FPGA Design finden sich auf Alchitry Labs weitere
Projekte für jeden Schwierigkeitsgrad. Mit Lucid bieten Sie ebenfalls einen niederschwelligen Einstieg für alle, die
Microkontroller Programmierung gewöhnt sind, da Lucid die Hürde kleiner machen soll als den Sprung von z.B. C zu
VHDL. Sollte jemand größeres Interesse daran finden, FPGA Design weiter zu vertiefen und eigene Projekte zu entwickeln,
würde ich nach diesen Erfahrungen und Beobachtungen empfehlen den Fokus auf VHDL oder Verilog als Beschreibungsspraache
zu legen und nicht zu lange den Umweg über Lucid zu nehmen. 

Das FPGA was auf dem Mojo V3 Board verbaut ist wird nicht mehr von XILINX unterstützt und auch Alchitry Labs hat weitere
Boards entwickelt, welche von Ihnen Emfohlen werden und die sicherlich einen Blick wert sind. Die Untersuchungen von
Alchitry labs und von diesem Projekt sind mit dieser Arbeit noch nicht abgeschlossen. Folgende Aufgaben könnten für
zukünfitge Projekte interessant sein:


1. Übertragen der Projektdateien von Lucid in VHDL oder Verilog. Lucid ist eine von Alchitry Labs entwickelte
   Beschreibungssprache, die es Programmierern von Mikrocontrollern leichter machen soll von der 
   Mikrocontroller-Programmierung auf FPGA-Programmierung umzusteigen bzw. dieses überhaupt zu probieren.
   
2. Ein weiterer Versuch könnte sein zu testen, ob andere Frequenzgrenzen erreicht werden können, wenn andere
   Lautstärkepegel genutzt werden können.
   
3. Das Gleiche gilt umgekehrt bei der Frage, ob andere Lautstärkepegel erreicht werden können, wenn eine andere Frequenz
   für den Versuch genutzt wird. 

