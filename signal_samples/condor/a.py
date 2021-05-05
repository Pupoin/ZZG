from __future__ import print_function
from ROOT import TCanvas, TGraph, TLegend, TGaxis, gPad, TPad, gStyle
from ROOT import gROOT, TMultiGraph
from math import sin
from array import array
 
 
c1 = TCanvas( 'c1', 'A Simple Graph Example', 300, 200, 700, 500 )
gStyle.Reset("Modern"); # "Modern", "Plain", "Classic"
c1.SetMargin(0.13, 0.13, 0.13, 0.13)# c1.SetFillColor( 42 )

 

xx= array('d', [-5.1, -4.5, -3.2, -2.1, -0.8 , 0.01, 0.9, 1.9, 2.8, 3.8, 4.9])
yx= array('d', [-25, -28, -30 , -20 , -10, 0, 10 , 20 , 30 , 27 , 25 ])

n = len(xx)
y = array( 'd' , [1408, 1403, 1474, 1580, 1650, 1753, 1648, 1530, 1488, 1401, 1404] )


grv = TGraph( 11, xx, y )
grv.SetLineColor( 1 )
grv.SetLineWidth( 4 )
grv.SetMarkerColor( 1 )
grv.SetMarkerStyle( 20 )
grv.GetXaxis().SetTitle( 'X [cm]' )
grv.GetYaxis().SetTitle( "f_{3} [Hz]" )
grv.GetYaxis().SetTitleSize(0.04)
grv.GetXaxis().SetTitleSize(0.04)
grv.GetYaxis().SetLabelSize(0.04)
grv.GetXaxis().SetLabelSize(0.04)



gr = TGraph( 11, xx, yx )
gr.SetLineColor( 2 )
gr.SetLineWidth( 4 )
gr.SetMarkerColor( 4 )
gr.SetMarkerStyle( 23 )
gr.SetTitle( '' )
gr.GetXaxis().SetTitle( 'X [cm]' )
gr.GetYaxis().SetTitle( "#Delta f_{12} [Hz]" )
gr.GetYaxis().SetTitleSize(0.04)
gr.GetXaxis().SetTitleSize(0.04)
gr.GetYaxis().SetLabelSize(0.04)
gr.GetXaxis().SetLabelSize(0.04)

# p1 =  TPad("p1", "", 0, 0, 1, 1)
# p2 =  TPad("p2", "", 0, 0, 1, 1)


# mg =  TMultiGraph("mg","mg")
# p1.Draw()
# p1.cd()
# gr.Draw( 'ACP' )
# gPad.Update()

# xmin = p1.GetUxmin()
# xmax = p2.GetUxmax()
# # print (xmax)
# # xmax=gr.GetMaximum()
# dx = (xmax - xmin) / 0.8 
# ymin = grv.GetHistogram().GetMinimum()
# ymax = grv.GetHistogram().GetMaximum()
# dy = (ymax - ymin) / 0.8 
# p2.Range(xmin-0.1*dx, ymin-0.1*dy, xmax+0.1*dx, ymax+0.1*dy)
# p2.Draw()
# p2.cd()
grv.Draw( ' CAP ')
# gPad.Update()

# c1.cd()
# mg.Add( gr )
# mg.Add( grv )
# grv.Draw("ALP")
# mg.Draw("ALP")

# axis = TGaxis(xmax, ymin, xmax, ymax, ymin, ymax, 505, "+L")
# axis.SetTitle("f_{3} [Hz]")
# axis.SetTitleSize(0.04)
# axis.SetLabelSize(0.04)
# axis.Draw()
# gPad.Update()


lg = TLegend(0.15, 0.68, 0.43, 0.85)
lg.AddEntry(gr, "#Delta f_{12}", "lp")
lg.AddEntry(grv, "f_{3}", "lp")
lg.SetLineColor(0)
lg.Draw()
gPad.Update()


# TCanvas.Update() draws the frame, after which one can change it
c1.Update()
# c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 12 )
c1.Modified()
c1.Update()
c1.cd()
c1.SaveAs("a.png")
# If the graph