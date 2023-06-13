#-----------------------------------
#-----------------------------------
#History:
#23.11.2020 - Created by Akeeper
#-----------------------------------
#-----------------------------------
#-----------------------------------

import json;

def calcDistance (x1,y1,x2,y2):
    z1 = (x1**2) + (y1**2);
    z2 = (x2**2) + (y2**2);

    if (z1 < z2):
        return int(z2-z1);
    else:
        return int(z1-z2);

file = open("cities.json","r");
cities = json.loads(file.read());

#Словарь одного города с его данными
cityDict = {};

#Список со словарями городов
cityList = [];

#Перевёрнутый список со словарями городов
reversedCityList = [];

#Дистанция для сравнивания
distTemp1 = 0;
distTemp2 = 0;

#Имена городов при минимуме
cityName1 = "";
cityName2 = "";
cityName3 = "";
cityName4 = "";

for city in cities:
    cityCoords = city["coord"];
    cityDict = {'id' : city["id"], 
                'name' : city["name"], 
                'state' : city["state"], 
                'country' : city["country"],
                'lon' : cityCoords["lon"],
                'lat' : cityCoords["lat"],}
    cityList.append(cityDict);

cityCount = len(cityList);

reversedCityList = cityList.copy();
reversedCityList.reverse();

for cityIndex in range(cityCount):
    #Получение текущего города
    city = cityList[cityIndex];
    rCity = reversedCityList[cityIndex];

     #Получение id городов и их проверка
    cityId = city['id'];
    rCityId = rCity['id'];
    if (cityId == rCityId):
        break;
    #Получение имени 1-го города
    name = city['name'];

    #Получение имени 2-го города
    rName = rCity['name'];

    #Получение координат 1-го города
    lon = city['lon'];
    lat = city['lat'];

    #Получение координат 2-го города
    rLon = rCity['lon'];
    rLat = rCity['lat'];

    #Получение дистанции
    dist = calcDistance(lon,lat,rLon,rLat);

    #Получение 1-го минимума
    if (distTemp1 == 0):
        distTemp1 = dist;
        cityName1 = city["name"];
        cityName2 = rCity["name"];
    elif (dist < distTemp1):
        distTemp1 = dist;
        cityName1 = city["name"];
        cityName2 = rCity["name"];

    #Получение 2-го минимума
    if (distTemp1 != 0 and dist != distTemp1 and distTemp2 == 0):
        distTemp2 = dist;
        cityName3 = city["name"];
        cityName4 = rCity["name"];
    elif (dist < distTemp2 and dist != distTemp1):
        distTemp2 = dist;
        cityName3 = city["name"];
        cityName4 = rCity["name"];

    print("Distance: " + str(dist) + " between cities " + name + " " + "and " + rName);

print("")
print("1 minimal: " + str(distTemp1) + " between cities " + cityName1 + " " + "and " + cityName2);
print("2 minimal: " + str(distTemp2) + " between cities " + cityName3 + " " + "and " + cityName4); 