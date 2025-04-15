import requests
import json
import datetime
import time
from math import radians, sin, cos, asin, sqrt, degrees, atan2
import ephem 

def get_location_automatically():
    """Attempt to get the user's location based on IP address"""
    try:
        print("Attempting to find your location automatically...")
        response = requests.get("https://ipapi.co/json/")
        if response.status_code == 200:
            data = response.json()
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            city = data.get('city')
            country = data.get('country_name')
            
            if latitude is not None and longitude is not None:
                print(f"Found your location: {city}, {country}")
                print(f"Coordinates: {latitude}, {longitude}")
                return latitude, longitude
        
        print("Could not automatically determine your location.")
        return manual_location_input()
    except Exception as e:
        print(f"Error getting location automatically: {e}")
        return manual_location_input()

def manual_location_input():
    """Get the user's location coordinates manually"""
    print("Please enter your location coordinates manually:")
    try:
        latitude = float(input("Latitude (decimal degrees, -90 to 90): "))
        longitude = float(input("Longitude (decimal degrees, -180 to 180): "))
        
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            print("Invalid coordinates range. Using default values (0, 0).")
            return 0, 0
        
        return latitude, longitude
    except ValueError:
        print("Invalid input. Using default values (0, 0).")
        return 0, 0

def get_location():
    """Get location either automatically or manually"""
    while True:
        choice = input("Do you want to detect your location automatically? (y/n): ").lower()
        if choice == 'y':
            return get_location_automatically()
        elif choice == 'n':
            return manual_location_input()
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def get_iss_pass(lat, lon):
    """Get ISS pass information for the location"""
    url = f"http://api.open-notify.org/iss-pass.json?lat={lat}&lon={lon}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data['response']
        else:
            print(f"Error getting ISS data: {data.get('reason', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"Failed to get ISS data: {e}")
        return []

def get_visible_planets(lat, lon):
    """Get currently visible planets from the location"""
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = ephem.now()
    
    planets = {
        'Mercury': ephem.Mercury(),
        'Venus': ephem.Venus(),
        'Mars': ephem.Mars(),
        'Jupiter': ephem.Jupiter(),
        'Saturn': ephem.Saturn(),
        'Uranus': ephem.Uranus(),
        'Neptune': ephem.Neptune()
    }
    
    visible_planets = []
    
    for name, planet in planets.items():
        planet.compute(observer)
        # Convert altitude from radians to degrees
        altitude_deg = degrees(planet.alt)
        
        # If altitude is greater than 0, the planet is above the horizon
        if altitude_deg > 0:
            visible_planets.append({
                'name': name,
                'altitude': round(altitude_deg, 2),
                'azimuth': round(degrees(planet.az), 2)
            })
    
    return visible_planets

def get_moon_info(lat, lon):
    """Get moon information from the location"""
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = ephem.now()
    
    moon = ephem.Moon()
    moon.compute(observer)
    
    # Check if moon is above horizon
    if degrees(moon.alt) > 0:
        return {
            'altitude': round(degrees(moon.alt), 2),
            'azimuth': round(degrees(moon.az), 2),
            'phase': round(moon.phase, 2),  # percentage illuminated
            'above_horizon': True
        }
    else:
        return {'above_horizon': False}

def get_sun_info(lat, lon):
    """Get sun information from the location"""
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = ephem.now()
    
    sun = ephem.Sun()
    sun.compute(observer)
    
    # Check if sun is above horizon
    if degrees(sun.alt) > 0:
        return {
            'altitude': round(degrees(sun.alt), 2),
            'azimuth': round(degrees(sun.az), 2),
            'above_horizon': True
        }
    else:
        return {'above_horizon': False}

def format_timestamp(timestamp):
    """Convert UNIX timestamp to readable format"""
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def main():
    print("=== Sky Observer - What's Above You? ===")
    print(f"Current user: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    latitude, longitude = get_location()
    print(f"\nGetting celestial information for: {latitude}°, {longitude}°\n")
    
    # Get ISS pass information
    print("Checking for ISS passes...")
    iss_passes = get_iss_pass(latitude, longitude)
    if iss_passes:
        print("\nUpcoming ISS passes:")
        for i, pass_info in enumerate(iss_passes[:3], 1):  # Show only next 3 passes
            print(f"  Pass #{i}:")
            print(f"    Time: {format_timestamp(pass_info['risetime'])}")
            print(f"    Duration: {pass_info['duration']} seconds")
    else:
        print("No ISS pass data available.")
    
    # Get visible planets
    print("\nChecking for visible planets...")
    visible_planets = get_visible_planets(latitude, longitude)
    if visible_planets:
        print("\nCurrently visible planets:")
        for planet in visible_planets:
            print(f"  {planet['name']}:")
            print(f"    Altitude: {planet['altitude']}°")
            print(f"    Azimuth: {planet['azimuth']}°")
    else:
        print("No planets are currently visible.")
    
    # Get moon information
    print("\nChecking moon position...")
    moon_info = get_moon_info(latitude, longitude)
    if moon_info['above_horizon']:
        print("\nMoon:")
        print(f"  Altitude: {moon_info['altitude']}°")
        print(f"  Azimuth: {moon_info['azimuth']}°")
        print(f"  Phase: {moon_info['phase']}% illuminated")
    else:
        print("The moon is currently below the horizon.")
    
    # Get sun information
    print("\nChecking sun position...")
    sun_info = get_sun_info(latitude, longitude)
    if sun_info['above_horizon']:
        print("\nSun:")
        print(f"  Altitude: {sun_info['altitude']}°")
        print(f"  Azimuth: {sun_info['azimuth']}°")
    else:
        print("The sun is currently below the horizon.")

if __name__ == "__main__":
    main()