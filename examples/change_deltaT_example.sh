
# You will need to copy this into the MEM directory and update the BASE directory and FILE list and DELTAT

BASE="Input_Data/n_years/" # Path to input files
DELTAT=24 # Number of hours per time step
HEADER=1 # Number of header rows in your selected MEM input files (this can vary from file to file)


for FILE in 20200624v4_PJM_2018_mthd3_1990-2019_solar_rmLeap FR_demand_unnormalized_expDT_rmLeap 20200624v4_ERCO_2018_mthd3_1990-2019_wind_rmLeap 20200624v4_NYIS_2018_mthd3_1990-2019_solar_rmLeap PJM_mem_1993-2019_expDT_rmLeap 20201230v3_FR_mthd3_1990-2019_wind_rmLeap 20201230v3_FR_mthd3_1990-2019_solar_rmLeap 20200624v4_PJM_2018_mthd3_1990-2019_wind_rmLeap 20200624v4_NYIS_2018_mthd3_1990-2019_wind_rmLeap 20200624v4_ERCO_2018_mthd3_1990-2019_solar_rmLeap ERCOT_mem_1998-2019_expDT_rmLeap NYISO_demand_unnormalized_expDT_rmLeap; do

    python change_delta_T_for_inputs.py "${BASE}${FILE}.csv" ${DELTAT} ${HEADER}
    echo ""
    echo ""

    echo "Prepending to file: ${BASE}${FILE}_deltaT${DELTAT}.csv"
    echo "BEGIN_DATA,,,," > tmp.csv
    cat "${BASE}${FILE}_deltaT${DELTAT}.csv" >> tmp.csv
    mv tmp.csv "${BASE}${FILE}_deltaT${DELTAT}.csv"
done
