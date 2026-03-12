"""
app.py — main entry point
Run with: python app.py
"""

import gradio as gr
from dotenv import load_dotenv

from core.repo_loader import clone_repo
from core.code_scanner import scan_repo, format_files_for_prompt
from core.repo_manager import RepoManager
from agents.chat_agent import chat_with_repo

load_dotenv()

# Global state — stores scanned files after analysis so chat can use them
repo_file_dump = {"value": None}


# ─────────────────────────────────────────
# Tab 1: Analyze
# ─────────────────────────────────────────

def analyze_repo(repo_url: str):
    if not repo_url.strip():
        return "⚠️ Please enter a GitHub repo URL.", gr.update(interactive=False)

    try:
        repo_path = clone_repo(repo_url.strip())
        files = scan_repo(repo_path)

        if not files:
            return "⚠️ No readable source files found.", gr.update(interactive=False)

        file_dump = format_files_for_prompt(files)
        repo_file_dump["value"] = file_dump

        manager = RepoManager()
        result = manager.run(files)

        return result, gr.update(interactive=True)

    except Exception as e:
        return f"❌ Error: {str(e)}", gr.update(interactive=False)


# ─────────────────────────────────────────
# Tab 2: Chat
# ─────────────────────────────────────────

def chat(question: str, history: list):
    if not question.strip():
        return history, ""

    if repo_file_dump["value"] is None:
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": "⚠️ Please analyze a repository first in the **Analyze** tab."})
        return history, ""

    try:
        # Convert Gradio message format to simple pairs for chat_agent
        pairs = []
        msgs = [m for m in history]
        for i in range(0, len(msgs) - 1, 2):
            if msgs[i]["role"] == "user" and msgs[i+1]["role"] == "assistant":
                pairs.append((msgs[i]["content"], msgs[i+1]["content"]))

        answer = chat_with_repo(question, repo_file_dump["value"], pairs)

        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        return history, ""

    except Exception as e:
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
        return history, ""


# ─────────────────────────────────────────
# Gradio UI (Gradio 6 compatible)
# ─────────────────────────────────────────

with gr.Blocks(title="AI Codebase Analyzer") as ui:

    gr.Markdown("""
    # 🤖 AI Codebase Analyzer
    Analyze any public GitHub repo — then chat with the code.
    """)

    with gr.Tabs():

        # ── Tab 1: Analyze ──
        with gr.Tab("🔍 Analyze Repo"):

            with gr.Row():
                repo_url = gr.Textbox(
                    label="GitHub Repo URL",
                    placeholder="https://github.com/user/repo",
                    scale=4
                )
                run_button = gr.Button("Analyze", variant="primary", scale=1)

            output_docs = gr.Markdown(label="Generated Documentation")

        # ── Tab 2: Chat ──
        with gr.Tab("💬 Chat with Repo"):

            chatbot = gr.Chatbot(
                label="Ask anything about the codebase",
                height=450,
                type="messages"
            )

            with gr.Row():
                chat_input = gr.Textbox(
                    label="Your question",
                    placeholder='e.g. "How does authentication work?"',
                    scale=4,
                    interactive=False
                )
                send_button = gr.Button("Send", variant="primary", scale=1, interactive=False)

            gr.Markdown("*Analyze a repo first to unlock the chat.*")

    # ── Wire up events ──

    run_button.click(
        fn=analyze_repo,
        inputs=repo_url,
        outputs=[output_docs, chat_input]
    ).then(
        fn=lambda: gr.update(interactive=True),
        inputs=None,
        outputs=send_button
    )

    send_button.click(
        fn=chat,
        inputs=[chat_input, chatbot],
        outputs=[chatbot, chat_input]
    )

    chat_input.submit(
        fn=chat,
        inputs=[chat_input, chatbot],
        outputs=[chatbot, chat_input]
    )


if __name__ == "__main__":
    ui.launch()