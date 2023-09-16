class ProfessorInformation:
    def __init__(self, name:str, quality_rating:float, sentiment:float, difficulty:int, wouldTakeAgain:int, summary:str):
        self.name = name
        self.sentiment = sentiment
        self.quality_rating = quality_rating
        self.difficulty = difficulty
        self.wouldTakeAgain = wouldTakeAgain
        self.summary = summary

    def to_dict(self):
        return {
            "name": self.name,
            "qualityRating": self.quality_rating,
            "sentiment": self.sentiment,
            "difficulty": self.difficulty,
            "wouldTakeAgain": self.wouldTakeAgain,
            "summary": self.summary
        }
