#Python script to facilitate using the MIT Photonic Bands Package.
#Work in progress
#By Chris Flower

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import matplotlib.image as mpimg

def correct_abberation(ctl_location,ctlname,dielectricfn): #for some reason the unit cell is janked unless we do this...
	command3 = ['h5topng']
	command3.append('-S')
	command3.append('3')
	command3.append(ctlname+'-epsilon.h5')

	process = subprocess.Popen(command3, stdout=subprocess.PIPE, cwd=ctl_location)
	(out,err) = process.communicate()
	print(out)

	command4 = ['mpb-data']
	command4.append('-r') #this is definitely right for triang lattices...
	command4.append('-m') #this is definitely right for triang lattices...
	command4.append('3') #this is definitely right for triang lattices...
	command4.append('-n') #this is definitely right for triang lattices...
	command4.append('32')
	command4.append(ctlname+'-epsilon.h5')

	process = subprocess.Popen(command4, stdout=subprocess.PIPE, cwd=ctl_location)
	(out2,err2) = process.communicate()
	print(out2)

	command5 = ['h5topng']
	command5.append(ctlname+'-epsilon.h5:data-new') #this is definitely right for triang lattices...
	process = subprocess.Popen(command5, stdout=subprocess.PIPE, cwd=ctl_location)
	(out3,err3) = process.communicate()
	print(out3)

	img = mpimg.imread(ctl_location+ctlname+'-epsilon.png')
	if (dielectricfn):
		plt.imshow(img)
		plt.show() #displays the dielectric function

def produce_bands(ctl_location, ctlname, modetype): #modetype input is 'te' or 'tm'
	print("Produce bands called")

	command2 = ['grep']
	command2.append(modetype+'freqs')
	command2.append(ctlname + '.out')
	#command2.append('>') #these guys also arent playing nice but it's just telling us how to write the output
	#command2.append(ctlname + '.'+modetype+'.dat')
	process = subprocess.Popen(command2, stdout=subprocess.PIPE, cwd=ctl_location)
	(out,err) = process.communicate()
	outfile = open(ctl_location+ctlname + '.'+modetype+'.dat','w')
	outfile.write(out)


def process_ctl(ctl_location, ctlname): #method to produce the mpb output 
	print("process ctl called")
	command1 = ['mpb']
	command1.append(ctlname + '.ctl')
	#command1.append('>&')
	#command1.append(ctlname + '.out') 

	process = subprocess.Popen(command1, stdout=subprocess.PIPE, cwd=ctl_location)
	(out,err) = process.communicate()

	#write the output manually since the >& output is giving problems
	outfile = open(ctl_location + ctlname+'.out','w')
	outfile.write(out)
	#print out

	#subprocess.run('mpb ' + ctl + '.ctl >& ' + ctl + '.out')
	#subprocess.run('grep tefreqs' + ctl + '.out >' + ctl + '.te.dat')
	#subprocess.run('grep tmfreqs' + ctl + '.out >' + ctl + '.tm.dat')

def process_data(num_bands, k_points, interp, filename, plt_at): #method to plot mpb band plots
	total_ks = (k_points)*(interp)+(k_points+1) #this is because kpoints doesnt count repeats i.e. going back to gamma
	columns = []
	for counter in range(1,num_bands+k_points+3): #calculates the number of columns the output has based on inputs
		columns.append(counter) #3 comes from the magnitude and the index column and indexing at 0

	indata = np.loadtxt(filename, unpack=True, dtype=str, skiprows=1, usecols=columns, delimiter=', ') #dont need this usecols I think...

	kindex = indata[0:1]
	kindex = kindex.astype(np.float)

	#write a loop to create a new array that holds the x y z coordinates of the k points 
	k_matrix = np.empty([total_ks, k_points]) 

	for step in range(0,k_points):
		k_matrix[:,step] = indata[step+1].astype(np.float)


	kmag = indata[k_points+1] #grab the magnitude column
	kmag = kmag.astype(np.float)

	band_matrix = np.empty([total_ks,num_bands])

	for step2 in range(0,num_bands):
		band_matrix[:,step2] = indata[step2+2+k_points].astype(np.float)

	kmag = np.transpose(kmag)
	kspace_path = np.linspace(0,total_ks-1, total_ks)

	for step3 in range(0,num_bands):
		plt.plot(kspace_path, np.transpose(band_matrix[:,step3]), plt_at)



main_dir = '/home/chris/Documents/Projects/MPB/honeycomb1/'
ctl = 'honeycomb_rod_ctl2'

process_ctl(main_dir, ctl)

produce_bands(main_dir, ctl, 'tm')
produce_bands(main_dir, ctl, 'te')

correct_abberation(main_dir,ctl,True)

process_data(8,3,5,main_dir+ctl+'.'+'tm.dat','-ro')
process_data(8,3,5,main_dir+ctl+'.'+'te.dat','-bo')
plt.show()