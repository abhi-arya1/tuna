import asyncio
import aiohttp
import pandas as pd
from datetime import datetime
from os import getenv

class Perplexity:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def _make_request(self, session: aiohttp.ClientSession, query: str) -> dict:
        try:
            payload = {
                "model": "sonar",
                "messages": [
                    {
                        "role": "system",
                        "content": "Be precise and concise."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.2,
                "top_p": 0.9,
                "search_domain_filter": None,
                "return_images": False,
                "return_related_questions": False,
                "top_k": 0,
                "stream": False,
                "presence_penalty": 0,
                "frequency_penalty": 1,
                "response_format": None
            }

            async with session.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                ssl=False
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            self.logger.error(f"Error in API request: {e}")
            return {}

    async def generate_dataset(self, queries: list) -> pd.DataFrame:
        all_results = []

        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            for i in range(0, len(queries), self.batch_size):
                batch = queries[i:i + self.batch_size]

                for query in batch:
                    response = await self._make_request(session, query)

                    if 'choices' in response:
                        result = {
                            "query": query,
                            "response": response['choices'][0]['message']['content'] if response['choices'] else "",
                            "timestamp": datetime.now().isoformat()
                        }
                        all_results.append(result)

                    await asyncio.sleep(1)

        df = pd.DataFrame(all_results)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"dataset_{timestamp}.csv"
        df.to_csv(output_path, index=False)

        return df




async def main():
    api_key = getenv("PPLX_API_KEY")
    generator = Perplexity(api_key)

    queries = [
        "What are the latest developments in transformer architecture? Include specific papers and implementations.",
        "Explain the most significant ML breakthroughs in 2024 with concrete examples and papers.",
        "What are the current state-of-the-art methods in computer vision? Include benchmarks and implementations.",
        "Describe recent advances in natural language processing, focusing on specific models and capabilities.",
        "What are the most promising applications of reinforcement learning in 2024? Include specific examples."
    ]

    dataset = await generator.generate_dataset(queries)
    print(f"Generated dataset with {len(dataset)} records")


if __name__ == "__main__":
    asyncio.run(main())