class ProjectContextBuilder:

    def build_context(self, analysis):
        parts = []

        for file_analysis in analysis:

            parts.append(f"File: {file_analysis['file']}\n\n")

            parts.append("Imports:\n")
            for imp in file_analysis["imports"]:
                parts.append(f"- {imp}\n")

            parts.append("\nTop-Level Functions:\n")

            for function in file_analysis["functions"]:
                parts.append(f"\nFunction: {function['name']}\n")
                parts.append(f"Arguments: {', '.join(function['arguments'])}\n")

                if function["docstring"]:
                    parts.append(f"Docstring:\n{function['docstring']}\n")

                parts.append("Source:\n")
                parts.append(function["source"])
                parts.append("\n")

            parts.append("\nClasses:\n")

            for cls in file_analysis["classes"]:
                parts.append(f"\nClass: {cls['name']}\n")

                if cls["docstring"]:
                    parts.append(f"Docstring:\n{cls['docstring']}\n")

                parts.append(
                    f"Methods: {', '.join(cls['methods'])}\n"
                )

                parts.append("Source:\n")
                parts.append(cls["source"])
                parts.append("\n")

            parts.append("\n" + "=" * 80 + "\n\n")

        return "".join(parts)