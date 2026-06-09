from definitions import RopewayFleetAnalysis
from definitions import short_pause

# Create object
path_fleet1 = r"Pandas\Mini Project_Ropeway Fleet Analysis Tool\fleet.csv"
path_maitenance = r"Pandas\Mini Project_Ropeway Fleet Analysis Tool\maitenance.csv"
path_export = r"Pandas\Mini Project_Ropeway Fleet Analysis Tool\export_ropeways.xlsx"


# MAIN

if __name__ == "__main__":
        #create analysis object
    fleet1 = RopewayFleetAnalysis(path_fleet1,path_maitenance)
        # Load DataFrame
    fleet1.load_data()
        # Filling, merge, calculate catenary/age in years/days since service
    fleet1.process_data() 
        # Calclating columns catenary_a, age_years,days_since_service
    fleet1.calculates_columns()
        # Sumary, total, count by type and region
    print("""
    =============
       RESULTS
    =============""")
    fleet1.fleet_sumary()
    short_pause()
        # Grouped by region
    fleet1.regional_analysis()
    short_pause()
        # Printing all high risk ropeways
    fleet1.risk_assessment()
    short_pause()
        # cost analysis
    fleet1.cost_analysis()
    short_pause()
        #export to excel_
    fleet1.export_report(path_export)
    print(f"\n====\nBYE\n====")
    
    