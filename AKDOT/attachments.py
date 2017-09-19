import arcpy, os

# Set local variables.
rootFolder = r'c:\Demos\AK\DOT\RatingWalls2016Sample'
sourcePoints = r'c:\Demos\AK\DOT\RWI.gdb\RetainingWalls'
sourceGDB = os.path.dirname(sourcePoints)
sourceAttachments = sourcePoints + '__ATTACH'
tempMatchTable = "MatchTable"

route_field = 'ICDSRtNN'
mp_field = 'ICDSMPN'

matchid_field = "MatchID"
matchfilepath_field = "Filename"

#truncate the attachments before running? If not, comment out the next line
arcpy.TruncateTable_management(in_table=sourceAttachments)

table = arcpy.CreateTable_management(out_path=sourceGDB, out_name=tempMatchTable, template="", config_keyword="")
arcpy.AddField_management(in_table=table, field_name=matchid_field, field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NON_NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=table, field_name=matchfilepath_field, field_type="TEXT", field_precision="", field_scale="", field_length="260", field_alias="", field_is_nullable="NON_NULLABLE", field_is_required="NON_REQUIRED", field_domain="")         

#Build the attachment match table by looping over all of the folders that contain photos
for route_folder in os.listdir(rootFolder):
    if route_folder[0].find('.gdb') == -1:
        for mp_folder in os.listdir(os.path.join(rootFolder, route_folder)):
            cursor = arcpy.da.InsertCursor(table,[matchid_field, matchfilepath_field])
            expr1 = route_field + "='" + route_folder + "' AND " + mp_field + "=" + mp_folder + ""
            with arcpy.da.SearchCursor(sourcePoints, ["OBJECTID", route_field, mp_field],where_clause=expr1) as cursor1:
                for row in cursor1:
                    print(row[0])
            for filename in os.listdir(os.path.join(rootFolder, route_folder, mp_folder)):
                fileUpper = filename.upper()
                #let's assume all of the files we want to add are jpeg files
                if fileUpper.endswith(".JPG"):
                    bHasFiles = True
                    cursor.insertRow([row[0],os.path.join(rootFolder, route_folder, mp_folder, filename)])
                    print("Inserting... " + fileUpper)
            del cursor
#add the attachments to the feature class based on the match table
arcpy.AddAttachments_management(in_dataset=sourcePoints, in_join_field="OBJECTID", in_match_table=os.path.join(sourceGDB,tempMatchTable), in_match_join_field="MatchID", in_match_path_field="Filename", in_working_folder="")

