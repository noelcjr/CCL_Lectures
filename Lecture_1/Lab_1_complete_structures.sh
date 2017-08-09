#!/bin/bash

# WARNING 1: Do not run this script in the same folder used to obtain the repository.
#            its outputs will be overwritten everytime the repository is updated pulled.
#            and you will lost your files. Copy this file to another directory and run it.

# Warning 2: Edit the variables ex, py and charmm to point to the location of these folders.

# 1. Download both 1BRS.pdb and 1BRS.cif
wget https://files.rcsb.org/view/1BRS.pdb
wget https://files.rcsb.org/view/1BRS.cif
#    1BRS has 6 chains, A,B,C,D,E and F. AD, BE and CF form dimers.
#    It is a crystal structure with three dimers, and we only need one.
#    Chains belonging to the smae dimers are not contiguous to each other
#    in alphatical order by adentifiers. Open both PDB and CIF file in your
#    editor and notice the formating. CIF is a newer and better version to PDB.
##########################################################

# 2. Watch the structure in VMD. VMD can only read PDB files.
vmd 1BRS.pdb

# 3. Separates chains corresponding to dimers.
#    We only need one dimer that we need to extract, or separate, from the other
#    two dimers. The following command separates chains from CIF files by AD,BE,CF
#    and generates outputs in PDB format.
/usr/bin/python /PATHTO/EntropyMaxima/src/cif.py --help
/usr/bin/python /PATHTO/EntropyMaxima/src/cif.py --extract --chains --groups AD,BE,CF --inp2 1BRS.cif
vmd 1BRS_0_AD.pdb
###########################################################

# 4. It is difficult to detect all the gaps in structure by visual inspection.
#    Gaps in the middle of the sequence are easy to miss, and gaps at the
#    begining or end of each chain of the proteins are even harder to detect visually.
#    The following command does a gap analysis that gives the parts of the protein
#    that are present in the sequence, but for which there is no coordinates in the X-structure.
/usr/bin/python /PATHTO/EntropyMaxima/src/pdb.py --help
/usr/bin/python /PATHTO/EntropyMaxima/src/pdb.py --gaps --inp 1BRS_0_AD.pdb
/usr/bin/python /PATHTO/EntropyMaxima/src/pdb.py --gaps --inp 1BRS_0_BE.pdb
/usr/bin/python /PATHTO/EntropyMaxima/src/pdb.py --gaps --inp 1BRS_0_CF.pdb
#########################################################

# completing resideus 1 and 2 missing in chain C from chain B."
/usr/bin/python /PATHTO/EntropyMaxima/src/pdb.py --align --refA 1BRS_0_BE.pdb --refatomsA CA,B,3,6 --fitA 1BRS_0_CF.pdb --fitatomsA CA,C,3,6 --outA 1BRS_complete_CD_1.pdb --addatomsA B,1,2:C,1,2

# 5. Now, There is another way to complete a structure.
#    This way is useful for when there is not a coplete structure
#    to fill in the gaps, and it is meant completely automated.
#    FOR HELP TYPE: /usr/bin/python /PATHTO/EntropyMaxima/src/gen_csv.py --help

/usr/bin/python /PATHTO/EntropyMaxima/src/gen_csv.py --fromcif --cif 1BRS.cif --out1 1BRS_0.csv --pep ../EntropyMaxima/charmm_templates/peptides.pdb

# ERROR: After a series of warnings (nothing to worry about), the program crashes. Why? CIF structures were meant
#        to have a more consisten format than PDB, but errors still happen because my code can not account for all those
#        differences in formating.

# 6. The original crystals structure 1BRS.pdb had an OXT oxygen that is not recognized
#    by the CHARMM parameter routine we used. We need to replace 'OXT' with 'O  '.
#
grep OXT 1BRS_complete_CF_1.pdb
perl -pi -e 's/OXT/O  /g' 1BRS_complete_CF_1.pdb

# 7. We know use the program reduce. The structure 1BRS.pdb has no hydrogen bonds whatsoever, so reduce does not
#    do a lot for this structure, but it is always important to include this. The pdb.py program following in the
#    next line checks histadines and considers the number of hydrogen atoms and its position in Histadine
#    to assign the right type of histidine. CHARMM has three types of histidin labeled HSD, HSE, HSP, and it 
#    has to read this labels because it will not recognize the label HIS.
reduce -HIS -FLIP -OH -ROTEXOH -BUILD -OCC0.0 -H2OOCC0.0 -H2OB1000 1BRS_complete_CF_1.pdb > 1brs_complete_cf_1r.pdb
vimdiff 1BRS_complete_CF_1.pdb 1brs_complete_cf_1r.pdb
/usr/bin/python /PATHTO/EntropyMaxima/src/pdb.py --prepare --pdbin1 1brs_complete_cf_1r.pdb --crdou 1brs_complete_cf_1r.crd --seqfix yes

# 8. Now that we have the right histidine types, we use CHARMM to add missing hydrogen atoms.
#    8.1 Copy a CHARMM script to your directory setup_one.inp
#    8.2 Modify the CHARMM script on the fly with the right parameters.
#    8.3 Run the CHARMM script
cp /PATHTO/EntropyMaxima/charmm_templates/setup_one.inp .

perl -pi -e 's/generate C1 first none last none setup/generate C first none last none setup/g' setup_one.inp
perl -pi -e 's/generate C2 first none last none setup/generate F first none last none setup/g' setup_one.inp
perl -pi -e 's/C1.SEQ/C.SEQ/g' setup_one.inp
perl -pi -e 's/C2.SEQ/F.SEQ/g' setup_one.inp
perl -pi -e 's/C1_FIXRES.INP/C_FIXRES.INP/g' setup_one.inp
perl -pi -e 's/C2_FIXRES.INP/F_FIXRES.INP/g' setup_one.inp
perl -pi -e 's/INFILE/1brs_complete_cf_1r/g' setup_one.inp
perl -pi -e 's/OUTFILE/1brs_complete_cf_1rr/g' setup_one.inp

charmm_40b2 < setup_one.inp > setup_one.out

# 9. We can add and remove residues from the files output by CHARMM. First, get the structure in a CSV format with gen_csv.py.
#    Then use add_residues.py and del_residues.py to modify the structure.
/usr/bin/python /PATHTO/EntropyMaxima/src/gen_csv.py --frompsfcrd --crd 1brs_complete_cf_1rr.crd --psf 1brs_complete_cf_1rr_xplo.psf
/usr/bin/python ../EntropyMaxima/src/add_residues.py --apn "1,1,C,Ndir" --res "LYS,LYS,LYS,ASP" --inp 1brs_complete_cf_1rr.csv --out 1brs_complete_cf_1rr.csv
/usr/bin/python ../EntropyMaxima/src/del_residue.py --rem "65,2,F,ASN" --inp 1brs_complete_cf_1rr.csv --out 1brs_complete_cf_1rr.csv
/usr/bin/python ../EntropyMaxima/src/del_residue.py --rem "64,2,F,GLU" --inp 1brs_complete_cf_1rr.csv --out 1brs_complete_cf_1rr.csv
/usr/bin/python ../EntropyMaxima/src/del_residue.py --rem "63,2,F,THR" --inp 1brs_complete_cf_1rr.csv --out 1brs_complete_cf_1rr.csv
