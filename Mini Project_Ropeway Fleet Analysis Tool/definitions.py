
import pandas as pd
from pathlib import Path
from time import sleep

def performance(time_s=1):
    print(".")
    sleep(time_s)
    print(".")
    sleep(time_s)
    print("Done")
    print()

def short_pause(time =1):
    print("")
    sleep(time)
    

def n_data():
    print("No data in memory")

class RopewayFleetAnalysis:
    def __init__(self, fleet_path,maintenance_path):
        self.fleet_path = fleet_path
        self.maintenance_path = maintenance_path
        self.loaded_data = False
        
    def load_data(self):
        if Path(self.fleet_path).exists():
            print("Loading fleet data")
            self.df_fleet = pd.read_csv(self.fleet_path)
            sleep(0.5)
            print("Fleet data was successfully loaded!")
        else:
            print("Wrong fleet path or file no exist")
            

        if Path(self.maintenance_path).exists():
            print("Loading maintenance data")
            self.df_maintenance = pd.read_csv(self.maintenance_path)
            sleep(0.5)
            print("Maintenance data was successfully loaded!")
        else:
            print("Wrong maintenance path or file no exist")
            

        if Path(self.fleet_path).exists() and Path(self.maintenance_path).exists():
            self.loaded_data = True
            print("Do you watn to show loded data? (y/n): ")
            while True: 
                 temp = input()                
                 if temp.upper() == "N": 
                     break
                 elif temp.upper() == "Y":
                     print(f"Fleet dataframe:\n{self.df_fleet}")
                     print(f"\nmaintenance dataframe:\n{self.df_maintenance}")
                     break
                 else:
                     print(f"Your input {temp} is wrong. Enter y or n ")
            
            
    def process_data(self):
            if self.loaded_data:
                print("""Next will be do:
    1. Fill missing values in fleet: 
        tension_kN → mean, 
        weight_kNm → mean, 
        span_m → median, 
        year_built → 2000
    2. Merges fleet with maintenance using left join on span_id. """)
                    #filling
                self.df_fleet["tension_kN"] = round(self.df_fleet["tension_kN"].fillna(self.df_fleet["tension_kN"].mean()),ndigits=0)
                self.df_fleet["weight_kNm"] = round(self.df_fleet["weight_kNm"].fillna(self.df_fleet["weight_kNm"].mean()),ndigits=1)
                self.df_fleet["span_m"] = self.df_fleet["span_m"].fillna(self.df_fleet["span_m"].median())
                self.df_fleet["year_built"] = self.df_fleet["year_built"].fillna(2000)
                    #Merging
                self.df_merg = pd.merge(self.df_fleet,self.df_maintenance,
                                        on = "span_id",
                                        how = "left")
            
                performance()

            else:
                n_data()
                
    def calculates_columns(self):
        if self.loaded_data:
            print("""Next will add column to merge DataFrame:
            1. Calculates catenary_a column = tension / weight rounded to 2 decimals
            2. Calculates age_years column = current year minus year_built
            3. Calculates days_since_service column as integer days """)

            self.df_merg["catenary_a"] = round(self.df_merg["tension_kN"] /
                                                self.df_merg["weight_kNm"],ndigits=2)
            self.df_merg["age_years"] = (pd.Timestamp.now()).year - self.df_merg["year_built"]
            
            self.df_merg["days_since_service"] = (pd.Timestamp.now() - pd.to_datetime(self.df_merg["last_service"])).dt.days
            
            performance()

        else:
            n_data()
        
    def fleet_sumary(self):
        self.total_ropeways = self.df_fleet.shape[0]
        print(f"Total number of ropeways: {self.total_ropeways}\n")

        count_by_type = self.df_fleet.groupby("type")["span_id"].count()
        print(f"Count table by {count_by_type}\n")

        count_by_region = self.df_fleet.groupby("region")["span_id"].count()
        print(f"Count table by {count_by_region}\n")

    def regional_analysis(self):
        # Groups by region, prints named aggregation table with: 
        # mean tension, max span, mean catenary_a, count — all rounded to 2 decimals
        self.df_reg_analys = round(self.df_merg.groupby("region").agg(
            mean_tension = ("tension_kN", "mean"),
            max_span = ("span_m","max"),
            mean_catenary_a = ("catenary_a","mean"),
            count_in_region = ("span_id", "count")),ndigits=2)
        print(f"Grouped by region:\n{self.df_reg_analys}")

    def risk_assessment(self):
        """
        Flags a ropeway as high risk if ANY of these are true:
            - age over 20 years
            - days since service over 500
            - no service record at all

        Prints all high risk ropeways with columns: 
            span_id, region, type, age_years, days_since_service, reason

        Prints total count and percentage of fleet
        """

        self.df_high_risk = self.df_merg[(self.df_merg["age_years"] > 20) | 
                            (self.df_merg["days_since_service"] > 500) |
                            (self.df_merg["last_service"].isna())]
        self.df_high_risk = self.df_high_risk[["span_id","region", "type","age_years","days_since_service"]]
        count_in_temp = self.df_high_risk.shape[0]
        percentil = 100/self.total_ropeways*count_in_temp

        print(f"\nRisk ropeways:\n{self.df_high_risk}")
        print(f"\nTotal high risk ropeways: {count_in_temp}\nPercentil high risk ropeways of whole fleet: {percentil:.2f} %")

        
    def cost_analysis(self):
        """
        - Groups by service_type — prints total cost, mean cost, count
        - Groups by technician — prints total cost per technician sorted descending
        - Prints which span had the most expensive single service
        """
        # Group by service
        self.group_by_ser = round(self.df_merg.groupby("service_type").agg(
            total_cost = ("cost_eur","sum"),
            mean_cost = ("cost_eur","mean"),
            coun_cost = ("cost_eur","count")),ndigits=2)
        #Group by technicion
        group_by_tech = self.df_merg.groupby("technician").agg(
            total_cost = ("cost_eur", "sum"))
        # Sorting descendong
        group_by_tech=group_by_tech.sort_values("total_cost",ascending=False)

        # find out position of the most expensive service
        most_expensive = self.df_merg["span_id"][self.df_merg["cost_eur"].idxmax()]
        
        print(f"\nCost analysis by service type:\n{self.group_by_ser}")
        print(f"\nCost analysis by technician:{group_by_tech}")
        print(f"Chairlift {most_expensive} had the most expensive service")

    def export_report(self, output_path):
        """
        Exports Excel file with 4 sheets:

            "Fleet" — full merged DataFrame
            "Regional" — regional analysis table
            "Risk" — high risk ropeways only
            "Costs" — cost summary by service type
        """
        self.output_path = output_path

        try:         
            with pd.ExcelWriter(self.output_path) as writer:
                self.df_merg.to_excel(writer,sheet_name="Fleet", index=False)
                self.df_reg_analys.to_excel(writer, sheet_name= "Regional", index = True)
                self.df_high_risk.to_excel(writer, sheet_name = "Risk", index = False)
                self.group_by_ser.to_excel(writer,sheet_name = "Costs", index = True)

                print(f"\nSaving data to {self.output_path}")
                performance()

        except PermissionError:

            print(f"!!!\nClose {self.output_path} and try again\n!!!")
            





            


                
        


