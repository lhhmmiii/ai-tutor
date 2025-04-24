from fastapi import APIRouter
from services.level_analysis_service import LevelAnalysisService
from schemas.level_analysis_schema import LevelAnalysis

level_analysis_router = APIRouter(tags = ["level_analysis"])
level_analysis_service = LevelAnalysisService()

@level_analysis_router.get("/level_analysis")
async def level_analysis(text: str) -> LevelAnalysis:
    """
    Analyze the writing level of the given text using the LevelAnalysisService.
    """
    # Call the level analysis service and return the result
    result = level_analysis_service.analyze_level(text)
    return result