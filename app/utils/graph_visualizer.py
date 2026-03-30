from app.graph.builder import build_graph


def save_graph_image(output_path: str = "graph.png"):
    """
    Builds the LangGraph and saves it as an image
    """

    graph = build_graph()

    try:
        # Get graph structure
        graph_obj = graph.get_graph()

        # Convert to PNG
        png_bytes = graph_obj.draw_mermaid_png()

        # Save file
        with open(output_path, "wb") as f:
            f.write(png_bytes)

        print(f"Graph saved at: {output_path}")

    except Exception as e:
        print(" Failed to generate graph image")
        print(str(e))

if __name__ == "__main__":
    print("Generating graph...")

    # Try PNG first
    try:
        save_graph_image("workflow.png")
    except Exception as e:
        print("⚠️ PNG failed, saving Mermaid instead...")
