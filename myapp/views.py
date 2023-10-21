# myapp/views.py
from django.shortcuts import render, HttpResponse
from .models import Files

# Create your views here.

def home(request):
    return render(request, "base.html")


def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def product(request):

    if request.method == "POST" and request.FILES['file'] and request.FILES['file2']:
        api_key = request.POST.get("key")
        API_KEY = api_key;
        import os
    
        import pandas as pd
        import googlemaps
        from datetime import datetime
        import numpy as np
        from django.conf import settings
        locations = request.FILES['file']
        print("locations")
        newStops = request.FILES['file2']
        print("newStops")
        locations = pd.read_csv(locations)
        newStops = pd.read_csv(newStops)
        gmaps =  googlemaps.Client(key = API_KEY)
        closestLocations = []
        newDistances = []
        newDuration = []
        newDistancesInText= []
        newDurationInText= []

        currentLocationCount = 0
        currentnewStopCount = 0
        indicesOfTheClosestLocations = []

        for newStop in newStops['Location']: #for the newstop
                locationChoices = []
                durationChoices = []
                durationChoicesTextVersion = []
                distanceChoices = []
                distanceChoicesInText = []
                indicesOfLocationChoices = []
                print("Current NewStop: " + newStop)
                print("NEW STOP NUMBER: " + str(currentnewStopCount))
                for location in locations['Location']: #go through every location
                            indicesOfLocationChoices.append(currentLocationCount)
                            print("NEW LOCATION COUNT: " + str(currentLocationCount))
                            print("Current Location: " + location)
                            def findDistance(location,newStop): #find the distance between the newstop and the current location
                            # url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={location}&destinations={newStop}&key={API_KEY}'
                                #print(url)
                                response_json = gmaps.distance_matrix(location, newStop, mode='driving', departure_time=datetime.now())
                                print(response_json)  # Print the entire JSON response
                                
                                distance_text = response_json['rows'][0]['elements'][0]['distance']['text']
                                duration_text = response_json['rows'][0]['elements'][0]['duration']['text']

                                distance = response_json['rows'][0]['elements'][0]['distance']['value']
                                duration = response_json['rows'][0]['elements'][0]['duration']['value']

                                print("Calculating Distance Between New Stop and Current Location...")
                                print("Distance Text: " + distance_text + ' Value: ' + str(distance))
                                print("Calculating Duration Between New Stop and Current Location...")
                                print("Duration Text:" + duration_text + ' Value: ' + str(duration))


                                print("Inserting current distance between currentNewStop and currentLocation into distanceChoices array so we can later choose the distance that is closest to the newStop...")
                                distanceChoices.append(distance)
                                print("Updated distanceChoices List " +  str(distanceChoices))
                                print("Inserting corresponding location to locationChoices so when we  find the closest location's index from distanceChoices we can get the actual location by the same index in locationChoices..")
                                locationChoices.append(location)
                                durationChoices.append(duration)
                                print("Updated Locations Choices:")
                                print(locationChoices)
                                durationChoicesTextVersion.append(duration_text)
                                distanceChoicesInText.append(distance_text)
                                
                            findDistance(location,newStop)
                            currentLocationCount += 1
                #After going through all the locations find the location that has the shortest distance
                print("After going through all the locations lets find which one is closest to the newStop...")
                def findClosestLocation():
                    print("Choosing the smallest distance from distanceChoices... getting the index...")
                    closest_location_Index = distanceChoices.index(min(distanceChoices))  # find the location that has the shortest distance from the newStop
                    print("Smallest Distance Index: " + str(closest_location_Index) )
                    print("Choosing the closest location from locationChoices... adding the location into closestLocations array... ")
                    closestLocations.append(locationChoices[closest_location_Index]) #add that location to the closestLocations list.
                    print("Updated closestLocations: ")
                    print(closestLocations)
                    print("Updating the corresponding distance of  the closets locaton to the newStop...")
                    newDistances.append(distanceChoices[closest_location_Index])
                    newDistancesInText.append(distanceChoicesInText[closest_location_Index])
                    print("newDistances ")
                    print(newDistances)
                    print("Updating the corresponding duration of  the closet location to the newStop...")
                    newDuration.append(durationChoices[closest_location_Index])
                    newDurationInText.append(durationChoicesTextVersion[closest_location_Index])
                    print("New Duration: ")
                    print(newDistances)
                    print("Inserting the index of the closest location to the newStop in indicesOfTheClosestLocations...")
                    indicesOfTheClosestLocations.append(closest_location_Index) 
                    print("THESE ARE THE INDICIES OF THE CLOSEST LOCATIONS: ")
                    print(indicesOfTheClosestLocations)
                    print("The Location with the shortest distance to " + newStop + " is " + location + " with " + str(distanceChoices[closest_location_Index]) + " meters.")
                    return closest_location_Index
                closest_location_Index = findClosestLocation()
                print("CLOSEST LOCATION INDEX " + str(closest_location_Index))
                # i never called the function *cries* 
                def InsertIntoLocationsDf(locations,newStop, closest_location_Index):
                    print("Finding the index of the closest location for this current new stop")
                    #closestLocationIndex = indicesOfTheClosestLocations[currentnewStopCount]
                    print("This is the index of the closest Location: " + str(closest_location_Index))
                
                    locationsArray = locations.values
                    maxIndexofDf = len(locations) -1

                    print("Time to insert new stop in the route...")
                    previousLocationIndex= closest_location_Index - 1
                    nextLocation = closest_location_Index + 1
                    beforePreviousIndex = closest_location_Index - 2

                    c = locations['Location'][closest_location_Index] 
                    d= newStop       
                    if beforePreviousIndex in locations.index:
                        a = locations['Location'][beforePreviousIndex]
                        print("a: " + a ) 
                    else:
                        print("a does not exist")
                        b = locations['Location'][previousLocationIndex]
                        print("b: " + b )
                        print("c: " + c )  
                        print("d: " + d )
                    if nextLocation in locations.index:
                        e = locations['Location'][nextLocation] 
                        print("e: " + e )
                    else:     
                        print("e does not exist")

                    if 'a' not in locals():
                        #Duration Before BD + DC + CE
                        response_json = gmaps.distance_matrix(b, d, mode='driving', departure_time=datetime.now())
                        durationBD= response_json['rows'][0]['elements'][0]['duration']['value']     
                        response_json = gmaps.distance_matrix(d, c, mode='driving', departure_time=datetime.now())
                        durationDC= response_json['rows'][0]['elements'][0]['duration']['value']    
                        response_json = gmaps.distance_matrix(c, e, mode='driving', departure_time=datetime.now())
                        durationCE= response_json['rows'][0]['elements'][0]['duration']['value']     
                        durationBefore = durationBD + durationDC + durationCE

                        #Duration After BC + CD + DE
                        response_json = gmaps.distance_matrix(b, c, mode='driving', departure_time=datetime.now())
                        durationBC= response_json['rows'][0]['elements'][0]['duration']['value']     
                        response_json = gmaps.distance_matrix(c, d, mode='driving', departure_time=datetime.now())
                        durationCD= response_json['rows'][0]['elements'][0]['duration']['value']    
                        response_json = gmaps.distance_matrix(d, e, mode='driving', departure_time=datetime.now())
                        durationDE= response_json['rows'][0]['elements'][0]['duration']['value']     
                        durationAfter= durationBC + durationCD + durationDE

                    elif 'b' not in locals(): #a is also not in locals
                        #Duration Before  DC + CE 
                        response_json = gmaps.distance_matrix(d, c, mode='driving', departure_time=datetime.now())
                        durationDC= response_json['rows'][0]['elements'][0]['duration']['value']    
                        response_json = gmaps.distance_matrix(c, e, mode='driving', departure_time=datetime.now())
                        durationCE= response_json['rows'][0]['elements'][0]['duration']['value']     
                        durationBefore = durationDC + durationCE

                        #Duration After  CD + DE
                        response_json = gmaps.distance_matrix(c, d, mode='driving', departure_time=datetime.now())
                        durationCD= response_json['rows'][0]['elements'][0]['duration']['value']    
                        response_json = gmaps.distance_matrix(d, e, mode='driving', departure_time=datetime.now())
                        durationDE= response_json['rows'][0]['elements'][0]['duration']['value']     
                        durationAfter=  durationCD + durationDE 
                    elif 'e' not in locals():
                        #Duration Before  AB + BD + DC
                        response_json = gmaps.distance_matrix(a, b, mode='driving', departure_time=datetime.now())
                        durationAB= response_json['rows'][0]['elements'][0]['duration']['value']    
                        response_json = gmaps.distance_matrix(b, d, mode='driving', departure_time=datetime.now())
                        durationBD= response_json['rows'][0]['elements'][0]['duration']['value']     
                        response_json = gmaps.distance_matrix(d, c, mode='driving', departure_time=datetime.now())
                        durationDC= response_json['rows'][0]['elements'][0]['duration']['value']     
                        durationBefore = durationAB + durationBD + durationDC

                        #Duration After  AB + BC + CD
                        response_json = gmaps.distance_matrix(a, b, mode='driving', departure_time=datetime.now())
                        durationAB= response_json['rows'][0]['elements'][0]['duration']['value']    
                        response_json = gmaps.distance_matrix(b, c, mode='driving', departure_time=datetime.now())
                        durationBC= response_json['rows'][0]['elements'][0]['duration']['value']     
                        response_json = gmaps.distance_matrix(c, d, mode='driving', departure_time=datetime.now())
                        durationCD= response_json['rows'][0]['elements'][0]['duration']['value']    
                        durationAfter= durationAB + durationBC + durationCD 
                    else:
                        #Duration Before AB + BC + CD + DE
                        response_json = gmaps.distance_matrix(a, b, mode='driving', departure_time=datetime.now())
                        durationAB= response_json['rows'][0]['elements'][0]['duration']['value']    
                        response_json = gmaps.distance_matrix(b,c, mode='driving', departure_time=datetime.now())
                        durationBC= response_json['rows'][0]['elements'][0]['duration']['value']     
                        response_json = gmaps.distance_matrix(c, d, mode='driving', departure_time=datetime.now())
                        durationCD= response_json['rows'][0]['elements'][0]['duration']['value']   
                        response_json = gmaps.distance_matrix(d, e, mode='driving', departure_time=datetime.now())
                        durationDE= response_json['rows'][0]['elements'][0]['duration']['value']   
                        durationBefore = durationAB + durationBC + durationCD + durationDE
                        #Duration After AB + BD + DC + CE
                        response_json = gmaps.distance_matrix(a, b, mode='driving', departure_time=datetime.now())
                        durationAB= response_json['rows'][0]['elements'][0]['duration']['value']    
                        response_json = gmaps.distance_matrix(b, d, mode='driving', departure_time=datetime.now())
                        durationBD= response_json['rows'][0]['elements'][0]['duration']['value']    
                        response_json = gmaps.distance_matrix(d, c, mode='driving', departure_time=datetime.now())
                        durationDC= response_json['rows'][0]['elements'][0]['duration']['value']    
                        response_json = gmaps.distance_matrix(c, e, mode='driving', departure_time=datetime.now())
                        durationCE= response_json['rows'][0]['elements'][0]['duration']['value']    
                        
                        durationAfter =  durationAB + durationBD + durationDC + durationCE 
                  
                    if durationBefore < durationAfter: #if placing the newStop before the closest location makes the route shorter than put it before (so replace the closest so that the closest just goes down 1)
                        print("Duration 1 is Less than Duration 2 so putting the new stop before the closest location will make the route shorter")
                        modifiedIndex = closest_location_Index #putting it right before
                        if modifiedIndex <= maxIndexofDf:
                            print("Inserting Now... (before)")
                            locationsArray = np.insert(locationsArray, modifiedIndex, values = [f'{newStop}'], axis = 0)
                            locations = pd.DataFrame(locationsArray, columns = ['Location'])
                        elif modifiedIndex > maxIndexofDf:
                            print("Appending Now...")
                            new_row = pd.DataFrame({'Location':[f'{newStop}']})
                            locations = pd.concat([locations, new_row],ignore_index = True)

                    elif durationBefore > durationAfter:  #if placing the newStop before the closest location makes the route longer than put it after
                        print("Duration 1 is Greater than Duration 2 so putting the new stop before the closest location  will make the route longer")
                        modifiedIndex = closest_location_Index + 1 #putting it right after
                        if modifiedIndex <= maxIndexofDf:
                            print("Inserting Now... (after)")
                            locationsArray = np.insert(locationsArray, modifiedIndex, values = [f'{newStop}'], axis = 0)
                            locations = pd.DataFrame(locationsArray, columns = ['Location'])
                        elif modifiedIndex > maxIndexofDf:
                            print("Appending Now...")
                            new_row = pd.DataFrame({'Location':[f'{newStop}']})
                            locations = pd.concat([locations, new_row],ignore_index = True)
                    else: 
                        print("Placing the newStop before or after its closest location does not seem to make a difference")
                        modifiedIndex = closest_location_Index - 1 #putting it right before
                        if modifiedIndex <= maxIndexofDf:
                            locationsArray = np.insert(locationsArray, modifiedIndex, values = [f'{newStop}'], axis = 0)
                            locations = pd.DataFrame(locationsArray, columns = ['Location'])
                        elif modifiedIndex > maxIndexofDf:
                            new_row = pd.DataFrame({'Location':[f'{newStop}']})
                            locations = pd.concat([locations, new_row],ignore_index = True)
                    return locations
                locations = InsertIntoLocationsDf(locations, newStop, closest_location_Index)
                currentnewStopCount +=1;
        
        newRoute = locations
        currentLocationCount = 0;
        amountOfLocations = len(newRoute['Location']) -1
        distanceValueColumn = ['0 mi']
        distanceTextColumn = ['0 km']
        durationTextColumn =['0 mins']
        durationValueColumn = [0]

        for location in newRoute['Location']:
            def findDistance(location):
                if currentLocationCount+1 in newRoute.index:
                    nextLocation = newRoute['Location'][currentLocationCount+1]
                    #Find Distance Between current location and nextLocation
                    print(f'Calculating Duration between {location} and {nextLocation}')
                    response_json = gmaps.distance_matrix(location, nextLocation, mode = "driving", departure_time=datetime.now())
                    print(response_json)
                    distance_text = response_json['rows'][0]['elements'][0]['distance']['text']
                    duration_text = response_json['rows'][0]['elements'][0]['duration_in_traffic']['text']

                    distance = response_json['rows'][0]['elements'][0]['distance']['value']
                    duration = response_json['rows'][0]['elements'][0]['duration_in_traffic']['value']
                
                    distanceValueColumn.append(f'{round(distance/1609.34,1)} mi') #to convert from meters to miles
                    distanceTextColumn.append(distance_text)
                    durationTextColumn.append(duration_text)
                    durationValueColumn.append(round(duration/60)) #to convert from seconds to minutes
                else:
                    None

            findDistance(location)
            currentLocationCount += 1;
                
        newRoute['Distance'] = distanceValueColumn #miles
        newRoute['Duration'] = durationTextColumn
        print("NEW ROUTE DONE")
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'newRoute.csv')
        newRoute.to_csv(file_path, index = False)
        newFile = Files(file = './media/uploads/newRoute.csv')
        print("Adding newRoute to the database...")
        print(type(newFile))
        newFile.save()
        print("Saving the new file to the database...")
        fileItems= Files.objects.all()
        print("adding all file items to fileitems...")
        open3 = True

        context = {"files": fileItems, "open3": open3}
        return render(request, "product.html", context)
    else:
        return render(request, "product.html")
