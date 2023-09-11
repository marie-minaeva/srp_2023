#!/bin/bash
module load python/3.10.8
cd /proj/lappalainen_lab1/users/marii/srp_2023
for e in 1e-10 #1e-4 1e-5 1e-6 1e-10 1e-20 1e-30
do
	echo "./ADRB2/ADRB2_$e.a3m"
	singularity exec ./hh-suite_latest.sif hhblits -e $e -p 20 -B 20000 -i ./ADRB2/ADRB2.fasta -o hhlist.txt -oa3m "./ADRB2/ADRB2_$e.a3m" -d ./UniRef30_2023_02_hhsuite/UniRef30_2023_02 -cpu 20
	singularity exec ./hh-suite_latest.sif  reformat.pl a3m fas "./ADRB2/ADRB2_$e.a3m" "./ADRB2/ADRB2_$e.fas"
	python parse_msa.py --file "./ADRB2/ADRB2_$e.fas"
	cd ./ADRB2
	mkdir $e
	cd $e
	echo "../ADRB2_"$e"ali.fasta"
	singularity exec ../../stockholm/gemme_gemme.sif python2.7 /opt/GEMME/gemme.py "../ADRB2_"$e"ali.fasta" -r input -f "../ADRB2_"$e"ali.fasta"
	cd ../../
done

