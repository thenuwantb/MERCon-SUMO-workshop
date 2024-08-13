import pandas as pd
import numpy as np
import random
from distfit import distfit

# 1. Constants
SHORT_DIST_MAX_SPEED = "9.72"
LONG_DIST_MAX_SPEED = "12.5"
OTHER_MAX_SPEED = "12.5"
SIGMA = 0.5

# 2. Define Bus Routes
STOPS_100_101 = ["01_cross_junction", "02_mendis_tower", "03_rawatawatta", "04_lakshapathiya", "05_commercial_bank_rw",
                 "06_katubedda_junc", "07_mallika_bakery", "08_german_tec", "09_soyza_flat", "10_golumadama",
                 "11_golumadama_sathosa", "12_belek_kade", "13_vijitha_hall", "14_maliban_junc"]
STOPS_255 = ["07_mallika_bakery", "08_german_tec", "09_soyza_flat", "10_golumadama",
             "11_golumadama_sathosa", "12_belek_kade", "13_vijitha_hall", "14_maliban_junc"]
STOPS_183 = ["01_cross_junction", "02_mendis_tower", "03_rawatawatta", "04_lakshapathiya", "05_commercial_bank_rw",
             "06_katubedda_junc", "07_mallika_bakery", "08_german_tec", "09_soyza_flat", "10_golumadama",
             "11_golumadama_sathosa", "12_belek_kade", "13_vijitha_hall", "14_maliban_junc"]
STOPS_154 = ["08_german_tec", "09_soyza_flat", "10_golumadama",
             "11_golumadama_sathosa", "12_belek_kade", "13_vijitha_hall", "14_maliban_junc"]
STOPS_192 = ["01_cross_junction", "02_mendis_tower", "03_rawatawatta", "04_lakshapathiya", "05_commercial_bank_rw",
             "06_katubedda_junc", "07_mallika_bakery", "08_german_tec", "09_soyza_flat", "10_golumadama",
             "11_golumadama_sathosa", "12_belek_kade", "13_vijitha_hall"]
STOPS_LONG_DISTANCE = ["01_cross_junction", "03_rawatawatta",
                       "05_commercial_bank_rw",
                       "06_katubedda_junc", "08_german_tec", "10_golumadama",
                       "12_belek_kade", "14_maliban_junc"]
OTHER_BUS_STOPS = ["06_katubedda_junc",
                   "09_soyza_flat", "14_maliban_junc"]

bus_routes = {
    100: {'headways': [{'start_time': 0, 'end_time': 3599, 'headway': 120}],
          'stops': STOPS_100_101,
          'route': 'bus_100',
          'bus_type': 'short_distance',
          'start_edge': '112446385#5',
          'end_edge': '102651364#23.9'},
    101: {'headways': [{'start_time': 0, 'end_time': 3599, 'headway': 120}],
          'stops': STOPS_100_101,
          'route': 'bus_101',
          'bus_type': 'short_distance',
          'start_edge': '51086283#3',
          'end_edge': '102651364#23.9'},
    154: {'headways': [{'start_time': 0, 'end_time': 3599, 'headway': 600}],
          'stops': STOPS_154,
          'route': 'bus_154',
          'bus_type': 'short_distance',
          'start_edge': 'OR_I_017',
          'end_edge': '102651364#23.9'},
    183: {'headways': [{'start_time': 0, 'end_time': 3599, 'headway': 600}],
          'stops': STOPS_183,
          'route': 'bus_183',
          'bus_type': 'short_distance',
          'start_edge': '51086283#3',
          'end_edge': '102651364#23.9'},
    192: {'headways': [{'start_time': 0, 'end_time': 3599, 'headway': 900}],
          'stops': STOPS_192,
          'route': 'bus_192',
          'bus_type': 'short_distance',
          'start_edge': '112446385#5',
          'end_edge': '19811337#1'},
    255: {'headways': [{'start_time': 0, 'end_time': 3599, 'headway': 300}],
          'stops': STOPS_255,
          'route': 'bus_255',
          'bus_type': 'short_distance',
          'start_edge': 'gneE5',
          'end_edge': '102651364#23.9'},
    'Long Distance': {'headways': [{'start_time': 0, 'end_time': 3599, 'headway': 90}],
                      'stops': STOPS_100_101,
                      'route': 'bus_long_dist',
                      'bus_type': 'long_distance',
                      'start_edge': '112446385#5',
                      'end_edge': '102651364#23.9'},
    'Other': {'headways': [{'start_time': 0, 'end_time': 3599, 'headway': 80}],
              'stops': OTHER_BUS_STOPS,
              'route': 'bus_other',
              'bus_type': 'other',
              'start_edge': '112446385#5',
              'end_edge': '102651364#23.9'}
}


