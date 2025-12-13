import httpx
from fastapi import HTTPException
from image_processing import ImageProcessing


class Predictor:
    def __init__(self, MODEL_URL) -> None:
        self._MODEL_URL = MODEL_URL

    async def predict(self, imageFile):
        if await self._isNotImage(imageFile):
            raise HTTPException(400, "Please upload an image.")

        imageArray = await ImageProcessing.imageBytesToArray(await imageFile.read())
        responseJSON = await self._makeInferenceRequest(imageArray)
        prediction = await self._interpretResponseJSON(responseJSON)
        return prediction

    async def _isNotImage(self, imageFile):
        contentType = imageFile.content_type
        return contentType is None or not contentType.startswith("image/")

    async def _makeInferenceRequest(self, imageArray):
        requestJSON = {"instances": imageArray.tolist()}

        async with httpx.AsyncClient(timeout=5) as client:
            response = await self._getResponse(client, requestJSON)
        json = await self._getResponseJSON(response)
        return json

    async def _getResponse(self, client, requestJSON):
        try:
            response = await client.post(self._MODEL_URL, json=requestJSON, timeout=5)
            response.raise_for_status()
        except httpx.TimeoutException:
            raise HTTPException(504, "Model server timed out")
        except httpx.HTTPError as e:
            raise HTTPException(502, f"Model server error: {e}")
        return response

    async def _getResponseJSON(self, response):
        try:
            return response.json()
        except ValueError:
            raise HTTPException(502, "Model returned invalid JSON")

    async def _interpretResponseJSON(self, json):
        agePrediction = json["predictions"][0]["output_0"][0]
        femaleProbability = json["predictions"][0]["output_1"][0]
        return {
            "age": round(agePrediction),
            "gender": await self._output1ToGender(femaleProbability),
        }

    async def _output1ToGender(self, femaleProbability):
        return "Female" if femaleProbability >= 0.5 else "Male"
