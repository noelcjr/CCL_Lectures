#!/bin/bash

pdb_cif.py prepare --input s_0_0_0_AA_BB.pdb --crdout s_0_0_0_AA_BB.crd --seqfix yes
charmm < setup_s_0_0_0_AA_BB.inp > setup_s_0_0_0_AA_BB.out

