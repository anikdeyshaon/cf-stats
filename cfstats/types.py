from typing import Optional, TypedDict


class UserStats(TypedDict):
    handle: str
    rank: Optional[str]
    rating: Optional[int]
    maxRank: Optional[str]
    maxRating: Optional[int]
    solvedCount: int
    contestCount: int


