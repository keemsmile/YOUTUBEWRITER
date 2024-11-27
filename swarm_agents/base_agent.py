from swarm.types import Agent, Result
from typing import List, Callable, Union, Optional
from pathlib import Path
import json
import openai
from pydantic import Field, ConfigDict

class BaseSwarmAgent(Agent):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    output_dir: Path = Field(default_factory=lambda: Path("data"))
    client: openai.OpenAI = Field(default_factory=openai.OpenAI)
    
    def __init__(
        self,
        name: str,
        model: str = "gpt-4",
        instructions: Union[str, Callable[[], str]] = None,
        functions: List[Callable] = None,
        parallel_tool_calls: bool = True
    ):
        super().__init__(
            name=name,
            model=model,
            instructions=instructions or self.default_instructions,
            functions=functions or [],
            parallel_tool_calls=parallel_tool_calls
        )
        self.output_dir = self.output_dir / name
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def default_instructions(self) -> str:
        return "You are a helpful agent."

    async def process_message(self, message) -> dict:
        """Process incoming messages and return responses"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.instructions if isinstance(self.instructions, str) else self.instructions()},
                    {"role": "user", "content": message["content"]}
                ],
                tools=[{"type": "function", "function": f} for f in self.functions] if self.functions else None,
                tool_choice=self.tool_choice
            )

            result = response.choices[0].message.content
            self.save_output({"message": message["content"], "response": result}, f"{message['id']}.json")

            return {
                "content": result,
                "sender": self.name,
                "receiver": message["sender"],
                "reply_to": message["id"]
            }

        except Exception as e:
            print(f"Error in {self.name}: {str(e)}")
            return {
                "content": f"Error: {str(e)}",
                "sender": self.name,
                "receiver": message["sender"],
                "reply_to": message["id"]
            }

    def save_output(self, data: dict, filename: str) -> None:
        """Save output data for debugging"""
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_output(self, filename: str) -> Optional[dict]:
        """Load previously saved output"""
        output_path = self.output_dir / filename
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                return json.load(f)
