from abc import ABC, abstractmethod
import json
from pathlib import Path

class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name
        self.output_dir = Path("data") / name
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def process(self, input_data):
        """Process the input data and return the result"""
        pass

    def save_output(self, data, filename):
        """Save the output data for debugging"""
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            if isinstance(data, (dict, list)):
                json.dump(data, f, indent=2)
            else:
                f.write(str(data))

    def load_output(self, filename):
        """Load previously saved output"""
        output_path = self.output_dir / filename
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                if filename.endswith('.json'):
                    return json.load(f)
                return f.read()
        return None
