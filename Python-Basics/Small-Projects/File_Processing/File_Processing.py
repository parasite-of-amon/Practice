with open(r'Introductiion.txt',"w") as myfile:
     myfile.write('Introduction \n Name: Soham Deepak Satpute \n Proffesion: Student \n Age: 15 years')
     myfile.write('\n \nPrivate Information \n Standard: 10th \n Intrests: Python, Chess, Mathematics \n Gender: Male \n  ')


with open(r'My First HTML Page.html','w') as myfile2:
     myfile2.write('''
     <html>
     <head>
     <title> My Information </title>
     </head>
     <body>
     <h1> My Information </h>
     <p align = "Center"> Introduction <br>
     Name: Soham Deepak Satpute <br>
     Proffesion: Student <br>
     Age: 15 years <br> <br>
 
     Private Information <b>
     Standard: 10th <br>
     Intrests: Python, Chess, Mathematics <br> 
     Gender: Male  <br> ''') 

with open(r'C:\BioProject\Biology-Mega_Page.html','w') as BioProject_Main:
     BioProject_Main.write('''
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <title>STEM CELLS AND THEIR IMPORTANCE IN MEDICAL SCIENCE</title>
</head>
<body bgcolor="#FFFF00">

<h1 align="center" style="background-color:#B603F4">___________________________________________________________________________________</h1>
<h1 align = 'center' style="color:#0000FF" >STEM CELLS</h1><u>
    <h1 align="center" style="color:#0000FF">_______}[------------------------------------------------]}_______</h1>
    <h5 align="center" style="color:#03A9F4">HomePage - Introduction</h5>
</u>
    <h5 align="center" >Soham-Deepak-Satpute</h5>
<h1 align="center" style="background-color:#B603F4">-----------------------------------------------------------------------------------------------------------------------------</h1>
<b><h1>What Are Stem Cells?</h1>
<h3 align="left" style="background-color:#00FFCC" > Stem cells are special human cells that can develop into many different cell types. This can range from muscle cells to brain cells.
    In some cases, they can also fix damaged tissues. Researchers believe that stem cell-based therapies may one day be used to treat serious illnesses such as paralysis and Alzheimer disease.
    Stem cells are the body's raw materials — cells from which all other cells with specialized functions are generated. Under the right conditions in the body or a laboratory,
    stem cells divide to form more cells called daughter cells.</h3>
<ol>
    <li>Stem cells provide new cells for the body as it grows and replace specialised cells that are damaged or lost. They have two unique properties that enable them to do this:</li>
    <ul>
        <li>They can divide repeatedly to produce new cells.</li>
        <li>As they divide, they can change into the other types of cell that make up the body.</li>
    </ul>
</ol>
</b>
<p align="center" style="background-color:#039BE5">
<img align="middle" height="400" border="color:black" width="400" src="Stemcells 2.png" alt="Stem_Cells">
</p>
<h2 align="right">Types Of Stem Cells -- <a href="Types_Of_StemCells_.html">Next Page</a></h2>
</body>
</html>''')