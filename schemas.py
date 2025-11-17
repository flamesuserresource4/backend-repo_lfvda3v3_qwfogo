"""
Database Schemas for Couples App

Each Pydantic model represents a collection in MongoDB.
Collection name is the lowercase of the class name.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Photo(BaseModel):
    uploader: str = Field(..., description="Name or identifier of who uploaded")
    caption: Optional[str] = Field(None, description="Photo caption")
    file_url: str = Field(..., description="Public URL to the uploaded image")
    favorite: bool = Field(False, description="Marked as favorite")


class Song(BaseModel):
    title: str
    artist: Optional[str] = None
    url: Optional[str] = Field(None, description="Optional streaming link")
    added_by: Optional[str] = None


class Movie(BaseModel):
    title: str
    year: Optional[int] = None
    link: Optional[str] = None
    planned_by: Optional[str] = None
    watched: bool = Field(False, description="Whether it's already watched")


class Note(BaseModel):
    author: str
    content: str


class Plan(BaseModel):
    author: str
    date: Optional[str] = Field(None, description="ISO date string, e.g., 2025-01-01")
    title: str
    details: Optional[str] = None
