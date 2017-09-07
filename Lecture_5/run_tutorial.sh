#!/bin/bash

yourfile="s_0_0_0_aa_bb"

mkdir $yourfile
cp $yourfile".pdb" $yourfile
cp /home/Programs/EntropyMaxima/charmm_templates/setup_one.inp $yourfile"/setup_one.inp"
cp /home/Programs/EntropyMaxima/charmm_templates/minimize.inp $yourfile"/minimize.inp"
cd $yourfile

perl -pi -e 's/INFILE/'$yourfile'/g' setup_one.inp
perl -pi -e 's/OUTFILE/'$yourfile'r/g' setup_one.inp

pdb_cif.py prepare --input $yourfile".pdb" --crdout $yourfile".crd" --seqfix yes

charmm < setup_one.inp > setup_one.out

perl -pi -e 's/INPUT/'$yourfile'r/g' minimize.inp
perl -pi -e 's/OUTPUT/'$yourfile'r/g' minimize.inp

charmm < minimize.inp > minimize.out

# Now, copy and paste the pdb files to your computer and load them in VMD

mkdir box_setup
cd box_setup
cp /home/Programs/EntropyMaxima/charmm_templates/waterbox.inp .

perl -pi -e "s/PATH/\/home\/CCL_Lectures\/Lecture_5\/"$yourfile"/g" waterbox.inp
perl -pi -e "s/INFILE/..\/"$yourfile"r/g" waterbox.inp
perl -pi -e "s/OUTFILE/"$yourfile"r_min3_box/g" waterbox.inp

charmm < waterbox.inp > waterbox.out

cd ..
mkdir add_ions
cd add_ions
cp /home/Programs/EntropyMaxima/charmm_templates/add_NaCl.inp .

perl -pi -e "s/PATH/\/home\/CCL_Lectures\/Lecture_5\/"$yourfile"box_setup/g" add_NaCl.inp
perl -pi -e "s/INPUT/"$yourfile"r_min3_box/g" add_NaCl.inp
perl -pi -e "s/OUTPUT/"$yourfile"r_min3_box_ions/g" add_NaCl.inp

charmm < add_NaCl.inp > add_NaCl.out

cd ..
mkdir NAMDsim
cd NAMDsim
cp /home/Programs/EntropyMaxima/charmm_templates/NAMD.conf $yourfile".conf"

perl -pi -e "s/PATH/\/home\/CCL_Lectures\/Lecture_5\/"$yourfile"\/add_ions/g" $yourfile".conf"
perl -pi -e "s/INPUT/"$yourfile"r_min3_box_ions/g" $yourfile".conf"
perl -pi -e "s/OUTPUT/"$yourfile"r_min3_box_ions_namd/g" $yourfile".conf"

pdb_cif.py maxmin --input ../add_ions/s_0_0_0_aa_bbr_min3_box_ions.pdb 
#('Number of Atoms ', 33357)
#('Xmin - Xmax', -54.646999, ' - ', 54.738998)
#('Ymin - Ymax', -30.139999, ' - ', 30.367001)
#('Zmin - Zmax', -25.535, ' - ', 25.527)
#--------------------------------
#('Celbasis X, Y, Z:', 109.386, 60.507, 51.062)

perl -pi -e "s/CELL_X/109.386/g" $yourfile".conf"
perl -pi -e "s/CELL_Y/60.507/g" $yourfile".conf"
perl -pi -e "s/CELL_Z/51.062/g" $yourfile".conf"

cp /home/Programs/NAMD/NAMD_2.11_Linux-x86_64-multicore/namd2 /usr/local/bin/namd2_multicore

namd2_multicore +p8 s_0_0_0_aa_bb.conf &> s_0_0_0_aa_bb_1.out &
