from src.steps.base_step import BaseStep

class TextAnalyzer(BaseStep):
    openai_prompt = """
        Analyze this text and provide key themes and insights.
        Return the items in a JSON array.
        Use provided function 'analyze_text' for resonse.
    """

    def __init__(self, output_folder,  openai):
        super().__init__("TextAnalyzer", output_folder, openai)
    
    def execute(self, text: str):
        self.log("3. Starting analysis...")
        try:
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo-0613",
                messages=[
                    {"role": "system", "content": self.openai_prompt},
                    {"role": "user", "content": text}
                ],
                tools=[
                     {
                        "type": "function",
                        "function": {
                            "name":"analyze_text",
                            "description": "Used to analyze text",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "key_points": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "title": { "type": "string" },
                                                "description": { "type": "string" }
                                            }
                                        }
                                    }
                                }
                            }
                        } 
                    }
                ],
                tool_choice={ "type": "function", "function": { "name": "analyze_text" } },
            )
            
            result = response.choices[0].message.tool_calls[0].function.arguments
            analysis_file_path = self.get_path("text_analyzer_result.txt")

            self.save_result(analysis_file_path, result)
            self.log(f"3. Analysis complete. Result is saved to: {analysis_file_path}")

            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None