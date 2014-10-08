# -*- coding: utf-8 -*-

#------------------------------------------------------ingranalo.py----#
#
#                     INGRANALO
#
#
# Copyright (C) 2014 Matteo Perini (perini.matteo@gmail.com)
# Copyright (C) 2014 Alessandro Navarini (navarini1997@gmail.com)
#
#
# Copyright (C) 2007 Aaron Spike  (aaron @ ekips.org)
# Copyright (C) 2007 Tavmjong Bah (tavmjong @ free.fr)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#-----------------------------------------------------------------------

#Importo la libreria math per inserire le funzioni matematiche
from math import *

#Importo le librerie per l'interfaccia grafica
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *


#Funzione che crea il file svg con i dati inseriti dell'utente
#Parametri d'ingresso: numero di denti, passo, angolo di pressione, diametro dell'eventuale foro e presenza del foro
def ingranalo(teeth, pitch, angle, diametro, foro, titolo):

    def involute_intersect_angle(Rb, R):
        Rb, R = float(Rb), float(R)
        return (sqrt(R**2 - Rb**2) / (Rb)) - (acos(Rb / R))

    def point_on_circle(radius, angle):
        x = radius * cos(angle)
        y = radius * sin(angle)
        return (x, y)

    def points_to_svgd(p):
        f = p[0]
        p = p[1:]
        svgd = 'M%.3f,%.3f' % f
        for x in p:
            svgd += 'L%.3f,%.3f' % x
        svgd += 'z'
        return svgd

    # print >>sys.stderr, "Teeth: %s\n"        % teeth

    two_pi = 2.0 * pi

    # Pitch (circular pitch): Length of the arc from one tooth to the next)
    # Pitch diameter: Diameter of pitch circle.
    pitch_diameter = float( teeth ) * pitch / pi
    pitch_radius   = pitch_diameter / 2.0

    # Base Circle
    base_diameter = pitch_diameter * cos( radians( angle ) )
    base_radius   = base_diameter / 2.0

    # Diametrial pitch: Number of teeth per unit length.
    pitch_diametrial = float( teeth )/ pitch_diameter

    # Addendum: Radial distance from pitch circle to outside circle.
    addendum = 1.0 / pitch_diametrial

    # Outer Circle
    outer_radius = pitch_radius + addendum
    outer_diameter = outer_radius * 2.0

    # Tooth thickness: Tooth width along pitch circle.
    tooth  = ( pi * pitch_diameter ) / ( 2.0 * float( teeth ) )

    # Undercut?
    undercut = (2.0 / ( sin( radians( angle ) ) ** 2))
    needs_undercut = teeth < undercut

    # Clearance: Radial distance between top of tooth on one gear to bottom of gap on another.
    clearance = 0.0

    # Dedendum: Radial distance from pitch circle to root diameter.
    dedendum = addendum + clearance

    # Root diameter: Diameter of bottom of tooth spaces. 
    root_radius =  pitch_radius - dedendum
    root_diameter = root_radius * 2.0

    half_thick_angle = two_pi / (4.0 * float( teeth ) )
    pitch_to_base_angle  = involute_intersect_angle( base_radius, pitch_radius )
    pitch_to_outer_angle = involute_intersect_angle( base_radius, outer_radius ) - pitch_to_base_angle

    centers = [(x * two_pi / float( teeth) ) for x in range( teeth ) ]

    points = []

    for c in centers:

        # Angles
        pitch1 = c - half_thick_angle
        base1  = pitch1 - pitch_to_base_angle
        outer1 = pitch1 + pitch_to_outer_angle

        pitch2 = c + half_thick_angle
        base2  = pitch2 + pitch_to_base_angle
        outer2 = pitch2 - pitch_to_outer_angle

        # Points
        b1 = point_on_circle( base_radius,  base1  )
        p1 = point_on_circle( pitch_radius, pitch1 )
        o1 = point_on_circle( outer_radius, outer1 )

        b2 = point_on_circle( base_radius,  base2  )
        p2 = point_on_circle( pitch_radius, pitch2 )
        o2 = point_on_circle( outer_radius, outer2 )

        if root_radius > base_radius:
            pitch_to_root_angle = pitch_to_base_angle - involute_intersect_angle(base_radius, root_radius )
            root1 = pitch1 - pitch_to_root_angle
            root2 = pitch2 + pitch_to_root_angle
            r1 = point_on_circle(root_radius, root1)
            r2 = point_on_circle(root_radius, root2)
            p_tmp = [r1,p1,o1,o2,p2,r2]
        else:
            r1 = point_on_circle(root_radius, base1)
            r2 = point_on_circle(root_radius, base2)
            p_tmp = [r1,b1,p1,o1,o2,p2,b2,r2]

        points.extend( p_tmp )

    path = points_to_svgd( points )
    #Apro il file svg e comincio a scriverlo considerando i dati dell'utente
    try:
        out_file=open(str(titolo),'w')    #Apro il file creato dalla finestra di salvataggio
        out_file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        out_file.write('<svg\n')
        out_file.write('   xmlns:dc="http://purl.org/dc/elements/1.1/"\n')
        out_file.write('   xmlns:cc="http://creativecommons.org/ns#"\n')
        out_file.write('   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n')
        out_file.write('   xmlns:svg="http://www.w3.org/2000/svg"\n')
        out_file.write('   xmlns="http://www.w3.org/2000/svg"\n')
        out_file.write('   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"\n')
        out_file.write('   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"\n')
        out_file.write('   width="'+str(1000)+'"\n')
        out_file.write('   height="'+str(1000)+'"\n')
        out_file.write('   id="svg2"\n')
        out_file.write('   version="1.1"\n')
        out_file.write('   inkscape:version="0.48.4 r9939">\n')

        out_file.write('  <sodipodi:namedview\n')
        out_file.write('     id="base"\n')
        out_file.write('     pagecolor="#ffffff"\n')
        out_file.write('     bordercolor="#666666"\n')
        out_file.write('     borderopacity="1.0"\n')
        out_file.write('     inkscape:pageopacity="0.0"\n')
        out_file.write('     inkscape:pageshadow="2"\n')
        out_file.write('     inkscape:zoom="0.35"\n')
        out_file.write('     inkscape:cx="500"\n')
        out_file.write('     inkscape:cy="500"\n')
        out_file.write('     inkscape:document-units="px"\n')
        out_file.write('     inkscape:current-layer="layer1"\n') 
        out_file.write('     />\n')        
        out_file.write('  <g\n')                 
        out_file.write('     inkscape:label="Livello 1"\n')
        out_file.write('     inkscape:groupmode="layer"\n')
        out_file.write('     id="layer1"\n')
        out_file.write('     transform="translate(500,500)"\n')
        out_file.write('     >\n')
        #Embed gear in group to make animation easier:
        #Translate group, Rotate path.

        ##t = 'translate(' + str( self.view_center[0] ) + ',' + str( self.view_center[1] ) + ')'
        ##g_attribs = {inkex.addNS('label','inkscape'):'Gear' + str( teeth ),
        ##             'transform':t }
        ##g = inkex.etree.SubElement(self.current_layer, 'g', g_attribs)

        # Create SVG Path for gear
        ##style = { 'stroke': '#000000', 'fill': 'none' }
        ##gear_attribs = {'style':simplestyle.formatStyle(style), 'd':path}
        ##gear = inkex.etree.SubElement(g, inkex.addNS('path','svg'), gear_attribs )

        out_file.write('<path\n')
        out_file.write('d="'+path+'"\n')
        out_file.write('style="fill:none;stroke:#000000;stroke-width:0.07086614" />\n')

        out_file.write('  </g>\n')
        out_file.write('  <g>\n')  
        if foro=="True":
            out_file.write('<circle cx="500" cy="500" r="'+str(diametro/2)+'" style="stroke:#000000;fill:none;stroke-width:0.07086614"/>\n')
        out_file.write('  </g>')
        out_file.write('</svg>')
        out_file.close()

        #Apro una finestra per avvisare l'utente che il file è stato creato
        showinfo("Avviso", "Il file è stato creato correttamente")
    except:
        pass

