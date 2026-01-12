import pywhatkit as pwk
import datetime
from geopy.geocoders import Nominatim

def sendInfoWA(imagepath,animal):
   
    # Initialize Nominatim API9284604268
    geolocator = Nominatim(user_agent="MyApp")

    location = geolocator.geocode("kuran")

    print("The latitude of the location is: ", location.latitude)
    print("The longitude of the location is: ", location.longitude)
    lat=str(location.latitude)
    longi=str(location.longitude)
    urlstr="https://www.google.com/maps/dir/"+lat+","+longi
    message="ALERT ALERT ALERT !!! \n"+"A "+animal+" has seen in the following location. Please be cautious \n";
    message=message+urlstr+"\n ";
    message=message+". And also attached Surveilliance Image for your reference. PLEASE TAKE ACTION IMMMEDIATLY \n ";
    message=message+" Regards - \n Automatic Wild Animal Vigilence System"
    mobilenumber="+918669473841";
    
 

    
     
   
    pwk.sendwhats_image(mobilenumber, imagepath,message)
    
 
if __name__ == '__main__':
    sendInfoWA()    