"""
Vehicle Registration Database
Maps license plates to owner phone numbers

In production, this would connect to actual RTO database
For now, using mock data for demonstration
"""

import json
import os
from pathlib import Path

class VehicleDatabase:
    """
    Manages vehicle registration data
    Maps license plates to owner contact information
    """
    
    def __init__(self, db_file='vehicle_db.json'):
        self.db_file = db_file
        self.data = self._load_database()
    
    def _load_database(self):
        """Load vehicle database from JSON file"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        else:
            # Create demo database
            demo_data = {
                'DL-01-AB-1234': {
                    'phone': '+919876543210',
                    'owner': 'Demo Driver 1',
                    'vehicle_type': 'Motorcycle'
                },
                'DL-02-CD-5678': {
                    'phone': '+919876543211',
                    'owner': 'Demo Driver 2',
                    'vehicle_type': 'Car'
                },
                'MH-12-EF-9012': {
                    'phone': '+919876543212',
                    'owner': 'Demo Driver 3',
                    'vehicle_type': 'Motorcycle'
                }
            }
            self._save_database(demo_data)
            return demo_data
    
    def _save_database(self, data):
        """Save database to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_vehicle_info(self, license_plate):
        """
        Get vehicle owner information by license plate
        
        Args:
            license_plate: Vehicle registration number
            
        Returns:
            dict: Vehicle owner info or None
        """
        # Normalize license plate (remove spaces, uppercase)
        normalized_plate = license_plate.upper().replace(' ', '').replace('-', '')
        
        # Try exact match first
        if license_plate in self.data:
            return self.data[license_plate]
        
        # Try normalized search
        for plate, info in self.data.items():
            normalized_db_plate = plate.upper().replace(' ', '').replace('-', '')
            if normalized_plate == normalized_db_plate:
                return info
        
        return None
    
    def register_vehicle(self, license_plate, phone, owner, vehicle_type):
        """
        Register a new vehicle in database
        
        Args:
            license_plate: Vehicle number
            phone: Owner contact number
            owner: Owner name
            vehicle_type: Type of vehicle
        """
        self.data[license_plate] = {
            'phone': phone,
            'owner': owner,
            'vehicle_type': vehicle_type
        }
        self._save_database(self.data)
        
        return True
    
    def get_all_vehicles(self):
        """Get all registered vehicles"""
        return self.data

# Initialize global database
vehicle_db = VehicleDatabase()
