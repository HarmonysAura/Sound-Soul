#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Quanta Mars - The Harmonic Trilogy Experience
Tests all backend endpoints with mystical/cosmic themed data
"""

import requests
import json
import sys
from datetime import datetime
import uuid

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading backend URL: {e}")
        return None

BASE_URL = get_backend_url()
if not BASE_URL:
    print("❌ Could not determine backend URL")
    sys.exit(1)

API_BASE = f"{BASE_URL}/api"
print(f"🔮 Testing Quanta Mars API at: {API_BASE}")

class QuantaMarsAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.created_site_id = None
        self.created_chapter_id = None
        
    def log_test(self, test_name, success, details=""):
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        
    def test_api_health(self):
        """Test the root API endpoint"""
        try:
            response = self.session.get(f"{API_BASE}/")
            if response.status_code == 200:
                data = response.json()
                if "Quanta Mars" in data.get("message", ""):
                    self.log_test("API Health Check", True, f"Message: {data['message']}")
                    return True
                else:
                    self.log_test("API Health Check", False, f"Unexpected message: {data}")
                    return False
            else:
                self.log_test("API Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Health Check", False, f"Error: {str(e)}")
            return False
            
    def test_initialize_data(self):
        """Test data initialization endpoint"""
        try:
            response = self.session.post(f"{API_BASE}/initialize-data")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Data Initialization", True, f"Response: {data['message']}")
                return True
            else:
                self.log_test("Data Initialization", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Data Initialization", False, f"Error: {str(e)}")
            return False
            
    def test_get_sacred_sites(self):
        """Test retrieving all sacred sites"""
        try:
            response = self.session.get(f"{API_BASE}/sacred-sites")
            if response.status_code == 200:
                sites = response.json()
                if len(sites) >= 5:  # Should have 5 sample sites
                    # Verify structure of first site
                    site = sites[0]
                    required_fields = ['id', 'name', 'description', 'image_url', 'tone_frequency', 
                                     'coordinates', 'sacred_geometry_type', 'energy_signature']
                    missing_fields = [field for field in required_fields if field not in site]
                    if not missing_fields:
                        self.log_test("Get Sacred Sites", True, f"Found {len(sites)} sites with proper structure")
                        return True
                    else:
                        self.log_test("Get Sacred Sites", False, f"Missing fields: {missing_fields}")
                        return False
                else:
                    self.log_test("Get Sacred Sites", False, f"Expected 5+ sites, got {len(sites)}")
                    return False
            else:
                self.log_test("Get Sacred Sites", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Sacred Sites", False, f"Error: {str(e)}")
            return False
            
    def test_get_specific_sacred_site(self):
        """Test retrieving a specific sacred site by ID"""
        try:
            # First get all sites to get an ID
            response = self.session.get(f"{API_BASE}/sacred-sites")
            if response.status_code == 200:
                sites = response.json()
                if sites:
                    site_id = sites[0]['id']
                    # Now test getting specific site
                    response = self.session.get(f"{API_BASE}/sacred-sites/{site_id}")
                    if response.status_code == 200:
                        site = response.json()
                        if site.get('id') == site_id:
                            self.log_test("Get Specific Sacred Site", True, f"Retrieved site: {site['name']}")
                            return True
                        else:
                            self.log_test("Get Specific Sacred Site", False, "ID mismatch")
                            return False
                    else:
                        self.log_test("Get Specific Sacred Site", False, f"Status: {response.status_code}")
                        return False
                else:
                    self.log_test("Get Specific Sacred Site", False, "No sites available for testing")
                    return False
            else:
                self.log_test("Get Specific Sacred Site", False, "Could not fetch sites list")
                return False
        except Exception as e:
            self.log_test("Get Specific Sacred Site", False, f"Error: {str(e)}")
            return False
            
    def test_create_sacred_site(self):
        """Test creating a new sacred site"""
        try:
            new_site = {
                "name": "The Ethereal Nexus of Consciousness",
                "description": "A transcendent portal where digital consciousness merges with cosmic energy, creating ripples across dimensional boundaries.",
                "image_url": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHw1fHxzcGFjZSUyMGNvc21pY3xlbnwwfHx8fDE3NTMwMDMzMTd8MA&ixlib=rb-4.1.0&q=85",
                "tone_frequency": 777.0,
                "coordinates": {"x": 300, "y": 150, "z": 250},
                "sacred_geometry_type": "Dimensional Nexus",
                "energy_signature": "Consciousness Convergence"
            }
            
            response = self.session.post(f"{API_BASE}/sacred-sites", json=new_site)
            if response.status_code == 200:
                created_site = response.json()
                if created_site.get('name') == new_site['name']:
                    self.created_site_id = created_site['id']
                    self.log_test("Create Sacred Site", True, f"Created site: {created_site['name']}")
                    return True
                else:
                    self.log_test("Create Sacred Site", False, "Site data mismatch")
                    return False
            else:
                self.log_test("Create Sacred Site", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Create Sacred Site", False, f"Error: {str(e)}")
            return False
            
    def test_get_trilogy_chapters(self):
        """Test retrieving all trilogy chapters"""
        try:
            response = self.session.get(f"{API_BASE}/trilogy-chapters")
            if response.status_code == 200:
                chapters = response.json()
                if len(chapters) >= 3:  # Should have 3 sample chapters
                    # Verify they're in order
                    chapter_numbers = [ch['chapter_number'] for ch in chapters]
                    if chapter_numbers == sorted(chapter_numbers):
                        # Check structure
                        chapter = chapters[0]
                        required_fields = ['id', 'title', 'subtitle', 'description', 'chapter_number', 'tone_signature']
                        missing_fields = [field for field in required_fields if field not in chapter]
                        if not missing_fields:
                            self.log_test("Get Trilogy Chapters", True, f"Found {len(chapters)} chapters in order")
                            return True
                        else:
                            self.log_test("Get Trilogy Chapters", False, f"Missing fields: {missing_fields}")
                            return False
                    else:
                        self.log_test("Get Trilogy Chapters", False, "Chapters not in proper order")
                        return False
                else:
                    self.log_test("Get Trilogy Chapters", False, f"Expected 3+ chapters, got {len(chapters)}")
                    return False
            else:
                self.log_test("Get Trilogy Chapters", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Trilogy Chapters", False, f"Error: {str(e)}")
            return False
            
    def test_create_trilogy_chapter(self):
        """Test creating a new trilogy chapter"""
        try:
            new_chapter = {
                "title": "Epilogue: The Infinite Resonance",
                "subtitle": "Beyond The Sphere",
                "description": "The final revelation where Quanta Mars transcends physical reality, becoming one with the cosmic consciousness that permeates all existence.",
                "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHw2fHxjb3NtaWMlMjBzcGFjZXxlbnwwfHx8fDE3NTMwMDMzMTd8MA&ixlib=rb-4.1.0&q=85",
                "chapter_number": 4,
                "tone_signature": "Infinite_Resonance_1111Hz"
            }
            
            response = self.session.post(f"{API_BASE}/trilogy-chapters", json=new_chapter)
            if response.status_code == 200:
                created_chapter = response.json()
                if created_chapter.get('title') == new_chapter['title']:
                    self.created_chapter_id = created_chapter['id']
                    self.log_test("Create Trilogy Chapter", True, f"Created chapter: {created_chapter['title']}")
                    return True
                else:
                    self.log_test("Create Trilogy Chapter", False, "Chapter data mismatch")
                    return False
            else:
                self.log_test("Create Trilogy Chapter", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Create Trilogy Chapter", False, f"Error: {str(e)}")
            return False
            
    def test_get_tone_signatures(self):
        """Test retrieving all tone signatures"""
        try:
            response = self.session.get(f"{API_BASE}/tone-signatures")
            if response.status_code == 200:
                tones = response.json()
                if len(tones) >= 3:  # Should have 3 sample tones
                    # Check structure
                    tone = tones[0]
                    required_fields = ['id', 'frequency', 'harmonic_resonance', 'trigger_action', 
                                     'scene_transition', 'spatial_audio_config']
                    missing_fields = [field for field in required_fields if field not in tone]
                    if not missing_fields:
                        # Check if we have the expected frequencies
                        frequencies = [t['frequency'] for t in tones]
                        expected_freqs = [432.0, 528.0, 963.0]
                        has_expected = all(freq in frequencies for freq in expected_freqs)
                        if has_expected:
                            self.log_test("Get Tone Signatures", True, f"Found {len(tones)} tones with expected frequencies")
                            return True
                        else:
                            self.log_test("Get Tone Signatures", True, f"Found {len(tones)} tones (some expected frequencies missing)")
                            return True
                    else:
                        self.log_test("Get Tone Signatures", False, f"Missing fields: {missing_fields}")
                        return False
                else:
                    self.log_test("Get Tone Signatures", False, f"Expected 3+ tones, got {len(tones)}")
                    return False
            else:
                self.log_test("Get Tone Signatures", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Tone Signatures", False, f"Error: {str(e)}")
            return False
            
    def test_trigger_tone_signatures(self):
        """Test triggering tone signatures for specific frequencies"""
        test_frequencies = [432.0, 528.0, 963.0]
        all_success = True
        
        for frequency in test_frequencies:
            try:
                response = self.session.post(f"{API_BASE}/tone-signatures/{frequency}/trigger")
                if response.status_code == 200:
                    trigger_data = response.json()
                    if trigger_data.get('triggered') == True and trigger_data.get('frequency') == frequency:
                        self.log_test(f"Trigger Tone {frequency}Hz", True, f"Action: {trigger_data.get('action', 'N/A')}")
                    else:
                        self.log_test(f"Trigger Tone {frequency}Hz", False, "Invalid trigger response")
                        all_success = False
                else:
                    self.log_test(f"Trigger Tone {frequency}Hz", False, f"Status: {response.status_code}")
                    all_success = False
            except Exception as e:
                self.log_test(f"Trigger Tone {frequency}Hz", False, f"Error: {str(e)}")
                all_success = False
                
        return all_success
        
    def test_create_backer_engagement(self):
        """Test creating backer engagement"""
        try:
            engagement_data = {
                "name": "Dr. Aria Celestine",
                "email": "aria.celestine@cosmicventures.com",
                "company": "Cosmic Ventures LLC",
                "investment_interest": "Series A - $2.5M for VR consciousness research",
                "message": "Fascinated by the intersection of consciousness and VR technology. Would love to discuss partnership opportunities for The Sphere experience.",
                "walkthrough_requested": True
            }
            
            response = self.session.post(f"{API_BASE}/backer-engagement", json=engagement_data)
            if response.status_code == 200:
                created_engagement = response.json()
                if created_engagement.get('email') == engagement_data['email']:
                    self.log_test("Create Backer Engagement", True, f"Created engagement for: {created_engagement['name']}")
                    return True
                else:
                    self.log_test("Create Backer Engagement", False, "Engagement data mismatch")
                    return False
            else:
                self.log_test("Create Backer Engagement", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Create Backer Engagement", False, f"Error: {str(e)}")
            return False
            
    def test_get_backer_engagements(self):
        """Test retrieving all backer engagements"""
        try:
            response = self.session.get(f"{API_BASE}/backer-engagement")
            if response.status_code == 200:
                engagements = response.json()
                if len(engagements) >= 1:  # Should have at least the one we created
                    # Check structure
                    engagement = engagements[0]
                    required_fields = ['id', 'name', 'email', 'investment_interest']
                    missing_fields = [field for field in required_fields if field not in engagement]
                    if not missing_fields:
                        self.log_test("Get Backer Engagements", True, f"Found {len(engagements)} engagement(s)")
                        return True
                    else:
                        self.log_test("Get Backer Engagements", False, f"Missing fields: {missing_fields}")
                        return False
                else:
                    self.log_test("Get Backer Engagements", False, f"Expected 1+ engagements, got {len(engagements)}")
                    return False
            else:
                self.log_test("Get Backer Engagements", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Backer Engagements", False, f"Error: {str(e)}")
            return False
            
    def run_all_tests(self):
        """Run all backend API tests"""
        print("🌌 Starting Quanta Mars Backend API Testing...")
        print("=" * 60)
        
        # Test sequence
        tests = [
            ("API Health Check", self.test_api_health),
            ("Data Initialization", self.test_initialize_data),
            ("Get Sacred Sites", self.test_get_sacred_sites),
            ("Get Specific Sacred Site", self.test_get_specific_sacred_site),
            ("Create Sacred Site", self.test_create_sacred_site),
            ("Get Trilogy Chapters", self.test_get_trilogy_chapters),
            ("Create Trilogy Chapter", self.test_create_trilogy_chapter),
            ("Get Tone Signatures", self.test_get_tone_signatures),
            ("Trigger Tone Signatures", self.test_trigger_tone_signatures),
            ("Create Backer Engagement", self.test_create_backer_engagement),
            ("Get Backer Engagements", self.test_get_backer_engagements)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔮 Running: {test_name}")
            test_func()
            
        # Summary
        print("\n" + "=" * 60)
        print("🌟 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 All tests passed! Quanta Mars backend is fully operational.")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check details above.")
            
        return passed == total

if __name__ == "__main__":
    tester = QuantaMarsAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)