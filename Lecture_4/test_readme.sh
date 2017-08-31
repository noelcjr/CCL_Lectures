#!/bin/bash

# 1. Download insulin (2HIU) and Leucine zipper (2ZTA).
echo "First get the insulin and leucine zipper CIF file, 1GDD and 1GIA PDB and CIFfiles from the rcsb.org"
wget https://files.rcsb.org/view/2HIU.cif
wget https://files.rcsb.org/view/2ZTA.cif


# 2. Check for gaps in the structure.
echo "Gaps test pased for both CIF and PDB file types/n"
pdb_cif.py --gaps --input 2HIU.cif
pdb_cif.py --gaps --input 2ZTA.cif


# 3. The last two steps found no gaps in the two structure by checking residue numbers only, the next steps considers sequence information for 
#    detecting gaps at the begining an the end of the protein. These steps also extract structures from CIF file to PDB files that can be open in VMD.
gen_csv.py --fromcif --cif 2HIU.cif --out1 2HIU.csv --pep ../../EntropyMaxima/charmm_templates/peptides.pdb --top ../../EntropyMaxima/params/charmm27.ff/
gen_csv.py --fromcif --cif 2ZTA.cif --out1 2ZTA.csv --pep ../../EntropyMaxima/charmm_templates/peptides.pdb --top ../../EntropyMaxima/params/charmm27.ff/

# 4. The previous steps add N and C terminals to cap the ends of proteins. 
del_residue.py --rem "1,1,A,ACE" --inp 2HIU.csv --out 2HIU.csv --par ../../EntropyMaxima/params/charmm27.ff/
del_residue.py --rem "1,2,B,ACE" --inp 2HIU.csv --out 2HIU.csv --par ../../EntropyMaxima/params/charmm27.ff/

# 5. Now let's add a string of amino acids to the N-terminal and in the N-terminal direction.
add_residues.py --apn "1,1,A,Ndir" --res "SER,GLY,ASP,ASP,ASP,ASP,LYS" --inp 2HIU.csv --out 2HIU.csv --pep ../../EntropyMaxima/charmm_templates/peptides.pdb --par ../../EntropyMaxima/params/charmm27.ff/
add_residues.py --apn "1,2,B,Ndir" --res "SER,GLY,ASP,ASP,ASP,ASP,LYS" --inp 2HIU.csv --out 2HIU.csv --pep ../../EntropyMaxima/charmm_templates/peptides.pdb --par ../../EntropyMaxima/params/charmm27.ff/

# 6. Clean up. We will work on only one insulin structure, so we will delete some other files to
#    make things neat.
rm 2HIU_2.pdb 2HIU_3.pdb 2HIU_4.pdb 2HIU_5.pdb 2HIU_6.pdb 2HIU_7.pdb 2HIU_8.pdb 2HIU_9.pdb 2HIU_10.pdb

# 7. For insulin, reduce adds hydrogens to histidines, pdb_cif.py --prepare prepares files for charmm, and then charmm is ran.
reduce -HIS -FLIP -OH -ROTEXOH -BUILD -OCC0.0 -H2OOCC0.0 -H2OB1000 2HIU_1.pdb > 2hiu_1r.pdb
pdb_cif.py --prepare --input 2hiu_1r.pdb --crdout 2hiu_1r.crd --seqfix yes
charmm_40b2 < setup_2hiu.inp > setup_2hiu.out

# 8. For leucine zipper, reduce adds hydrogens to histidines, pdb_cif.py --prepare prepares files for charmm, and then charmm is ran.
reduce -HIS -FLIP -OH -ROTEXOH -BUILD -OCC0.0 -H2OOCC0.0 -H2OB1000 2ZTA_1.pdb > 2zta_1r.pdb
pdb_cif.py --prepare --input 2zta_1r.pdb --crdout 2zta_1r.crd --seqfix yes
charmm_40b2 < setup_2zta.inp > setup_2zta.out

# 9. This next step is to get some information to determine the best parameters for align and join insulin and leucine zipper.
pdb_cif.py --maxmin --input 2HIU_1.pdb
pdb_cif.py --maxmin --input 2ZTA_1.pdb

# 10. Build a flower or dandalion type of ensemble.
flower.py --center 2hiu_1rr.pdb --rotate 2zta_1rr.pdb --angle 45 --distance 45 --map yes --link "A:A,B:B" --par ../../EntropyMaxima/params/charmm27.ff/
flower.py --center 2hiu_1rr.pdb --rotate 2zta_1rr.pdb --angle 45 --distance 45 --map yes --link "A:B,B:A" --par ../../EntropyMaxima/params/charmm27.ff/
