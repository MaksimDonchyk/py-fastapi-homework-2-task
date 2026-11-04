from datetime import date, timedelta
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.functional_serializers import PlainSerializer
from typing_extensions import Annotated

CustomDate = Annotated[
    Optional[date | str],
    PlainSerializer(lambda v: v.isoformat() if isinstance(v, date) else v, return_type=Optional[str])
]

MovieStatus = Literal["Released", "Post Production", "In Production"]


class CountrySchema(BaseModel):
    id: int
    code: str
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class GenreSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ActorSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class LanguageSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: CustomDate = None
    score: Optional[float] = None
    overview: Optional[str] = None
    status: Optional[str] = None
    budget: Optional[float] = None
    revenue: Optional[float] = None
    country: Optional[CountrySchema] = None
    genres: list[GenreSchema] = []
    actors: list[ActorSchema] = []
    languages: list[LanguageSchema] = []

    model_config = ConfigDict(from_attributes=True)


MovieDetailSchema = MovieDetailResponseSchema


class MovieListItemSchema(BaseModel):
    id: int
    name: str
    date: CustomDate = None
    score: Optional[float] = None
    overview: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieListItemSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int


class MovieCreateSchema(BaseModel):
    name: str = Field(..., max_length=255)
    date: date
    score: float = Field(..., ge=0, le=100)
    overview: Optional[str] = None
    status: Optional[MovieStatus] = None
    budget: float = Field(..., ge=0)
    revenue: float = Field(..., ge=0)
    # Строгий формат ISO 3166-1 alpha-3 (рівно 3 великі літери)
    country: str = Field(..., pattern=r"^[A-Z]{3}$")
    genres: list[str] = []
    actors: list[str] = []
    languages: list[str] = []

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: date) -> date:
        max_allowed_date = date.today() + timedelta(days=365)
        if v > max_allowed_date:
            raise ValueError("The release date cannot be more than one year in the future.")
        return v


class MovieUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    date: Optional[date] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    overview: Optional[str] = None
    status: Optional[MovieStatus] = None
    budget: Optional[float] = Field(None, ge=0)
    revenue: Optional[float] = Field(None, ge=0)
    # Строгий формат ISO 3166-1 alpha-3 для оновлення
    country: Optional[str] = Field(None, pattern=r"^[A-Z]{3}$")

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: Optional[date]) -> Optional[date]:
        if v is not None:
            max_allowed_date = date.today() + timedelta(days=365)
            if v > max_allowed_date:
                raise ValueError("The release date cannot be more than one year in the future.")
        return v
