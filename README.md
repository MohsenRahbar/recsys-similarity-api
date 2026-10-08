# RecSys Similarity API

A lightweight REST API built with **FastAPI**, **NumPy**, and **Pydantic** to calculate cosine similarity between two feature or rating vectors.

The API compares two vectors and returns a similarity score, a percentage representation, and a textual classification.

## Features

- Calculate cosine similarity between two vectors.
- Validate that both vectors have the same length.
- Handle zero vectors without division-by-zero errors.
- Return structured JSON responses using Pydantic models.
- Automatically generate interactive API documentation through FastAPI.

## Tech Stack

- **Python** — Core programming language
- **FastAPI** — REST API framework
- **NumPy** — Vector operations and cosine similarity calculation
- **Pydantic** — Request and response validation

## Installation

Clone the repository:

```bash
git clone https://github.com/MohsenRahbar/RecSys-Similarity-API.git
cd RecSys-Similarity-API
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install fastapi "uvicorn[standard]" numpy
```

## Running the API

Start the development server:

```bash
uvicorn main:app --reload
```

Replace `main` with your Python filename if it is different.

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## API Reference

### `POST /recommend/similarity`

Calculates the cosine similarity between two vectors.

**Request body:**

```json
{
  "vector_a": [5, 4, 1, 0, 5],
  "vector_b": [4, 5, 1, 1, 4]
}
```

**Example response:**

```json
{
  "score": 0.9135,
  "percentage": "91.4%",
  "status": "Very similar"
}
```

The numerical values above are illustrative; the actual response is calculated from the supplied vectors.

### Response fields

| Field | Description |
|---|---|
| `score` | Cosine similarity score, rounded to four decimal places |
| `percentage` | Score multiplied by 100 and formatted as a percentage |
| `status` | Textual classification based on the similarity score |

### Similarity classification

| Score | Status |
|---|---|
| `score >= 0.6` | `Very similar` |
| `score <= -0.6` | `Strongly opposite` |
| `-0.2 <= score <= 0.2` | `Not similar` |
| Other values | `Moderately similar` |

### Error handling

If the vectors have different lengths, the API returns HTTP `400 Bad Request`.

Example:

```json
{
  "detail": "Both vectors must have the same length."
}
```

## How It Works

Cosine similarity measures the cosine of the angle between two non-zero vectors:

\[
\operatorname{similarity}(A,B)=
\frac{A\cdot B}{\|A\|\|B\|}
\]

The score ranges from `-1` to `1` for general real-valued vectors:

- `1` indicates vectors pointing in the same direction.
- `0` indicates orthogonal vectors.
- `-1` indicates vectors pointing in opposite directions.

The API's `percentage` field is a scaled representation of the score, **not a statistical probability or a calibrated measure of recommendation accuracy**. For non-negative rating or feature vectors, cosine similarity is typically between `0` and `1`.

## Limitations

- Both vectors must have the same length.
- The API compares supplied vectors; it does not generate features or train a recommendation model.
- Similarity thresholds are predefined and may need adjustment for a specific dataset.
- A zero vector returns a score of `0.0`.
- The percentage representation should not be interpreted as a probability.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.