def generate_bus_trips_df(bus_trips_df, bus_route_dict, seed):
    # Set Random Seed
    random.seed(seed)

    # Initiate Empty Lists to Capture Values Generated
    depart_times = []
    veh_ids = []
    bus_types = []
    start_edges = []
    end_edges = []
    bus_stops = []
    stop_times = []

    for route_no, route_details in bus_route_dict.items():
        rand_num = random.randint(0, 450)
        sub_departure_time = []
        sub_veh_ids = []
        for headway in route_details['headways']:
            route_depart = np.arange(start=headway['start_time'] + rand_num, stop=headway['end_time'],
                                     step=headway['headway']).tolist()
            route_veh_id = [f"{route_details['route']}_{headway['start_time']}_{headway['end_time']}{i + 1}" for i, dep_time in enumerate(route_depart)]

            sub_departure_time.extend(route_depart)
            sub_veh_ids.extend(route_veh_id)

        bus_type = [route_details['bus_type']] * len(sub_departure_time)
        start_edge = [route_details['start_edge']] * len(sub_departure_time)
        end_edge = [route_details['end_edge']] * len(sub_departure_time)
        stops = [route_details['stops']] * len(sub_departure_time)

        depart_times.extend(sub_departure_time)
        veh_ids.extend(sub_veh_ids)
        bus_types.extend(bus_type)
        start_edges.extend(start_edge)
        end_edges.extend(end_edge)
        bus_stops.extend(stops)

        # generate stop times
        route_emp_stop_times = bus_trips_df[bus_trips_df['Route No.'] == route_no][
            "Stop Time (Sec)"].to_numpy()

        dist_fit = distfit()

        print(f"Fitting stop time distribution for route  {route_no}")
        dist_fit.fit_transform(route_emp_stop_times, verbose='silent')


        for index, departed_bus in enumerate(sub_departure_time):
            # print(departed_bus)
            gen_stop_times = dist_fit.generate(len(route_details['stops']), random_state=index)
            gen_stop_times_int_cap = [np.clip(gen_stop_times.astype(int), a_min=0, a_max=180).tolist()]
            stop_times.extend(gen_stop_times_int_cap)

    route_df = pd.DataFrame({"trip_id": veh_ids,
                             "depart": depart_times,
                             "start_edge": start_edges,
                             "bus_type": bus_types,
                             "end_edge": end_edges,
                             "bus_stops": bus_stops,
                             "stop_times": stop_times})

    # Sorting the data frame so that the vehicles can be inserted in to the simulation orderly
    route_df.sort_values(by="depart", ascending=True, inplace=True, ignore_index=True)

    return route_df


def generate_bus_trips_xml(bus_trips_df, output_file, warmup=900):
    # 2. Generate XML File

    with open(output_file, 'w') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write(
            '<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n')
        fh.write('\n')

        # Define Vehicle Types

        fh.write(
            f"\t<vType id=\"short_distance\" vClass=\"bus\" accel=\"2.6\" decel=\"4.5\" sigma=\"{SIGMA}\" length=\"12\" minGap=\"3\" maxSpeed=\"{SHORT_DIST_MAX_SPEED}\"/>\n")
        fh.write(
            f"\t<vType id=\"long_distance\" vClass=\"bus\" accel=\"2.6\" decel=\"4.5\" sigma=\"{SIGMA}\" length=\"12\" minGap=\"3\" maxSpeed=\"{LONG_DIST_MAX_SPEED}\"/>\n")
        fh.write(
            f"\t<vType id=\"other\" vClass=\"bus\" accel=\"2.6\" decel=\"4.5\" sigma=\"{SIGMA}\" length=\"12\" minGap=\"3\" maxSpeed=\"{OTHER_MAX_SPEED}\"/>\n")

        fh.write(f"\n")

        for _, row in bus_trips_df.iterrows():
            trip_id = row['trip_id']
            bus_type = row['bus_type']
            vehicle_depart = row['depart'] + warmup
            start_edge = row['start_edge']
            end_edge = row['end_edge']
            bus_stops = row['bus_stops']
            stop_times = row['stop_times']

            fh.write(
                f"\t<trip id=\"{trip_id}\" type=\"{bus_type}\" depart=\"{vehicle_depart}\" from=\"{start_edge}\" to=\"{end_edge}\">\n")
            for stop, stop_time in zip(bus_stops, stop_times):
                fh.write(f"\t\t<stop busStop=\"{stop}\" duration=\"{stop_time}\"/>\n")
            fh.write(f"\t</trip>\n")

        fh.write('</additional>')

        fh.close()
