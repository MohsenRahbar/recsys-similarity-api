import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="RecSys Similarity API")


class SimilarityRequest(BaseModel):
    vector_a: list[float] = Field(
        ...,
        example=[5, 4, 1, 0, 5],
        description="Feature or rating vector for the first user",
    )
    vector_b: list[float] = Field(
        ...,
        example=[4, 5, 1, 1, 4],
        description="Feature or rating vector for the second user",
    )


class SimilarityResponse(BaseModel):
    score: float
    percentage: str
    status: str


def compute_cosine_similarity(
    vec_a: list[float],
    vec_b: list[float],
) -> float:
    a = np.array(vec_a)
    b = np.array(vec_b)

    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)

    if a_norm == 0 or b_norm == 0:
        return 0.0

    return float(np.dot(a, b) / (a_norm * b_norm))


@app.post("/recommend/similarity", response_model=SimilarityResponse)
def get_similarity(data: SimilarityRequest):
    if len(data.vector_a) != len(data.vector_b):
        raise HTTPException(
            status_code=400,
            detail="Both vectors must have the same length.",
        )

    score = compute_cosine_similarity(data.vector_a, data.vector_b)

    percentage_str = f"{score * 100:.1f}%"

    if score >= 0.6:
        status = "Very similar"
    elif score <= -0.6:
        status = "Strongly opposite"
    elif -0.2 <= score <= 0.2:
        status = "Not similar"
    else:
        status = "Moderately similar"

    return SimilarityResponse(
        score=round(score, 4),
        percentage=percentage_str,
        status=status,
    )