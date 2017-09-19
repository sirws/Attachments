Python script that will attach photos to features in a local file geodatabase.

This assumes you have a folder structure like this:
![Thumbnail](https://github.com/sirws/Attachments/blob/master/AKDOT/Images/Folder_Structure.png?raw=true)

And some data with fields that contain data that match up with the names of the folders in the folder structure:
![Thumbnail](https://github.com/sirws/Attachments/blob/master/AKDOT/Images/Data_Structure.png?raw=true)

Note the ICDSRtNN field matches the top level folders and the ICDSMPN matches the next level below those folders.  These are the features we want to attach our images to.  In this case, we will attach all .JPG files in the ICDSMPN folders to a matching feature in the RetainingWalls featureclass.

The script will loop over all of the folders in the RatingWalls2016Sample folder looking for images to attach.  The script creates a match table and then runs the Add Attachment geoprocessing tool.
