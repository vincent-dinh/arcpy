#want to fix the bug? initialliser la list description_list = symbology value lenght


layer = arcpy.GetParameterAsText(0)
valuefield = arcpy.GetParameterAsText(1)
descfield = arcpy.GetParameterAsText(2)
out_table = arcpy.GetParameterAsText(3)

def describe(layer,valuefield,descfield,out_table):

	mxd = arcpy.mapping.MapDocument("CURRENT")
	layer = arcpy.mapping.ListLayers(mxd, layer)[0]
	try:
		arcpy.Statistics_analysis (layer, out_table, [[valuefield, "FIRST"]],descfield)
		arcpy.AddMessage("Statistic analysis DONE")

		arcpy.MakeTableView_management(out_table)
		#print "Layer" + nameTable + "is included in the DataFrame"
	except Exception as e:
	    print e.message
	    
	    # If using this code within a script tool, AddError can be used to return messages 
	    #   back to a script tool.  If not, AddError will have no effect.
	    arcpy.AddError(e.message)

	try:
		 
		description_list = [''] * len(layer.symbology.classValues)
		positionInList = 0

		for value in layer.symbology.classValues :
			
			column = 'FIRST_'+valuefield
			
			
			
			with arcpy.da.SearchCursor(out_table, [column, descfield]) as cursor:
				for row in cursor:
					if value == row[0]:
						description_list[positionInList] = row[1]
					else:	
						pass

			positionInList += 1 
		
		arcpy.AddMessage(str(description_list))
		layer.symbology.classDescriptions = description_list
		arcpy.AddMessage("description completed")

	except Exception as e:
	    print e.message
	    
	    # If using this code within a script tool, AddError can be used to return messages 
	    #   back to a script tool.  If not, AddError will have no effect.
	    arcpy.AddError(e.message)


describe(layer,valuefield,descfield,out_table)