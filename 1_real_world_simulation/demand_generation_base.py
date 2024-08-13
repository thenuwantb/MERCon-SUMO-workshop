import os
import pandas as pd
import helper.generate_edge_relation_xml as gen_veh
import helper.generate_bus_trips_xml as gen_bus
import subprocess
import numpy as np
from xml.etree import ElementTree as et

np.random.seed(55)

# 1. Set Working Directory (This folder path has to be changed based on your folder arrangement)
os.chdir("E:\\MERCon\\pythonProject\\Guide\\1_real_world_simulation")

# 2.1 Read Data (will be read relative to the working directory set)
warmup_count = pd.read_excel("data/traffic_counts_all.xlsx", sheet_name='545am_6am_minor_warmup')
counts_6am_7am = pd.read_excel("data/traffic_counts_all.xlsx", sheet_name='6am_7am_with_minor_warmup')

# 2.2. Read bus related data
bus_route_dict = gen_bus.bus_routes
bus_trips = pd.read_pickle("data/bus/bus_trips_morning_peak.pkl")

# 3. Generate Edge relation file (This will output a SUMO readable file)
gen_veh.generate_edge_relation_xml(warmup_count, output_file='demand/edge_relation_warmup.xml')
gen_veh.generate_edge_relation_xml(counts_6am_7am, output_file='demand/edge_relation_6am_7am.xml')

# 4. Set the random seed (you can set any 5-digit number of your choice)
random_seed = 12345

# 4.1. Access the xml tree structure of the .sumocfg XML file
sumo_config_file = "run_simulation.sumocfg"
tree = et.parse(sumo_config_file)
root = tree.getroot()

# 4.2. random_num_tag is a variable which has a placeholder to the seed value which we need to change
random_num_tag = root.find("./random_number/seed")
print(f"Random Seed : {random_seed}")

# 5. Generate Bus Trips. The output of this is a SUMO readable .xml file
bus_trips_df = gen_bus.generate_bus_trips_df(bus_trips_df=bus_trips, bus_route_dict=bus_route_dict,
                                             seed=random_seed)
gen_bus.generate_bus_trips_xml(bus_trips_df=bus_trips_df, output_file='additional/bus/bus_trips_6am_7am.xml',
                               warmup=900)

############# 5. Using SUMO Python built-in Python scripts ###################
# 5.1. Random trips call
white_list_warmup = ("randomTrips.py "
                     "--net-file network/colombo_galleroad.net.xml "
                     "--end 900 "
                     "--fringe-factor 200 "
                     "--min-distance 150 "
                     "--max-distance 5000 "
                     "--period 0.1 "
                     f"--seed {random_seed} "
                     "--speed-exponent 4.0 "
                     "--validate "
                     "--route-file intermediate_output/whitelist_warmup.rou.xml")

white_list_6am_7am = ("randomTrips.py "
                      "--net-file network/colombo_galleroad.net.xml "
                      "--end 3600 "
                      "--fringe-factor 200 "
                      "--min-distance 150 "
                      "--max-distance 5000 "
                      "--period 0.1 "
                      f"--seed {random_seed} "
                      "--speed-exponent 4.0 "
                      "--validate "
                      "--route-file intermediate_output/whitelist_6am_7am.rou.xml")

subprocess.run(white_list_warmup, shell=True)
subprocess.run(white_list_6am_7am, shell=True)

# 5.2. Route sampler call
route_sampler_warmup = ("routeSampler.py "
                        "--route-files intermediate_output/whitelist_warmup.rou.xml "
                        "--turn-files demand/edge_relation_warmup.xml "
                        "--verbose "
                        f"--seed {random_seed} "
                        "--minimize-vehicles 0.1 "
                        "--min-count 1 "
                        "--output-file demand/calibrated_demand_warmup.rou.xml "
                        "--attributes=\"type=\"'warmup'\" departLane=\"'free'\" \"departSpeed=\"'max'\" ")

route_sampler_6am_7am = ("routeSampler.py "
                         "--route-files intermediate_output/whitelist_6am_7am.rou.xml "
                         "--turn-files demand/edge_relation_6am_7am.xml "
                         "--verbose "
                         f"--seed {random_seed} "
                         "--minimize-vehicles 0.1 "
                         "--min-count 1 "
                         "--output-file demand/calibrated_demand_6am_7am.rou.xml "
                         "--attributes=\"type=\"'6am_7am'\" departLane=\"'free'\" \"departSpeed=\"'max'\" ")

subprocess.run(route_sampler_warmup, shell=True)
subprocess.run(route_sampler_6am_7am, shell=True)

###################################################################

# 6. Update the random seed and create a temporary .sumofcg file
random_num_tag.attrib["value"] = str(random_seed)
tree.write('config_temp_base.sumocfg')

# 7. Run simulation
run_simulation = ("sumo -c "
                  "config_temp_base.sumocfg")
subprocess.run(run_simulation, shell=True)

# 8. Dealing with outputs
# xml2csv.py is a python script available with SUMO installation
# This will output a csv file of the same data, with the same filename (with .csv extention)
xml2csv_call = """python "%SUMO_HOME%\\tools\\xml\\xml2csv.py "\
                      output/edge/edge_data_output_base.xml -s , \
                   """
subprocess.run(xml2csv_call, shell=True)

# 8.1 Read that generated .csv file as a pandas dataframe
edge_data_temp = pd.read_csv('output/edge/edge_data_output_base.csv')

# 8.2. Add the current random seed as a column (for recording purposes)
edge_data_temp['random_seed'] = random_seed
edge_data_temp['scenario'] = 'base_scenario'
print(edge_data_temp.head())

# 9. Save the data collected from all random seeds as a csv file.
edge_data_temp.to_csv('simulation_output/edge_output_base_agg_300.csv', )
