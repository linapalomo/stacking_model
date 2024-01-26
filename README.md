# ECOLOGICAL AND ECONOMIC MODELLING – ANALYSIS OF COST-EFFECTIVENESS GAINS FROM STACKING OF ECOSYSTEM SERVICES FOCUSSING ON THE COMPARISON OF ECOSYSTEM SERVICES AND LAND USE TRADING 

This is the model for the master thesis. 
1. The standard deviation is established in file stack_0_comb.py for costs std_dev_lu = [0.50] and for benefits std_dev_b = [0.50], the standard deviations can be 0.25 or 0.50.
2. The stack_0_distr.py file generates the parameter combination randomly and assigns each combination an index from 0 to 63. In total there are 64 parameter combinations.
3. The file stack_0_distr.py  must be assigned an index (from 0 to 63) in the variable data data = all_data[0]
4. The stack_0_distr.py file generates a landscape randomly and with the parameters of the combination assigned in the data variable and the standard deviations. This code also assigns land uses to the parcels randomly.
5. The stack_main_file.py file runs files  stack_0_distr.py (which generates the landscape), stack_1_lu.py which corresponds to the first compensation scheme with fixed land uses and finally runs file stack_1_ess.py which is the scheme with fixed ESS.
6. The stack_main_file.py file runs the three files 50 times and saves the results in an excel file with the combination number added in the save file line. 

- The folders contain the excel files with the 50 runs for every combination of parameters for each standard deviation. And there is one excel file that contains the sensitivity analisis of the results for each standard deviation. 
