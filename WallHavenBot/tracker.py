from pymongo.collection import Collection
from WallHavenBot import db_client


class PostTracker:

    def __init__(self) -> None:
        self.col = Collection(db_client["WallHaven"], "tracker")
        self.post_id = self.col.find_one({"_id": "tracker"})["post_id"]
    
    def update(self, post_id: str):
        try:
            return self.col.find_one_and_update({"_id": "tracker"}, {"$set": {"post_id": post_id}})
        except Exception:
            return None