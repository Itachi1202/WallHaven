

class PostTracker:

    def __init__(self) -> None:
        self.file_path = "./WallHavenBot/tracker.txt"
        self.post_id = open(self.file_path, "r").read()
    
    def update(self, post_id: str):
        try:
            with open(self.file_path, "w") as tracker:
                tracker.write(post_id)
            return post_id
        except Exception:
            return None