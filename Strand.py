import bpy
from math import radians
import math


class Strand():

    First = None
    Last = None

    LengthFirst = -1
    LengthLast = -1

    Crossing = -1

    TouchingFirst = None
    TouchingLast = None

    Enabled = False

    staple = None

    CurrentStrand = None


    def setStrand(this, Lista, stp):
        this.CurrentStrand = Lista
        this.staple = stp


    def growStep(this):
        if this.CurrentStrand != None and this.staple != None:
            if len(this.CurrentStrand) > 1:
                this.growFirst()
                this.growLast()


    def growFirst(this):
        First = this.First = this.CurrentStrand[0]

        if First != None :
            Next = this.First.getNext()
            if Next != None and Next != First:
                dx = abs(Next.getX() - First.getX())
                stp = Next.getStaple()
                if stp == None:
                    if Next.getRod() == First.getRod() and dx == 1:
                        this.First = Next
                        Next.setStaple(this.staple)
                        this.CurrentStrand.insert(0,Next)
                else:
                    if stp != this.staple:
                        this.TouchingFirst = stp






    def growLast(this):
        Last = this.Last = this.CurrentStrand[-1]

        if Last != None :
            Next = this.Last.getPrev()
            if Next != None and Next != Last:
                dx = abs(Next.getX() - Last.getX())
                stp = Next.getStaple()
                if stp == None:
                    if Next.getRod() == Last.getRod() and dx == 1:
                        this.Last = Next
                        Next.setStaple(this.staple)
                        this.CurrentStrand.append(Next)
                else:
                    if stp != this.staple:
                        this.TouchingLast = stp

    
