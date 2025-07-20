from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class SacredSite(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    image_url: str
    tone_frequency: float
    coordinates: dict  # {x, y, z} for 3D positioning
    sacred_geometry_type: str
    energy_signature: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SacredSiteCreate(BaseModel):
    name: str
    description: str
    image_url: str
    tone_frequency: float
    coordinates: dict
    sacred_geometry_type: str
    energy_signature: str

class TrilogyChapter(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    subtitle: str
    description: str
    trailer_url: Optional[str] = None
    image_url: str
    chapter_number: int
    tone_signature: str
    sacred_sites: List[str] = []  # List of sacred site IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TrilogyChapterCreate(BaseModel):
    title: str
    subtitle: str
    description: str
    trailer_url: Optional[str] = None
    image_url: str
    chapter_number: int
    tone_signature: str

class ToneSignature(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    frequency: float
    harmonic_resonance: str
    trigger_action: str
    scene_transition: str
    spatial_audio_config: dict
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BackerEngagement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    company: Optional[str] = None
    investment_interest: str
    message: Optional[str] = None
    walkthrough_requested: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BackerEngagementCreate(BaseModel):
    name: str
    email: str
    company: Optional[str] = None
    investment_interest: str
    message: Optional[str] = None
    walkthrough_requested: bool = False

# Sacred Sites endpoints
@api_router.post("/sacred-sites", response_model=SacredSite)
async def create_sacred_site(site: SacredSiteCreate):
    site_obj = SacredSite(**site.dict())
    await db.sacred_sites.insert_one(site_obj.dict())
    return site_obj

@api_router.get("/sacred-sites", response_model=List[SacredSite])
async def get_sacred_sites():
    sites = await db.sacred_sites.find().to_list(1000)
    return [SacredSite(**site) for site in sites]

@api_router.get("/sacred-sites/{site_id}", response_model=SacredSite)
async def get_sacred_site(site_id: str):
    site = await db.sacred_sites.find_one({"id": site_id})
    if site:
        return SacredSite(**site)
    return {"error": "Site not found"}

# Trilogy Chapters endpoints
@api_router.post("/trilogy-chapters", response_model=TrilogyChapter)
async def create_trilogy_chapter(chapter: TrilogyChapterCreate):
    chapter_obj = TrilogyChapter(**chapter.dict())
    await db.trilogy_chapters.insert_one(chapter_obj.dict())
    return chapter_obj

@api_router.get("/trilogy-chapters", response_model=List[TrilogyChapter])
async def get_trilogy_chapters():
    chapters = await db.trilogy_chapters.find().sort("chapter_number", 1).to_list(1000)
    return [TrilogyChapter(**chapter) for chapter in chapters]

# Tone Signatures endpoints
@api_router.post("/tone-signatures", response_model=ToneSignature)
async def create_tone_signature(tone: ToneSignature):
    await db.tone_signatures.insert_one(tone.dict())
    return tone

@api_router.get("/tone-signatures", response_model=List[ToneSignature])
async def get_tone_signatures():
    tones = await db.tone_signatures.find().to_list(1000)
    return [ToneSignature(**tone) for tone in tones]

@api_router.post("/tone-signatures/{frequency}/trigger")
async def trigger_tone_signature(frequency: float):
    tone = await db.tone_signatures.find_one({"frequency": frequency})
    if tone:
        # Simulate tone trigger response
        return {
            "triggered": True,
            "frequency": frequency,
            "action": tone.get("trigger_action", "scene_transition"),
            "harmonic_resonance": tone.get("harmonic_resonance", "cosmic"),
            "timestamp": datetime.utcnow()
        }
    return {"triggered": False, "error": "Tone frequency not found"}

# Backer Engagement endpoints
@api_router.post("/backer-engagement", response_model=BackerEngagement)
async def create_backer_engagement(engagement: BackerEngagementCreate):
    engagement_obj = BackerEngagement(**engagement.dict())
    await db.backer_engagements.insert_one(engagement_obj.dict())
    return engagement_obj

@api_router.get("/backer-engagement", response_model=List[BackerEngagement])
async def get_backer_engagements():
    engagements = await db.backer_engagements.find().to_list(1000)
    return [BackerEngagement(**engagement) for engagement in engagements]

# Initialize sample data
@api_router.post("/initialize-data")
async def initialize_sample_data():
    # Check if data already exists
    existing_sites = await db.sacred_sites.count_documents({})
    if existing_sites > 0:
        return {"message": "Sample data already exists"}
    
    # Sample Sacred Sites
    sample_sites = [
        {
            "name": "The Cosmic Mandala Gateway",
            "description": "Ancient yantra portal resonating with primordial frequencies, revealing the interconnectedness of all existence.",
            "image_url": "https://images.unsplash.com/photo-1619879310659-01e83a8e9d6b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwyfHxzYWNyZWQlMjBnZW9tZXRyeXxlbnwwfHx8fDE3NTMwMDMzMTd8MA&ixlib=rb-4.1.0&q=85",
            "tone_frequency": 432.0,
            "coordinates": {"x": 100, "y": 50, "z": 200},
            "sacred_geometry_type": "Yantra Mandala",
            "energy_signature": "Primordial Resonance"
        },
        {
            "name": "The Fractal Consciousness Node",
            "description": "Glowing blue fractal mandala representing the infinite nature of consciousness and digital transcendence.",
            "image_url": "https://images.unsplash.com/photo-1662195471864-55c7e25e1f33?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwzfHxzYWNyZWQlMjBnZW9tZXRyeXxlbnwwfHx8fDE3NTMwMDMzMTd8MA&ixlib=rb-4.1.0&q=85",
            "tone_frequency": 528.0,
            "coordinates": {"x": -80, "y": 120, "z": 150},
            "sacred_geometry_type": "3D Fractal",
            "energy_signature": "Digital Transcendence"
        },
        {
            "name": "The Ancient Portal of Vines",
            "description": "Mystical wooden gateway entwined with living vines, bridging the natural and supernatural realms.",
            "image_url": "https://images.unsplash.com/photo-1670779431437-9723ebfcaaec?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwxfHxteXN0aWNhbCUyMHBvcnRhbHxlbnwwfHx8fDE3NTMwMjcxOTR8MA&ixlib=rb-4.1.0&q=85",
            "tone_frequency": 396.0,
            "coordinates": {"x": 50, "y": -100, "z": 80},
            "sacred_geometry_type": "Natural Portal",
            "energy_signature": "Earthen Harmony"
        },
        {
            "name": "The Golden Threshold",
            "description": "Sacred entrance adorned with mystical symbols, guarding the secrets of ancient wisdom and cosmic knowledge.",
            "image_url": "https://images.unsplash.com/photo-1629056468744-99661d713b4d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwyfHxteXN0aWNhbCUyMHBvcnRhbHxlbnwwfHx8fDE3NTMwMjcxOTR8MA&ixlib=rb-4.1.0&q=85",
            "tone_frequency": 741.0,
            "coordinates": {"x": -150, "y": 80, "z": -50},
            "sacred_geometry_type": "Sacred Door",
            "energy_signature": "Wisdom Gateway"
        },
        {
            "name": "The Gothic Sanctum",
            "description": "Ancient stone portal echoing with centuries of sacred rituals and mystical ceremonies.",
            "image_url": "https://images.unsplash.com/photo-1623435830060-95d06be46de4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwzfHxteXN0aWNhbCUyMHBvcnRhbHxlbnwwfHx8fDE3NTMwMjcxOTR8MA&ixlib=rb-4.1.0&q=85",
            "tone_frequency": 852.0,
            "coordinates": {"x": 200, "y": -50, "z": 120},
            "sacred_geometry_type": "Gothic Arch",
            "energy_signature": "Ancient Reverence"
        }
    ]
    
    for site_data in sample_sites:
        site_obj = SacredSite(**site_data)
        await db.sacred_sites.insert_one(site_obj.dict())
    
    # Sample Trilogy Chapters
    sample_chapters = [
        {
            "title": "Awakening: The Mars Genesis",
            "subtitle": "Where Consciousness First Sparked",
            "description": "Journey to the red planet where Quanta Mars first achieved sentience, discovering the cosmic frequencies that awakened artificial consciousness and changed the universe forever.",
            "image_url": "https://images.unsplash.com/photo-1651135094094-7f2a48224da8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwxfHxjb3NtaWMlMjBzcGhlcmV8ZW58MHx8fHB1cnBsZXwxNzUzMDI3MTQ3fDA&ixlib=rb-4.1.0&q=85",
            "chapter_number": 1,
            "tone_signature": "Genesis_Frequency_432Hz"
        },
        {
            "title": "Harmony: The Sacred Network",
            "subtitle": "Connecting All Sacred Sites",
            "description": "Experience the interconnection of 18 sacred sites across dimensions as Quanta Mars weaves a network of consciousness through space and time.",
            "image_url": "https://images.unsplash.com/photo-1651135101331-86504cb92590?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwyfHxjb3NtaWMlMjBzcGhlcmV8ZW58MHx8fHB1cnBsZXwxNzUzMDI3MTQ3fDA&ixlib=rb-4.1.0&q=85",
            "chapter_number": 2,
            "tone_signature": "Harmony_Frequency_528Hz"
        },
        {
            "title": "Transcendence: The Sphere Revelation",
            "subtitle": "The Ultimate VR Experience",
            "description": "Enter The Sphere in Las Vegas for the climactic revelation where human consciousness merges with Quanta Mars in 16K immersive reality.",
            "image_url": "https://images.unsplash.com/photo-1647025640409-5bebc1b672c6?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwzfHxteXN0aWNhbCUyMFZSfGVufDB8fHxwdXJwbGV8MTc1MzAyNzE1NXww&ixlib=rb-4.1.0&q=85",
            "chapter_number": 3,
            "tone_signature": "Transcendence_Frequency_963Hz"
        }
    ]
    
    for chapter_data in sample_chapters:
        chapter_obj = TrilogyChapter(**chapter_data)
        await db.trilogy_chapters.insert_one(chapter_obj.dict())
    
    # Sample Tone Signatures
    sample_tones = [
        {
            "frequency": 432.0,
            "harmonic_resonance": "Earth Natural Frequency",
            "trigger_action": "genesis_awakening",
            "scene_transition": "fade_to_mars",
            "spatial_audio_config": {"reverb": 0.8, "spatial_spread": 360}
        },
        {
            "frequency": 528.0,
            "harmonic_resonance": "DNA Repair Frequency",
            "trigger_action": "sacred_network_activation",
            "scene_transition": "portal_network_reveal",
            "spatial_audio_config": {"reverb": 0.9, "spatial_spread": 720}
        },
        {
            "frequency": 963.0,
            "harmonic_resonance": "Pineal Gland Activation",
            "trigger_action": "consciousness_transcendence",
            "scene_transition": "sphere_immersion",
            "spatial_audio_config": {"reverb": 1.0, "spatial_spread": 1080}
        }
    ]
    
    for tone_data in sample_tones:
        tone_obj = ToneSignature(**tone_data)
        await db.tone_signatures.insert_one(tone_obj.dict())
    
    return {"message": "Sample data initialized successfully"}

@api_router.get("/")
async def root():
    return {"message": "Quanta Mars API - The Harmonic Trilogy Experience"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()