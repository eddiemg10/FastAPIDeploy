import pandas as pd
import io
from fastapi.responses import StreamingResponse, JSONResponse
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import base64
import firebase_admin
from firebase_admin import credentials, storage
from urllib.parse import quote
from fastapi import FastAPI, HTTPException

cred = credentials.Certificate("firebase_admin.json")
firebase_admin.initialize_app(cred, {"storageBucket": "nourishke-dcb1a.appspot.com"})

def get_shapefile():
    counties = gpd.read_file("app/core/repository/locations/gis/counties/County.shp")
    return counties

def image_exists(blob_name):
    bucket = storage.bucket()
    blob = bucket.blob(blob_name)
    try:
        blob.reload()
        return True
    except Exception:
        return False

def get_all_counties(image_flag = False):
    # cred = credentials.Certificate("firebase_admin.json")
    # firebase_admin.initialize_app(cred, {"storageBucket": "nourishke-dcb1a.appspot.com"})
    counties = get_shapefile()
    ax = counties.plot(figsize=(10, 10), edgecolor='k', facecolor='none')

    # Customize the plot if needed
    # For example, you can add a title
    ax.set_title("Kenyan Counties Map")

    # Save the plot to a BytesIO buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
        
    blob_name = "kenyan_counties.png"
    if not image_exists(blob_name):
        # Upload the image to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(blob_name)
        blob.upload_from_file(io.BytesIO(img_buffer.read()), content_type="image/png")

    # Return image, not json
    if image_flag:
        # Return the image as a streaming response
        return StreamingResponse(io.BytesIO(img_buffer.read()), media_type="image/png")
    
    # Get the download URL
    image_url = f"https://firebasestorage.googleapis.com/v0/b/nourishke-dcb1a.appspot.com/o/{blob_name}?alt=media"

    # Close the plot to free up resources
    plt.close()

    return {"image": image_url, "description": "All Kenyan regions"}


def find_county_and_highlight(coordinate, highlight=True, image_flag = False):
    mapping = {
    "coast" : {"Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita Taveta"},
    "north eastern": {"Garissa", "Wajir", "Mandera"},
    "eastern": {"Marsabit", "Isiolo", "Meru", "Tharaka", "Embu", "Kitui", "Machakos", "Makueni"},
    "central": {"Nyandarua", "Nyeri", "Kirinyaga", "Murang'a", "Kiambu"},
    "rift valley": {"Turkana", "West Pokot", "Samburu", "Trans Nzoia", "Uasin Gishu", "Keiyo-Marakwet", "Nandi", "Baringo", "Laikipia", "Nakuru", "Narok", "Kajiado", "Kericho", "Bomet"},
    "western": {"Kakamega", "Vihiga", "Bungoma", "Busia"},
    "nyanza": {"Siaya", "Kisumu", "Homa Bay", "Migori", "Kisii", "Nyamira"},
    "nairobi": {"Nairobi"}
    }

    counties_df = get_shapefile()
    # Create a Point geometry object from the coordinate
    point = Point(coordinate)

    highlighted_county = None  # Store the highlighted county for later use

    # Iterate through the counties and check if the point is within each county
    for idx, county in counties_df.iterrows():
        if point.within(county['geometry']):
            # Store the selected county
            highlighted_county = county
            break  # Exit the loop when a match is found
    
    if highlighted_county is None:
        raise HTTPException(status_code=404, detail="Coordinates could not be resolved to an area in kenya") 
    
    if highlighted_county is not None and highlight:
        # Get the region
        region = None
        for province, counties in mapping.items():
            if highlighted_county['COUNTY'] in counties:
                region = province
                
        # Create a GeoDataFrame with the selected county
        highlighted_gdf = gpd.GeoDataFrame([highlighted_county], geometry='geometry')

        # Create a GeoDataFrame with the selected region
        counties_in_region = []
        # print(mapping[region])
        for idx, county in counties_df.iterrows():
            if county['COUNTY'] in mapping[region]:
                counties_in_region.append(county)
                # print(f"Added {county['COUNTY']}")
        highlighted_region_gdf = gpd.GeoDataFrame(counties_in_region, geometry='geometry')

        # Plot all counties in the original color (e.g., light gray) and the selected county in red
        ax = counties_df.boundary.plot(color='lightgray', linewidth=0.5)
        highlighted_region_gdf.plot(ax=ax, color='pink', linewidth=2)
        highlighted_gdf.plot(ax=ax, color='red', linewidth=2)

        ax.set_title(f"Your location (County): {highlighted_county['COUNTY']}. Region: {region.capitalize()}")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        # Save the plot to a BytesIO buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
        
    blob_name = f"{highlighted_county['COUNTY']}.png"
    if not image_exists(blob_name):
        # Upload the image to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(blob_name)
        blob.upload_from_file(io.BytesIO(img_buffer.read()), content_type="image/png")

    # Return image, not json
    if image_flag:
        # Return the image as a streaming response
        return StreamingResponse(io.BytesIO(img_buffer.read()), media_type="image/png")
    
    # Get the download URL
    image_url = f"https://firebasestorage.googleapis.com/v0/b/nourishke-dcb1a.appspot.com/o/{blob_name}?alt=media"

    # Close the plot to free up resources
    plt.close()

    return {"image": image_url, 
            "county": highlighted_county['COUNTY'],
            "region" : region
            }
    

    
    # return highlighted_county['COUNTY'] if highlighted_county is not None else 'Not Found'
    