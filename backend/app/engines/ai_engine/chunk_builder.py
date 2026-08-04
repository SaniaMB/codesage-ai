class ChunkBuilder:

    MAX_CHARS = 1500

    def build_chunks(self, analysis):

        chunks = []

        for file_analysis in analysis:

            file_name = file_analysis["file"]

            # Functions
            for function in file_analysis["functions"]:

                for index, piece in enumerate(self.split_text(function["source"])):

                    chunks.append({
                        "type": "function",
                        "file": file_name,
                        "name": function["name"],
                        "part": index + 1,
                        "content": piece
                    })

            # Classes
            for cls in file_analysis["classes"]:

                for index, piece in enumerate(self.split_text(cls["source"])):

                    chunks.append({
                        "type": "class",
                        "file": file_name,
                        "name": cls["name"],
                        "part": index + 1,
                        "content": piece
                    })

        return chunks

    def split_text(self, text: str):

        return [
            text[i:i + self.MAX_CHARS]
            for i in range(0, len(text), self.MAX_CHARS)
        ]