input_file = "D:\\Desktop\\2020.osm"
output_file = "D:\\Desktop\\2022.osm"
type = True
#"D:\\Desktop\\35000000.osm"
#"D:\\Desktop\\data\\changesets-240226.osm\\changesets-240226.osm"
with open(input_file, 'r',encoding='utf-8') as f_in, open(output_file, 'w',encoding='utf-8') as f_out:
    for index, line in enumerate(f_in):
        if index >= 10000000:
            if "<changeset" in line and "2022-07" in line and type:
                type = False
                f_out.write("<test>\n")
                print(line)
            if not type:
                if index % 10000000 == 0:
                    print(index)
                f_out.write(line)