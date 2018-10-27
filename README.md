# 224w-education-graphs
Final project for cs224w (fall 2018)

# Data processing pipeline
- Parse xml to csv:
	- `python util/parse_xml.py` Parses the default `Posts.xml`
	- `python util/parse_xml.py <PATH_TO_FILE>.xml` Parses whatever xml file you pass as the first command line arg
	- This saves a csv in the same directory as the original xml.
- Read csv:
	- Use pandas `DataFrame.read_csv('<PATH_TO_FILE>.csv', usecols=['body', 'owneruserid', 'id'])`
	- Replace `usecols` with the desired column names 
