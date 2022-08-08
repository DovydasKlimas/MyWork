import numpy as np;
import matplotlib.pyplot as plt;
import random
import failas4
duomenys = ["0_1", "0_2", "0_3", "1_1", "1_2", "1_3", "2_1", "2_2", "2_3", "3_1", "3_2", "3_3", "4_1", "4_2", "4_3", "5_1", "5_2", "5_3", "6_1", "6_2", "6_3", "7_1", "7_2", "7_3", "8_1", "8_2", "8_3", "9_1", "9_2", "9_3"]
TansSet = ["0", "0", "0", "1", "1", "1", "2", "2", "2", "3", "3", "3", "4", "4", "4", "5", "5", "5", "6", "6", "6", "7", "7", "7", "8", "8", "8", "9", "9", "9"]
test = ["0_t",  "1_t", "2_t", "3_t", "4_t", "5_t", "6_t", "7_t", "8_t", "9_t"]


duomenys = ["01", "02", "03", "11", "12", "13", "21", "22", "23", "31", "32", "33", "41", "42", "43", "51", "52", "53", "61", "62", "63", "71", "72", "73", "81", "82", "83", "91", "92", "93"]
TansSet = ["0", "0", "0", "1", "1", "1", "2", "2", "2", "3", "3", "3", "4", "4", "4", "5", "5", "5", "6", "6", "6", "7", "7", "7", "8", "8", "8", "9", "9", "9"]
test = ["0test",  "1test", "2test", "3test", "4test", "5test", "6test", "7test", "8test", "9test"]

def VienasNN(X, W): #1 neuronas, ivesti sudaro X signalai ir ju svoriai W
    svsuma = W[0];
    for i in range(len(X)):
        svsuma += X[i]*W[i+1] #svorine suma suzadinimo funkcijai
    return Sigmoide(svsuma) #neurono atsakas i X signalus yra suzadinimo funckijos atsakymas

def Sigmoide(x):#neurono suzadinimo funckija
    # print(x)
    return 1/(1+np.exp(-x + 10)) #analitine israiska

def ViensluoksnisT(X,W): # Neuronu (gali buti bet koks skaicius) vieno sluoksnio tinklas
    eil=len(W); #Svoriu matricoje yra tinklo architekturos dimensijos, t.y. neuronu skaicius
    st=len(W[0]); #ir ivesties signalu skaicius
    Y=[]; # masyvas kaupti visu neuronu atsakus
    for i in range(eil):
        Y.append(VienasNN(X,W[i])); #suzadinamas kaskart vis kitas neuronas, kurio atsakas kaupiamas i bendra masyva
    return Y #grazinami visi neuronu atsakai i zadinima

def SklaidosAtvirkstinisSklidimasTrainSet(XSet, W, YSet): # Neuroninio vieno sluoksnio tinklo treniravimas
    iterMax = 250; #numatytas mokymo iteraciju skaicius
    eps = 1e-6; #norimas tikslumas treniruoteje
    iterNr = 1;
    derr = []; #daliniu klaidos funkcijos ivestiniu masyvas (gradientas)
    step = 0.5; #zingsnis svoriams keisti "minus" gradiento kryptimi
    TestSetElSk = len(XSet); #kelioms reiksmems treniruojamas tinklas
    TestSetElNr = 0; #einamoji "treniruojamoji" reiksmes numeris
    # X = XSet[TestSetElNr] #saugojamos "treniruojamos" reiksmes
    NNTans = YSet[TestSetElNr]; #tikrasis tinklo atsakymas, t.y. "mokytojas"
    # X1 = [1] + X #formuojamas signalu ivesciu masyvas sandaugai su svoriais (9 signalai, taciau +1 suderinti su nulinio svoriu koeficientu w0)
    for i in range(len(NNTans)): #iniciliazuojame pradines reiksmes isvestinems
        derr.append(1e10) #kadangi nenaudojama array is numpy, priskyrimas atliekamas tiesiog panariui

    history = [[] for i in range(TestSetElSk)];

    Testi = 1 #treniravimo stabdymo salyga
    while Testi: #startuoja "treniravimas"
        Testi = 0
        for TestSetElNr in range(TestSetElSk):
            X = XSet[TestSetElNr];
            NNTans = YSet[TestSetElNr];
            X1 = [1] + X;
            NNFans=ViensluoksnisT(X,W); #kiekvienas tinklo neuronas bandomas zadinti, NNFans - faktinis neurono atsakas i X signalus ir ju svorius
            # print(NNFans) #tarpiniai faktiniai neuronu atsakai
            for i in range(len(NNTans)):
                derr[i] = (NNTans[i] - NNFans[i]) * NNFans[i] * (1-NNFans[i]); #kaskart skaiciuojamos dalines klaidos funkcijos isvestines kiekvieno svorio atvzilgiu (gradientas)
                for j in range(len(W[0])): #iteruojama per kiekviena svori atskirai
                    W[i][j] += derr[i]*X1[j]*step # kiekvienas svoris atnaujinamas gradiento kryptimi
            ABSderr = max([abs(el) for el in derr]); #el - elementas: #didziausia absoliutine verte isvestiniu masyve
            TestiLok = (ABSderr > eps) and (iterNr < iterMax); #jeigu didziausia paklaida pasiekia norima tiksluma, stabdome treniravima
            Testi = Testi or TestiLok; #while salygos atnaujinimas

            history[TestSetElNr].append(ABSderr);
        iterNr += 1 #sukasi iteracijos

    # graph(history);

    return W; #grazinamas istreniruoto neuroninio tinklo svoriu rinkinys visiems neuronams

def graph(history):
    for i in range(nums):
        plt.xlabel("iterNr");
        plt.ylabel("ABSderr");
        plt.title(i);
        for j in range(numsets):
            plt.plot(range(1, len(history[i * numsets + j]) + 1), history[i * numsets + j], label = j + 1);
        plt.legend();
        plt.savefig(f"{i}.png");
        plt.show();
        plt.clf();

def testNetwork():
    mainSum = 0;
    testSum = 0;
    for i in range(nums):
        print(f"{i}: ", end = "")
        for j in range(numsets):
            res = ViensluoksnisT(XSet[i * numsets + j], NewW);
            guess = res.index(max(res))
            print(guess, end = " ");
            if (i == guess):
                mainSum += 1;
        res = ViensluoksnisT(XtestSet[i], NewW);
        guess = res.index(max(res));
        print("|", guess, end = " ");
        if (i == guess):
            testSum += 1;
        print();

    print(f"Pagrindines reiksmiu teisingumas: {mainSum / nums / numsets * 100}%");
    print(f"Testiniu reiksmiu teisingumas: {testSum / nums * 100}%");

XSet = [];
XtestSet = []
NNTansSet = [];
W=[];


for i in range(len(duomenys)):
    XSet.append(failas4.read(duomenys[i], "duom"))
    NNTansSet.append(failas4.read(TansSet[i], "NNtansSet"))

for i in range(len(test)):
    XtestSet.append(failas4.read(test[i], "duom"))

SluoksDydzMas=[81+1,10] #architekturos parametrai (30 signalu svoriai + 1 w0 "bias")
for i in range(SluoksDydzMas[1]):
    W.append([])
    for j in range(SluoksDydzMas[0]):
            W[i].append(random.random())
nums = 10;
numsets = 3;
inputs = 81;

NewW = SklaidosAtvirkstinisSklidimasTrainSet(XSet, W, NNTansSet);
testNetwork();