#Costante per convertire i millimetri in pixel
from_mm_to_pixel = 3.5433071

#Funzione che cotrolla se il contenuto delle caselle di testo è numerico
def controllo(Input):
    try:
        variabile = float(Input)
        return Input
    except:
        showerror("Errore", "Non hai inserito un valore numerico, riprova.")
        return None

def pulsante():
    continua = True     #Si recuperano i valori dalle caselle di testo e dalla checkbox
    udmm = udm.get()    #Unita' di misura selezionata
    denti_ = controllo(denti.get().replace(",", "."))   #Numero dei denti
    passo_ = controllo(passo.get().replace(",", "."))    #Altezza
    angolo_ =  controllo(angolo.get().replace(",", "."))     #Angolo di pressione
    foro_ = str(bool(foro.get()))       #Foro
    if foro_=="False":
        diametro_ = 0        #Se foro non è selezionato metto 0 nella variabile per non ricevere errori
    else:
        diametro_ = controllo(diametro.get().replace(",", "."))    #Altrimenti eseguo i controlli

    #Controlla se il valore delle variabili è valido
    if (denti_<>None and passo_<>None and angolo_<>None and diametro_<>None):

        #Conversione inch --> millimetri
        if udmm=="inch":
            passo_*=25.4
            diametro_*=25.4

        #Conversione centimetri --> millimetri
        elif udmm=="centimetri":
            passo_*=10
            diametro_*=10

        #Controllo se il numero di denti è un numero intero
        if str(denti_).find('.')<>-1:
            showwarning("Attenzione", "Il numero di denti deve essere un valore intero")
            continua=False

        #Controllo se l'angolo di pressione è compreso fra 15 e 30 gradi
        if int(angolo_)<15 or int(angolo_)>30:
            showwarning("Attenzione", "L'angolo di pressione deve essere compreso fra 15 e 30 gradi")
            continua=False

        #Se i controlli non riscontrano problemi si procede con la creazione del file svg 
        if continua==True:

            print "Denti:", denti_, "millimetri"
            print "Altezza:", passo_, "millimetri"
            print "Angolo:", angolo_, "millimetri"
            print "Foro:", foro_
            print "Diametro foro:", diametro_, "millimetri"

            #Finestra per il salvataggio del file    
            titolo_ = asksaveasfilename(defaultextension='.svg', title='Salvataggio del file')

            #Conversione millimetri --> pixel
            if udmm=="millimetri":
                passo_=float(passo_)*from_mm_to_pixel
                diametro_=float(diametro_)*from_mm_to_pixel
                angolo_=float(angolo_)
                denti_=int(denti_)
            else:
                passo_=float(passo_)
                diametro_=float(diametro_)
                angolo_=float(angolo_)
                denti_=int(denti_)

            #Chiamo la funzione che crea il file svg
            ingranalo(denti_, passo_, angolo_, diametro_, foro_, titolo_)

