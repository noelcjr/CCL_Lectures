#!/bin/bash

echo "First get the 1GDD and 1GIA PDB and CIFfiles from the rcsb.org"
wget https://files.rcsb.org/view/1GDD.pdb
wget https://files.rcsb.org/view/1GDD.cif

wget https://files.rcsb.org/view/1GIA.pdb
wget https://files.rcsb.org/view/1GIA.cif


echo "Gaps test pased for both CIF and PDB file types/n"
pdb_cif.py --gaps --inputfile 1GDD.pdb
pdb_cif.py --gaps --inputfile 1GDD.cif

echo "First just fit 1GDD (incomplete) to 1GIA (complete) no added atoms"
pdb_cif.py --align --inputfile 1GIA.pdb --refatoms CA,A,198,201:CA,A,218,221 --fit 1GDD.pdb --fitatoms CA,A,198,201:CA,A,218,221 --out 1GDD_to_1GIA_just_fit.pdb

echo "Then we repeat the same procedure but this time we add the missing region."
pdb_cif.py --align --inputfile 1GIA.pdb --refatoms CA,A,198,201:CA,A,218,221 --fit 1GDD.pdb --fitatoms CA,A,198,201:CA,A,218,221 --out 1GDD_to_1GIA_fit_and_add.pdb --addatoms A,202,217:A,202,217

# 5. Now, There is another way to complete a structure.
#    This way is useful for when there is not a coplete structure
#    to fill in the gaps, and it is meant completely automated.
#    FOR HELP TYPE: /usr/bin/python /PATHTO/EntropyMaxima/src/gen_csv.py --help

gen_csv.py --fromcif --cif 1BRS.cif --out1 1BRS_0.csv --pep ../../EntropyMaxima/charmm_templates/peptides.pdb

# ERROR: After a series of warnings (nothing to worry about), the program crashes. Why? CIF structures were meant
#        to have a more consisten format than PDB, but errors still happen because my code can not account for all those
#        differences in formating.

# 6. The original crystals structure 1BRS.pdb had an OXT oxygen that is not recognized
#    by the CHARMM parameter routine we used. We need to replace 'OXT' with 'O  '.
#
grep OXT 1BRS_complete_CF_1.pdb
