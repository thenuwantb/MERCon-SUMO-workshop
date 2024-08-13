def generate_edge_relation_xml(count_df, output_file='edge_relation_data.xml'):
    """
        Generate an XML file containing edge relation data based on the provided DataFrame.

        Parameters:
        - count_df (DataFrame): DataFrame containing edge relation data.
        - output_file (str): Path to the output XML file. Default is 'edge_relation_data.xml'.

        Returns:
        - None (outputs an edge relation file)
    """
    starting_intervals = count_df['Interval Begin'].unique().tolist()
    ending_intervals = count_df['Interval End'].unique().tolist()

    with open(output_file, 'w') as fh:
        fh.write("<data>\n")

        for start, end in zip(starting_intervals, ending_intervals):
            df_interval = count_df[
                (count_df['Interval Begin'] == start) & (count_df['Interval End'] == end)].reset_index()
            interval_id = df_interval['Time'][0]
            fh.write(f"\t<interval id=\"{interval_id}\" begin=\"{start}\" end=\"{end}\">\n")

            for index, row in df_interval.iterrows():
                from_edge = row['From Road (in SUMO NET)']
                to_edge = row['To Road (in SUMO NET)']
                veh_count = row['Total (Except Route Bus)']
                description = "Junction : " + row['Location'] + " Direction : " + row['Direction']

                fh.write(f"\t\t<!--\"{description}\"-->")
                fh.write("\n")
                write_edge_relation(fh, from_edge, to_edge, veh_count)

            fh.write(f"\t</interval>\n")
            fh.write("\n")

        fh.write("</data>")

    fh.close()


def write_edge_relation(fh, from_edge, to_edge, veh_count):
    """
       Write edge relation data to the given file handle.

       Parameters:
       - fh (file handle): File handle to write data.
       - from_edge (str): Name of the starting edge.
       - to_edge (str): Name of the ending edge.
       - veh_count (int): Vehicle count for the edge relation.

       Returns:
       - None
    """
    fh.write(f"\t\t<edgeRelation from=\"{from_edge}\" to=\"{to_edge}\" count=\"{veh_count}\"/>\n")