#Interfaccia grafica con Tkinter
#Le label vuote sono state posizionate per riempire gli spazi e mantenere allineate le righe
#Gli elementi della finestra sono disposti in tre frame verticali: sinistra, centro e destra

#Creo la finestra
main = Tk()
main.title("Ingranalo")

#Suddivido la finestra in tre frame
sinistra = Frame(main)
centro = Frame(main)
destra = Frame(main)

#Frame sinistra: descrizioni
l1=Label(sinistra, text="Unita' di misura").pack(pady=1)
l2=Label(sinistra, text="Numero dei denti").pack(pady=1)
l3=Label(sinistra, text="Passo").pack(pady=1)
l4=Label(sinistra, text="Angolo di pressione").pack(pady=1)
l5=Label(sinistra, text="Diametro foro").pack(pady=1)
sinistra.pack(side=LEFT, fill=BOTH)

#Frame centro: raccolta input e pulsante
udm=Spinbox(centro, values=('millimetri', 'centimetri', 'inch', 'pixel'))
udm.pack()
denti = Entry(centro)
denti.pack()
passo = Entry(centro)
passo.pack()
angolo = Entry(centro)
angolo.pack()
diametro = Entry(centro, text="0")
diametro.pack()
p = Button (centro, text="Disegna", command=pulsante)
p.pack()
centro.pack(side=LEFT, fill=BOTH)

#Frame destra: checkbox
l20=Label(destra, text="").pack(pady=1)
l21=Label(destra, text=" ").pack(pady=1)
l22=Label(destra, text=" ").pack(pady=1)
l23=Label(destra, text=" ").pack(pady=1)
foro=BooleanVar()
w = Checkbutton (destra, text="Foro", variable = foro, onvalue = True, offvalue = False)
w.pack()
destra.pack(side=LEFT, fill=BOTH)

#Avvio la routine che aggiorna l'interfaccia grafica di Tkinter
main.mainloop()
